-- =============================================================================
-- SQL Sales Data Analysis & Business Intelligence Queries
-- Database: SQLite (data/sales_database.db)
-- Table: sales
-- Author: Jeelani Mohammad
-- Description: Beginner-to-intermediate SQL queries analyzing revenue, profit,
--              regional distribution, product performance, and monthly trends.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- SCHEMA DEFINITION (For reference or manual recreation)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sales (
    Order_ID VARCHAR(20) PRIMARY KEY,
    Order_Date DATE,
    Year_Month VARCHAR(7),
    Order_Year INTEGER,
    Order_Month INTEGER,
    Month_Name VARCHAR(10),
    Customer_Name VARCHAR(100),
    Product VARCHAR(100),
    Category VARCHAR(50),
    Region VARCHAR(50),
    Quantity INTEGER,
    Unit_Price REAL,
    Discount REAL,
    Sales REAL,
    Profit REAL,
    Profit_Margin_Pct REAL
);

-- -----------------------------------------------------------------------------
-- 1. OVERALL BUSINESS PERFORMANCE KPIS
-- Calculates Total Sales, Total Profit, Total Quantity Sold, and Average Sales.
-- -----------------------------------------------------------------------------
SELECT 
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity_Sold,
    ROUND(AVG(Sales), 2) AS Average_Sales_Per_Order,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Overall_Profit_Margin_Pct
FROM sales;

-- -----------------------------------------------------------------------------
-- 2. SALES AND PROFIT BY REGION
-- Identifies geographical performance and regional profitability.
-- -----------------------------------------------------------------------------
SELECT 
    Region,
    COUNT(Order_ID) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC;

-- -----------------------------------------------------------------------------
-- 3. SALES AND PROFIT BY CATEGORY
-- Analyzes sales distribution across Technology, Furniture, and Office Supplies.
-- -----------------------------------------------------------------------------
SELECT 
    Category,
    COUNT(Order_ID) AS Total_Orders,
    SUM(Quantity) AS Units_Sold,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
FROM sales
GROUP BY Category
ORDER BY Total_Sales DESC;

-- -----------------------------------------------------------------------------
-- 4. TOP 10 BEST-SELLING PRODUCTS BY TOTAL REVENUE
-- Highlights high-revenue drivers for inventory planning.
-- -----------------------------------------------------------------------------
SELECT 
    Product,
    Category,
    SUM(Quantity) AS Units_Sold,
    ROUND(SUM(Sales), 2) AS Total_Revenue
FROM sales
GROUP BY Product, Category
ORDER BY Total_Revenue DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- 5. TOP 10 HIGHEST PROFIT-GENERATING PRODUCTS
-- Identifies products delivering the highest absolute dollar profit.
-- -----------------------------------------------------------------------------
SELECT 
    Product,
    Category,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
FROM sales
GROUP BY Product, Category
ORDER BY Total_Profit DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- 6. MONTHLY SALES AND PROFIT TREND
-- Tracks revenue and profit progression over time.
-- -----------------------------------------------------------------------------
SELECT 
    Year_Month,
    COUNT(Order_ID) AS Orders_Count,
    ROUND(SUM(Sales), 2) AS Monthly_Sales,
    ROUND(SUM(Profit), 2) AS Monthly_Profit
FROM sales
GROUP BY Year_Month
ORDER BY Year_Month ASC;

-- -----------------------------------------------------------------------------
-- 7. AVERAGE ORDER VALUE (AOV) AND BASKET SIZE BY REGION
-- Measures customer spend per order across different territories.
-- -----------------------------------------------------------------------------
SELECT 
    Region,
    ROUND(AVG(Sales), 2) AS Avg_Order_Value,
    ROUND(AVG(Quantity), 1) AS Avg_Items_Per_Order,
    ROUND(AVG(Discount) * 100, 2) AS Avg_Discount_Pct
FROM sales
GROUP BY Region
ORDER BY Avg_Order_Value DESC;

-- -----------------------------------------------------------------------------
-- 8. DISCOUNT IMPACT ANALYSIS
-- Evaluates sales and margins comparing discounted vs. full-price transactions.
-- -----------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN Discount = 0 THEN 'No Discount (0%)'
        WHEN Discount <= 0.10 THEN 'Low Discount (1-10%)'
        ELSE 'High Discount (>10%)'
    END AS Discount_Bracket,
    COUNT(Order_ID) AS Order_Count,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
FROM sales
GROUP BY Discount_Bracket
ORDER BY Total_Sales DESC;

-- -----------------------------------------------------------------------------
-- 9. TOP 10 CUSTOMERS BY TOTAL EXPENDITURE
-- Identifies high-value customers for loyalty programs and marketing.
-- -----------------------------------------------------------------------------
SELECT 
    Customer_Name,
    COUNT(Order_ID) AS Total_Orders,
    SUM(Quantity) AS Total_Items_Bought,
    ROUND(SUM(Sales), 2) AS Total_Spend
FROM sales
WHERE Customer_Name != 'Guest Customer'
GROUP BY Customer_Name
ORDER BY Total_Spend DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- 10. CATEGORY BREAKDOWN WITHIN EACH REGION
-- Multi-dimensional grouping of sales across geography and product categories.
-- -----------------------------------------------------------------------------
SELECT 
    Region,
    Category,
    COUNT(Order_ID) AS Orders,
    ROUND(SUM(Sales), 2) AS Regional_Category_Sales
FROM sales
GROUP BY Region, Category
ORDER BY Region ASC, Regional_Category_Sales DESC;
