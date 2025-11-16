import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

# Load dataset
df = pd.read_csv("C:\\Users\\shrut\\Desktop\\QTechnologies\\Project 1\\ai4i2020.csv")

# Required columns for training
required_columns = ['Type', 'Air temperature [K]', 'Process temperature [K]', 
                    'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'Machine failure']

# Ensure required columns exist
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in dataset: {missing_cols}")

# Drop unnecessary columns
df = df[required_columns]

# Encode 'Type'
label_encoder = LabelEncoder()
df['Type'] = label_encoder.fit_transform(df['Type'])

# Separate features (X) and target (y)
X = df.drop(columns=['Machine failure'])
y = df['Machine failure']

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save scaler for consistent preprocessing
import joblib
joblib.dump(scaler, 'scaler.pkl')

# Train on non-failure data (y == 0)
X_train, X_test = train_test_split(X_scaled[y == 0], test_size=0.2, random_state=42)

# Define Autoencoder Model
input_dim = X_train.shape[1]
input_layer = Input(shape=(input_dim,))
encoded = Dense(8, activation="relu")(input_layer)
encoded = Dense(4, activation="relu")(encoded)
decoded = Dense(8, activation="relu")(encoded)
decoded = Dense(input_dim, activation="sigmoid")(decoded)

autoencoder = Model(input_layer, decoded)
autoencoder.compile(optimizer="adam", loss="mse")

# Train Autoencoder
autoencoder.fit(X_train, X_train, epochs=50, batch_size=32, shuffle=True, validation_data=(X_test, X_test))

# Save Model
autoencoder.save("autoencoder_model.h5")
print("✅ Autoencoder model saved as 'autoencoder_model.h5'")
