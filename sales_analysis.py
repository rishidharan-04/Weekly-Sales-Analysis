import pandas as pd
import os

# Load original dataset
df = pd.read_csv("dataset/messy_sales_data.csv")

print("Original Records:", len(df))

# --------------------------------
# 1. HANDLE DUPLICATE ORDERS
# --------------------------------

print("\n--- DUPLICATE REMOVAL ---")

print("Duplicates before cleaning:",
      df["order_id"].duplicated().sum())

df = df.drop_duplicates(
    subset="order_id",
    keep="first"
)

print("Records after removing duplicates:", len(df))

# --------------------------------
# 2. HANDLE MISSING AMOUNTS
# --------------------------------

print("\n--- MISSING AMOUNT HANDLING ---")

print("Missing amounts:", df["amount"].isnull().sum())

# Preserve missing amounts.
# Do not invent revenue values.

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)

# --------------------------------
# 3. STANDARDIZE DATE FORMATS
# --------------------------------

print("\n--- DATE CLEANING ---")

dates = df["order_date"].astype(str)

df["order_date"] = pd.NaT

# Format 1: YYYY/MM/DD
mask1 = dates.str.match(r"^\d{4}/")

df.loc[mask1, "order_date"] = pd.to_datetime(
    dates[mask1],
    format="%Y/%m/%d"
)

# Format 2: MM/DD/YYYY
mask2 = dates.str.match(r"^\d{2}/\d{2}/\d{4}$")

df.loc[mask2, "order_date"] = pd.to_datetime(
    dates[mask2],
    format="%m/%d/%Y"
)

# Format 3: DD-MM-YYYY
mask3 = dates.str.match(r"^\d{2}-\d{2}-\d{4}$")

df.loc[mask3, "order_date"] = pd.to_datetime(
    dates[mask3],
    format="%d-%m-%Y"
)

print("Invalid dates:", df["order_date"].isnull().sum())

print("Invalid dates:", df["order_date"].isnull().sum())

print("\n--- DATE VALIDATION ---")

print(
    pd.DataFrame({
        "Original_Date": dates,
        "Cleaned_Date": df["order_date"]
    }).head(15)
)

# --------------------------------
# 4. CHECK DATA TYPES
# --------------------------------

print("\n--- CLEANED DATA TYPES ---")

print(df.dtypes)

# --------------------------------
# 5. SAVE CLEANED DATASET
# --------------------------------

os.makedirs("output", exist_ok=True)

df.to_csv(
    "output/cleaned_sales_data.csv",
    index=False
)

print("\n--- CLEANING COMPLETED ---")

print("Final records:", len(df))
print("Missing amounts:", df["amount"].isnull().sum())
print("Duplicate order IDs:", df["order_id"].duplicated().sum())

print("\nCleaned dataset saved successfully!")
