import pandas as pd
import numpy as np

def clean_customers(customers):
    df = customers.copy()
    
    df.columns = df.columns.str.strip().str.lower()
    
    if 'customer_name' in df.columns:
        df['customer_name'] = (
            df['customer_name']
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.title()
        )
        
    if 'email' in df.columns:
        df['email'] = (
            df['email']
            .astype("string")
            .str.strip()
            .str.lower()
            .str.replace(r"\s+", "", regex=True)
        )
        
    if 'city' in df.columns:
        df['city'] = df['city'].astype("string").str.strip().str.title()
        city_mapping = {
            "Lhr": "Lahore",
            "Lahore City": "Lahore",
            "Khi": "Karachi",
            "Isb": "Islamabad"
        }
        df['city'] = df['city'].replace(city_mapping)
        df['city'] = df['city'].fillna("Unknown")
        
    if 'registration_date' in df.columns:
        df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
        
    if 'customer_type' in df.columns:
        df['customer_type'] = df['customer_type'].astype("string").str.strip().str.title()
        df['customer_type'] = df['customer_type'].fillna("Regular")
        
    return df

def perform_numpy_checks(orders_df):
    quantities = pd.to_numeric(orders_df.get('quantity', pd.Series()), errors='coerce').values
    
    negative_count = np.sum(quantities < 0)
    cleaned_quantities = np.where(quantities <= 0, np.nan, quantities)
    
    valid_q = cleaned_quantities[~np.isnan(cleaned_quantities)]
    stats = {}
    if len(valid_q) > 0:
        stats['min'] = np.min(valid_q)
        stats['max'] = np.max(valid_q)
        stats['mean'] = np.mean(valid_q)
        stats['median'] = np.median(valid_q)
        
    return cleaned_quantities, stats

def clean_products(products):
    df = products.copy()
    
    df.columns = df.columns.str.strip().str.lower()
    
    if 'product_name' in df.columns:
        df['product_name'] = df['product_name'].astype("string").str.strip().str.title()
        
    if 'category' in df.columns:
        df['category'] = df['category'].astype("string").str.strip().str.title()
        category_mapping = {
            "Electronics": "Electronics",
            "Electronic": "Electronics",
            "Furniture": "Furniture",
            "Stationery": "Stationery"
        }
        df['category'] = df['category'].replace(category_mapping)
        df['category'] = df['category'].fillna("General")
        
    if 'unit_price' in df.columns:
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
        df['unit_price'] = np.where(df['unit_price'] < 0, np.nan, df['unit_price'])
        
    if 'stock_quantity' in df.columns:
        df['stock_quantity'] = pd.to_numeric(df['stock_quantity'], errors='coerce')
        df['stock_quantity'] = np.where(df['stock_quantity'] < 0, 0, df['stock_quantity'])
        
    if 'supplier_name' in df.columns:
        df['supplier_name'] = df['supplier_name'].astype("string").str.strip().str.title()
        df['supplier_name'] = df['supplier_name'].fillna("Unknown Supplier")
        
    return df

def clean_orders(orders):
    df = orders.copy()
    
    df.columns = df.columns.str.strip().str.lower()
    
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        current_date = pd.Timestamp.now()
        df.loc[df['order_date'] > current_date, 'order_date'] = pd.NaT
        
    if 'quantity' in df.columns:
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['quantity'] = np.where(df['quantity'] <= 0, np.nan, df['quantity'])
        
    if 'discount' in df.columns:
        if df['discount'].dtype == 'object':
            df['discount'] = df['discount'].astype(str).str.replace('%', '', regex=True)
        df['discount'] = pd.to_numeric(df['discount'], errors='coerce')
        df.loc[df['discount'] > 1.0, 'discount'] = df['discount'] / 100.0
        df['discount'] = df['discount'].fillna(0.0)
        
    if 'payment_status' in df.columns:
        df['payment_status'] = df['payment_status'].astype("string").str.strip().str.title()
        df['payment_status'] = df['payment_status'].fillna("Pending")
        
    if 'sales_channel' in df.columns:
        df['sales_channel'] = df['sales_channel'].astype("string").str.strip().str.title()
        df['sales_channel'] = df['sales_channel'].fillna("Online")
        
    if 'order_id' in df.columns:
        df = df.drop_duplicates(subset=['order_id'], keep='first')
        
    return df