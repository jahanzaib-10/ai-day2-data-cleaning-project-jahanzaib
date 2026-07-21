import pandas as pd
import re

def validate_schema(sales, customers=None, products=None):
    print("--- STARTING SCHEMA VALIDATION ---")
    
    # 1. Required Columns Check
    required_columns = {
        "order_id",
        "customer_id",
        "product_id",
        "order_date",
        "quantity",
        "unit_price"
    }
    missing_columns = required_columns - set(sales.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # 2. Primary Keys Missing Check
    if sales["order_id"].isnull().any():
        raise ValueError("Primary key 'order_id' contains missing/null values.")
    if sales["customer_id"].isnull().any():
        raise ValueError("Primary key 'customer_id' contains missing/null values.")
    if sales["product_id"].isnull().any():
        raise ValueError("Primary key 'product_id' contains missing/null values.")

    # 3. Primary Keys Uniqueness Check
    if not sales["order_id"].is_unique:
        raise ValueError("Validation Error: 'order_id' contains duplicate primary keys.")

    # 4. Numeric Value Range Validations
    if (sales["quantity"] <= 0).any():
        raise ValueError("Validation Error: Found non-positive quantities (quantity must be > 0).")
    
    if (sales["unit_price"] < 0).any():
        raise ValueError("Validation Error: Found negative unit prices (unit_price must be >= 0).")
        
    if "discount" in sales.columns:
        if ((sales["discount"] < 0) | (sales["discount"] > 1)).any():
            raise ValueError("Validation Error: Discount values must be between 0 and 1.")

    # 5. Date Validations (Not in future)
    current_date = pd.Timestamp.now()
    if (sales["order_date"] > current_date).any():
        raise ValueError("Validation Error: Future dates detected in 'order_date'.")

    # 6. Approved Categories / Values Check
    if "payment_status" in sales.columns:
        approved_payment_status = {"Pending", "Completed", "Failed", "Paid"}
        invalid_payments = set(sales["payment_status"].dropna().unique()) - approved_payment_status
        # If strict check is needed, we can log or raise:
        if invalid_payments:
            print(f"Warning/Notice: Unapproved payment status categories found: {invalid_payments}")

    if "sales_channel" in sales.columns:
        approved_channels = {"Online", "In-Store", "App", "Website"}
        invalid_channels = set(sales["sales_channel"].dropna().unique()) - approved_channels
        if invalid_channels:
            print(f"Warning/Notice: Unapproved sales channels found: {invalid_channels}")

    # 7. Referential Integrity / Foreign Key Existence Check
    if customers is not None and "customer_id" in customers.columns:
        missing_customers = ~sales["customer_id"].isin(customers["customer_id"])
        if missing_customers.any():
            print(f"Warning: Found {missing_customers.sum()} orders with customer_id not present in master customers table.")

    if products is not None and "product_id" in products.columns:
        missing_products = ~sales["product_id"].isin(products["product_id"])
        if missing_products.any():
            print(f"Warning: Found {missing_products.sum()} orders with product_id not present in master products table.")

    print("--- SCHEMA VALIDATION COMPLETED SUCCESSFULLY ---")
    return True