# sales-prediction-streamlit
Retail sales analysis and forecasting dashboard built with Streamlit and ARIMA.

## 🛍️ Retail Sales Predictor

An interactive Streamlit application that analyzes historical retail sales data and predicts the next top 10 best-selling products using ARIMA time-series forecasting.

---

### 📌 Features

- ✅ Upload CSV files containing retail sales data
- ✅ Validates required columns:
  - `date`
  - `product_id`
  - `product_name`
  - `units_sold`
  - `total_amount`
- ✅ Generates visual insights for:
  - Past top 10 best-selling products
  - Predicted top 10 best-sellers (next 1 year)
- ✅ Uses ARIMA model for per-product sales forecasting
- ✅ Clean and interactive UI with Streamlit

---

### 🧪 Sample CSV Format

| date       | product_id | product_name | units_sold | total_amount |
|------------|------------|--------------|------------|--------------|
| 2023-01-01 | 101        | Product A    | 10         | 500          |
| 2023-01-01 | 102        | Product B    | 5          | 300          |

Ensure your file follows this structure and is encoded in UTF-8.

---

### 🧪 Sample CSV Included

A sample CSV file (expanded_retail_data) is included in this repository for testing purposes.

