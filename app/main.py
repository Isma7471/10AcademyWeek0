import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Title and Introduction
st.title("Solar Farm Data Analysis Dashboard")
st.markdown("Explore solar radiation data from Benin, Sierra Leone, and Togo.")

# Data Loading and Preprocessing
@st.cache_data  # Cache the data to improve performance
def load_and_preprocess_data(benin_file, sl_file, togo_file):
    try:
        benin_data = pd.read_csv(benin_file)  
        sl_data = pd.read_csv(sl_file)
        togo_data = pd.read_csv(togo_file)

        # Combine datasets (add a 'country' column)
        benin_data['country'] = 'Benin'
        sl_data['country'] = 'Sierra Leone'
        togo_data['country'] = 'Togo'
        all_data = pd.concat([benin_data, sl_data, togo_data])

        # Convert 'Timestamp' to datetime objects
        all_data['Timestamp'] = pd.to_datetime(all_data['Timestamp'])

        # Data Cleaning (handle missing values - basic example)
        for col in ['GHI', 'DNI', 'DHI', 'Tamb', 'ModA', 'ModB', 'WS', 'RH', 'BP']:
            all_data[col] = all_data.groupby('country')[col].transform(lambda x: x.fillna(x.mean()))

        return all_data
    except Exception as e:  # Handle file upload errors
        st.error(f"Error loading data: {e}")
        return None

# File Uploaders
benin_file = st.file_uploader("Upload Benin Data (CSV)", type="csv")
sl_file = st.file_uploader("Upload Sierra Leone Data (CSV)", type="csv")
togo_file = st.file_uploader("Upload Togo Data (CSV)", type="csv")

# Load data if files are uploaded
if benin_file and sl_file and togo_file:
    all_data = load_and_preprocess_data(benin_file, sl_file, togo_file)

    if all_data is not None:

        # Country Selection
        selected_countries = st.multiselect("Select Countries", all_data['country'].unique(), all_data['country'].unique())
        filtered_data = all_data[all_data['country'].isin(selected_countries)]

        # Date Range Selection
        start_date = st.date_input("Start Date", value=filtered_data['Timestamp'].min().date())
        end_date = st.date_input("End Date", value=filtered_data['Timestamp'].max().date())

        filtered_data = filtered_data[(filtered_data['Timestamp'].dt.date >= start_date) & (filtered_data['Timestamp'].dt.date <= end_date)]


        # Variable Selection
        selected_variable = st.selectbox("Select Variable", ['GHI', 'DNI', 'DHI', 'Tamb', 'ModA', 'ModB', 'WS', 'RH', 'BP'])

        # Visualization Type
        visualization_type = st.radio("Select Visualization", ['Line Chart', 'Histogram', 'Scatter Plot'])

# Create Visualizations
        if visualization_type == 'Line Chart':
            plt.figure(figsize=(12, 6))
            sns.lineplot(x='Timestamp', y=selected_variable, data=filtered_data, hue='country')
            plt.title(f"{selected_variable} Over Time")
            plt.xticks(rotation=45)
            st.pyplot(plt)

        elif visualization_type == 'Histogram':
            plt.figure(figsize=(8, 6))  # Adjust figure size for better visualization
            plt.hist(filtered_data[selected_variable], bins=20) # Increased bins for more detail
            plt.title(f"Histogram of {selected_variable}")
            plt.xlabel(selected_variable)
            plt.ylabel('Frequency')
            st.pyplot(plt)

        elif visualization_type == 'Scatter Plot':
            x_variable = st.selectbox("Select X-axis Variable", ['GHI', 'DNI', 'DHI', 'Tamb', 'ModA', 'ModB', 'WS', 'RH', 'BP'])
            y_variable = st.selectbox("Select Y-axis Variable", ['GHI', 'DNI', 'DHI', 'Tamb', 'ModA', 'ModB', 'WS', 'RH', 'BP'], index=1) # Default to second option

            plt.figure(figsize=(8, 6))
            sns.scatterplot(x=x_variable, y=y_variable, data=filtered_data, hue='country')
            plt.title(f"{x_variable} vs. {y_variable}")
            st.pyplot(plt)

        # Display Data (optional)
        if st.checkbox("Show Data"):
            st.dataframe(filtered_data)

else:
    st.warning("Please upload all three CSV files to begin.")