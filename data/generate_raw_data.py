"""
Raw Sales Data Generator
Generates a realistic e-commerce/retail sales dataset (800 rows) with
deliberate data quality issues (duplicates, missing values, inconsistent formats)
to demonstrate data cleaning and transformation in Python/Pandas.
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Product catalog with Categories and standard Unit Prices
catalog = [
    # Technology
    {"Product": "MacBook Air M2", "Category": "Technology", "BasePrice": 999.00},
    {"Product": "Dell XPS 15", "Category": "Technology", "BasePrice": 1250.00},
    {"Product": "ThinkPad Carbon X1", "Category": "Technology", "BasePrice": 1150.00},
    {"Product": "iPad Air", "Category": "Technology", "BasePrice": 599.00},
    {"Product": "Samsung Galaxy S23", "Category": "Technology", "BasePrice": 799.00},
    {"Product": "AirPods Pro", "Category": "Technology", "BasePrice": 249.00},
    {"Product": "Sony WH-1000XM5", "Category": "Technology", "BasePrice": 399.00},
    {"Product": "Logitech MX Master 3", "Category": "Technology", "BasePrice": 99.00},
    {"Product": "Mechanical Keyboard RGB", "Category": "Technology", "BasePrice": 129.00},
    {"Product": "4K Ultra HD Monitor 27\"", "Category": "Technology", "BasePrice": 349.00},
    {"Product": "USB-C Multiport Hub", "Category": "Technology", "BasePrice": 49.00},

    # Furniture
    {"Product": "Ergonomic Office Chair", "Category": "Furniture", "BasePrice": 289.00},
    {"Product": "Electric Standing Desk", "Category": "Furniture", "BasePrice": 450.00},
    {"Product": "Executive Leather Chair", "Category": "Furniture", "BasePrice": 350.00},
    {"Product": "Wooden Bookshelf 5-Tier", "Category": "Furniture", "BasePrice": 180.00},
    {"Product": "Steel Filing Cabinet", "Category": "Furniture", "BasePrice": 140.00},
    {"Product": "Conference Room Table", "Category": "Furniture", "BasePrice": 620.00},
    {"Product": "LED Desk Lamp with Wireless Charger", "Category": "Furniture", "BasePrice": 55.00},

    # Office Supplies
    {"Product": "Heavy-Duty Paper Shredder", "Category": "Office Supplies", "BasePrice": 89.00},
    {"Product": "Wireless Laser Pointer", "Category": "Office Supplies", "BasePrice": 29.00},
    {"Product": "Premium Notebook 3-Pack", "Category": "Office Supplies", "BasePrice": 22.00},
    {"Product": "Gel Pen Set 12-Pack", "Category": "Office Supplies", "BasePrice": 15.00},
    {"Product": "Mesh Desktop Organizer", "Category": "Office Supplies", "BasePrice": 25.00},
    {"Product": "Dry Erase Whiteboard 36x24", "Category": "Office Supplies", "BasePrice": 65.00},
    {"Product": "Stapler & Punch Kit", "Category": "Office Supplies", "BasePrice": 18.00},
]

customer_pool = [
    "Aarav Sharma", "Priya Patel", "Rohan Mehta", "Neha Gupta", "Vikram Reddy",
    "Ananya Singh", "Rahul Verma", "Sneha Nair", "Amit Joshi", "Pooja Desai",
    "John Smith", "Emma Johnson", "Michael Brown", "Sarah Davis", "David Wilson",
    "James Anderson", "Emily Taylor", "Robert Martinez", "Olivia White", "Daniel Clark",
    "Arjun Kapoor", "Kavita Rao", "Deepak Chopra", "Swati Iyer", "Manoj Kumar"
]

regions = ["North", "South", "East", "West"]
discounts = [0.0, 0.05, 0.10, 0.15, 0.20]

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 6, 30)
date_range_days = (end_date - start_date).days

records = []
num_records = 800

for i in range(1, num_records + 1):
    order_id = f"ORD-{2023 if i < 450 else 2024}-{1000 + i}"
    
    # Generate random date
    random_days = random.randint(0, date_range_days)
    order_dt = start_date + timedelta(days=random_days)
    
    # Inconsistent date formats intentionally added for data cleaning demo
    date_style = random.random()
    if date_style < 0.70:
        date_str = order_dt.strftime("%Y-%m-%d")        # Standard ISO: 2023-04-15
    elif date_style < 0.85:
        date_str = order_dt.strftime("%d/%m/%Y")        # European style: 15/04/2023
    else:
        date_str = order_dt.strftime("%m-%d-%Y")        # US style: 04-15-2023
    
    customer = random.choice(customer_pool)
    prod_info = random.choice(catalog)
    product = prod_info["Product"]
    category = prod_info["Category"]
    region = random.choice(regions)
    
    quantity = random.randint(1, 8)
    unit_price = prod_info["BasePrice"]
    discount = random.choice(discounts)
    
    # Calculate Sales and Profit
    # Sales = Quantity * Unit_Price * (1 - Discount)
    gross_sales = quantity * unit_price
    sales = round(gross_sales * (1.0 - discount), 2)
    
    # Profit margin varies by category (Technology ~ 18-25%, Furniture ~ 12-20%, Office Supplies ~ 25-35%)
    if category == "Technology":
        cost_margin = random.uniform(0.72, 0.80)
    elif category == "Furniture":
        cost_margin = random.uniform(0.78, 0.86)
    else:
        cost_margin = random.uniform(0.60, 0.72)
        
    estimated_cost = gross_sales * cost_margin
    profit = round(sales - estimated_cost, 2)
    
    records.append({
        "Order ID": order_id,
        "Order Date": date_str,
        "Customer Name": customer,
        "Product": product,
        "Category": category,
        "Region": region,
        "Quantity": quantity,
        "Unit Price": unit_price,
        "Sales": sales,
        "Discount": discount,
        "Profit": profit
    })

df = pd.DataFrame(records)

# 1. Introduce 15 duplicate rows to demonstrate deduplication
duplicate_indices = random.sample(range(len(df)), 15)
duplicates = df.iloc[duplicate_indices].copy()
df = pd.concat([df, duplicates], ignore_index=True)

# 2. Introduce deliberate missing values (NaN / None)
# Missing Customer Names (10 rows)
null_cust_idx = random.sample(range(len(df)), 10)
df.loc[null_cust_idx, "Customer Name"] = np.nan

# Missing Region (8 rows)
null_region_idx = random.sample(range(len(df)), 8)
df.loc[null_region_idx, "Region"] = np.nan

# Missing Discount (12 rows)
null_disc_idx = random.sample(range(len(df)), 12)
df.loc[null_disc_idx, "Discount"] = np.nan

# 3. Introduce whitespace inconsistencies in text columns
whitespace_idx = random.sample(range(len(df)), 25)
for idx in whitespace_idx:
    if pd.notnull(df.loc[idx, "Region"]):
        df.loc[idx, "Region"] = f"  {df.loc[idx, 'Region']} "
    if pd.notnull(df.loc[idx, "Category"]):
        df.loc[idx, "Category"] = f"{df.loc[idx, 'Category']}  "

# Shuffle rows
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

output_file = os.path.join("data", "raw_sales_data.csv")
df.to_csv(output_file, index=False)

print(f"Generated raw sales dataset: {output_file}")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Missing values count:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"Duplicate rows count: {df.duplicated().sum()}")
