"""
=============================================================================
SQL Query Runner
Executes sales_analysis.sql queries on the SQLite database (sales_database.db)
and formats results neatly in the terminal for interview demonstration.
=============================================================================
"""

import os
import sqlite3
import pandas as pd

def run_queries():
    db_path = os.path.join("data", "sales_database.db")
    sql_file = os.path.join("sql", "sales_analysis.sql")

    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}. Run python/data_cleaning.py first.")
        return

    conn = sqlite3.connect(db_path)

    queries = [
        ("1. Overall Business Performance KPIs", """
            SELECT 
                ROUND(SUM(Sales), 2) AS Total_Sales,
                ROUND(SUM(Profit), 2) AS Total_Profit,
                SUM(Quantity) AS Total_Quantity_Sold,
                ROUND(AVG(Sales), 2) AS Average_Sales,
                ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
            FROM sales;
        """),
        ("2. Sales and Profit by Region", """
            SELECT 
                Region,
                COUNT(Order_ID) AS Total_Orders,
                ROUND(SUM(Sales), 2) AS Total_Sales,
                ROUND(SUM(Profit), 2) AS Total_Profit,
                ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Margin_Pct
            FROM sales
            GROUP BY Region
            ORDER BY Total_Sales DESC;
        """),
        ("3. Sales and Profit by Category", """
            SELECT 
                Category,
                COUNT(Order_ID) AS Total_Orders,
                SUM(Quantity) AS Units_Sold,
                ROUND(SUM(Sales), 2) AS Total_Sales,
                ROUND(SUM(Profit), 2) AS Total_Profit,
                ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Margin_Pct
            FROM sales
            GROUP BY Category
            ORDER BY Total_Sales DESC;
        """),
        ("4. Top 10 Best-Selling Products by Revenue", """
            SELECT 
                Product,
                Category,
                SUM(Quantity) AS Units_Sold,
                ROUND(SUM(Sales), 2) AS Total_Revenue
            FROM sales
            GROUP BY Product, Category
            ORDER BY Total_Revenue DESC
            LIMIT 10;
        """),
        ("5. Top 10 Highest-Profit Products", """
            SELECT 
                Product,
                Category,
                ROUND(SUM(Profit), 2) AS Total_Profit,
                ROUND(SUM(Sales), 2) AS Total_Sales,
                ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Margin_Pct
            FROM sales
            GROUP BY Product, Category
            ORDER BY Total_Profit DESC
            LIMIT 10;
        """),
        ("6. Monthly Sales and Profit Trend (Recent 10 Months)", """
            SELECT 
                Year_Month,
                COUNT(Order_ID) AS Orders,
                ROUND(SUM(Sales), 2) AS Monthly_Sales,
                ROUND(SUM(Profit), 2) AS Monthly_Profit
            FROM sales
            GROUP BY Year_Month
            ORDER BY Year_Month DESC
            LIMIT 10;
        """),
        ("7. Discount Impact Analysis", """
            SELECT 
                CASE 
                    WHEN Discount = 0 THEN 'No Discount (0%)'
                    WHEN Discount <= 0.10 THEN 'Low Discount (1-10%)'
                    ELSE 'High Discount (>10%)'
                END AS Discount_Bracket,
                COUNT(Order_ID) AS Order_Count,
                ROUND(SUM(Sales), 2) AS Total_Sales,
                ROUND(SUM(Profit), 2) AS Total_Profit,
                ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Margin_Pct
            FROM sales
            GROUP BY Discount_Bracket
            ORDER BY Total_Sales DESC;
        """)
    ]

    print("\n" + "=" * 70)
    print("EXECUTING SQL ANALYSIS QUERIES ON SQLITE DATABASE")
    print("=" * 70)

    for title, query in queries:
        print(f"\n>>> QUERY: {title}")
        print("-" * 70)
        df_result = pd.read_sql_query(query, conn)
        print(df_result.to_string(index=False))
        print("-" * 70)

    conn.close()
    print("\nAll SQL queries executed successfully!")

if __name__ == "__main__":
    run_queries()
