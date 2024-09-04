import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import os

# Function to generate interactive plot
def generate_interactive_plot(dff, selected_columns):
    fig = go.Figure()
    for column in selected_columns:
        fig.add_trace(go.Scatter(
            x=dff.index,
            y=dff[column],
            mode='lines+markers',
            name=column
        ))

    fig.update_layout(
        title="Stock Price Trends",
        xaxis_title="Date",
        yaxis_title="Price",
        legend_title="Price Type",
        xaxis_rangeslider_visible=True
    )
    return fig

# Streamlit application
st.title('Stock Plot Generator')

# Folder path
folder_path = "C:/Users/shrut/Desktop/Github/Projects/Shruti_Repository/StocksData/NIFTY50"

# List CSV files in the folder
file_list = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# File selection
selected_file = st.selectbox("Select CSV file", file_list)

if selected_file:
    file_path = os.path.join(folder_path, selected_file)
    df = pd.read_csv(file_path)
    
    # Convert 'Date' column to datetime, assuming it is in 'YYYY-MM-DD' format
    df['Date'] = pd.to_datetime(df['Date'])  # No need for format specifier
    
    # Get unique dates for the date input
    unique_dates = sorted(df['Date'].unique())
    min_date = unique_dates[0]
    max_date = unique_dates[-1]

    st.write("Data Preview:")
    st.write(df.head())

    # Create a list of columns for plotting
    columns = [col for col in df.columns if col != 'Date']

    # Display multi-select for column selection
    st.header('Select Columns for Plotting')
    selected_columns = st.multiselect("Choose columns to plot", options=columns, default=columns[:1])

    if selected_columns:
        # Input for start date and number of days
        start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
        number_of_days = st.slider("Number of Days", min_value=1, max_value=len(df), value=10)

        if st.button("Generate Plot"):
            start_date_parsed = pd.to_datetime(start_date)
            if start_date_parsed in df['Date'].values:
                start_index = df[df['Date'] == start_date_parsed].index[0]
                end_index = min(start_index + number_of_days, len(df))  # Ensure index does not exceed the dataframe

                dff = df.iloc[start_index:end_index]
                dff.set_index('Date', inplace=True)
                
                # Generate interactive plot
                fig = generate_interactive_plot(dff, selected_columns)
                
                # Display plot
                st.plotly_chart(fig)
            else:
                st.error("Selected start date is not in the data.")
