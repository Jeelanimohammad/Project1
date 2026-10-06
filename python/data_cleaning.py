"""
=============================================================================
Data Cleaning and Transformation Pipeline
Project: Sales Data Analysis & Business Intelligence Dashboard
Author: Jeelani Mohammad

Description:
This script performs automated Extract-Transform-Load (ETL) processing:
1. Loads raw sales CSV data into Pandas.
2. Identifies and documents data quality issues (missing values, duplicates).
3. Strips inconsistent whitespace from text fields.
4. Removes duplicate records.
5. Imputes missing values with business-justified strategies:
   - Missing Discount -> Imputed as 0.0 (default: no discount)
   - Missing Customer Name -> Imputed as 'Guest Customer'
   - Missing Region -> Imputed with statistical mode (most common region)
6. Standardizes date formatting to ISO YYYY-MM-DD.
7. Validates and enforces correct data types across all columns.
8. Generates calculated business metrics (Sales, Profit Margin %, Year, Month, Year-Month).
9. Exports the cleaned dataset to CSV and loads into a SQLite database.
=============================================================================
"""

import os
import sqlite3
import pandas as pd
import numpy as np

def run_data_cleaning():
    raw_path = os.path.join("data", "raw_sales_data.csv")
    cleaned_csv_path = os.path.join("data", "cleaned_sales_data.csv")
    db_path = os.path.join("data", "sales_database.db")
    
    print("=" * 70)
    print("STARTING DATA CLEANING & ETL PIPELINE")
    print("=" * 70)
    
    # Step 1: Load raw dataset
    print(f"\n[Step 1] Loading raw dataset from: {raw_path}")
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_path}. Run generate_raw_data.py first.")
    
    df = pd.read_csv(raw_path)
    initial_rows, initial_cols = df.shape
    print(f" -> Raw Dataset Loaded: {initial_rows} rows, {initial_cols} columns")
    
    # Step 2: Diagnostic summary of data quality
    print("\n[Step 2] Diagnostic Check for Data Quality Issues:")
    duplicates_count = df.duplicated().sum()
    missing_summary = df.isnull().sum()
    missing_cols = missing_summary[missing_summary > 0]
    
    print(f" -> Duplicate rows detected: {duplicates_count}")
    print(" -> Missing values detected by column:")
    if len(missing_cols) > 0:
        for col, cnt in missing_cols.items():
            pct = (cnt / initial_rows) * 100
            print(f"    - {col}: {cnt} missing ({pct:.2f}%)")
    else:
        print("    - None")
        
    # Step 3: Strip extraneous whitespace from categorical columns
    print("\n[Step 3] Cleaning text fields (removing whitespace)...")
    # Select text columns cleanly across pandas versions
    string_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()
        # Re-convert string 'nan' back to actual np.nan
        df[col] = df[col].replace({"nan": np.nan, "None": np.nan, "": np.nan})
    print(" -> Text fields stripped and trimmed.")

    # Step 4: Deduplication
    print("\n[Step 4] Removing duplicate records...")
    df = df.drop_duplicates().reset_index(drop=True)
    post_dedup_rows = len(df)
    print(f" -> Dropped {initial_rows - post_dedup_rows} duplicate rows. Remaining: {post_dedup_rows} rows.")

    # Step 5: Handling Missing Values
    print("\n[Step 5] Handling missing values with business logic:")
    
    # 5a. Customer Name: fill missing with 'Guest Customer'
    cust_missing = df["Customer Name"].isnull().sum()
    df["Customer Name"] = df["Customer Name"].fillna("Guest Customer")
    print(f" -> Imputed {cust_missing} missing 'Customer Name' values with 'Guest Customer'")
    
    # 5b. Discount: fill missing with 0.0 (no discount applied)
    disc_missing = df["Discount"].isnull().sum()
    df["Discount"] = df["Discount"].fillna(0.0)
    print(f" -> Imputed {disc_missing} missing 'Discount' values with 0.0 (default no discount)")
    
    # 5c. Region: fill missing with mode (most frequent region)
    region_missing = df["Region"].isnull().sum()
    mode_region = df["Region"].mode()[0]
    df["Region"] = df["Region"].fillna(mode_region)
    print(f" -> Imputed {region_missing} missing 'Region' values with mode: '{mode_region}'")

    # Step 6: Standardizing Date column
    print("\n[Step 6] Standardizing Order Date to datetime format...")
    # pd.to_datetime with format='mixed' parses mixed ISO, EU, and US date strings seamlessly
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed", errors="coerce")
    
    # Check if any dates failed to parse
    failed_dates = df["Order Date"].isnull().sum()
    if failed_dates > 0:
        print(f" -> Warning: {failed_dates} unparseable dates dropped.")
        df = df.dropna(subset=["Order Date"]).reset_index(drop=True)
        
    print(f" -> Date format standardized. Date range: {df['Order Date'].min().strftime('%Y-%m-%d')} to {df['Order Date'].max().strftime('%Y-%m-%d')}")

    # Step 7: Enforcing strict data types
    print("\n[Step 7] Enforcing schema data types:")
    df["Quantity"] = df["Quantity"].astype(int)
    df["Unit Price"] = df["Unit Price"].astype(float).round(2)
    df["Discount"] = df["Discount"].astype(float).round(2)
    df["Sales"] = df["Sales"].astype(float).round(2)
    df["Profit"] = df["Profit"].astype(float).round(2)
    print(" -> Data types verified: Numeric columns coerced to int/float.")

    # Step 8: Calculated columns & Business metrics
    print("\n[Step 8] Creating calculated columns for Analytics & BI:")
    # Re-verify and ensure Sales column precision
    df["Sales"] = (df["Quantity"] * df["Unit Price"] * (1.0 - df["Discount"])).round(2)
    
    # Profit Margin (%) = (Profit / Sales) * 100
    df["Profit Margin (%)"] = np.where(df["Sales"] > 0, ((df["Profit"] / df["Sales"]) * 100).round(2), 0.0)
    
    # Temporal attributes for monthly reporting
    df["Order Year"] = df["Order Date"].dt.year
    df["Order Month"] = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Year-Month"] = df["Order Date"].dt.strftime("%Y-%m")
    
    # Re-format Order Date to clean string YYYY-MM-DD for CSV/SQLite export
    df["Order Date"] = df["Order Date"].dt.strftime("%Y-%m-%d")
    print(" -> Added: 'Profit Margin (%)', 'Order Year', 'Order Month', 'Month Name', 'Year-Month'")

    # Step 9: Column reordering & standardized naming
    column_order = [
        "Order ID", "Order Date", "Year-Month", "Order Year", "Order Month", "Month Name",
        "Customer Name", "Product", "Category", "Region",
        "Quantity", "Unit Price", "Discount", "Sales", "Profit", "Profit Margin (%)"
    ]
    df = df[column_order]

    # Step 10: Export to Cleaned CSV
    print(f"\n[Step 10] Exporting cleaned dataset to: {cleaned_csv_path}")
    df.to_csv(cleaned_csv_path, index=False)
    print(f" -> Cleaned CSV saved ({len(df)} rows, {len(df.columns)} columns)")

    # Step 11: Export to SQLite Database
    print(f"\n[Step 11] Storing cleaned dataset into SQLite database: {db_path}")
    # SQLite table column names with underscores for standard SQL syntax
    sql_df = df.copy()
    sql_df.columns = [col.replace(" ", "_").replace("(", "").replace(")", "").replace("%", "Pct").replace("-", "_") for col in sql_df.columns]
    
    conn = sqlite3.connect(db_path)
    sql_df.to_sql("sales", conn, if_exists="replace", index=False)
    
    # Verify database insert
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    db_count = cursor.fetchone()[0]
    conn.close()
    
    print(f" -> Successfully loaded {db_count} records into SQLite table 'sales'")
    print("=" * 70)
    print("DATA CLEANING & PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    
    return df

if __name__ == "__main__":
    run_data_cleaning()
