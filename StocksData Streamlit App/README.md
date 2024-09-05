Here’s an updated README file that includes information about the recording:

---

# Stock Plot Generator

## Overview

The **Stock Plot Generator** is a Streamlit application designed to visualize stock price trends from CSV files. This application focuses on stock data related to the **NIFTY 50** index, a major stock market index in India. Users can select a CSV file containing historical stock data, choose columns to plot, and define a date range for the visualization. The resulting interactive plot displays stock price trends over the selected period.

## About NIFTY 50

The **NIFTY 50** is a benchmark stock market index in India, representing the top 50 large-cap companies listed on the National Stock Exchange (NSE). It is widely used as a barometer for the Indian equity market and provides a comprehensive view of the Indian economy. The index includes companies from various sectors, ensuring broad market coverage and liquidity.

## Features

- **File Selection**: Choose a CSV file from a predefined folder containing NIFTY 50 stock data.
- **Data Preview**: View a preview of the selected CSV file to understand the data structure.
- **Column Selection**: Select which columns (e.g., stock prices) to plot from the data.
- **Date Range Selection**: Specify the start date and the number of days for the plot.
- **Interactive Plot**: Generate an interactive line plot with markers showing the stock price trends over the selected date range.

## Installation

To run this application, you need to have Python and the required packages installed. Follow these steps to set up your environment:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```

2. **Install Dependencies**

   Create a virtual environment and install the required packages using `pip`:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   pip install -r requirements.txt
   ```

   Alternatively, you can install the packages directly:

   ```bash
   pip install streamlit pandas plotly
   ```

## Usage

1. **Prepare Your Data**

   Place your CSV files containing NIFTY 50 stock data in the `StocksData/NIFTY50` folder. Ensure that your CSV files have a `Date` column in the `YYYY-MM-DD` format and other columns representing stock prices.

2. **Run the Application**

   Start the Streamlit server by running:

   ```bash
   streamlit run app.py
   ```

   Open the provided local URL in your web browser.

3. **Interact with the Application**

   - **Select CSV File**: Choose a CSV file from the dropdown menu that contains NIFTY 50 stock data.
   - **Preview Data**: View a preview of the selected file's data.
   - **Select Columns**: Choose which columns to plot from the provided list (e.g., different stock price metrics).
   - **Set Date Range**: Specify the start date and number of days for the plot.
   - **Generate Plot**: Click the "Generate Plot" button to display the interactive plot.

## Recording

To see a demonstration of how the application works, you can view the following recording:

[Streamlit App Recording](StreamlitApp_Recording.mp4)

## Requirements

- Python 3.6 or higher
- Streamlit
- pandas
- plotly

## Acknowledgments

- [Streamlit](https://streamlit.io/) - An open-source app framework for Machine Learning and Data Science.
- [Plotly](https://plotly.com/) - A graphing library for making interactive, publication-quality graphs online.

## Contact

For any questions or feedback, please reach out to me.

---
