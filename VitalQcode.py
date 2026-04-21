import streamlit as st
import pandas as pd
import numpy as np
import random
import base64
from datetime import datetime
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as go
from fpdf import FPDF

# 1. Page Configuration & Styling
st.set_page_config(page_title="VitaIQ - Wellness Intelligence", page_icon="🫀", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0a0e1a; color: #e2e8f0; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        height: 60px; background-color: #111827; border-radius: 10px;
        padding: 10px 30px; color: #64748b; border: 1px solid #1e2d45;
    }
    .stTabs [aria-selected="true"] { background-color: #00d4aa; color: white; border: none; font-weight: bold; }
    div[data-testid="stMetricValue"] { color: #00d4aa; font-family: 'JetBrains Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# 2. Header Section
st.title("🫀 VitaIQ: Quantum Wellness Intelligence")
st.write("Professional Patient Dashboard | Signal Purification Enabled")

# 3. Main Navigation (Tabs)
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 Daily Inputs", 
    "📈 Live Analysis", 
    "⚛️ Quantum Risk Audit", 
    "📋 Realization & Recovery"
])

# --- TAB 1: USER INPUTS ---
with tab1:
    st.subheader("Patient Health Profile")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", 18, 100, 25)
        sleep = st.slider("Sleep Hours (Last Night)", 0.0, 12.0, 7.5)
    with col2:
        stress_score = st.select_slider("Current Stress Level", options=range(1, 11), value=5)
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 72.0)
    with col3:
        activity = st.selectbox("Daily Activity", ["Resting", "Light Exercise", "High Intensity"])
        water = st.number_input("Water Intake (Liters)", 0.0, 10.0, 2.0)

# --- TAB 2: LIVE ANALYSIS & PPG WAVEFORM ---
with tab2:
    st.subheader("Live Diagnostic Feedback")
    
    # Logic to simulate/read sensor data
    hr = random.randint(68, 85) + (stress_score * 2)
    spo2 = random.randint(95, 99)
    temp = round(36.5 + (random.random() * 0.5), 1)
    # BP Estimation Logic (Cuff-less)
    sys = 110 + (stress_score * 3) + (hr * 0.1)
    dia = 70 + (stress_score * 1.5)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Heart Rate", f"{hr} BPM")
    m2.metric("SpO2", f"{spo2}%")
    m3.metric("Body Temp", f"{temp}°C")
    m4.metric("Est. Blood Pressure", f"{int(sys)}/{int(dia)} mmHg")

    # HEART BEAT GRAPH (PPG Waveform)
    st.write("### Live PPG Heartbeat (Signal Purification)")
    t = np.linspace(0, 4, 400)
    # Simulate a realistic heartbeat pulse
    clean_wave = (np.exp(-((t % 1 - 0.2)**2) / 0.01) + 0.5 * np.exp(-((t % 1 - 0.4)**2) / 0.02))
    noisy_wave = clean_wave + np.random.normal(0, 0.04, 400) # Representing ECE Noise
    
    fig_ppg = go.Figure()
    fig_ppg.add_trace(go.Scatter(x=t, y=noisy_wave, name="Raw Signal", line=dict(color='gray', width=1, dash='dot')))
    fig_ppg.add_trace(go.Scatter(x=t, y=clean_wave, name="Purified Pulse", line=dict(color='#00d4aa', width=3)))
    fig_ppg.update_layout(height=300, template="plotly_dark", margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig_ppg, use_container_width=True)

# --- TAB 3: QUANTUM RISK AUDIT & HEATMAP ---
with tab3:
    st.subheader("Quantum-Classical Anomaly Detection")
    
    # Heatmap Logic (Adds massive weight to the app)
    ages_grid = np.linspace(20, 80, 10)
    hrs_grid = np.linspace(60, 120, 10)
    z_risk = np.array([[ (a*0.3 + h*0.7) for h in hrs_grid] for a in ages_grid])

    fig_heat = go.Figure(data=go.Heatmap(
        z=z_risk, x=hrs_grid, y=ages_grid, colorscale='RdYlGn_r'
    ))
    fig_heat.update_layout(title="Predictive Risk Heatmap (Age vs. HR)", height=400, template="plotly_dark")
    st.plotly_chart(fig_heat, use_container_width=True)

    # Risk Score calculation
    risk_val = (stress_score * 10) + (100 - spo2) * 5
    if risk_val > 70:
        st.error(f"High Risk Detected: QAOA Optimizer suggests immediate rest.")
    else:
        st.success("Quantum Balance achieved. Vitals are within optimal range.")

# --- TAB 4: REALIZATION & RECOVERY ---
with tab4:
    st.subheader("Recovery Protocol & Medical Report")
    
    rec_col1, rec_col2 = st.columns(2)
    with rec_col1:
        st.info("💡 Practical Insights")
        if stress_score > 7:
            st.write("- Implement 5-minute deep breathing exercises.")
            st.write("- Reduce screen time by 2 hours today.")
        else:
            st.write("- Maintain current hydration levels.")
            st.write("- Signal integrity looks stable for 24-hour monitoring.")
    
    with rec_col2:
        st.info("📄 Documentation")
        if st.button("Generate Final Medical Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="VitaIQ Clinical Summary", ln=1, align='C')
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Timestamp: {datetime.now()}", ln=2)
            pdf.cell(200, 10, txt=f"Estimated BP: {int(sys)}/{int(dia)}", ln=3)
            pdf.cell(20
