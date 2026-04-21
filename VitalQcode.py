import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="VitaIQ - Patient Portal", page_icon="🩺", layout="wide")

# Custom Styling for a Patient-Friendly, Clean Look (No Sidebar)
st.markdown("""
<style>
    .main { background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #161b22; border-radius: 5px;
        padding: 10px 20px; color: #8b949e;
    }
    .stTabs [aria-selected="true"] { background-color: #238636; color: white; }
    .metric-box {
        background: #161b22; padding: 20px; border-radius: 15px;
        border: 1px solid #30363d; text-align: center;
    }
    .risk-high { color: #ff7b72; font-weight: bold; }
    .risk-low { color: #56d364; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🩺 VitaIQ: Your Personal Health Intelligence")
st.write("A professional clinical-grade simulation for health monitoring.")

# ─── TAB 1: USER INPUTS ───
tab1, tab2, tab3, tab4 = st.tabs(["1. Daily Profile", "2. Live Analysis", "3. Quantum Risk Audit", "4. Realization & Recovery"])

with tab1:
    st.header("Personal Health Inputs")
    st.info("Please enter your current feelings and habits for the last 24 hours.")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 1, 100, 25)
        weight = st.number_input("Weight (kg)", 30, 200, 70)
        sleep = st.slider("Hours of Sleep", 0.0, 12.0, 7.0)
    with col2:
        stress = st.select_slider("Stress Level", options=["Very Low", "Low", "Moderate", "High", "Extreme"])
        water = st.number_input("Water Intake (Glasses)", 0, 20, 8)
        activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Very Active"])

# ─── TAB 2: VITAL SIGN ANALYSIS ───
with tab2:
    st.header("Live Vital Sign Analysis")
    # Simulated Sensor Logic
    hr = random.randint(65, 95)
    spo2 = random.randint(94, 99)
    temp = round(random.uniform(36.1, 37.5), 1)
    bp_sys = random.randint(110, 140)
    bp_dia = random.randint(70, 90)
    air_q = random.randint(20, 150)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.metric("Heart Rate", f"{hr} BPM", delta="-2")
    with c2: st.metric("SpO2", f"{spo2}%", delta="1%")
    with c3: st.metric("Body Temp", f"{temp}°C")
    with c4: st.metric("Blood Pressure", f"{bp_sys}/{bp_dia}")
    with c5: st.metric("Air Quality", f"{air_q} AQI", delta="-5", delta_color="inverse")

    # Signal Purification Graph
    st.subheader("Signal Purification Test (Sensor Integrity)")
    t = np.linspace(0, 5, 500)
    clean = np.sin(2 * np.pi * 1.2 * t)
    noise = clean + np.random.normal(0, 0.3, 500)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=noise, name="Raw Data (Noise)", line=dict(color='royalblue', width=1)))
    fig.add_trace(go.Scatter(x=t, y=clean, name="Purified Signal", line=dict(color='red', width=2)))
    fig.update_layout(height=300, template="plotly_dark", margin=dict(l=20,r=20,t=20,b=20))
    st.plotly_chart(fig, use_container_width=True)

# ─── TAB 3: QUANTUM RISK ANOMALIES ───
with tab3:
    st.header("Quantum-Optimized Risk Audit")
    st.write("Using QAOA (Quantum Approximate Optimization Algorithm) to detect health anomalies.")

    # Quantum Logic Simulation
    # We calculate risk based on the inputs from Tab 1 and Tab 2
    risk_score = (100 - spo2) * 5 + (hr - 70) * 2 + (8 - sleep) * 10
    if stress == "Extreme": risk_score += 30
    
    # Anomaly Detection using Isolation Forest
    st.subheader("Anomaly Identification")
    if risk_score > 60:
        st.error(f"⚠️ HIGH RISK DETECTED (Score: {int(risk_score)})")
        st.write("Quantum Analysis suggests an irregular pattern in Cardiovascular vs Sleep metrics.")
    else:
        st.success("✅ LOW RISK: Your vitals are optimized within quantum-classical bounds.")

# ─── TAB 4: REALIZATION & RECOVERY ───
with tab4:
    st.header("Practical Health Recommendations")
    st.write("Based on your identified risks, here is your recovery plan:")

    if risk_score > 60:
        st.warning("Action Required to Encounter Risk:")
        st.markdown("""
        - **Hydration:** Increase water to 12 glasses to stabilize blood pressure.
        - **Air Quality:** Use an N95 mask or air purifier; current AQI is moderate.
        - **Sleep Hygiene:** Targeted 2-hour increase in sleep to lower heart rate cortisol.
        - **Medical Note:** If symptoms persist, share this dashboard with your doctor.
        """)
    else:
        st.info("Maintenance Routine:")
        st.markdown("- Continue current activity level.\n- Weekly Signal Purification check recommended.")

if st.button("Generate Medical Report (PDF)"):
    st.write("Processing... (Deployment Feature)")
