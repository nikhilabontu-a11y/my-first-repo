import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

st.set_page_config(page_title="VitalQ Health Intelligence", layout="wide")

# ─────────────────────────────────────────────
# 🎨 PREMIUM UI
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0e1117;
    color: #e5e7eb;
}

h1 { font-size: 32px; font-weight: 700; }
h2 { font-size: 22px; }

.card {
    background: #151a2e;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #2a2f45;
    margin-bottom: 15px;
}

.stButton > button {
    background: linear-gradient(90deg, #00d4aa, #3b82f6);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🔧 SENSOR SIMULATION
# ─────────────────────────────────────────────
def read_sensors():
    return {
        "hr": round(random.gauss(75, 8)),
        "spo2": round(random.gauss(97, 1)),
        "temp": round(random.gauss(36.6, 0.3), 1),
        "bp_sys": round(random.gauss(120, 10)),
        "bp_dia": round(random.gauss(80, 5)),
        "air": round(random.gauss(350, 50))
    }

# ─────────────────────────────────────────────
# 🧠 SCORE
# ─────────────────────────────────────────────
def compute_score(s, i):
    score = 100
    if s["spo2"] < 95: score -= 10
    if s["hr"] > 100: score -= 10
    if s["temp"] > 37.5: score -= 10
    if i["sleep"] < 6: score -= 10
    if i["water"] < 5: score -= 10
    if i["stress"] > 6: score -= 15
    return max(score, 0)

# ─────────────────────────────────────────────
# ⚛️ QUANTUM-INSPIRED RISK
# ─────────────────────────────────────────────
def quantum_risk(s, i):
    risk = []
    if s["spo2"] < 95: risk.append("Low Oxygen Level")
    if s["hr"] > 100: risk.append("High Heart Rate")
    if s["temp"] > 37.5: risk.append("Fever Risk")
    if i["stress"] > 6: risk.append("High Stress")
    if i["sleep"] < 6: risk.append("Sleep Deficiency")
    return risk

# ─────────────────────────────────────────────
# 💡 RECOMMENDATIONS
# ─────────────────────────────────────────────
def recommendations(risks):
    rec = []
    for r in risks:
        if "Oxygen" in r: rec.append("Practice deep breathing")
        if "Heart" in r: rec.append("Avoid stress & heavy activity")
        if "Fever" in r: rec.append("Hydrate and monitor temp")
        if "Stress" in r: rec.append("Meditation recommended")
        if "Sleep" in r: rec.append("Sleep at least 7 hours")
    return rec

# ─────────────────────────────────────────────
# 🧾 HEADER
# ─────────────────────────────────────────────
st.markdown("""
<h1>🫀 VitalQ Health Intelligence</h1>
<p style='color:#9ca3af;'>AI-powered health monitoring with smart insights</p>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 📌 TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📥 Inputs",
    "📊 Analysis",
    "⚠️ Risk",
    "💡 Recommendations"
])

# ─────────────────────────────────────────────
# 📥 TAB 1 INPUTS
# ─────────────────────────────────────────────
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    sleep = st.slider("😴 Sleep", 0, 12, 7)
    water = st.slider("💧 Water", 0, 15, 8)
    stress = st.slider("🧠 Stress", 1, 10, 3)
    activity = st.slider("🚶 Activity", 0, 10000, 4000)

    user_inputs = {
        "sleep": sleep,
        "water": water,
        "stress": stress,
        "activity": activity
    }

    st.success("Inputs recorded")

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 📊 TAB 2 ANALYSIS
# ─────────────────────────────────────────────
with tab2:
    sensors = read_sensors()

    score = compute_score(sensors, user_inputs)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.metric("Wellness Score", f"{score}/100")

    c1, c2, c3 = st.columns(3)
    c1.metric("❤️ HR", f"{sensors['hr']} BPM")
    c2.metric("🫁 SpO2", f"{sensors['spo2']} %")
    c3.metric("🌡 Temp", f"{sensors['temp']} °C")

    c4, c5 = st.columns(2)
    c4.metric("🩸 BP", f"{sensors['bp_sys']}/{sensors['bp_dia']}")
    c5.metric("🌫 Air", f"{sensors['air']} ppm")

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ⚠️ TAB 3 RISK
# ─────────────────────────────────────────────
with tab3:
    risks = quantum_risk(sensors, user_inputs)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if not risks:
        st.success("No risks detected")
    else:
        for r in risks:
            st.error(r)

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 💡 TAB 4 RECOMMENDATIONS
# ─────────────────────────────────────────────
with tab4:
    recs = recommendations(risks)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if not recs:
        st.success("Maintain current lifestyle")
    else:
        for r in recs:
            st.write(f"✔ {r}")

    st.markdown("</div>", unsafe_allow_html=True)
