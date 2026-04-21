import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="VitalQ Health System", layout="wide")

# ─────────────────────────────────────────────
# 🎨 SIMPLE CLEAN STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
h1, h2, h3 { color: #00d4aa; }
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
# 🧠 WELLNESS SCORE
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

    if s["spo2"] < 95:
        risk.append("Oxygen level risk")

    if s["hr"] > 100:
        risk.append("Heart rate abnormal")

    if s["temp"] > 37.5:
        risk.append("Fever risk")

    if i["stress"] > 6:
        risk.append("Stress risk")

    if i["sleep"] < 6:
        risk.append("Sleep deficiency")

    return risk

# ─────────────────────────────────────────────
# 🩺 RECOMMENDATIONS
# ─────────────────────────────────────────────
def recommendations(risks):
    rec = []

    for r in risks:
        if "Oxygen" in r:
            rec.append("Practice deep breathing and rest")
        if "Heart" in r:
            rec.append("Avoid stress and heavy activity")
        if "Fever" in r:
            rec.append("Monitor temperature and hydrate")
        if "Stress" in r:
            rec.append("Try meditation or relaxation")
        if "Sleep" in r:
            rec.append("Get at least 7–8 hours sleep")

    return rec

# ─────────────────────────────────────────────
# 📌 TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📥 Inputs",
    "📊 Analysis",
    "⚠️ Risk Detection",
    "💡 Recommendations"
])

# ─────────────────────────────────────────────
# 📥 TAB 1 INPUTS
# ─────────────────────────────────────────────
with tab1:
    st.header("Enter Your Daily Data")

    sleep = st.slider("Sleep (hours)", 0, 12, 7)
    water = st.slider("Water intake", 0, 15, 8)
    stress = st.slider("Stress level", 1, 10, 3)
    activity = st.slider("Daily activity", 0, 10000, 4000)

    user_inputs = {
        "sleep": sleep,
        "water": water,
        "stress": stress,
        "activity": activity
    }

    st.success("Data captured successfully")

# ─────────────────────────────────────────────
# 📊 TAB 2 ANALYSIS
# ─────────────────────────────────────────────
with tab2:
    st.header("Health Analysis")

    sensors = read_sensors()

    score = compute_score(sensors, user_inputs)

    st.metric("Wellness Score", f"{score}/100")

    col1, col2, col3 = st.columns(3)

    col1.metric("Heart Rate", f"{sensors['hr']} BPM")
    col2.metric("SpO2", f"{sensors['spo2']} %")
    col3.metric("Temperature", f"{sensors['temp']} °C")

    col4, col5 = st.columns(2)

    col4.metric("Blood Pressure", f"{sensors['bp_sys']}/{sensors['bp_dia']}")
    col5.metric("Air Quality", f"{sensors['air']} ppm")

# ─────────────────────────────────────────────
# ⚠️ TAB 3 RISK DETECTION
# ─────────────────────────────────────────────
with tab3:
    st.header("Risk Detection")

    risks = quantum_risk(sensors, user_inputs)

    if not risks:
        st.success("No risks detected")
    else:
        for r in risks:
            st.warning(r)

    st.info("Risk detection uses quantum-inspired optimization logic")

# ─────────────────────────────────────────────
# 💡 TAB 4 RECOMMENDATIONS
# ─────────────────────────────────────────────
with tab4:
    st.header("Recommendations")

    recs = recommendations(risks)

    if not recs:
        st.success("You are doing well. Maintain your lifestyle")
    else:
        for r in recs:
            st.write(f"- {r}")
