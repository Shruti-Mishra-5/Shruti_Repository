# Car Data Streamlit App

## Overview

This Streamlit app allows users to interact with a dataset of used cars to understand their prices and various features. The application includes features for filtering data, predicting car prices, and visualizing data through an interactive dashboard.

## Features

1. **Introduction**
   - Learn about the factors affecting car prices such as age, odometer reading, fuel type, dealing type, gear system, and number of owners.

2. **Filter Data**
   - Filter the dataset based on car model, dealing type, and gear system to view specific subsets of the data.

3. **Price Predictor**
   - Predict the price of a car based on user inputs including car model, age, odometer reading, dealing type, gear system, and number of owners.

4. **Dashboard**
   - Visualize data using different types of plots such as scatter plots, histograms, box plots, and violin plots. Customize plots by selecting features for the x-axis, y-axis, color, and size.

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**
   ```bash
   cd <project-directory>
   ```

3. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App**
   ```bash
   streamlit run app.py
   ```

## Data

The app uses a dataset of used cars which should be available in the following name:
```
Car Prices Dataset.txt
```
Make sure to adjust the path if the dataset is located elsewhere.

## How to Use

1. **Introduction Page**
   - Provides an overview of factors influencing car prices.

2. **Filter Data Page**
   - Use the sidebar to select car models, dealing types, and gear systems to filter the dataset. The filtered data will be displayed in the main area.

3. **Price Predictor Page**
   - Input car details including model, age, odometer reading, dealing type, gear system, and number of owners to predict the car's price. The predicted price will be shown based on the input values.

4. **Dashboard Page**
   - Choose features for visualization and select the type of plot to generate interactive graphs. You can customize the x-axis, y-axis, color, and size features of the plots.

## Images/Recording

For a visual demonstration of how the app works, you can watch the recording at the following link:

[Car Streamlit App Recording](C:/Users/shrut/Desktop/Car Data Handling & Predictive Model/CarStreamltApp_Recording.mp4)


---
