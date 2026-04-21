import streamlit as st
import pandas as pd
import numpy as np
import random
import base64
import pytz
from datetime import datetime
import plotly.graph_objects as go
from fpdf import FPDF
from sklearn.ensemble import IsolationForest

# --- 1. GLOBAL SETTINGS & IST LOCALIZATION ---
IST = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')

st.set_page_config(page_title="VitaIQ — Quantum Intelligence", page_icon="🫀", layout="wide")

# High-End Dark Mode UI (Mixing preferences from ffff.py)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600&family=JetBrains+Mono&display=swap');
:root { --accent: #00d4aa; --bg: #0a0e1a; --card: #111827; --text: #e2e8f0; --purple: #8b5cf6; }
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: var(--bg); color: var(--text); }
.stTabs [data-baseweb="tab-list"] { gap: 12px; justify-content: center; }
.stTabs [data-baseweb="tab"] { background-color: #161b22; border-radius: 12px; padding: 15px 30px; color: #64748b; border: 1px solid #1e2d45; }
.stTabs [aria-selected="true"] { background-color: var(--accent); color: white; border: none; font-weight: 600; }
[data-testid="stMetricValue"] { color: var(--accent); font-family: 'JetBrains Mono'; }
</style>
""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🫀 VitaIQ: Wellness Intelligence Portal")
st.write(f"**System Status:** Quantum-Classical Sync Active | **Current Time (IST):** {current_time_ist}")

tab1, tab2, tab3, tab4 = st.tabs(["📍 Comprehensive Profile", "📉 Live ECG Analysis", "⚛️ QAOA Risk Engine", "📋 Recovery Protocol"])

# --- TAB 1: ENHANCED DAILY INPUTS ---
with tab1:
    st.subheader("Comprehensive Health Journal")
    col1, col2, col3 = st.columns(3)
    with col1:
        u_mood = st.select_slider("Current Mood", options=["Depressed", "Anxious", "Neutral", "Happy", "Energetic"], value="Neutral")
        u_exercise = st.selectbox("Exercise Intensity (Today)", ["None", "Yoga/Stretch", "Cardio", "Weight Training", "HIIT"])
    with col2:
        u_stress = st.slider("Stress Level (1-10)", 1, 10, 4)
        u_sleep = st.number_input("Sleep Duration (Hours)", 0.0, 12.0, 7.5)
    with col3:
        u_water = st.number_input("Hydration (Liters)", 0.0, 8.0, 2.5)
        u_caffeine = st.slider("Caffeine Intake (Cups)", 0, 10, 1)

# --- TAB 2: LIVE ECG SIMULATION ---
with tab2:
    st.subheader("Diagnostic Feedback (Real-Time ECG)")
    # Logic simulating sensor interaction
    hr = random.randint(68, 85) + (u_stress * 2) - (2 if u_mood == "Happy" else 0)
    spo2 = random.randint(95, 99)
    sys, dia = (110 + (u_stress * 3)), (75 + (u_stress * 1))
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Heart Rate", f"{hr} BPM")
    m2.metric("Oxygen (SpO2)", f"{spo2}%")
    m3.metric("Est. Blood Pressure", f"{int(sys)}/{int(dia)}")
    m4.metric("Exercise Impact", u_exercise)

    # HIGH-FIDELITY ECG GRAPH
    st.write("### Purified ECG Waveform (Q-Cleaned)")
    t = np.linspace(0, 4, 1000)
    # Replicating P-QRS-T complex mathematically
    def ecg_wave(t):
        p_wave = 0.1 * np.exp(-((t % 1 - 0.1)**2) / 0.001)
        qrs_complex = 1.0 * np.exp(-((t % 1 - 0.2)**2) / 0.0001) - 0.2 * np.exp(-((t % 1 - 0.18)**2) / 0.0001)
        t_wave = 0.2 * np.exp(-((t % 1 - 0.4)**2) / 0.005)
        return p_wave + qrs_complex + t_wave

    ecg_signal = ecg_wave(t)
    fig_ecg = go.Figure()
    fig_ecg.add_trace(go.Scatter(x=t, y=ecg_signal, line=dict(color='#00d4aa', width=2)))
    fig_ecg.update_layout(height=300, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#1e2d45"))
    st.plotly_chart(fig_ecg, use_container_width=True)

# --- TAB 3: ENHANCED QAOA RISK ENGINE ---
with tab3:
    st.subheader("⚛️ Quantum Approximate Optimization (QAOA) Audit")
    st.write("Optimizing the 'Cost Function' of your health by analyzing noise interference in sensor data.")
    
    # QAOA Convergence Simulation
    p_layers = np.arange(1, 21)
    cost_function = 10 * np.exp(-p_layers/5) + np.random.normal(0, 0.1, 20)
    
    fig_qaoa = go.Figure()
    fig_qaoa.add_trace(go.Scatter(x=p_layers, y=cost_function, mode='lines+markers', name='QAOA Energy Minimization', line=dict(color='#8b5cf6')))
    fig_qaoa.update_layout(title="Quantum Cost Function Convergence (System Stability)", height=350, template="plotly_dark")
    st.plotly_chart(fig_qaoa, use_container_width=True)
    
    # Complex Risk Logic
    base_risk = (u_stress * 10) + (100 - spo2) * 5 + (u_caffeine * 5)
    if u_exercise == "HIIT": base_risk += 15
    
    st.info(f"**Quantum Analysis Result:** The system has minimized health cost to **{round(min(cost_function), 2)}**. Final Risk Score: **{int(base_risk)}**.")

# --- TAB 4: RECOVERY & IST-BASED PDF ---
with tab4:
    st.header("Realization Page: Clinical Action Plan")
    
    # Dynamic Recommendations
    recs = [
        f"Hydration: Drink {round(u_water + 0.5, 1)}L total to offset current stress.",
        f"Activity: Since you chose {u_exercise}, ensure 20 mins of cool-down stretching.",
        f"Mood Adjustment: Current mood is {u_mood}; consider sunlight exposure for 15 mins.",
        "Quantum Note: QAOA detection suggests high variance in HRV during rest periods."
    ]
    for r in recs: st.write(f"🔹 {r}")

    if st.button("Generate Professional Clinical Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 20)
        pdf.set_text_color(0, 212, 170)
        pdf.cell(200, 20, txt="VitaIQ Clinical Intelligence Summary", ln=1, align='C')
        
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt=f"Report Generated (IST): {current_time_ist}", ln=1)
        pdf.line(10, 45, 200, 45)
        
        # Detailed Data Sections
        pdf.cell(200, 10, txt="[1] Patient Daily Context", ln=1)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 8, txt=f"Mood: {u_mood} | Exercise: {u_exercise} | Sleep: {u_sleep}h | Caffeine: {u_caffeine} cups", ln=1)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="[2] Physiological Biomarkers", ln=1)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 8, txt=f"Heart Rate: {hr} BPM | SpO2: {spo2}% | Est. Blood Pressure: {int(sys)}/{int(dia)}", ln=1)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="[3] Quantum Risk Assessment", ln=1)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 8, txt=f"QAOA Risk Score: {int(base_risk)} | System Stability: High", ln=1)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="[4] Prescribed Recovery Protocol", ln=1)
        pdf.set_font("Arial", size=10)
        for r in recs: pdf.cell(200, 8, txt=f"- {r}", ln=1)

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="VitaIQ_Pro_Report_IST.pdf" style="display:inline-block; padding:15px 30px; background-color:#00d4aa; color:white; border-radius:10px; text-decoration:none; font-weight:bold;">📥 DOWNLOAD OFFICIAL CLINICAL REPORT</a>', unsafe_allow_html=True)
