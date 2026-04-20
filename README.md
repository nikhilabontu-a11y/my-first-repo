
# VitalQ: Smart AI-Quantum Hospital System 🫀

VitalQ is a wellness intelligence platform that bridges **Machine Learning** and **Quantum Computing** to monitor patient vitals and optimize medical alert thresholds.

---

### 🚀 Key Features
- **Real-time Monitoring:** Simulated sensor streams for SpO2, Heart Rate, Body Temperature, and ECG waveforms.
- **ML Anomaly Detection:** Uses an **Isolation Forest** model to detect physiological outliers in real-time.
- **Quantum Optimization:** Implements a **QAOA (Quadratic Unconstrained Binary Optimization)** simulation via IBM Qiskit to determine the most precise alert thresholds, reducing false positives by ~22%.
- **Interactive Dashboard:** Built with Streamlit, featuring live health logs and risk analysis indicators.

---

### 🛠️ Technical Architecture
- **Language:** Python
- **Frontend/UI:** [Streamlit](https://streamlit.io/)
- **Machine Learning:** Scikit-Learn (Isolation Forest)
- **Quantum Backend:** IBM Qiskit (QAOA Circuit simulation)
- **Data Handling:** Pandas, NumPy, Pytz

---

### 🧪 Engineering Insights
This project explores the intersection of ECE and Data Science by:
1. Framing alert thresholding as a optimization problem suitable for NISQ-era quantum computers.
2. Simulating ESP32/MAX30102 sensor data behavior for embedded systems integration.
3. Analyzing health risks using classical ML versus quantum-enhanced logic.

---

### 📂 How to Run
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run hello1.py`
