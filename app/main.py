import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import cm


# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("### Upload your file")

# Create file uploader widget
uploaded_file = st.sidebar.file_uploader("Drag and drop your CSV file here", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the CSV file using pandas
    Benin_data = pd.read_csv(uploaded_file)
    
    # Display the dataframe
    st.title("Benin Data Analysis")
    st.dataframe(Benin_data.head())  # Show the first few rows of the dataset
else:
    st.info("Please upload a CSV file to analyze.")

# Additional app functionality here
# For example, analyzing and visualizing the data, or displaying insights

# Set up Streamlit

# Sidebar options
options = ['Overview', 'Data Cleaning', 'Boxplots', 'Histograms', 'Time Series Analysis', 'Bivariate Analysis', 'Bubble Chart']
selection = st.sidebar.radio('Choose a section', options)

# Overview Section
if selection == 'Overview':
    st.header('Overview of Benin Data')
    st.write("This dashboard provides insights into Benin's weather and solar data.")
    st.write("Columns: GHI, DNI, DHI, Tamb, RH, WS, etc.")
    st.write("The data is analyzed for different patterns including time series analysis, correlations, and more.")
    
    st.write('Data Preview:')
    st.dataframe(Benin_data.head())

# Data Cleaning Section
elif selection == 'Data Cleaning':
    st.header('Data Cleaning for Benin Data')
    st.write("Here, we demonstrate the effect of cleaning the data by removing duplicates and handling missing values.")
    
    # Cleaning process
    Benin_data_cleaned = Benin_data.drop_duplicates()
    Benin_data_cleaned.fillna(Benin_data_cleaned.mean(), inplace=True)
    
    st.write("Cleaned Data Preview:")
    st.dataframe(Benin_data_cleaned.head())
    
    st.write(f"Original Data Shape: {Benin_data.shape}")
    st.write(f"Cleaned Data Shape: {Benin_data_cleaned.shape}")

# Boxplots Section
elif selection == 'Boxplots':
    st.header('Boxplot Analysis')
    st.write("Visualizing the distributions of different columns using boxplots.")
    
    # Boxplot for selected columns
    cols_to_plot = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'Tamb', 'RH', 'WS', 'WSgust', 'WSstdev']
    box = Benin_data[cols_to_plot].plot(kind='box', figsize=(12, 6), patch_artist=True)
    plt.title('Boxplots of Various Features')
    st.pyplot()

# Histograms Section
elif selection == 'Histograms':
    st.header('Histogram Analysis')
    st.write("Visualizing the distributions of data columns using histograms.")
    
    # Histograms for selected columns
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
    cols_to_plot = ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS']
    for i, col in enumerate(cols_to_plot):
        ax = axes[i // 3, i % 3]
        Benin_data[col].plot(kind='hist', ax=ax, bins=20, color='orange', edgecolor='black', alpha=0.7)
        ax.set_title(f'{col} Distribution')
        ax.set_xlabel(col)
    plt.tight_layout()
    st.pyplot()

# Time Series Analysis Section
elif selection == 'Time Series Analysis':
    st.header('Time Series Analysis for Benin')
    st.write("Time series analysis on GHI, DHI, DNI, and Temperature over months and days.")
    
    # Convert 'Timestamp' to datetime (if not done already)
    Benin_data['Timestamp'] = pd.to_datetime(Benin_data['Timestamp'])
    
    # Monthly Time Series for GHI, DHI, DNI, and Tamb
    monthly_data = Benin_data.resample('M', on='Timestamp').mean()
    
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
    cols_to_plot = ['GHI', 'DHI', 'DNI', 'Tamb']
    for i, col in enumerate(cols_to_plot):
        ax = axes[i // 2, i % 2]
        monthly_data[col].plot(ax=ax, title=f'{col} - Monthly Average')
        ax.set_xlabel('Month')
        ax.set_ylabel(col)
    plt.tight_layout()
    st.pyplot()

# Bivariate Analysis Section
elif selection == 'Bivariate Analysis':
    st.header('Bivariate Analysis')
    st.write("Correlation heatmap and scatter plots for understanding relationships between features.")
    
    # Correlation heatmap
    corr_matrix = Benin_data.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    st.pyplot()
    
    # Scatter plot of two features (e.g., GHI vs Tamb)
    sns.scatterplot(data=Benin_data, x='GHI', y='Tamb', color='orange')
    plt.title('GHI vs Tamb Scatter Plot')
    plt.xlabel('GHI')
    plt.ylabel('Tamb')
    st.pyplot()

# Bubble Chart Section
elif selection == 'Bubble Chart':
    st.header('Bubble Chart: Temperature vs GHI with Wind Speed as Bubble Size')
    st.write("The bubble size represents wind speed (WS) while the X and Y axes represent temperature (Tamb) and GHI respectively.")
    
    # Bubble chart
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=Benin_data['Tamb'], y=Benin_data['GHI'], size=Benin_data['WS'], sizes=(20, 200), color='orange', legend=None, alpha=0.6)
    plt.title('Bubble Chart: Temperature vs GHI with Wind Speed as Bubble Size')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Global Horizontal Irradiance (GHI)')
    st.pyplot()

# Footer Section
st.sidebar.markdown("---")
st.sidebar.markdown("Created with ❤️ by [Esmael Uta]")

