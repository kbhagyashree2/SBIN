import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns  # Import seaborn for heatmap
import numpy as np  # For gradient color computation

# Apply custom CSS for Color Combination 1: Dark Blue and Coral with Darker Background
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

# Ensure the 'Date' column is a datetime object
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar for user input
st.sidebar.title("SBIN Stock Analysis")
year = st.sidebar.slider("Select Year", 2000, 2024, 2024)  # Adjust the range as needed
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
    # Real-time graph options
    if selected_insight == "Daily Price Range":
        st.subheader("Daily Price Range (High - Low)")
        filtered_df['Daily Price Range'] = filtered_df['High'] - filtered_df['Low']
        fig = px.line(
            filtered_df,
            x='Date',
            y='Daily Price Range',
            title='Daily Price Range Over Time',
            labels={'Daily Price Range': 'Price Range', 'Date': 'Date'},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Conclusion")
        st.write("Days with higher price ranges indicate higher volatility, which could signify trading opportunities or market uncertainty. This information is valuable for day traders who rely on volatility to make quick profits. However, prolonged high volatility may also suggest market instability, warranting caution.")

    elif selected_insight == "Stock Performance Trend":
        st.subheader("Stock Performance Trend (Closing Price)")
        fig = px.line(
            filtered_df,
            x='Date',
            y='Close',
            title='Stock Performance Trend (Closing Price)',
            labels={'Close': 'Closing Price', 'Date': 'Date'},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Conclusion")
        st.write("The trend of closing prices provides insights into the overall market sentiment and stock performance during the selected year. A consistent uptrend could signal investor confidence, while frequent fluctuations may indicate uncertain market conditions. Observing these trends helps investors decide the optimal time to enter or exit positions.")

    elif selected_insight == "Volume Over Time":
        st.subheader("Trading Volume Over Time")
        fig = px.bar(
            filtered_df,
            x='Date',
            y='Volume',
            title='Trading Volume Over Time',
            labels={'Volume': 'Volume', 'Date': 'Date'},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Conclusion")
        st.write("Spikes in trading volume often coincide with significant market events, such as announcements or news related to the stock. High volume suggests increased investor interest, which can lead to either rapid price appreciation or depreciation depending on the sentiment. Monitoring volume trends is crucial for identifying potential breakout opportunities.")

    elif selected_insight == "Top N Days by Closing Price":
        st.subheader(f"Top 5 Days by Closing Price in {year}")
        top_days = filtered_df.nlargest(5, 'Close')
        st.dataframe(top_days[['Date', 'Close']])
    
        # Plot using Matplotlib with a gradient of blue shades
        colors = plt.cm.Blues(np.linspace(0.4, 1, len(top_days)))  # Generate blue shades
        plt.figure(figsize=(10, 6))
        plt.bar(top_days['Date'].dt.strftime('%Y-%m-%d'), top_days['Close'], color=colors)
        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.title("Top 5 Closing Prices")
        st.pyplot(plt)

        st.markdown("### Conclusion")
        st.write("The top-performing days indicate peak market performance, which may be linked to positive news or market sentiment. Such days highlight periods of high investor confidence and can serve as reference points for future technical analysis or trend identification.")

    elif selected_insight == "Correlation Between High, Low, and Volume":
        st.subheader("Correlation Between High, Low, and Volume")
        if not filtered_df.empty:
            correlation_matrix = filtered_df[['High', 'Low', 'Volume']].corr()
            st.write("Correlation Matrix:")
            st.dataframe(correlation_matrix)
            
            # Plotting correlation heatmap using seaborn
            plt.figure(figsize=(8, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title("Correlation Heatmap")
            st.pyplot(plt)

            st.markdown("### Conclusion")
            st.write("Strong correlations indicate the interdependence between price and volume metrics, helping investors understand market behavior. For example, a high correlation between volume and price changes could suggest that significant trading activity influences market movements. Such insights assist traders in aligning their strategies with market dynamics.")
        else:
            st.warning("No data available for the selected year.")
