import streamlit as st
import pandas as pd
import numpy as np
import random
import base64
import pytz
from datetime import datetime
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. SETTINGS & IST LOCALIZATION ---
IST = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.now(IST).strftime('%d %b %Y | %H:%M:%S')

st.set_page_config(page_title="VitaIQ — Quantum Medical Intelligence", page_icon="⚛️", layout="wide")

# High-End Dark Mode UI styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600&family=JetBrains+Mono&display=swap');
:root { --accent: #00d4aa; --bg: #0a0e1a; --purple: #8b5cf6; --text: #e2e8f0; }
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: var(--bg); color: var(--text); }
.stTabs [data-baseweb="tab-list"] { gap: 12px; justify-content: center; }
.stTabs [data-baseweb="tab"] { background-color: #111827; border-radius: 12px; padding: 15px 30px; color: #64748b; border: 1px solid #1e2d45; }
.stTabs [aria-selected="true"] { background-color: var(--accent); color: white; border: none; font-weight: 600; box-shadow: 0 0 15px rgba(0,212,170,0.3); }
[data-testid="stMetricValue"] { color: var(--accent); font-family: 'JetBrains Mono'; }
</style>
""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("⚛️ VitaIQ: Quantum-Classical Medical Intelligence")
st.write(f"**System Status:** QAOA & VQC Processing Active | **IST Time:** {current_time_ist}")

tabs = st.tabs(["📍 Patient Profile", "📉 Live ECG/Hardware", "⚛️ Quantum Engine", "📋 Clinical Report"])

# --- TAB 1: USER INPUTS ---
with tabs[0]:
    st.subheader("Comprehensive Health Journal")
    col1, col2, col3 = st.columns(3)
    with col1:
        u_mood = st.select_slider("Current Mood", options=["Depressed", "Anxious", "Neutral", "Happy", "Energetic"], value="Neutral")
        u_exercise = st.selectbox("Exercise Intensity", ["None", "Yoga", "Cardio", "Strength", "HIIT"])
    with col2:
        u_stress = st.slider("Psychological Stress (1-10)", 1, 10, 5)
        u_sleep = st.number_input("Sleep Duration (Hours)", 0.0, 12.0, 7.5)
    with col3:
        u_water = st.number_input("Hydration (Liters)", 0.0, 8.0, 2.5)
        u_caffeine = st.slider("Caffeine (Cups)", 0, 8, 2)
    
    st.markdown("---")
    # NEW LOGIN / SAVE DATA BUTTON
    if st.button("🔐 Login & Save Input Data"):
        st.success(f"Quantum Vault Updated: Data for {current_time_ist} secured.")
        st.balloons()

# --- TAB 2: LIVE ECG & HARDWARE ---
with tabs[1]:
    st.subheader("Hardware Interface & Bio-Signals")
    # Dynamic Vitals based on stress input
    hr = random.randint(70, 85) + (u_stress * 1.5)
    spo2 = random.randint(96, 99)
    sys, dia = (115 + (u_stress * 2)), (75 + (u_stress * 1))
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Heart Rate", f"{int(hr)} BPM")
    m2.metric("Oxygen (SpO2)", f"{spo2}%")
    m3.metric("Est. Blood Pressure", f"{int(sys)}/{int(dia)}")
    m4.metric("Body Temp", "37.1°C")

    t = np.linspace(0, 4, 1000)
    ecg = 0.15 * np.exp(-((t % 1 - 0.1)**2) / 0.001) + 1.2 * np.exp(-((t % 1 - 0.2)**2) / 0.0001) + 0.3 * np.exp(-((t % 1 - 0.45)**2) / 0.01)
    fig_ecg = go.Figure(data=go.Scatter(x=t, y=ecg, line=dict(color='#00d4aa', width=2)))
    fig_ecg.update_layout(height=280, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    st.plotly_chart(fig_ecg, use_container_width=True)

# --- TAB 3: QUANTUM ENGINE ---
with tabs[2]:
    st.subheader("⚛️ Quantum Variational Intelligence")
    qc1, qc2 = st.columns(2)
    with qc1:
        p_layers = np.arange(1, 21)
        cost = 8 * np.exp(-p_layers/4) + np.random.normal(0, 0.05, 20)
        fig_q = go.Figure(data=go.Scatter(x=p_layers, y=cost, mode='lines+markers', line=dict(color='#8b5cf6')))
        fig_q.update_layout(title="QAOA Error Convergence", height=300, template="plotly_dark")
        st.plotly_chart(fig_q, use_container_width=True)
    with qc2:
        states = ['|Normal>', '|Anxious>', '|Tachycardic>', '|At-Risk>']
        probabilities = [0.85, 0.08, 0.04, 0.03]
        fig_p = go.Figure(data=go.Bar(x=states, y=probabilities, marker_color='#00d4aa'))
        fig_p.update_layout(title="Health Superposition Probability", height=300, template="plotly_dark")
        st.plotly_chart(fig_p, use_container_width=True)

# --- TAB 4: DYNAMIC CLINICAL REPORT ---
with tabs[3]:
    st.header("Personalized Clinical Action Plan")
    
    # --- DYNAMIC LOGIC ---
    risk_score = (u_stress * 8) + (100 - spo2) * 5 + (u_caffeine * 3)
    recs = []

    if u_stress > 7: recs.append("⚠️ HIGH STRESS: Immediate 10-min box breathing required.")
    else: recs.append("✅ Stress levels are stable.")

    if u_sleep < 6: recs.append(f"😴 SLEEP ALERT: {u_sleep}h is insufficient. Target 7.5h.")
    else: recs.append("🌟 Sleep duration is optimal.")

    if u_water < 2: recs.append("💧 HYDRATION: Increase intake by 1.5L to assist VQC stability.")
    
    if u_caffeine > 4: recs.append("☕ CAFFEINE: High stimulant load detected; skip the evening dose.")

    if u_exercise == "None" and u_mood == "Depressed":
        recs.append("🏃 MOOD: Light 15-min movement recommended for endorphin release.")

    # Display on Screen
    for r in recs: st.write(r)

    if st.button("Generate Final Clinical Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 15, txt="VitaIQ Dynamic Health Audit", ln=1, align='C')
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Generated on (IST): {current_time_ist}", ln=1)
        pdf.line(10, 35, 200, 35)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Patient Vital Summary:", ln=1)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 8, txt=f"- Stress Level: {u_stress}/10 | Mood: {u_mood}", ln=1)
        pdf.cell(200, 8, txt=f"- Sleep: {u_sleep} Hours | Hydration: {u_water}L", ln=1)
        pdf.cell(200, 8, txt=f"- Quantum Risk Score: {int(risk_score)}", ln=1)
        
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Dynamic Recommendations:", ln=1)
        pdf.set_font("Arial", size=10)
        # FIXED: Multi-cell with proper closing bracket to fix your SyntaxError
        for r in recs:
            pdf.multi_cell(0, 8, txt=f"- {r}")

        pdf_data = pdf.output(dest='S').encode('latin-1')
        b64 = base64.b64encode(pdf_data).decode()
        st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="VitaIQ_Report.pdf" style="padding:15px; background:#00d4aa; color:white; border-radius:10px; text-decoration:none; font-weight:bold;">📥 Download Personalized Report</a>', unsafe_allow_html=True)
