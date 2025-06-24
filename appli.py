import pandas as pd
import streamlit as st
import os
import subprocess
import sys
import uuid
import matplotlib.pyplot as plt

st.header("Retail Sales Prediction")
st.subheader("CSV File Upload Example")

REQUIRED_COLUMNS = {"date", "product_id", "product_name", "units_sold", "total_amount"}

st.markdown("""
    **Note**: Please upload a CSV file with the following columns only:
    - `date`
    - `product_id`
    - `product_name`
    - `units_sold`
    - `total_amount`
""")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # ✅ Read the uploaded file
        df = pd.read_csv(uploaded_file, encoding="utf-8")

        # ✅ Convert column names to lowercase and remove spaces
        df.columns = df.columns.str.strip().str.lower()

        # ✅ Get the actual columns in the uploaded file
        uploaded_columns = set(df.columns)

        # ✅ Check for missing columns
        missing_columns = REQUIRED_COLUMNS - uploaded_columns
        if missing_columns:
            formatted_missing_columns = "\n".join([f"- {col}" for col in missing_columns])  # Format nicely
            formatted_uploaded_columns = "\n".join([f"- {col}" for col in uploaded_columns])  # Show existing columns

            st.error(f"❌ Missing required columns:\n{formatted_missing_columns}")
            st.warning(f"📌 Columns found in uploaded file:\n{formatted_uploaded_columns}")
            st.stop()

        # ✅ Generate a unique filename
        unique_filename = f"uploaded_csv_{uuid.uuid4().hex[:8]}.csv"
        df.to_csv(unique_filename, index=False)

        # ✅ Show success message and first 10 rows of data
        st.success(f"✅ CSV file successfully uploaded and saved as `{unique_filename}`!")
        st.write(df.head(10))

        # ✅ Get Python executable and sales.py path
        python_executable = sys.executable
        script_path = os.path.abspath("sales.py")

        if not os.path.exists(script_path):
            st.error("❌ Error: `sales.py` not found!")
            st.stop()

        # ✅ Run `sales.py` with the uploaded file
        with st.spinner("Processing the data and generating predictions..."):
            process = subprocess.run(
                [python_executable, script_path, unique_filename],  # ✅ Pass correct file
                capture_output=True,
                text=True,
                encoding="utf-8"
            )

        if process.returncode != 0:
            st.error(f"❌ Error running prediction script:\n\n{process.stderr}")
            print(f"❌ Error running script: {process.stderr}")  # Debugging print
            st.stop()

        # ✅ **Move the Analysis Button Above the Data Tables**
        st.markdown("### 🔍 Want to analyze the data?")

        # Add both Show Analysis and Cancel buttons
        analysis_button = st.button("📊 Show Analysis")
        cancel_button = st.button("❌ Cancel Analysis")

        if analysis_button:
            st.subheader("📊 Sales Analysis")

            # ✅ Load and display **Top 10 Best-Selling Products**
            best_sellers_file = "top_10_best_sellers.csv"
            if os.path.exists(best_sellers_file):
                best_sellers_df = pd.read_csv(best_sellers_file)
                st.write("### 🏆 Top 10 Best-Selling Products(previous)")
                fig, ax = plt.subplots()
                ax.barh(best_sellers_df["product_name"], best_sellers_df["units_sold"], color="skyblue")
                ax.set_xlabel("Units Sold")
                ax.set_ylabel("Product Name")
                ax.set_title("Top 10 Best-Selling Products")
                st.pyplot(fig)
            else:
                st.error("❌ Best-Sellers file not found!")

            # ✅ Load and display **Predicted Next Top 10 Best-Selling Products**
            result_file = "next_top_10_sellers.csv"
            if os.path.exists(result_file):
                predictions_df = pd.read_csv(result_file)
                st.write("### 📈 Predicted Next Top 10 Best-Selling Products(Upcoming Year)")
                fig, ax = plt.subplots()
                ax.barh(predictions_df["product_name"], predictions_df["predicted_annual_sales"], color="lightcoral")
                ax.set_xlabel("Predicted Sales")
                ax.set_ylabel("Product Name")
                ax.set_title("Predicted Next Top 10 Best-Selling Products")
                st.pyplot(fig)
            else:
                st.error("❌ Prediction file not found!")

        elif cancel_button:
            st.warning("❌ Analysis has been cancelled!")

        # ✅ Show Data Tables Below the Button
        best_sellers_file = "top_10_best_sellers.csv"
        if os.path.exists(best_sellers_file):
            best_sellers_df = pd.read_csv(best_sellers_file)
            st.success("🏆 **Top 10 Best-Selling Products:**(Previous)")
            st.write(best_sellers_df)
        else:
            st.error("❌ Best-Sellers file not found!")

        result_file = "next_top_10_sellers.csv"
        if os.path.exists(result_file):
            predictions_df = pd.read_csv(result_file)
            st.success("🎯 **Predicted Next Top 10 Best-Selling Products:**(Upcoming Year)")
            st.write(predictions_df)
        else:
            st.error("❌ Prediction file not found!")

    except Exception as e:
        st.error(f"❌ Error processing the CSV file: {e}")
        print(f"❌ Exception in appli.py: {e}")  # Debugging print
