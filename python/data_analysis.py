"""
=============================================================================
Exploratory Sales Data Analysis & Visualization
Project: Sales Data Analysis & Business Intelligence Dashboard
Author: Jeelani Mohammad
Target: Cloud Data Engineering Portfolio / HCLTech Interview

Description:
This script performs exploratory data analysis (EDA) on the cleaned sales data:
1. Computes core business KPIs (Revenue, Profit, Margin, Order Volume).
2. Evaluates regional performance and identifies the leading markets.
3. Analyzes product category contributions.
4. Identifies top 10 revenue-generating and top 10 profit-yielding products.
5. Performs time-series monthly trend analysis.
6. Generates publication-ready visualizations saved to the 'screenshots/' directory:
   - monthly_sales_trend.png
   - sales_by_region.png
   - sales_by_category.png
   - top_10_products.png
   - executive_dashboard_summary.png
=============================================================================
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Configure Matplotlib styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8

def format_currency(x, pos):
    """Format tick labels as clean currency strings ($K or $M)"""
    if x >= 1e6:
        return f"${x*1e-6:.1f}M"
    elif x >= 1e3:
        return f"${x*1e-3:.0f}K"
    else:
        return f"${x:.0f}"

def run_analysis():
    cleaned_path = os.path.join("data", "cleaned_sales_data.csv")
    output_dir = "screenshots"
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 70)
    print("SALES DATA EXPLORATORY ANALYSIS & REPORTING")
    print("=" * 70)

    if not os.path.exists(cleaned_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {cleaned_path}. Run python/data_cleaning.py first.")

    df = pd.read_csv(cleaned_path)
    print(f"Loaded Cleaned Dataset: {len(df)} rows, {len(df.columns)} columns\n")

    # 1. CORE EXECUTIVE KPIS
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_quantity = df["Quantity"].sum()
    total_orders = df["Order ID"].nunique()
    avg_order_value = total_sales / total_orders
    overall_profit_margin = (total_profit / total_sales) * 100
    avg_discount = df["Discount"].mean() * 100

    print("1. EXECUTIVE SUMMARY KPIS")
    print("-" * 50)
    print(f"Total Revenue         : ${total_sales:,.2f}")
    print(f"Total Gross Profit    : ${total_profit:,.2f}")
    print(f"Overall Profit Margin : {overall_profit_margin:.2f}%")
    print(f"Total Units Sold      : {total_quantity:,}")
    print(f"Total Unique Orders   : {total_orders:,}")
    print(f"Average Order Value   : ${avg_order_value:,.2f}")
    print(f"Average Discount Rate : {avg_discount:.2f}%\n")

    # 2. REGIONAL PERFORMANCE
    region_summary = df.groupby("Region").agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    ).reset_index()
    region_summary["Profit_Margin_Pct"] = (region_summary["Total_Profit"] / region_summary["Total_Sales"]) * 100
    region_summary = region_summary.sort_values(by="Total_Sales", ascending=False)

    print("2. REGIONAL PERFORMANCE BREAKDOWN")
    print("-" * 50)
    print(region_summary.to_string(index=False))
    print()

    # 3. CATEGORY PERFORMANCE
    cat_summary = df.groupby("Category").agg(
        Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    ).reset_index()
    cat_summary["Profit_Margin_Pct"] = (cat_summary["Total_Profit"] / cat_summary["Total_Sales"]) * 100
    cat_summary = cat_summary.sort_values(by="Total_Sales", ascending=False)

    print("3. CATEGORY PERFORMANCE BREAKDOWN")
    print("-" * 50)
    print(cat_summary.to_string(index=False))
    print()

    # 4. TOP 10 PRODUCTS BY REVENUE
    top_products_sales = df.groupby(["Product", "Category"]).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    ).reset_index().sort_values(by="Total_Sales", ascending=False).head(10)

    print("4. TOP 10 PRODUCTS BY REVENUE")
    print("-" * 50)
    print(top_products_sales.to_string(index=False))
    print()

    # 5. MONTHLY SALES TREND
    monthly_trend = df.groupby("Year-Month").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Orders=("Order ID", "count")
    ).reset_index().sort_values(by="Year-Month")

    # Filter out partial trailing months if volume is less than 5 orders to show clean trends
    monthly_trend_clean = monthly_trend[monthly_trend["Orders"] >= 5].copy()

    # =========================================================================
    # GENERATING PUBLICATION-QUALITY CHARTS
    # =========================================================================
    print("GENERATING VISUALIZATIONS FOR PORTFOLIO SCREENSHOTS...")

    currency_fmt = ticker.FuncFormatter(format_currency)

    # -------------------------------------------------------------------------
    # Chart 1: Monthly Sales & Profit Trend
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
    months = monthly_trend_clean["Year-Month"]
    sales_vals = monthly_trend_clean["Total_Sales"]
    profit_vals = monthly_trend_clean["Total_Profit"]

    ax.plot(months, sales_vals, marker="o", linewidth=2.5, color="#0284C7", label="Monthly Revenue ($)")
    ax.plot(months, profit_vals, marker="s", linewidth=2.0, color="#10B981", linestyle="--", label="Monthly Profit ($)")
    ax.fill_between(months, sales_vals, color="#0284C7", alpha=0.08)

    ax.set_title("Monthly Sales & Profit Trend (2023 - 2024)", fontsize=14, fontweight="bold", pad=15, color="#0F172A")
    ax.set_xlabel("Year-Month", fontsize=11, fontweight="bold", labelpad=10, color="#334155")
    ax.set_ylabel("Amount (USD)", fontsize=11, fontweight="bold", labelpad=10, color="#334155")
    ax.yaxis.set_major_formatter(currency_fmt)
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(fontsize=9)
    ax.legend(frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=10)
    plt.tight_layout()

    chart1_path = os.path.join(output_dir, "monthly_sales_trend.png")
    plt.savefig(chart1_path, dpi=200)
    plt.close()
    print(f" -> Saved: {chart1_path}")

    # -------------------------------------------------------------------------
    # Chart 2: Sales and Profit by Region
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
    x = np.arange(len(region_summary))
    width = 0.35

    rects1 = ax.bar(x - width/2, region_summary["Total_Sales"], width, label="Total Sales", color="#3B82F6", edgecolor="#1D4ED8", alpha=0.9)
    rects2 = ax.bar(x + width/2, region_summary["Total_Profit"], width, label="Total Profit", color="#10B981", edgecolor="#047857", alpha=0.9)

    ax.set_title("Sales & Profit by Geographical Region", fontsize=14, fontweight="bold", pad=15, color="#0F172A")
    ax.set_xticks(x)
    ax.set_xticklabels(region_summary["Region"], fontsize=10, fontweight="bold")
    ax.yaxis.set_major_formatter(currency_fmt)
    ax.set_ylabel("Amount (USD)", fontsize=11, fontweight="bold", color="#334155")
    ax.legend(frameon=True, facecolor="#F8FAFC", edgecolor="#CBD5E1", fontsize=10)

    # Add data labels
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f"${height/1000:.0f}K",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, fontweight="bold", color="#1E293B")

    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "sales_by_region.png")
    plt.savefig(chart2_path, dpi=200)
    plt.close()
    print(f" -> Saved: {chart2_path}")

    # -------------------------------------------------------------------------
    # Chart 3: Sales by Product Category
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5), dpi=200)

    # Donut chart for sales distribution
    colors = ["#3B82F6", "#F59E0B", "#10B981"]
    wedges, texts, autotexts = ax1.pie(
        cat_summary["Total_Sales"],
        labels=cat_summary["Category"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
        pctdistance=0.75
    )
    for text in texts:
        text.set_fontsize(10)
        text.set_fontweight("bold")
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_color("#0F172A")
        autotext.set_fontweight("bold")
    ax1.set_title("Sales Share by Category", fontsize=13, fontweight="bold", color="#0F172A")

    # Bar chart for profit margins
    margin_bars = ax2.bar(cat_summary["Category"], cat_summary["Profit_Margin_Pct"], color=colors, edgecolor="#334155", width=0.5)
    ax2.set_title("Profit Margin (%) by Category", fontsize=13, fontweight="bold", color="#0F172A")
    ax2.set_ylabel("Profit Margin (%)", fontsize=10, fontweight="bold", color="#334155")
    for bar in margin_bars:
        h = bar.get_height()
        ax2.annotate(f"{h:.1f}%",
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha="center", va="bottom", fontsize=9, fontweight="bold")
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "sales_by_category.png")
    plt.savefig(chart3_path, dpi=200)
    plt.close()
    print(f" -> Saved: {chart3_path}")

    # -------------------------------------------------------------------------
    # Chart 4: Top 10 Best-Selling Products
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
    sorted_top = top_products_sales.sort_values(by="Total_Sales", ascending=True)
    bars = ax.barh(sorted_top["Product"], sorted_top["Total_Sales"], color="#6366F1", edgecolor="#4338CA", height=0.65)
    ax.set_title("Top 10 Products by Total Revenue", fontsize=14, fontweight="bold", pad=15, color="#0F172A")
    ax.xaxis.set_major_formatter(currency_fmt)
    ax.set_xlabel("Total Revenue (USD)", fontsize=11, fontweight="bold", color="#334155")
    plt.yticks(fontsize=9, fontweight="medium")

    for bar in bars:
        w = bar.get_width()
        ax.annotate(f" ${w/1000:.1f}K",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=8.5, fontweight="bold", color="#1E293B")
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "top_10_products.png")
    plt.savefig(chart4_path, dpi=200)
    plt.close()
    print(f" -> Saved: {chart4_path}")

    # -------------------------------------------------------------------------
    # Chart 5: Executive Dashboard Overview (Composite Figure)
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(14, 9), dpi=200, facecolor="#F8FAFC")
    gs = fig.add_gridspec(3, 2, height_ratios=[0.35, 1, 1], hspace=0.35, wspace=0.25)

    # Top KPI Header Banner
    ax_kpi = fig.add_subplot(gs[0, :])
    ax_kpi.axis("off")
    kpis = [
        ("TOTAL REVENUE", f"${total_sales:,.0f}", "#0284C7"),
        ("TOTAL PROFIT", f"${total_profit:,.0f}", "#10B981"),
        ("PROFIT MARGIN", f"{overall_profit_margin:.1f}%", "#6366F1"),
        ("UNITS SOLD", f"{total_quantity:,}", "#F59E0B"),
        ("AVG ORDER VALUE", f"${avg_order_value:.0f}", "#EC4899")
    ]
    for i, (title, val, col) in enumerate(kpis):
        x_pos = 0.10 + i * 0.19
        ax_kpi.text(x_pos, 0.70, title, fontsize=9, fontweight="bold", color="#64748B", ha="center")
        ax_kpi.text(x_pos, 0.25, val, fontsize=16, fontweight="heavy", color=col, ha="center")
    
    # Bottom Left: Monthly Trend
    ax_trend = fig.add_subplot(gs[1, 0])
    ax_trend.plot(monthly_trend_clean["Year-Month"], monthly_trend_clean["Total_Sales"], marker="o", color="#0284C7", linewidth=2)
    ax_trend.set_title("Monthly Revenue Progression", fontsize=11, fontweight="bold", color="#0F172A")
    ax_trend.yaxis.set_major_formatter(currency_fmt)
    ax_trend.tick_params(axis="x", rotation=45, labelsize=8)
    ax_trend.tick_params(axis="y", labelsize=8)

    # Bottom Right: Sales by Region
    ax_reg = fig.add_subplot(gs[1, 1])
    ax_reg.bar(region_summary["Region"], region_summary["Total_Sales"], color="#3B82F6", width=0.55)
    ax_reg.set_title("Revenue by Geographic Region", fontsize=11, fontweight="bold", color="#0F172A")
    ax_reg.yaxis.set_major_formatter(currency_fmt)
    ax_reg.tick_params(axis="x", labelsize=9)
    ax_reg.tick_params(axis="y", labelsize=8)

    # Lower Left: Sales by Category Donut
    ax_cat = fig.add_subplot(gs[2, 0])
    ax_cat.pie(cat_summary["Total_Sales"], labels=cat_summary["Category"], autopct="%1.0f%%",
               colors=["#3B82F6", "#F59E0B", "#10B981"], wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2))
    ax_cat.set_title("Revenue by Category", fontsize=11, fontweight="bold", color="#0F172A")

    # Lower Right: Top 5 Products
    ax_prod = fig.add_subplot(gs[2, 1])
    top5 = top_products_sales.head(5).sort_values(by="Total_Sales", ascending=True)
    ax_prod.barh(top5["Product"], top5["Total_Sales"], color="#8B5CF6", height=0.55)
    ax_prod.set_title("Top 5 Products by Revenue", fontsize=11, fontweight="bold", color="#0F172A")
    ax_prod.xaxis.set_major_formatter(currency_fmt)
    ax_prod.tick_params(axis="y", labelsize=8)
    ax_prod.tick_params(axis="x", labelsize=8)

    chart5_path = os.path.join(output_dir, "executive_dashboard_summary.png")
    plt.savefig(chart5_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f" -> Saved: {chart5_path}")

    print("=" * 70)
    print("ALL CHARTS GENERATED & SAVED TO screenshots/ DIRECTORY")
    print("=" * 70)

if __name__ == "__main__":
    run_analysis()
