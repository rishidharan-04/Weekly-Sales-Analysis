import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import FuncFormatter

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("output/cleaned_sales_data.csv")

df["order_date"] = pd.to_datetime(df["order_date"])

# Store missing amount count before filtering
missing_amounts = df["amount"].isnull().sum()

# Keep records with valid revenue
sales = df.dropna(subset=["amount"]).copy()

# ==========================================
# 2. CALCULATE KPIs
# ==========================================

total_revenue = sales["amount"].sum()

total_orders = len(sales)

average_order_value = total_revenue / total_orders if total_orders else 0

total_products = sales["product_name"].nunique()

total_records = len(df)

# ==========================================
# 3. WEEKLY REVENUE
# ==========================================

weekly_sales = (
    sales.groupby(
        pd.Grouper(key="order_date", freq="W")
    )["amount"]
    .sum()
    .reset_index()
)

weekly_sales.columns = ["Week", "Revenue"]

# ==========================================
# 4. PRODUCT REVENUE
# ==========================================

product_sales = (
    sales.groupby("product_name")["amount"]
    .sum()
    .sort_values(ascending=True)
)

# ==========================================
# 5. PRINT SUMMARY
# ==========================================

print("\n========== SALES SUMMARY ==========")

print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Valid Orders: {total_orders}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")
print(f"Total Products: {total_products}")
print(f"Missing Amounts: {missing_amounts}")

print("\n========== WEEKLY REVENUE ==========")

print(weekly_sales.to_string(index=False))

print("\n========== PRODUCT REVENUE ==========")

print(product_sales.sort_values(ascending=False))

# ==========================================
# 6. CREATE DASHBOARD
# ==========================================

fig = plt.figure(figsize=(16, 11))

fig.suptitle(
    "WEEKLY SALES ANALYTICS DASHBOARD",
    fontsize=22,
    fontweight="bold",
    y=0.97
)

# Reporting period
fig.text(
    0.5, 0.925,
    f"Reporting Period: {df['order_date'].min():%d %b %Y} - "
    f"{df['order_date'].max():%d %b %Y}",
    ha="center",
    fontsize=11
)

# ==========================================
# 7. KPI CARDS
# ==========================================

kpis = [
    ("TOTAL REVENUE", f"₹{total_revenue:,.0f}"),
    ("VALID ORDERS", f"{total_orders}"),
    ("AVERAGE ORDER VALUE", f"₹{average_order_value:,.0f}"),
    ("TOTAL PRODUCTS", f"{total_products}"),
    ("MISSING AMOUNTS", f"{missing_amounts}")
]

positions = [0.05, 0.24, 0.43, 0.62, 0.81]

for (title, value), x in zip(kpis, positions):

    fig.text(
        x, 0.84,
        title,
        ha="left",
        fontsize=10,
        fontweight="bold"
    )

    fig.text(
        x, 0.79,
        value,
        ha="left",
        fontsize=17,
        fontweight="bold"
    )

# ==========================================
# 8. WEEKLY REVENUE LINE CHART
# ==========================================

ax1 = fig.add_axes([0.08, 0.43, 0.84, 0.27])

ax1.plot(
    weekly_sales["Week"],
    weekly_sales["Revenue"],
    marker="o",
    linewidth=2,
    markersize=7
)

ax1.set_title(
    "Weekly Revenue Trend",
    fontsize=14,
    fontweight="bold"
)

ax1.set_xlabel("Week Ending")

ax1.set_ylabel("Revenue (INR)")

ax1.yaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f"₹{x:,.0f}")
)

ax1.grid(True, alpha=0.3)

# Data labels
for x, y in zip(
    weekly_sales["Week"],
    weekly_sales["Revenue"]
):
    ax1.annotate(
        f"₹{y:,.0f}",
        (x, y),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=8
    )

# ==========================================
# 9. PRODUCT REVENUE BAR CHART
# ==========================================

ax2 = fig.add_axes([0.12, 0.10, 0.76, 0.25])

bars = ax2.barh(
    product_sales.index,
    product_sales.values
)

ax2.set_title(
    "Revenue by Product",
    fontsize=14,
    fontweight="bold"
)

ax2.set_xlabel("Revenue (INR)")

ax2.xaxis.set_major_formatter(
    FuncFormatter(lambda x, _: f"₹{x:,.0f}")
)

ax2.grid(axis="x", alpha=0.3)

# Data labels
for bar in bars:

    width = bar.get_width()

    ax2.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        f" ₹{width:,.0f}",
        va="center",
        fontsize=9
    )

# ==========================================
# 10. FOOTER
# ==========================================

fig.text(
    0.5, 0.035,
    f"Source: Cleaned Sales Dataset | "
    f"{total_records} cleaned records | "
    f"{missing_amounts} missing amounts excluded from revenue",
    ha="center",
    fontsize=9
)

# ==========================================
# 11. SAVE DASHBOARD
# ==========================================

os.makedirs("output", exist_ok=True)

plt.savefig(
    "output/sales_analytics_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nSales dashboard generated successfully!")

plt.show()