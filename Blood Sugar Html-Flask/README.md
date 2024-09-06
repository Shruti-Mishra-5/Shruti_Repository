
# Blood Sugar Predictor Application

This repository contains a web-based Diabetes Prediction Application that utilizes a machine learning model to predict the likelihood of diabetes based on various health parameters. The application is built using Flask for the backend API, python for the machine learning model and HTML, CSS, and JavaScript for the frontend.

## Features

- **User Interface**: Simple and intuitive web interface for entering health parameters.
- **Machine Learning**: The backend is powered by a trained machine learning model (diabetes_model_final.pkl) to predict Blood Sugar Level.
- **Real-time Prediction**: Users receive an instant prediction after submitting their data.
- **Responsive Design**: The frontend is designed to be user-friendly and accessible on different devices.

## Getting Started

### Prerequisites

- **Python 3.7+**
- **Flask**
- **Pickle** (for loading the model)
- **jQuery** (for frontend interactions)

### Installation

1. **Clone the Repository**:

2. **Set up a Virtual Environment** (optional but recommended):

3. **Install Required Python Packages**:

4. **Adjust all the file paths according to your laptop**:

5. **Run the Flask Application**:

6. **Open the HTML File**:

## Screenshots

### 1. User Interface

![UI Output](./Output_images/UI%20Output%20Image.png)

### 2. Prediction Result

![Prediction Output](./Output_images/Prediction%20Image.png)

## Usage

1. Navigate to the application's URL in your web browser.

2. Enter the required health parameters (age, sex (0 for Male and 1 for Female), BMI, BP, S1, S2, S3, S4, S5, S6).

3. Click on the "Submit Data" button.

4. View the predicted diabetes outcome displayed on the page.

## Project Structure

- **REST_API.py**: The Flask backend that handles prediction requests.
- **diabetes_model_final.pkl**: The pre-trained machine learning model.
- **index.html**: The frontend HTML file.
- **/static**: Folder for static assets like CSS and images.
- **/templates**: Folder for HTML templates.

## Acknowledgements

- The machine learning model is based on the Diabetes Dataset from sklearn.
- Special thanks to [jQuery] for simplifying frontend JavaScript.
