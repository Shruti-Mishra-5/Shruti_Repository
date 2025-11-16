
# Traffic Condition Prediction Application

This repository contains a Machine Learning Pipeline project designed to predict **traffic conditions** based on various real-world traffic and environmental parameters.  
The project focuses on **complete data preprocessing**, **pipeline deployment**, and **model comparison using AUC-ROC**.

The system preprocesses raw traffic data, builds ML pipelines, compares multiple classification models, and finally saves the best model for later use.

---

## Features

- Complete data preprocessing pipeline
- Automatic handling of missing values
- Encoding of categorical features
- Scaling of numerical features
- Comparison of multiple ML models
- AUC-ROC based model selection
- Model saved as pickle file for reuse

---

## Data Processing Workflow

The dataset contained **both numerical and categorical columns** along with missing values.  
The following preprocessing steps were applied:

### 1. Missing Value Handling
Multiple imputation strategies were used:
- Mean Imputation (for continuous numeric columns)
- Mode Imputation (for categorical columns)
- Constant Imputation (for outlier-prone columns)
- Custom Random Sample Imputation (for probabilistic replacement)

A custom transformer class (`RandomSampleImputer`) was implemented.

### 2. Encoding of Categorical Features
Different encoding techniques were used:
- One-Hot Encoding
- Ordinal Encoding (for ordered categories such as traffic light state)
- Target Encoding (optional, for categorical columns correlated with output)

### 3. Scaling of Numerical Features
Numerical columns were normalized using:
- StandardScaler
- MaxAbsScaler
- RobustScaler (for skewed distributions)

### 4. ColumnTransformer + Pipeline
A **ColumnTransformer** was used to apply different transformations to different column types.


## Machine Learning Models Used

Three different pipelines were trained and compared:

1. Logistic Regression Pipeline
2. K-Nearest Neighbors Classifier Pipeline
3. Linear SVM Classifier Pipeline

Each model used the **same preprocessing block** to ensure fair comparison.

---

## Model Evaluation

Evaluation Metrics Used:

- Train/Test Accuracy
- F1 Score
- Confusion Matrix
- Cross-Validation Accuracy
- Hyperparameter Tuning using GridSearchCV
- AUC-ROC Curve Comparison (Multiclass OVR)

AUC-ROC was used to determine the final best-performing model.

---

## Output Files

- `models.pkl` – Contains trained ML models saved using pickle
- Preprocessed dataset stored in memory before training
- ROC curves generated for comparison

---

## Project Structure

---

## Technologies Used

- Python 3
- NumPy, Pandas
- Scikit-Learn
- Matplotlib
- Seaborn
- category-encoders
- Pickle

---

## How to Run

1. Install required libraries

2. Place dataset in the project directory

3. Run the notebook or Python script

4. A pickle file (`models.pkl`) will be generated

---

## Acknowledgements

- Dataset based on synthetic traffic features
- Scikit-Learn for ML models and pipeline support
- Matplotlib and Seaborn for visualization


