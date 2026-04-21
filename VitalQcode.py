import streamlit as st
import pandas as pd
import numpy as np
import random
import base64
from datetime import datetime
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as go
from fpdf import FPDF

# 1. Page Configuration
st.set_page_config(page_title="VitaIQ - Health Intelligence", page_icon="🫀", layout="wide")

# Custom Styling (Removing Sidebar & Adding Patient-Friendly UI)
st.markdown("""
<style>
    .main { background-color: #0a0e1a; color: #e2e8f0; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #111827; border-radius: 10px;
        padding: 10px 25px; color: #64748b; border: 1px solid #1e2d45;
    }
    .stTabs [aria-selected="true"] { background-color: #00d4aa; color: white; border: none; }
</style>
""", unsafe_allow_html=True)

st.title("🫀 VitaIQ: Wellness Intelligence Portal")

# 2. Main Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Daily Profile", 
    "2. Live Analysis", 
    "3. Quantum Risk Audit", 
    "4. Realization & Recovery"
])

# --- TAB 1: USER INPUTS ---
with tab1:
    st.header("Personal Health Inputs")
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Age", 18, 100, 25)
        sleep = st.slider("Sleep Hours", 0.0, 12.0, 7.0)
    with c2:
        stress = st.select_slider("Stress Level", options=range(1, 11), value=5)
        water = st.number_input("Water Intake (Glasses)", 0, 20, 8)

# --- TAB 2: LIVE ANALYSIS ---
with tab2:
    st.header("Diagnostic Feedback")
    # Simulated Vitals
    hr = random.randint(70, 90) + (stress * 2)
    spo2 = random.randint(95, 99)
    temp = round(36.5 + (random.random() * 0.4), 1)
    sys, dia = 110 + (stress * 2), 70 + (stress * 1) # Estimated BP

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Heart Rate", f"{hr} BPM")
    m2.metric("SpO2", f"{spo2}%")
    m3.metric("Body Temp", f"{temp}°C")
    m4.metric("Est. BP", f"{sys}/{dia}")

    # Heart Beat Graph (PPG Waveform)
    st.subheader("Live PPG Waveform")
    t = np.linspace(0, 4, 400)
    clean_wave = (np.exp(-((t % 1 - 0.2)**2) / 0.01) + 0.5 * np.exp(-((t % 1 - 0.4)**2) / 0.02))
    fig_ppg = go.Figure()
    fig_ppg.add_trace(go.Scatter(x=t, y=clean_wave, name="Purified Pulse", line=dict(color='#00d4aa', width=3)))
    fig_ppg.update_layout(height=250, template="plotly_dark", margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig_ppg, use_container_width=True)

# --- TAB 3: QUANTUM RISK AUDIT ---
with tab3:
    st.header("Quantum-Classical Anomaly Detection")
    # Risk Heatmap for Weight
    ages = np.linspace(20, 80, 10)
    hrs = np.linspace(60, 120, 10)
    risk_z = np.array([[ (a*0.2 + h*0.8) for h in hrs] for a in ages])
    
    fig_heat = go.Figure(data=go.Heatmap(z=risk_z, x=hrs, y=ages, colorscale='RdYlGn_r'))
    fig_heat.update_layout(title="Risk Zone Mapping", height=400, template="plotly_dark")
    st.plotly_chart(fig_heat, use_container_width=True)

# --- TAB 4: REALIZATION & RECOVERY ---
with tab4:
    st.header("Recovery Protocol")
    risk_score = (stress * 10) + (100 - spo2) * 5
    recommendations = ["Increase hydration.", "Target 8 hours of sleep."] if risk_score < 60 else ["Immediate rest required.", "Avoid caffeine.", "Monitor oxygen levels."]
    
    for r in recommendations:
        st.write(f"✅ {r}")

    # Functional PDF Report Generator
    if st.button("Generate Medical Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="VitaIQ Clinical Report", ln=1, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Risk Score: {int(risk_score)}", ln=2)
        pdf.cell(200, 10, txt=f"Vitals: {hr} BPM | {spo2}% SpO2", ln=3)
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        b64 = base64.b64encode(pdf_output).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="VitaIQ_Report.pdf">📥 Download Report</a>'
        st.markdown(href, unsafe_allow_html=True)
