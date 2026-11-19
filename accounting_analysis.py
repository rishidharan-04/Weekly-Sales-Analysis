import pandas as pd

# Load original dataset
original = pd.read_csv("dataset/messy_sales_data.csv")

# Load cleaned dataset
cleaned = pd.read_csv("output/cleaned_sales_data.csv")

# Convert original amounts
original["amount"] = pd.to_numeric(
    original["amount"],
    errors="coerce"
)

# Convert original dates using known formats
dates = original["order_date"].astype(str)

original["order_date"] = pd.NaT

mask1 = dates.str.match(r"^\d{4}/")
mask2 = dates.str.match(r"^\d{2}/\d{2}/\d{4}$")
mask3 = dates.str.match(r"^\d{2}-\d{2}-\d{4}$")

original.loc[mask1, "order_date"] = pd.to_datetime(
    dates[mask1], format="%Y/%m/%d"
)

original.loc[mask2, "order_date"] = pd.to_datetime(
    dates[mask2], format="%m/%d/%Y"
)

original.loc[mask3, "order_date"] = pd.to_datetime(
    dates[mask3], format="%d-%m-%Y"
)

# Remove duplicate orders
original_cleaned = original.drop_duplicates(
    subset="order_id",
    keep="first"
)

# Select October records
original_october = original[
    original["order_date"].dt.month == 10
]

cleaned_october = original_cleaned[
    original_cleaned["order_date"].dt.month == 10
]

# Calculate revenue
original_revenue = original_october["amount"].sum()

cleaned_revenue = cleaned_october["amount"].sum()

duplicate_impact = original_revenue - cleaned_revenue

print("\n--- OCTOBER ACCOUNTING INVESTIGATION ---")

print("October revenue before duplicate removal:",
      original_revenue)

print("October revenue after duplicate removal:",
      cleaned_revenue)

print("Revenue difference due to duplicates:",
      duplicate_impact)

print("\nDuplicate October orders:")

print(
    original_october[
        original_october.duplicated(
            subset="order_id",
            keep="first"
        )
    ]
)

print("\nMissing October amounts:",
      cleaned_october["amount"].isnull().sum())