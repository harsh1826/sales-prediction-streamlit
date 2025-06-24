import sys
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import LabelEncoder

# ✅ **Fix Unicode Error for Windows CMD/PowerShell**
sys.stdout.reconfigure(encoding="utf-8")

# ✅ **Ensure script gets correct file path**
if len(sys.argv) < 2:
    print("❌ Error: No file provided.")
    sys.exit(1)

file_path = sys.argv[1]  # ✅ Get the uploaded file path

# ✅ Debugging print (REMOVED EMOJIS TO AVOID UNICODE ERROR)
print(f"Trying to read file: {file_path}")

try:
    df = pd.read_csv(file_path, encoding="utf-8")  # ✅ Read uploaded file
    print("✅ File loaded successfully!")
except FileNotFoundError:
    print(f"❌ File not found: {file_path}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error reading file: {e}")
    sys.exit(1)

# ✅ Standardize column names
df.columns = df.columns.str.strip().str.lower()

# ✅ Ensure required columns exist
required_columns = {"date", "product_name", "units_sold"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    print(f"❌ Missing columns: {missing_columns}")
    sys.exit(1)

# ✅ Convert 'date' column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df.dropna(subset=["date"], inplace=True)

# ✅ Encode product names
label_encoder = LabelEncoder()
df["product_name"] = label_encoder.fit_transform(df["product_name"])

# **🏆 Top 10 Best-Selling Products**
top_products = df.groupby("product_name")[["units_sold"]].sum().sort_values(by="units_sold", ascending=False).head(10)
top_products = top_products.reset_index()
top_products["product_name"] = label_encoder.inverse_transform(top_products["product_name"])

# ✅ Save top 10 best-sellers to CSV
top_products.to_csv("top_10_best_sellers.csv", index=False)
print("\nTop 10 Best-Selling Products:\n")
print(top_products)
print("\n✔ Top 10 Best-Sellers saved as 'top_10_best_sellers.csv'")

# **📊 Predict Next Top 10 Best-Selling Products Using ARIMA**
forecast_results = {}

for product in df["product_name"].unique():
    product_data = df[df["product_name"] == product][["date", "units_sold"]].groupby("date").sum().asfreq("D").fillna(0)
    if product_data["units_sold"].nunique() <= 1:
        continue
    try:
        arima_model = ARIMA(product_data["units_sold"], order=(2, 1, 2)).fit()
        forecast = arima_model.forecast(steps=365)
        total_forecasted_sales = forecast.sum()
    except Exception:
        continue

    forecast_results[product] = total_forecasted_sales

# ✅ Get Top 10 Predicted Products
top_10_products = sorted(forecast_results.items(), key=lambda x: x[1], reverse=True)[:10]

# ✅ Save predictions to CSV
top_sellers_df = pd.DataFrame(top_10_products, columns=["product_name", "predicted_annual_sales"])
top_sellers_df["product_name"] = label_encoder.inverse_transform(top_sellers_df["product_name"].astype(int))
top_sellers_df.to_csv("next_top_10_sellers.csv", index=False)

print("\nPredicted Next Top 10 Best-Selling Products:\n")
print(top_sellers_df)
print("\n✔ Predictions saved as 'next_top_10_sellers.csv'")
