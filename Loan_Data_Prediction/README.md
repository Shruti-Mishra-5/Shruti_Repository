# Loan Approval Prediction Using Machine Learning Pipelines

## Problem Statement
The objective of this project is to preprocess a loan dataset using multiple techniques for handling missing values, encoding categorical variables, and scaling numerical variables. The processed data is then used to train and evaluate machine learning models, followed by ensemble methods to compare model performance.

---

## Objectives
- Handle missing values using multiple imputation techniques
- Apply appropriate encoders for categorical variables
- Scale numerical variables using different scaling techniques
- Train baseline and advanced machine learning models
- Compare ensemble models: Voting, Bagging, and Stacking
- Evaluate model performance using multiple metrics

---

## Libraries Used
- Pandas, NumPy
- Matplotlib, Seaborn
- scikit-learn (models, preprocessing, evaluation)
- category_encoders (Target Encoder)
- Custom Transformers (Random Sample Imputer)

---

## Workflow

### 1. Load Dataset
- Read CSV/Excel file
- Split into independent variables (X) and target variable (y)

### 2. Handle Missing Values
Techniques used:
- Complete Case Analysis
- SimpleImputer
- Random Sample Imputation (custom method)

### 3. Encode Categorical Variables
| Encoder | Usage |
|---------|-------|
| OneHotEncoder | Nominal categorical variables |
| OrdinalEncoder | Ordered categorical variables |
| Target Encoder | High-cardinality categorical fields |

### 4. Scale Numerical Variables
| Scaler | Usage |
|--------|-------|
| StandardScaler | Continuous numeric values |
| RobustScaler | Outlier-sensitive numeric values |
| MaxAbsScaler | Range-based numeric values |

### 5. Model Training
Models trained and evaluated:
- Logistic Regression
- Random Forest
- Support Vector Machine (SVM)
- KNN (optional baseline)

Evaluation Metrics:
- Accuracy
- Precision
- Recall
- F1 Score
- Cross-Validation
- GridSearchCV for tuning

### 6. Ensemble Learning
| Method | Description |
|--------|-------------|
| Hard Voting | Majority voting on predictions |
| Soft Voting | Probability average voting |
| Bagging | Reduces variance through resampling |
| Stacking | Meta-learning on base models |
---

