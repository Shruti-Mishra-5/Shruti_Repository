import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Car Data Streamlit App",
    page_icon="🚊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS to set the theme
st.markdown("""
    <style>
        /* Set the background color for the main page */
        .main {
            background-color: #2c003e; /* Dark purple background */
            color: #d3d3d3; /* Light grey text */
        }
        
        /* Set the background color and text color for the sidebar */
        .sidebar .sidebar-content {
            background-color: #1a001a; /* Black sidebar */
            color: #d3d3d3; /* Light grey text */
        }
        
        /* Customize the color of the Streamlit components */
        .stButton>button {
            background-color: #4a0080; /* Purple button */
            color: white;
            border-radius: 4px;
        }
        
        .stButton>button:hover {
            background-color: #3b0066; /* Darker purple on hover */
        }
        
        .stTextInput>div>input,
        .stSelectbox>div>div>input {
            border: 2px solid #4a0080; /* Purple border */
            border-radius: 4px;
        }
        
        .stTextInput>div>input:focus,
        .stSelectbox>div>div>input:focus {
            border-color: #3b0066; /* Darker purple border on focus */
        }
        
        .stMarkdown {
            color: #d3d3d3; /* Light grey for markdown text */
        }
        
        .stImage {
            border: 2px solid #4a0080; /* Purple border for images */
        }
        
        /* Customize headers */
        .stTitle,
        .stHeader,
        .stSubheader {
            color: #d3d3d3; /* Light grey headers */
        }
        
        /* Add some spacing and styling for better layout */
        .stTextInput,
        .stSelectbox,
        .stButton {
            margin-bottom: 20px;
        }
        
        .stDataFrame {
            border: 2px solid #4a0080; /* Purple border for dataframes */
            border-radius: 4px;
        }
        
        .stMarkdown {
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)



# Load Data
@st.cache_data
def load_data():
    try:
        # Assuming the dataset is tab-separated
        df = pd.read_csv("C:\\Users\\shrut\\Desktop\\Github\\Projects\\Shruti_Repository\\Car Data Streamlit App\\Car Prices Dataset.txt", delimiter="        ")
        
        # Manually rename the columns if the header is missing or incorrect
        df.columns = ['CarModel', 'AgeOfCar', 'Price', 'OdoMeterReading', 'Fuel', 'DealingType', 'GearSystem', 'NoOfOwners']
        
        return df
    except pd.errors.ParserError as e:
        st.error(f"Error reading the CSV file: {e}")
        return None

df = load_data()

# Preprocess Data
def preprocess_data(df):
    lb = LabelEncoder()
    oe = OrdinalEncoder()
    scaler = MinMaxScaler()

    # Encode CarModel
    if 'CarModel' in df.columns:
        df['CarModel_encoded'] = lb.fit_transform(df['CarModel'])
    else:
        st.error("CarModel column missing in the dataset.")
        return df, lb, oe, scaler

    # Encode DealingType
    if 'DealingType' in df.columns:
        df['DealingType_encoded'] = lb.fit_transform(df['DealingType'])

    # Encode GearSystem
    if 'GearSystem' in df.columns:
        df['GearSystem_encoded'] = lb.fit_transform(df['GearSystem'])
    
    # Encode NoOfOwners
    if 'NoOfOwners' in df.columns:
        df['NoOfOwners_encoded'] = oe.fit_transform(df[['NoOfOwners']])
    
    # Scale AgeOfCar
    if 'AgeOfCar' in df.columns:
        df['AgeOfCar_scaled'] = scaler.fit_transform(df[['AgeOfCar']])
    
    # Scale OdoMeterReading
    if 'OdoMeterReading' in df.columns:
        df['OdoMeterReading_scaled'] = scaler.fit_transform(df[['OdoMeterReading']])
    
    # Scale Price
    if 'Price' in df.columns:
        df['Price_scaled'] = scaler.fit_transform(df[['Price']])
    
    return df, lb, oe, scaler

# Train Model
def train_model(df):
    X = df[['CarModel_encoded', 'AgeOfCar_scaled', 'OdoMeterReading_scaled', 'DealingType_encoded', 'GearSystem_encoded', 'NoOfOwners_encoded']]
    y = df['Price_scaled']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model

# Helper function to handle unseen labels
def safe_transform(encoder, value, column_name):
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        st.warning(f"Unseen label '{value}' encountered in '{column_name}'. Using a default value.")
        return -1  # You can use a default value, such as -1 or any other appropriate value


# Set up the Streamlit pages
def main():
    st.title("Car Data Streamlit App")
    
    df = load_data()
    if df is not None:
        df, lb, oe, scaler = preprocess_data(df)
        model = train_model(df)

        # Page 1: Introduction
        page = st.sidebar.selectbox("Select a page:", ["Introduction","Choose Car By Features", "Price Predictor", "Dashboard"], key="page_selector")

        if page == "Introduction":
            st.write("""
                ## Welcome to the Car Data Streamlit App!
                
                In this app, you can interact with a dataset of used cars to understand their prices and various features.
                
                **Why is it important to check various aspects of a car before buying or selling it?**
                
                1. **Age of the Car**: Older cars may have more wear and tear, which can affect their performance and value. Checking the age helps in understanding depreciation and potential maintenance issues.
                
                2. **Odometer Reading**: The distance a car has traveled is a key indicator of its condition. High mileage can lead to more frequent repairs and lower resale value.
                
                3. **Fuel Type**: Different fuels (petrol, diesel, electric) have different implications for running costs, environmental impact, and maintenance needs.
                
                4. **Dealing Type**: Understanding whether the car was bought from a dealership or a private seller can affect the pricing and warranty status.
                
                5. **Gear System**: Manual vs. automatic transmission can influence the driving experience, fuel efficiency, and resale value.
                
                6. **Number of Owners**: Fewer owners generally indicate a well-maintained vehicle. Multiple owners may suggest potential issues or a troubled history.
                
                7. **Overall Condition**: Regular maintenance and timely repairs play a significant role in a car's longevity and performance. Checking service records can provide insights into the car's history.
                
                **Understanding these factors can help you make informed decisions whether you're buying or selling a car.** 
            """)

        # Page 2: Filter Data
        # Page 2: Filter Data
        elif page == "Choose Car By Features":
            st.title("Choose Car By Features")
            st.sidebar.header("Filter Options")
            
            car_models = st.sidebar.multiselect("Select Car Models", df['CarModel'].unique(), key="car_model_selector")
            dealing_types = st.sidebar.multiselect("Select Dealing Types", df['DealingType'].unique(), key="dealing_type_selector")
            gear_systems = st.sidebar.multiselect("Select Gear Systems", df['GearSystem'].unique(), key="gear_system_selector")
            
            filtered_df = df.copy()  # Start with the original DataFrame

            # Apply filters if the user selects any options
            if car_models:
                filtered_df = filtered_df[filtered_df['CarModel'].isin(car_models)]
            if dealing_types:
                filtered_df = filtered_df[filtered_df['DealingType'].isin(dealing_types)]
            if gear_systems:
                filtered_df = filtered_df[filtered_df['GearSystem'].isin(gear_systems)]
            
            st.write(f"Showing {len(filtered_df)} cars.")
            st.dataframe(filtered_df)

        # Page 3: Price Predictor
        # Page 3: Price Predictor

        # Page 3: Price Predictor
        # Page 3: Price Predictor
        # Page 3: Price Predictor
        elif page == "Price Predictor":
            st.title("Price Predictor")
            
            # User inputs
            car_model_input = st.selectbox("Select Car Model", df['CarModel'].unique(), key="car_model_selectbox")
            age_input = st.number_input("Enter Age of Car (in years)", min_value=0, max_value=int(df['AgeOfCar'].max()), value=3, step=1)
            odo_input = st.number_input("Enter Odometer Reading (in kilometers)", min_value=0, max_value=int(df['OdoMeterReading'].max()), value=50000, step=1000)
            dealing_type_input = st.selectbox("Select Dealing Type", df['DealingType'].unique(), key="dealing_type_selectbox")
            gear_system_input = st.selectbox("Select Gear System", df['GearSystem'].unique(), key="gear_system_selectbox")
            owners_input = st.selectbox("Select Number of Owners", df['NoOfOwners'].unique(), key="owners_selectbox")
            
            # Predict Button
            if st.button("Predict Price"):
                # Check and update the LabelEncoder with any unseen labels
                if car_model_input not in lb.classes_:
                    lb.classes_ = np.append(lb.classes_, car_model_input)
                car_model_encoded = lb.transform([car_model_input])[0]
                
                if dealing_type_input not in lb.classes_:
                    lb.classes_ = np.append(lb.classes_, dealing_type_input)
                dealing_type_encoded = lb.transform([dealing_type_input])[0]
                
                if gear_system_input not in lb.classes_:
                    lb.classes_ = np.append(lb.classes_, gear_system_input)
                gear_system_encoded = lb.transform([gear_system_input])[0]
                
                owners_encoded = oe.transform([[owners_input]])[0][0]
                
                # Scale numerical inputs
                age_scaled = scaler.transform([[age_input]])[0][0]
                odo_scaled = scaler.transform([[odo_input]])[0][0]
                
                # Prepare input features
                input_features = np.array([[car_model_encoded, age_scaled, odo_scaled, dealing_type_encoded, gear_system_encoded, owners_encoded]])
                
                # Predict scaled price
                predicted_price_scaled = model.predict(input_features)[0]
                
                # Inverse transform to get the actual price
                predicted_price = scaler.inverse_transform([[predicted_price_scaled]])[0][0]
                
                # Display the results
                st.write(f"### Predicted Price: ₹{predicted_price:.2f}")
                st.write(f"Based on your inputs, the estimated price for a **{car_model_input}** is approximately **₹{predicted_price:.2f}**.")


        # Page 4: Dashboard
        # Page 4: Dashboard
        # Page 4: Dashboard
        elif page == "Dashboard":
            st.title("Interactive Dashboard")
            
            st.sidebar.header("Choose Features for Visualization")
            
            # Feature selection for the x-axis and y-axis
            x_feature = st.sidebar.selectbox("Select X-axis Feature", options=df.columns, index=df.columns.get_loc("AgeOfCar"))
            y_feature = st.sidebar.selectbox("Select Y-axis Feature", options=df.columns, index=df.columns.get_loc("Price"))
            
            # Optional feature for color or size in scatter plots
            color_feature = st.sidebar.selectbox("Select Color Feature (Optional)", options=[None] + list(df.columns), index=0)
            size_feature = st.sidebar.selectbox("Select Size Feature (Optional)", options=[None] + list(df.columns), index=0)
            
            # Type of plot
            plot_type = st.sidebar.selectbox("Select Plot Type", ["Scatter Plot", "Histogram", "Box Plot", "Violin Plot"])
            
            # Plot generation
            if plot_type == "Scatter Plot":
                fig = px.scatter(df, x=x_feature, y=y_feature, color=color_feature, size=size_feature,
                                title=f'{y_feature} vs {x_feature}', template="plotly_dark")
            
            elif plot_type == "Histogram":
                fig = px.histogram(df, x=x_feature, color=color_feature, nbins=50,
                                title=f'Distribution of {x_feature}', template="plotly_dark", marginal="rug")
            
            elif plot_type == "Box Plot":
                fig = px.box(df, x=x_feature, y=y_feature, color=color_feature,
                            title=f'{y_feature} by {x_feature}', template="plotly_dark")
            
            elif plot_type == "Violin Plot":
                fig = px.violin(df, x=x_feature, y=y_feature, color=color_feature,
                                title=f'{y_feature} by {x_feature}', template="plotly_dark", box=True, points="all")
            
            # Display the plot
            st.plotly_chart(fig)
            
if __name__ == "__main__":
    main()
