
## **README.md** – *Industrial Equipment Failure Prediction System*

---

# Industrial Equipment Failure Prediction System

**A dual-layer system to predict and prevent industrial equipment failures using deep learning and real-time graph simulation.**

---

## **Project Overview**

This project uses:

1. **Autoencoder Model** – Detects machine failures by identifying anomalies in sensor data.  
2. **Graph-Based Simulation** – Simulates real-time equipment behavior and highlights at-risk components.

---

## **Features:**
**1. Upload Machine Data (CSV)** – Analyze any dataset with relevant machinery readings.  
2. **Failure Detection** – Identify abnormal machine behavior using a trained **autoencoder**.  
3. **Real-Time Stress Simulation** – Simulate and track equipment failures in real time.  
4. **Dynamic Alerts** – Receive alerts when potential failures are detected.  
5. **Visual Outputs** – Clear charts and network graphs for easy understanding.  

---

## **Technologies Used**
- **Python 3.x** – Core programming language.  
- **TensorFlow/Keras** – For training and deploying the **autoencoder**.  
- **Streamlit** – To provide an **interactive user interface**.  
- **Scikit-learn** – For **data preprocessing** and normalization.  
- **NetworkX** – For **graph-based** equipment monitoring.  
- **Matplotlib** – For plotting graphs and **data visualization**.  

---

## **Project Structure**

```
Project 1/
├── app.py                   # Streamlit UI (User interface)
├── model_training.py        # Autoencoder model training
├── real_time_predictor.py   # Graph-based failure predictor
├── requirements.txt         # Python package dependencies
└── Images
└── ai4i2020.csv             # Machine data (Sample dataset)
```

---

## **How the System Works**

### 1. **Machine Failure Prediction (Autoencoder)**

- **Input**: Machine data (e.g., temperature, torque, speed).
- **Process**:
    - Preprocess and normalize input data.
    - Reconstruct normal machine behavior.
    - Flag anomalies when reconstruction errors exceed a threshold.
- **Output**: Detects abnormal machine behavior and predicts potential failures.

### 2. **Graph-Based Real-Time Monitoring**

- **Input**: Number of machine components (nodes) and sensitivity settings.
- **Process**:
    - Simulate equipment behavior in real time.
    - Track overworked machine parts (nodes/edges).
    - Identify failure risks based on load.
- **Output**: Alerts and visualizations for at-risk components.

---

## **Installation Guide**

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-username/Industrial-Failure-Predictor.git
cd Industrial-Failure-Predictor
```

### 2. **Set Up a Virtual Environment** (Optional but Recommended)

- **Windows**:
```bash
python -m venv venv
.\venv\Scripts\activate
```

- **Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install Dependencies**
Ensure **Python 3.x** is installed and run:

```bash
pip install -r requirements.txt
```

### 4. **Check the Dataset**
Ensure your **machine data** (e.g., `ai4i2020.csv`) is in the `/data` folder.  
You can use any CSV file with the following columns:

| Column Name             | Description                      |
|-------------------------|----------------------------------|
| **Type**                | Machine Type (L, M, H)           |
| **Air temperature [K]** | Air temperature in Kelvin        |
| **Process temperature**  | Internal process temperature     |
| **Rotational speed [rpm]** | Machine speed in RPM         |
| **Torque [Nm]**         | Torque applied (Newton-meters)   |
| **Tool wear [min]**     | Time tool has been in operation  |
| **Machine failure**     | 1 = Failure, 0 = No failure      |

---

## **Running the System**

### 1. **Train the Autoencoder**
If this is your **first time running** the system, train the autoencoder:

```bash
python model_training.py
```

This will:
- Preprocess the data.
- Train the **autoencoder** on non-failure data.
- Save the model as `autoencoder_model.h5`.

---

### 2. **Start the Streamlit Application**
To launch the interactive interface:

```bash
streamlit run app.py
```

---

## **Using the App**

1. **Upload Machine Data**:
   - Upload a CSV with relevant machinery data.
   - View **detected failures** and **anomaly analysis**.
2. **Simulate Equipment Stress**:
   - Choose node size and sensitivity.
   - Identify at-risk components **in real time**.

---

## **Output Examples**

**When No Failures Are Detected:**
```
No Machine Failures Detected! Your equipment is operating normally.
```

**When Failures Are Found:**
```
⚠️ Detected 3 Failures out of 120 records!

Recommendation: Inspect flagged machines for potential issues.
```

**Graph-Based Stress Alerts:**
```
Step 5/50:
⚠️ Potential Failures Detected!
🔴 At-Risk Components (Nodes): [6, 18]
🟠 At-Risk Connections (Edges): [(6, 9), (10, 18)]
```

---

## **Customizing the App**

### 1. **Change the Model Parameters**
Modify **autoencoder layers** in **model_training.py**:
```python
encoded = Dense(16, activation="relu")(input_layer)  # Increase layer size
```

### 2. **Adjust Failure Sensitivity**
In **app.py**, change the detection threshold:
```python
threshold = np.percentile(mse, 90)  # More sensitive (lower value)
```

### 3. **Use Different Datasets**
Upload any dataset in CSV format with the expected columns.

---

## **Troubleshooting**

1. **Shape Mismatch Error**  
   Ensure input features during prediction match those used during training.  
2. **Streamlit Not Recognized**  
   Install Streamlit again:
   ```bash
   pip install streamlit
   ```

---

## **Future Enhancements:**
**Live IoT Data** – Integrate real-time machine sensor feeds.  
**Failure Dashboard** – Generate reports for management insights.  
**Automated Alerts** – Send email notifications for critical failures.  

---

## **Contributing**
Feel free to contribute by:
1. **Forking the repo**
2. **Creating a feature branch**
3. **Submitting a pull request**

---

## **License**
This project is licensed under the **MIT License**.

---

## **Contact**
For questions or suggestions:
- **Your Name**
- Email: your@email.com
- GitHub: [your-username](https://github.com/your-username)

---

**Thank you for using the Industrial Equipment Failure Prediction System!**  
We hope this tool helps you maintain **safe**, **efficient**, and **reliable** equipment.
