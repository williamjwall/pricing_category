import streamlit as st
import pandas as pd
import os

# Function to read the Excel file and process the data
def read_excel(file_path):
    df = pd.read_excel(file_path, sheet_name='Total')
    headers = df.columns
    prices = {}

    for _, row in df.iterrows():
        category = row[0]
        if category:
            prices[category] = {}
            for header in headers[2:]:
                weight = header.strip()
                price = row[header]
                if pd.notna(price):
                    prices[category][weight] = price
    return prices

# File path to the Excel file
file_path = 'Return Pro ChatGPT V3.xlsx'

# Ensure the file exists in the directory
if os.path.exists(file_path):
    prices = read_excel(file_path)

    st.header("ReturnPro Service Selection")

    # Select Category
    category = st.selectbox("Select Category or Subcategory:", [""] + list(prices.keys()))

    if category:
        # Select Weight
        weight = st.selectbox("Select Weight:", [""] + list(prices[category].keys()))

        if weight:
            # Display Price
            price = prices[category][weight]
            st.write(f"Price: ${price:.2f}")
else:
    st.error(f"The file {file_path} does not exist in the current directory.")
