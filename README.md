# Weekly Sales Report – Data Analytics Project

## 1. Project Overview

This project analyzes a small shop's weekly sales data using Python, Pandas, SQL and Matplotlib.

The original sales data contains missing amounts, mixed date formats and duplicate orders. The objective is to clean the data, calculate product revenue, generate a weekly sales chart and investigate differences between sales totals and accounting reports.

## 2. Technologies Used

- Python 3
- Pandas – Data cleaning and analysis
- SQLite – SQL queries and data storage
- Matplotlib – Data visualization
- VS Code – Development environment

## 3. Project Structure

```text
Weekly_Sales_Analysis/
│
├── data/
│   ├── messy_orders.csv
│   └── cleaned_orders.csv
│
├── output/
│   └── weekly_revenue.png
│
├── create_data.py
├── clean_data.py
├── analysis.py
├── sales_queries.sql
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 4. Dataset Description

The project uses a sample sales dataset containing:

- 63 raw records
- 5 columns: order_id, order_date, product_id, product_name and amount
- 4 blank amount values
- 3 intentionally duplicated order records
- Multiple date formats

The dataset is generated using `create_data.py`.

## 5. Installation and Setup

### Step 1: Install Python

Install Python 3 on your computer.

### Step 2: Open the Project

Open the project folder in VS Code.

### Step 3: Create a Virtual Environment

For macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## 6. How to Run the Project

Execute the following commands in the VS Code terminal:

```bash
python create_data.py
python clean_data.py
python analysis.py
```

**Script descriptions:**

- `create_data.py`: Generates the sample messy sales dataset.
- `clean_data.py`: Cleans the dataset using Pandas.
- `analysis.py`: Performs SQL analysis, calculates revenue, investigates accounting differences and generates the weekly revenue chart.

The final chart is saved in the `output` folder.

## 7. Data Cleaning and Business Rules

The following cleaning operations were performed:

### 7.1 Fixing Mixed Date Formats

The dataset contains different date formats:

- YYYY-MM-DD
- DD/MM/YYYY
- Mon DD, YYYY

Pandas was used to convert the dates into a consistent YYYY-MM-DD format.

The slash-separated dates were interpreted as day/month/year.

### 7.2 Handling Missing Amounts

Four records contain blank amounts.

The missing values were replaced with zero using:

```python
df["amount"] = df["amount"].fillna(0)
```

This prevents missing values from affecting calculations while retaining the order records.

In an actual business environment, missing amounts should be checked against invoices or accounting records.

### 7.3 Removing Duplicate Orders

Three duplicate order records were identified.

Duplicate records were removed using:

```python
df = df.drop_duplicates(
    subset=["order_id"],
    keep="first"
)
```

The first occurrence of each order ID was retained because order IDs are assumed to be unique.

### 7.4 Handling Invalid Dates

Records with invalid dates were removed because they cannot be assigned reliably to a reporting period.

### 7.5 Saving Cleaned Data

The final cleaned dataset is saved as:

`data/cleaned_orders.csv`

## 8. SQL Analysis – Top 5 Products

An SQL query was created to identify the top five products based on revenue during the last 30 days of available dataset dates.

The query groups sales by product, calculates total revenue and sorts the results in descending order.

```sql
SELECT
    product_id,
    product_name,
    SUM(amount) AS total_revenue
FROM orders
WHERE date(order_date) >=
    date(
        (SELECT MAX(date(order_date)) FROM orders),
        '-30 days'
    )
GROUP BY product_id, product_name
ORDER BY total_revenue DESC
LIMIT 5;
```

The query is available in `sales_queries.sql`.

## 9. Weekly Revenue Visualization

Matplotlib is used to generate a weekly revenue chart.

The chart displays total revenue for each week and helps identify sales trends over time.

The chart is saved as:

`output/weekly_revenue.png`

## 10. Accounting Mismatch Investigation

The raw sales total did not match the cleaned sales total.

After investigating the dataset, duplicate orders were identified as the likely cause of the difference.

### Data Comparison

| Description | Result |
|---|---:|
| Original records | 63 |
| Cleaned records | 60 |
| Duplicate records removed | 3 |
| Blank amounts | 4 |
| Raw known-amount total | ₹19,564 |
| Cleaned sales total | ₹19,119 |
| Difference | ₹445 |

The duplicate order IDs were:

- O0006
- O0019
- O0043

Their duplicated amounts were ₹30, ₹140 and ₹275 respectively.

Total duplicate amount:

₹30 + ₹140 + ₹275 = ₹445

Therefore, the duplicate records account for the entire ₹445 difference in the supplied sample dataset.

This confirms that duplicate orders caused the discrepancy in this synthetic dataset.

## 11. Test Scenarios

The following test scenarios were considered:

1. Verify that the raw dataset contains at least 40 records.
2. Check that all required columns are present.
3. Verify that mixed date formats are converted correctly.
4. Check that blank amounts are replaced with zero.
5. Confirm that duplicate order IDs are removed.
6. Verify that the cleaned dataset contains 60 records.
7. Check that the SQL query returns no more than five products.
8. Confirm that the weekly revenue chart is generated successfully.
9. Verify the ₹445 difference caused by duplicate records.

## 12. Environment Variables

No environment variables or external credentials are required.

An `.env.example` file is included for documentation purposes.

## 13. Assumptions

- Every order ID should be unique.
- The first occurrence of a duplicate order is retained.
- Missing amounts are treated as zero for this analysis.
- Slash-separated dates use the day/month/year format.
- Weekly revenue is grouped from Monday to Sunday.
- The last 30 days are calculated relative to the latest available dataset date.

## 14. Limitations and Future Improvements

- The dataset contains synthetic sample sales records.
- Missing amounts should be verified against actual invoices.
- Duplicate orders should be manually reviewed in a real business environment.
- Automated unit tests can be added in future versions.
- The analysis can be extended with Power BI dashboards and real accounting data.

## 15. Conclusion

This project demonstrates how Python, Pandas, SQL and Matplotlib can be used to clean messy sales data, analyze product performance, visualize weekly revenue and investigate accounting discrepancies.

The analysis identified duplicate orders as the cause of the ₹445 difference in the supplied sample dataset.

The project provides a simple data analytics workflow that can be extended for real-world business reporting.