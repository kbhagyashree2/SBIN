import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # For heatmaps
import numpy as np  # For gradient color computation

# Apply custom CSS for the dark theme
st.markdown(
    """
    <style>
    /* Set the main background color to a darker blue */
    .stApp {
        background-color: #1E3A5F;  /* Dark Blue background */
        color: #004080;             /* Alice Blue font color for the main content */
        font-family: 'Arial', sans-serif;  /* Change font style */
    }

    /* Style the sidebar */
    .css-1d391kg {  /* Class for sidebar container */
        background-color: #004080;  /* Dark Blue background for sidebar */
        color: #FFFFFF;             /* White font color for sidebar */
    }

    /* Sidebar title color */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #FFD700;  /* Golden color for sidebar title */
    }

    /* Style widgets within the sidebar */
    .css-17eq0hr a, .css-1d391kg a {
        color: #FF6347; /* Coral for hyperlinks */
    }
    .css-1d391kg .css-1lcbmhc { /* Sidebar widget text */
        color: #FFFFFF; /* White font color for sidebar widget text */
    }

    /* Style the main content text */
    .block-container {
        color: #F5F5F5; /* Light gray text for the main content */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the data
df = pd.read_csv("SBIN_New_Data.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar for user input
st.sidebar.title("SBIN Stock Analysis")
year = st.sidebar.slider("Select Year", 2000, 2024, 2024)
selected_insight = st.sidebar.selectbox(
    "Select Insight",
    ["Daily Price Range", "Stock Performance Trend", "Volume Over Time", "Top N Days by Closing Price", "Correlation Between High, Low, and Volume"]
)

st.title("Real-Time SBIN Stock Data Insights")

# Filter data by year
df['Year'] = df['Date'].dt.year
filtered_df = df[df['Year'] == year]

if filtered_df.empty:
    st.warning("No data available for the selected year.")
else:
    if selected_insight == "Daily Price Range":
        st.subheader("Daily Price Range (High - Low)")
        filtered_df['Daily Price Range'] = filtered_df['High'] - filtered_df['Low']
        
        # Plot using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_df['Date'], filtered_df['Daily Price Range'], color='coral', marker='o', linestyle='-', linewidth=2)
        plt.title('Daily Price Range Over Time')
        plt.xlabel('Date')
        plt.ylabel('Price Range')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif selected_insight == "Stock Performance Trend":
        st.subheader("Stock Performance Trend (Closing Price)")

        # Plot using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_df['Date'], filtered_df['Close'], color='blue', marker='o', linestyle='-', linewidth=2)
        plt.title('Stock Performance Trend')
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif selected_insight == "Volume Over Time":
        st.subheader("Trading Volume Over Time")

        # Plot using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.bar(filtered_df['Date'], filtered_df['Volume'], color='skyblue')
        plt.title('Trading Volume Over Time')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif selected_insight == "Top N Days by Closing Price":
        st.subheader(f"Top 5 Days by Closing Price in {year}")
        top_days = filtered_df.nlargest(5, 'Close')
        st.dataframe(top_days[['Date', 'Close']])
        
        # Plot using Matplotlib
        colors = plt.cm.Blues(np.linspace(0.4, 1, len(top_days)))
        plt.figure(figsize=(10, 6))
        plt.bar(top_days['Date'].dt.strftime('%Y-%m-%d'), top_days['Close'], color=colors)
        plt.title("Top 5 Closing Prices")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.xticks(rotation=45)
        st.pyplot(plt)

    elif selected_insight == "Correlation Between High, Low, and Volume":
        st.subheader("Correlation Between High, Low, and Volume")

        correlation_matrix = filtered_df[['High', 'Low', 'Volume']].corr()
        st.write("Correlation Matrix:")
        st.dataframe(correlation_matrix)

        # Plot heatmap using Seaborn
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Heatmap")
        st.pyplot(plt)
