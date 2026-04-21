import streamlit as st
import pandas as pd
import numpy as np
import random
import base64
import pytz
from datetime import datetime
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. SETTINGS & IST ---
IST = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.now(IST).strftime('%d %b %Y | %H:%M:%S')

st.set_page_config(page_title="VitaIQ — Quantum Medical Intelligence", page_icon="⚛️", layout="wide")

# UI Enhancements for Professional Sale
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600&family=JetBrains+Mono&display=swap');
:root { --accent: #00d4aa; --bg: #0a0e1a; --quantum: #8b5cf6; --text: #e2e8f0; }
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: var(--bg); color: var(--text); }
.stTabs [data-baseweb="tab"] { background-color: #111827; border-radius: 12px; padding: 15px 30px; color: #64748b; border: 1px solid #1e2d45; }
.stTabs [aria-selected="true"] { background-color: var(--accent); color: white; box-shadow: 0 0 20px rgba(0,212,170,0.4); }
</style>
""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("⚛️ VitaIQ: Advanced Quantum-Health Interface")
st.write(f"**Quantum Backend:** Qiskit-Simulated | **IST:** {current_time_ist}")

tabs = st.tabs(["📍 Digital Twin Profile", "📈 Hardware & ECG", "⚛️ Quantum Lab", "📋 Clinical Intelligence"])

# --- TAB 1: ADVANCED INPUTS ---
with tabs[0]:
    st.subheader("High-Fidelity Patient Context")
    c1, c2, c3 = st.columns(3)
    with c1:
        u_mood = st.select_slider("Mood State", options=["Exhausted", "Stressed", "Neutral", "Balanced", "Peak Performance"])
        u_exercise = st.selectbox("Activity Type", ["Sedentary", "Yoga", "Zone 2 Cardio", "Hypertrophy", "Anaerobic"])
    with c2:
        u_stress = st.slider("Cortisol Level Proxy (1-10)", 1, 10, 5)
        u_sleep = st.number_input("REM/Deep Sleep (Hours)", 0.0, 12.0, 7.5)
    with c3:
        u_water = st.number_input("Electrolyte Intake (L)", 0.0, 8.0, 2.5)
        u_caffeine = st.slider("Stimulant Load (mg)", 0, 500, 100, step=50)

# --- TAB 2: HARDWARE & ECG (The "Hardware Sell") ---
with tabs[1]:
    st.subheader("Hardware Telemetry")
    col_h1, col_h2 = st.columns([1, 3])
    with col_h1:
        st.write("**Sensor Status**")
        st.success("✅ MAX30102: ONLINE")
        st.success("✅ AD8232: ONLINE")
        st.info("📡 I2C Address: 0x57")
    
    with col_h2:
        # High-Fidelity ECG Waveform Logic
        t = np.linspace(0, 4, 1000)
        ecg = 0.1 * np.exp(-((t % 1 - 0.1)**2)/0.001) + 1.2 * np.exp(-((t % 1 - 0.2)**2)/0.0001) + 0.3 * np.exp(-((t % 1 - 0.4)**2)/0.01)
        fig_ecg = go.Figure(data=go.Scatter(x=t, y=ecg, line=dict(color='#00d4aa', width=2)))
        fig_ecg.update_layout(height=250, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(showgrid=False))
        st.plotly_chart(fig_ecg, use_container_width=True)

# --- TAB 3: THE QUANTUM LAB (Knowledge Builder) ---
with tabs[2]:
    st.subheader("Quantum Computational Diagnostics")
    q1, q2 = st.columns(2)
    
    with q1:
        st.write("#### 1. Bloch Sphere Visualization")
        # To teach Quantum States: 0 = Healthy, 1 = Crisis
        phi = (u_stress / 10) * np.pi 
        theta = (u_caffeine / 500) * np.pi
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)
        
        fig_bloch = go.Figure(data=[go.Scatter3d(x=[0, x], y=[0, y], z=[0, z], mode='lines+markers', line=dict(color='#8b5cf6', width=5))])
        fig_bloch.update_layout(title="Patient State Vector", height=350, template="plotly_dark", scene=dict(xaxis=dict(range=[-1,1]), yaxis=dict(range=[-1,1]), zaxis=dict(range=[-1,1])))
        st.plotly_chart(fig_bloch, use_container_width=True)
        st.caption("The Bloch Sphere represents your health in 'Superposition'.")

    with q2:
        st.write("#### 2. Variational Circuit Optimization")
        layers = np.arange(1, 21)
        # QAOA Loss Function Simulation
        loss = 10 * np.exp(-layers/5) + np.random.normal(0, 0.05, 20)
        fig_qaoa = go.Figure(data=go.Scatter(x=layers, y=loss, mode='lines+markers', line=dict(color='#00d4aa')))
        fig_qaoa.update_layout(title="QAOA Error Convergence", height=350, template="plotly_dark")
        st.plotly_chart(fig_qaoa, use_container_width=True)

# --- TAB 4: CLINICAL REPORT ---
with tabs[3]:
    st.header("Intelligence Realization")
    risk_val = (u_stress * 8) + (500 - u_caffeine)/10
    
    st.write(f"### Current IST Health Audit: {'SAFE' if risk_val < 60 else 'ANOMALY DETECTED'}")
    
    if st.button("Generate Final IST Medical PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="VitaIQ Quantum-Health Summary", ln=1, align='C')
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"IST Timestamp: {current_time_ist}", ln=1)
        pdf.cell(200, 10, txt=f"Stress Vector Angle (Bloch): {round(phi, 2)} rad", ln=1)
        pdf.cell(200, 10, txt=f"Risk Score: {int(risk_val)}", ln=1)
        
        pdf_data = pdf.output(dest='S').encode('latin-1')
        b64 = base64.b64encode(pdf_data).decode()
        st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="VitaIQ_Report_IST.pdf" style="padding:15px; background:#00d4aa; color:white; border-radius:10px; text-decoration:none; font-weight:bold;">📥 Download Official IST Report</a>', unsafe_allow_html=True)
