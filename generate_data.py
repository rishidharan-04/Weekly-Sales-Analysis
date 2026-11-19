import pandas as pd
import random
import os

random.seed(42)

# Product details
products = {
    101: ("Laptop", 55000),
    102: ("Mouse", 500),
    103: ("Keyboard", 1200),
    104: ("Monitor", 12000),
    105: ("Headphones", 2500),
    106: ("USB Cable", 300),
    107: ("Printer", 15000),
    108: ("Webcam", 3500)
}

orders = []

# Generate 60 sales records
for i in range(1, 61):

    product_id = random.choice(list(products.keys()))
    product_name, price = products[product_id]

    amount = random.choice([
        price,
        price * 2,
        price * 3,
        price * 4,
        None
    ])

    # Generate dates between September and November 2026
    date = pd.Timestamp("2026-09-01") + pd.Timedelta(
        days=random.randint(0, 79)
    )

    # Introduce mixed date formats
    if i % 3 == 0:
        order_date = date.strftime("%d-%m-%Y")
    elif i % 3 == 1:
        order_date = date.strftime("%Y/%m/%d")
    else:
        order_date = date.strftime("%m/%d/%Y")

    orders.append({
        "order_id": i,
        "order_date": order_date,
        "product_id": product_id,
        "product_name": product_name,
        "amount": amount
    })

# Introduce 3 duplicate orders
orders.append(orders[4].copy())
orders.append(orders[14].copy())
orders.append(orders[24].copy())

# Convert to DataFrame
df = pd.DataFrame(orders)

# Save CSV file
os.makedirs("dataset", exist_ok=True)

df.to_csv("dataset/messy_sales_data.csv", index=False)

print("Dataset generated successfully!")
print("Total records:", len(df))

print("\nFirst 10 records:")
print(df.head(10))

print("\nMissing amounts:")
print(df["amount"].isnull().sum())

print("\nDuplicate order IDs:")
print(df["order_id"].duplicated().sum())