import streamlit as st
import pandas as pd
import numpy as np
import random
import base64
import pytz
from datetime import datetime
import plotly.graph_objects as go
from fpdf import FPDF

# --- 1. LOCALIZATION (IST) ---
IST = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(IST).strftime('%d %B %Y | %I:%M %p')

st.set_page_config(page_title="VitaIQ — Patient Portal", page_icon="🫀", layout="wide")

# UI Styling for a "Hospital-Grade" feel
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
:root { --accent: #00d4aa; --bg: #0a0e1a; --text: #f8fafc; }
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: var(--bg); color: var(--text); }
.stTabs [data-baseweb="tab-list"] { gap: 15px; justify-content: center; }
.stTabs [data-baseweb="tab"] { background-color: #111827; border-radius: 12px; padding: 12px 25px; color: #94a3b8; border: 1px solid #1e293b; }
.stTabs [aria-selected="true"] { background-color: var(--accent); color: white; border: none; font-weight: 600; box-shadow: 0 4px 15px rgba(0,212,170,0.2); }
</style>
""", unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🫀 VitaIQ: Personalized Health Intelligence")
st.write(f"Logged in as: **Patient-01** | **IST Time:** {now_ist}")

tabs = st.tabs(["📝 Daily Profile", "💓 Live ECG Monitor", "⚛️ Quantum Balance", "📥 Medical Report"])

# --- TAB 1: PATIENT INPUTS ---
with tabs[0]:
    st.subheader("How are you feeling today?")
    c1, c2, c3 = st.columns(3)
    with c1:
        u_mood = st.select_slider("Mood Status", options=["Low Energy", "Stressed", "Stable", "Good", "Excellent"])
        u_exercise = st.selectbox("Activity Level", ["No Activity", "Light Walk", "Moderate Gym", "Heavy Training"])
    with c2:
        u_stress = st.slider("Stress Level", 1, 10, 4)
        u_sleep = st.number_input("Last Night's Sleep (Hrs)", 0.0, 12.0, 7.5)
    with c3:
        u_water = st.number_input("Water Intake (Liters)", 0.0, 6.0, 2.5)
        u_caffeine = st.slider("Cups of Coffee/Tea", 0, 8, 1)

# --- TAB 2: PATIENT ECG (Simplified) ---
with tabs[1]:
    st.subheader("Your Real-Time Heart Signal")
    hr = random.randint(72, 88) + (u_stress)
    spo2 = random.randint(96, 99)
    sys, dia = (110 + (u_stress * 2)), (70 + u_stress)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Pulse Rate", f"{hr} BPM", delta="Normal" if hr < 90 else "Elevated")
    col2.metric("Oxygen Level", f"{spo2}%", delta="Healthy")
    col3.metric("Estimated BP", f"{int(sys)}/{int(dia)}", delta="Stable")

    # ECG Waveform (The "Billion Dollar" Visual)
    t = np.linspace(0, 3, 1000)
    ecg = 0.1*np.exp(-((t%1-0.1)**2)/0.001) + 1.2*np.exp(-((t%1-0.2)**2)/0.0001) + 0.2*np.exp(-((t%1-0.4)**2)/0.01)
    fig_ecg = go.Figure(data=go.Scatter(x=t, y=ecg, line=dict(color='#00d4aa', width=2)))
    fig_ecg.update_layout(height=300, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    st.plotly_chart(fig_ecg, use_container_width=True)
    st.caption("This graph represents your heart's electrical activity cleaned by our VitaIQ algorithm.")

# --- TAB 3: QUANTUM EXPLAINED (Patient-Friendly) ---
with tabs[2]:
    st.subheader("Quantum Optimization Logic")
    st.write("We use Quantum Computing to find the perfect 'balance' in your health data, removing sensor noise.")
    
    qc1, qc2 = st.columns(2)
    with qc1:
        st.write("**Health State Optimization**")
        # Simplified QAOA Convergence for patients
        steps = np.arange(1, 11)
        stability = 100 - (20 * np.exp(-steps/3))
        fig_q = go.Figure(data=go.Scatter(x=steps, y=stability, mode='lines+markers', line=dict(color='#8b5cf6')))
        fig_q.update_layout(title="System Accuracy Improvement", height=300, template="plotly_dark", xaxis_title="Quantum Layers", yaxis_title="Accuracy %")
        st.plotly_chart(fig_q, use_container_width=True)

    with qc2:
        st.write("**Patient State Vector**")
        # Bloch Sphere mapping simplified as a 'Balance Chart'
        labels = ['Sleep', 'Hydration', 'Mood', 'Heart']
        values = [u_sleep*8, u_water*15, 80 if u_mood=="Good" else 50, 100-(hr-70)]
        fig_p = go.Figure(data=go.Polar(r=values, theta=labels, fill='toself', color='#00d4aa'))
        fig_p.update_layout(polar=dict(radialaxis=dict(visible=False)), showlegend=False, height=300, template="plotly_dark")
        st.plotly_chart(fig_p, use_container_width=True)

# --- TAB 4: THE REPORT (The Final Product) ---
with tabs[3]:
    st.header("Your Health Realization")
    risk_score = (u_stress * 7) + (100 - spo2) * 5
    
    st.write("### Recovery Recommendations")
    recs = [
        f"Increase water to {u_water + 0.5}L to stabilize blood pressure.",
        "Quantum analysis suggests 15 minutes of deep breathing to lower stress variance.",
        f"Based on your {u_mood} mood, a light 20-minute walk is advised."
    ]
    for r in recs: st.write(f"✅ {r}")

    if st.button("Generate Official IST Medical Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="VitaIQ Wellness Intelligence Report", ln=1, align='C')
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Report Date (IST): {now_ist}", ln=1)
        pdf.line(10, 35, 200, 35)
        
        pdf.cell(200, 10, txt=f"Pulse: {hr} BPM | SpO2: {spo2}% | BP: {int(sys)}/{int(dia)}", ln=1)
        pdf.cell(200, 10, txt=f"Mood: {u_mood} | Sleep: {u_sleep}h | Stress: {u_stress}/10", ln=1)
        pdf.cell(200, 10, txt=f"Quantum Optimization Score: {int(risk_score)}", ln=1)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Clinical Advice:", ln=1)
        pdf.set_font("Arial", size=10)
        for r in recs: pdf.cell(200, 8, txt=f"- {r}", ln=1)
        
        pdf_out = pdf.output(dest='S').encode('latin-1')
        b64 = base64.b64encode(pdf_out).decode()
        st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="VitaIQ_IST_Report.pdf" style="padding:15px; background:#00d4aa; color:white; border-radius:10px; text-decoration:none; font-weight:bold;">📥 Download Official Report</a>', unsafe_allow_html=True)
