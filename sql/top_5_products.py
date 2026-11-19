import sqlite3
import pandas as pd

CSV = "output/cleaned_sales_data.csv"

df = pd.read_csv(CSV)
df["order_date"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m-%d")

conn = sqlite3.connect(":memory:")
df.to_sql("orders", conn, index=False)

query = """
SELECT
    product_id,
    product_name,
    SUM(amount) AS total_revenue
FROM orders
WHERE order_date >= date('now', '-30 day')
  AND order_date <= date('now')
  AND amount IS NOT NULL
GROUP BY product_id, product_name
ORDER BY total_revenue DESC
LIMIT 5;
"""

result = pd.read_sql_query(query, conn)
print(result)

result.to_csv("output/top_5_products_last_30_days.csv", index=False)
conn.close()