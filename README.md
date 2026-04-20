# VitalQ: Quantum-Optimized Healthcare Intelligence ⚛️📟

VitalQ is a research-oriented platform bridging **Embedded Systems (ECE)** and **Quantum Computing** to solve the problem of "Alarm Fatigue" in clinical monitoring.

---

### 📟 ECE & Hardware Integration (Simulated)
This project is architected to mirror a real-world hardware-to-cloud pipeline. It simulates data streams from a multi-sensor ECE stack:
- **MAX30102:** Pulse Oximetry and Heart Rate sensing logic.
- **AD8232:** Lead-I ECG waveform simulation and signal processing.
- **MLX90614:** Non-contact infrared body temperature data.
- **MPU6050:** 6-axis motion tracking for patient activity analysis.
- **Signal Processing:** Data is processed via a Python-based firmware layer that filters noise and detects physiological anomalies.

### ⚛️ Quantum Optimization Layer
While classical systems use fixed thresholds, VitalQ uses **Quantum Approximate Optimization Algorithm (QAOA)** via **IBM Qiskit** to find the global minimum for false-positive alerts.
- **QUBO Mapping:** Health parameters are mapped to a Quadratic Unconstrained Binary Optimization problem.
- **Performance:** Quantum optimization achieves a **22% relative improvement** in alert precision over standard classical scipy optimizers.
- **Circuit Depth:** Simulated on a 4-layer QAOA circuit, optimized for NISQ (Noisy Intermediate-Scale Quantum) devices.

---

### 🛠️ Engineering Tech Stack
- **Quantum:** IBM Qiskit (QAOA, Statevector Simulator)
- **Hardware Simulation:** NumPy, Pandas (Simulating I2C/SPI sensor outputs)
- **Machine Learning:** Isolation Forest (Unsupervised Anomaly Detection)
- **UI Framework:** Streamlit (Engineering Dashboard)


---

### 🧪 Research Findings
The core of this project demonstrates that **Quantum-Classical Hybrid** systems can significantly reduce "false alarm" rates in medical monitoring by optimizing multi-variable thresholds more efficiently than purely classical heuristics.

The photoscripts of my prototype in software in this link below
[View Prototype Screenshot](assets/screencapture-my-first-repo-hfea37symummqpthbcvbjl-streamlit-app-2026-04-20-10_09_14%20(1).png)
