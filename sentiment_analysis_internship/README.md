# Customer Satisfaction Sentiment Analysis 

This project is a Flask web application that allows users to upload CSV or Excel files containing customer reviews and analyzes the sentiment of these reviews (positive, neutral, negative) using the Groq API. The app then displays the results on a web page.

## Features
- Upload CSV or Excel files containing customer reviews.
- Sentiment analysis (positive, negative, neutral) performed using the Groq API.
- Results displayed on the web interface in an easy-to-read format.

## Requirements

### Python Dependencies

The following libraries are required to run the app:

- flask
- Pandas
- Requests
- Os (if working with Excel files)
- time


## Setting Up

### 1. Install all the requirements

You can install the required libraries using `pip`:

```bash
pip install flask pandas requests os time
```

### 2. Set Up API Key

You need to obtain an API key from Groq to use their sentiment analysis service.

Once you have the key, add it to your application.

You need to create your own API Key for it to work properly.

#### Option 1: Hardcoding the API Key

In the `app.py` file, replace the existing API key with your own:

```python
GROQ_API_KEY = 'your_new_groq_api_key'
```

#### Option 2: Using Environment Variables (Recommended)

You can store the API key as an environment variable for better security. Modify the `app.py` file to:

```python
import os
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
```

Then set the environment variable in your terminal:

- ```cmd
  set GROQ_API_KEY=your_new_groq_api_key
  ```

### 3. Run the Application

You can run the app locally using Flask's development server.

The app will be available at `http://127.0.0.1:5000/`.

### 4. Upload a File

- Visit `http://127.0.0.1:5000/` in your browser.
- Upload a CSV or Excel file containing customer reviews.
- The app will process the file, analyze each review's sentiment, and display the results.

## Project Structure

```bash
.
├── sentiment_analysis_internship.py 
├── templates
│   └── upload.html    
├── static
│   └── styles.css     
├── README.md           

```

## File Format

Ensure that your file follows these guidelines for proper analysis:
- File type: `.csv` or `.xlsx`
- Column with reviews: **Review**
- Example:

| Review                   |
|---------------------------|
| This product is amazing!   |
| The service was terrible.  |
| I had a neutral experience.|

## API Usage

The app sends each review to the Groq API for sentiment analysis using the endpoint. The results are categorized as positive, negative, or neutral.

## Customizing the Project

Further file can be modified to:
- Add support for more file formats.
- Use different models from the Groq API.
- Display additional statistics like word clouds, review counts, etc.

## Troubleshooting

- If the app fails to analyze reviews, ensure that:
  - You have set the correct Groq API key.
  - The file format is supported.
  - The column with reviews is named `Review`.
- If you get a rate limit error from Groq, consider adding a delay between API requests or upgrading your API plan.


## Requirements of the project

This project is exactly according to the requirements asked with an addition of front end work while trying to maintain a proper structure, appropriate variable names, error handling and proper documentation.


