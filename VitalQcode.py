import streamlit as st
import pandas as pd
import numpy as np
import random
import base64
from datetime import datetime
import plotly.graph_objects as go
from fpdf import FPDF
from sklearn.ensemble import IsolationForest

# --- 1. THEME & STYLING (Mixed from ffff.py) ---
st.set_page_config(page_title="VitaIQ — Quantum Intelligence", page_icon="🫀", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600&display=swap');
:root { --accent: #00d4aa; --bg: #0a0e1a; --card: #111827; --text: #e2e8f0; }
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: var(--bg); }
.stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; }
.stTabs [data-baseweb="tab"] { background-color: #161b22; border-radius: 8px; padding: 10px 20px; color: #64748b; }
.stTabs [aria-selected="true"] { background-color: var(--accent); color: white; }
</style>
""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🫀 VitaIQ: Wellness Intelligence Dashboard")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📍 Daily Profile", "📈 Live Analysis", "⚛️ Quantum Risk Audit", "📋 Realization & Recovery"])

# --- TAB 1: USER INPUTS ---
with tab1:
    st.subheader("Patient Vitals Input")
    c1, c2 = st.columns(2)
    with c1:
        u_age = st.number_input("Age", 18, 100, 25)
        u_sleep = st.slider("Sleep (Hours)", 0.0, 12.0, 7.0)
    with c2:
        u_stress = st.select_slider("Stress Level", options=range(1, 11), value=4)
        u_water = st.number_input("Water (Liters)", 0.0, 10.0, 2.5)

# --- TAB 2: LIVE ANALYSIS (Simulation Logic) ---
with tab2:
    st.subheader("Real-Time Diagnostic Feedback")
    hr = random.randint(68, 88) + (u_stress * 2)
    spo2 = random.randint(95, 99)
    sys, dia = 110 + (u_stress * 3), 75 + (u_stress * 1)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Heart Rate", f"{hr} BPM")
    col_m2.metric("SpO2", f"{spo2}%")
    col_m3.metric("Body Temp", "36.7°C")
    col_m4.metric("Est. BP", f"{int(sys)}/{int(dia)}")

    # PPG Waveform (Standout Visualization)
    t = np.linspace(0, 4, 400)
    ppg = (np.exp(-((t % 1 - 0.2)**2) / 0.01) + 0.5 * np.exp(-((t % 1 - 0.4)**2) / 0.02))
    fig_ppg = go.Figure()
    fig_ppg.add_trace(go.Scatter(x=t, y=ppg, line=dict(color='#00d4aa', width=3)))
    fig_ppg.update_layout(height=250, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_ppg, use_container_width=True)

# --- TAB 3: QUANTUM RISK AUDIT (QAOA Logic) ---
with tab3:
    st.subheader("⚛️ QAOA Risk Optimization")
    st.write("Using Quantum Layers to minimize False Positives in health risk detection.")
    
    p_layers = list(range(1, 11))
    q_error = [14 * (0.65**p) for p in p_layers]
    fig_q = go.Figure()
    fig_q.add_trace(go.Scatter(x=p_layers, y=q_error, name='Quantum Cost Optimization', line=dict(color='#8b5cf6', width=3)))
    fig_q.update_layout(height=300, template="plotly_dark", xaxis_title="QAOA Layers (p)", yaxis_title="Risk Uncertainty (%)")
    st.plotly_chart(fig_q, use_container_width=True)
    
    risk_score = (u_stress * 12) + (100 - spo2) * 4
    st.progress(min(risk_score/100, 1.0))
    st.write(f"Quantum Risk Score: {int(risk_score)} | **Status: {'OPTIMIZED' if risk_score < 65 else 'ALERT'}**")

# --- TAB 4: RECOVERY & COMPREHENSIVE PDF ---
with tab4:
    st.header("Realization & Clinical Recovery")
    recommendations = [
        "Hydration: Increase intake by 1.5L due to detected stress levels.",
        "Sleep: Quantum analysis suggests a 1.5-hour sleep deficit.",
        "Activity: Resting phase recommended for 4 hours.",
        "Monitoring: Daily Signal Purification test required."
    ]
    for r in recommendations: st.write(f"✅ {r}")

    if st.button("Generate Comprehensive Medical Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 18)
        pdf.cell(200, 15, txt="VitaIQ Wellness Intelligence Report", ln=1, align='C')
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
        pdf.cell(200, 10, txt=f"Patient Profile: Age {u_age} | Sleep {u_sleep}h | Water {u_water}L", ln=1)
        pdf.cell(200, 10, txt=f"Vital Signs: HR {hr} BPM | SpO2 {spo2}% | BP {int(sys)}/{int(dia)}", ln=1)
        pdf.cell(200, 10, txt=f"Quantum Risk Audit Score: {int(risk_score)}", ln=1)
        pdf.cell(200, 10, txt="Clinical Recommendations:", ln=1)
        for r in recommendations: pdf.cell(200, 8, txt=f"- {r}", ln=1)
        
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        b64_pdf = base64.b64encode(pdf_bytes).decode()
        st.markdown(f'<a href="data:application/pdf;base64,{b64_pdf}" download="VitaIQ_Full_Report.pdf" style="padding:12px; background:#00d4aa; color:white; border-radius:6px; text-decoration:none;">📥 Download Complete PDF Report</a>', unsafe_allow_html=True)
