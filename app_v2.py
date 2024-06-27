import streamlit as st
import pandas as pd
import os

# Function to read the CSV file and process the data
def read_csv(file_path):
    df = pd.read_csv(file_path)
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

# File paths to the CSV files
files = {
    'Supply Chain': 'Supply Chain.csv',
    'VAS': 'VAS.csv',
    'Total': 'Total.csv'
}

# Set Streamlit theme
st.set_page_config(
    page_title="ReturnPro Service Selection",
    page_icon=":package:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar for sheet selection
st.sidebar.header("Select Data Source")
available_files = {name: path for name, path in files.items() if os.path.exists(path)}
sheet_name = st.sidebar.selectbox("Select Sheet:", list(available_files.keys()))

if sheet_name:
    file_path = available_files[sheet_name]
    prices = read_csv(file_path)

    st.header("ReturnPro Service Selection")

    # Main section for category and weight selection
    col1, col2 = st.columns(2)

    with col1:
        # Select Category
        category = st.selectbox("Select Category or Subcategory:", [""] + list(prices.keys()))

    if category:
        with col2:
            # Select Weight
            weight = st.selectbox("Select Weight:", [""] + list(prices[category].keys()))

        if weight:
            # Display Price with styling
            price = prices[category][weight]
            st.markdown(f"<h2 style='color: #4CAF50;'>Price: ${price:.2f}</h2>", unsafe_allow_html=True)

else:
    st.error("Please select a valid sheet and ensure the corresponding file exists in the current directory.")
