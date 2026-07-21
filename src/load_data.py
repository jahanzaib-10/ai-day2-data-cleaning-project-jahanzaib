import pandas as pd
import os

RAW_DIR = "data/raw"

def load_raw_data():
    customers_path = os.path.join(RAW_DIR, "customers.csv")
    products_path = os.path.join(RAW_DIR, "products.csv")
    orders_path = os.path.join(RAW_DIR, "orders.csv")
    
    customers = pd.read_csv(customers_path)
    products = pd.read_csv(products_path)
    orders = pd.read_csv(orders_path)
    
    return customers, products, orders

def inspect_dataset(df, name):
    print(f"================ {name.upper()} DATASET INSPECTION ================")
    print(f"1. Number of rows: {df.shape[0]}")
    print(f"2. Number of columns: {df.shape[1]}")
    print(f"3. Column names: {list(df.columns)}")
    print("4. First five records:\n", df.head())
    print("5. Last five records:\n", df.tail())
    print("6. Data types:\n", df.dtypes)
    print("7. Missing-value count:\n", df.isnull().sum())
    print(f"8. Duplicate-record count: {df.duplicated().sum()}")
    print("9. Unique-value count:\n", df.nunique())
    print("10. Summary statistics:\n", df.describe(include='all'))
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    customers, products, orders = load_raw_data()
    
    inspect_dataset(customers, "Customers")
    inspect_dataset(products, "Products")
    inspect_dataset(orders, "Orders")
    
    print("--- INITIAL OBSERVATIONS ---")
    print("1. Customers Dataset: Contains customer details with extra spaces in names and inconsistent city names.")
    print("2. Products Dataset: Contains product pricing and stock quantities where some numeric columns contain text or negative values.")
    print("3. Orders Dataset: Contains order transactions with repeated order IDs, missing customer IDs, and future dates.")