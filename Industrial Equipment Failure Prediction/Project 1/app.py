import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import joblib
from tensorflow.keras.models import load_model
from real_time_predictor import RealTimeFailurePredictor
import random

# Load Autoencoder Model and Scaler
autoencoder = load_model("autoencoder_model.h5")
scaler = joblib.load("scaler.pkl")

# Define required columns
required_columns = ['Type', 'Air temperature [K]', 'Process temperature [K]', 
                    'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']

# ✅ Welcome Message
st.title("⚙️ Universal Machine Failure Prediction System")
st.write("""
This system predicts **machine failures** by analyzing sensor data and simulating real-time equipment stress.  
You can:
1. **Upload a dataset** to detect potential failures.
2. **Simulate equipment stress** and observe vulnerable machine parts.
""")

# 📤 Upload CSV
uploaded_file = st.file_uploader("📊 Upload Machine Data (CSV)", type=["csv"])

# 🔎 Preprocess Data Function
def preprocess_data(df):
    # Inform the user of uploaded columns
    st.write("📋 Uploaded Columns: ", df.columns.tolist())
    
    # Ensure required columns are present
    for col in required_columns:
        if col not in df.columns:
            st.warning(f"⚠️ Missing column '{col}', filling with zero.")
            df[col] = 0

    # Keep only required columns (ensure consistent input shape)
    df = df[required_columns]

    # Encode 'Type' column
    df['Type'] = pd.factorize(df['Type'])[0]

    # Normalize input using the original scaler
    X = scaler.transform(df)

    st.write(f"✅ Data Prepared! Shape: {X.shape}")
    return X

# 📊 Machine Failure Prediction Workflow
if uploaded_file:
    # Load Data
    df = pd.read_csv(uploaded_file)
    st.write("📄 **Dataset Preview**:", df.head())
    
    # Preprocess Data
    X = preprocess_data(df)

    # Prediction Process
    st.write("🔍 **Analyzing Data for Anomalies...**")
    X_pred = autoencoder.predict(X)

    # Mean Squared Error Calculation
    mse = np.mean(np.square(X - X_pred), axis=1)

    # Set Dynamic Threshold (95th Percentile of Normal Data)
    threshold = np.percentile(mse, 95)

    # Identify Anomalies (Failures)
    anomalies = mse > threshold
    total_failures = np.sum(anomalies)

    # Display Prediction Results
    if total_failures == 0:
        st.success("✅ **No Machine Failures Detected!** Your equipment is operating normally.")
    else:
        st.error(f"⚠️ **Detected {total_failures} Failures** out of {len(X)} records!")
        st.write("👉 **Recommendation:** Inspect flagged machines for potential issues.")

    # 📊 Visualize Anomalies
    plt.figure(figsize=(10, 5))
    plt.hist(mse, bins=50, alpha=0.7, color="blue", label="Normal Data")
    plt.axvline(threshold, color="red", linestyle="dashed", label="Failure Threshold")
    plt.title("Machine Failure Detection")
    plt.xlabel("Reconstruction Error")
    plt.ylabel("Frequency")
    plt.legend()
    st.pyplot(plt)

# 📈 Graph-Based Failure Simulation
st.sidebar.header("🛠️ Simulate Equipment Stress")
num_nodes = st.sidebar.slider("🔢 Number of Components (Nodes)", 50, 200, 100)
failure_threshold = st.sidebar.slider("⚠️ Failure Sensitivity", 0.5, 1.0, 0.8)

# Create Graph for Monitoring
G = nx.erdos_renyi_graph(num_nodes, 0.1)
predictor = RealTimeFailurePredictor(G, failure_threshold=failure_threshold)

# 🕵️ Real-Time Graph Simulation
if st.sidebar.button("▶️ Start Simulation"):
    st.write("⏳ **Simulating Real-Time Equipment Behavior...**")

    for step in range(50):
        active_nodes = random.sample(list(G.nodes()), len(G) // 4)
        active_edges = random.sample(list(G.edges()), len(G.edges()) // 4)

        predictor.update_loads(active_nodes, active_edges)
        failing_nodes, failing_edges = predictor.predict_failures()

        st.write(f"📊 **Step {step + 1}/50:**")
        if failing_nodes or failing_edges:
            st.warning("⚠️ **Potential Failures Detected!**")
            if failing_nodes:
                st.write(f"🔴 **At-Risk Components (Nodes):** {failing_nodes}")
            if failing_edges:
                st.write(f"🟠 **At-Risk Connections (Edges):** {failing_edges}")
        else:
            st.info("✅ **All systems stable.**")

        # Graph Visualization
        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 8))
        nx.draw(G, pos, with_labels=True, node_size=300, node_color="lightblue")
        nx.draw_networkx_nodes(G, pos, nodelist=failing_nodes, node_color="red")
        nx.draw_networkx_edges(G, pos, edgelist=failing_edges, edge_color="orange")
        plt.title("Equipment Stress Simulation")
        st.pyplot(plt)

    st.success("🏁 **Simulation Complete!**")

