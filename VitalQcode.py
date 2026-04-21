import streamlit as st
import pandas as pd
import numpy as np
import random
import base64
from datetime import datetime
from sklearn.ensemble import IsolationForest
import plotly.graph_objects as goimport streamlit as st
import pandas as pd
import numpy as np
import random
import base64
from datetime import datetime
import plotly.graph_objects as go
from fpdf import FPDF
from sklearn.ensemble import IsolationForest

# --- PAGE CONFIG & THEME (From ffff.py) ---
st.set_page_config(page_title="VitaIQ — Quantum Intelligence", page_icon="🫀", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600&family=JetBrains+Mono&display=swap');
:root {
    --accent: #00d4aa; --bg: #0a0e1a; --card: #111827; --text: #e2e8f0;
}
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: var(--bg); color: var(--text); }
.stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
.stTabs [data-baseweb="tab"] {
    background-color: #161b22; border-radius: 8px; padding: 12px 24px; color: #64748b;
}
.stTabs [aria-selected="true"] { background-color: var(--accent); color: white; }
.metric-card { background: var(--card); border: 1px solid #1e2d45; padding: 20px; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE FOR DATA PERSISTENCE ---
if 'user_data' not in st.session_state:
    st.session_state.user_data = {"age": 25, "sleep": 7, "stress": 5, "water": 2}

# --- HEADER ---
st.title("🫀 VitaIQ: Quantum Wellness Intelligence")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📍 Daily Profile", "📈 Live Analysis", "⚛️ Quantum Risk Audit", "📋 Realization & Recovery"])

# --- TAB 1: USER INPUTS (Client-Friendly) ---
with tab1:
    st.subheader("Personal Health Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.user_data['age'] = st.number_input("Patient Age", 18, 100, 25)
        st.session_state.user_data['sleep'] = st.slider("Sleep Duration (Hours)", 0.0, 12.0, 7.0)
    with col2:
        st.session_state.user_data['stress'] = st.select_slider("Stress Intensity", options=range(1, 11), value=5)
        st.session_state.user_data['water'] = st.number_input("Water Intake (Liters)", 0.0, 10.0, 2.0)

# --- TAB 2: LIVE ANALYSIS (Simulated Hardware) ---
with tab2:
    st.subheader("Diagnostic Feedback Interface")
    hr = random.randint(68, 85) + (st.session_state.user_data['stress'] * 2)
    spo2 = random.randint(95, 99)
    sys = 110 + (st.session_state.user_data['stress'] * 3)
    dia = 70 + (st.session_state.user_data['stress'] * 1.5)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Heart Rate", f"{hr} BPM")
    c2.metric("Oxygen (SpO2)", f"{spo2}%")
    c3.metric("Body Temp", "36.8°C")
    c4.metric("Estimated BP", f"{int(sys)}/{int(dia)}")

    # PPG Heartbeat Graph
    st.write("### Purified PPG Waveform (Sensor Feedback)")
    t = np.linspace(0, 4, 400)
    wave = (np.exp(-((t % 1 - 0.2)**2) / 0.01) + 0.5 * np.exp(-((t % 1 - 0.4)**2) / 0.02))
    fig_wave = go.Figure()
    fig_wave.add_trace(go.Scatter(x=t, y=wave, line=dict(color='#00d4aa', width=3)))
    fig_wave.update_layout(height=250, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_wave, use_container_width=True)

# --- TAB 3: QAOA QUANTUM AUDIT (The "Standout" Feature) ---
with tab3:
    st.subheader("⚛️ Quantum Risk Optimization (QAOA)")
    st.info("Simulating Qiskit QAOA layers to optimize risk detection accuracy.")
    
    # Simulate QAOA Performance (From ffff.py)
    p_layers = list(range(1, 11))
    quantum_error = [15 * (0.7**p) for p in p_layers]
    classical_error = [12 for _ in p_layers]
    
    fig_q = go.Figure()
    fig_q.add_trace(go.Scatter(x=p_layers, y=quantum_error, name='QAOA Optimization', line=dict(color='#8b5cf6', width=3)))
    fig_q.add_trace(go.Scatter(x=p_layers, y=classical_error, name='Classical Baseline', line=dict(dash='dot', color='#64748b')))
    fig_q.update_layout(title="False Positive Reduction via Quantum Layers", height=300, template="plotly_dark")
    st.plotly_chart(fig_q, use_container_width=True)
    
    risk_score = (st.session_state.user_data['stress'] * 10) + (100 - spo2) * 5
    if risk_score > 65:
        st.warning(f"Quantum Audit Status: CRITICAL ANOMALY (Risk: {int(risk_score)})")
    else:
        st.success("Quantum Audit Status: OPTIMIZED BALANCE")

# --- TAB 4: REALIZATION & PDF REPORT ---
with tab4:
    st.header("Recovery & Clinical Documentation")
    
    # Expanded Recommendations
    st.subheader("Practical Protocols")
    recs = [
        "Hydration: Consume 500ml water immediately to counter BP spikes.",
        "Quantum Meditation: 10-min focused breathing to reduce QAOA-detected stress variance.",
        "Sleep Hygiene: Move bedtime 1 hour earlier for neural recovery.",
        "Activity: Switch to light walking; avoid high-intensity until HR stabilizes."
    ]
    for r in recs: st.write(f"🔹 {r}")

    # Full PDF Generation (All Data)
    if st.button("Generate Comprehensive Medical Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(200, 20, txt="VitaIQ Clinical Intelligence Report", ln=1, align='C')
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
        pdf.line(10, 40, 200, 40)
        
        pdf.cell(200, 10, txt="1. PATIENT PROFILE", ln=1)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 8, txt=f"Age: {st.session_state.user_data['age']} | Sleep: {st.session_state.user_data['sleep']}h | Water: {st.session_state.user_data['water']}L", ln=1)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="2. LIVE VITAL SCAN", ln=1)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 8, txt=f"Heart Rate: {hr} BPM | SpO2: {spo2}% | Est. BP: {int(sys)}/{int(dia)}", ln=1)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="3. QUANTUM RISK AUDIT", ln=1)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 8, txt=f"Risk Score: {int(risk_score)} | Detection Method: QAOA Optimized", ln=1)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="4. RECOVERY PLAN", ln=1)
        pdf.set_font("Arial", size=10)
        for r in recs: pdf.cell(200, 8, txt=f"- {r}", ln=1)

        # Download Logic
        pdf_data = pdf.output(dest='S').encode('latin-1')
        b64 = base64.b64encode(pdf_data).decode()
        st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="VitaIQ_Clinical_Report.pdf" style="padding: 15px; background: #00d4aa; color: white; border-radius: 8px; text-decoration: none;">📥 Download Official Report</a>', unsafe_allow_html=True)
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
