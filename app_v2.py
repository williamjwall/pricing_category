import streamlit as st
import pandas as pd
import os

# Function to read the CSV file and process the data
def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        headers = df.columns
        prices = {}
        activities = {}

        for _, row in df.iterrows():
            category = row['Categories']
            if category:
                prices[category] = {}
                if 'Activities' in headers:
                    activities[category] = row['Activities']
                for header in headers[2:]:
                    weight = header.strip()
                    price = row[header]
                    if pd.notna(price) and price != '-':
                        prices[category][weight] = price
        return prices, activities
    except Exception as e:
        st.error(f"Error reading {file_path}: {e}")
        return {}, {}

# File paths to the CSV files
files = {
    'Supply Chain': 'Supply Chain.csv',
    'VAS': 'VAS.csv',
    'Total': 'Total (1).csv'
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
    prices, activities = read_csv(file_path)

    if prices:
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

                # Display Activities if available
                if category in activities:
                    activity = activities[category]
                    # Split the activities into a list
                    activity_list = activity.split(", ")
                    st.markdown("<h3 style='color: #2196F3;'>Activities:</h3>", unsafe_allow_html=True)
                    st.markdown("<ul>", unsafe_allow_html=True)
                    for act in activity_list:
                        st.markdown(f"<li style='color: #2196F3;'>{act}</li>", unsafe_allow_html=True)
                    st.markdown("</ul>", unsafe_allow_html=True)

    else:
        st.error("No data available to display. Please check the file content.")
else:
    st.error("Please select a valid sheet and ensure the corresponding file exists in the current directory.")
