import streamlit as st
import pandas as pd
import numpy as np
import json
import random
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import warnings
import pytz


# Define India Timezone
IST = pytz.timezone('Asia/Kolkata')
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="VitaIQ — Wellness Intelligence",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="auto"
)
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

col1, col2 = st.columns([1, 10])
with col1:
    if st.button("☰"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open

if st.session_state.sidebar_open:
    st.sidebar.markdown("### Navigation")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0a0e1a;
    --bg2: #0f1525;
    --bg3: #151c30;
    --card: #111827;
    --border: #1e2d45;
    --accent: #00d4aa;
    --accent2: #3b82f6;
    --accent3: #f59e0b;
    --danger: #ef4444;
    --text: #f1f5f9;
    --muted: #94a3b8;
}

/* GLOBAL */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 16px !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.main .block-container {
    padding: 2.5rem 3rem !important;
    max-width: 1200px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 4px 0 20px rgba(0,0,0,0.4);
}

/* HEADINGS */
h1 { font-size: 36px !important; font-weight: 800 !important; }
h2 { font-size: 26px !important; }
h3 { font-size: 20px !important; }

/* CARDS */
.metric-card {
    background: rgba(17,24,39,0.85);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 22px;
    transition: all 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: #00d4aa;
}

.metric-label {
    font-size: 13px;
    color: var(--muted);
}

.metric-value {
    font-size: 42px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

.metric-unit {
    font-size: 14px;
    color: var(--muted);
}

.metric-status {
    font-size: 12px;
}

/* ALERT */
.alert-box {
    font-size: 14px;
    padding: 16px 20px;
}

/* INPUTS FIX */
div[data-testid="stSelectbox"] > div,
div[data-testid="stMultiSelect"] > div {
    background-color: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

div[data-testid="stSelectbox"] *,
div[data-testid="stMultiSelect"] * {
    color: var(--text) !important;
}

/* BUTTON */
.stButton > button {
    font-size: 14px !important;
    padding: 12px 26px !important;
}

/* CLEAN UI */
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }

</style>
""", unsafe_allow_html=True)
st.markdown("### 🎛 Live Health Controls")

col1, col2, col3 = st.columns(3)

with col1:
    sleep_live = st.slider("Sleep (hrs)", 0.0, 12.0, 7.0)

with col2:
    water_live = st.slider("Water (glasses)", 0, 16, 8)

with col3:
    stress_live = st.slider("Stress (1–10)", 1, 10, 3)

# NEW ROW
col4, col5 = st.columns(2)

with col4:
    food_live = st.selectbox("Food Intake", [
        "Balanced diet",
        "Mostly healthy",
        "Average",
        "Junk food",
        "Skipped meals"
    ])

with col5:
    mood_live = st.selectbox("Mood", [
        "😊 Happy",
        "😐 Neutral",
        "😟 Stressed",
        "😴 Tired"
    ])

# Convert to scores (VERY IMPORTANT)
diet_map = {
    "Balanced diet": 10,
    "Mostly healthy": 8,
    "Average": 6,
    "Junk food": 3,
    "Skipped meals": 1
}

mood_stress_map = {
    "😊 Happy": 2,
    "😐 Neutral": 4,
    "😟 Stressed": 7,
    "😴 Tired": 6
}

# FINAL LIVE INPUT OBJECT
current_inputs = {
    'sleep': sleep_live,
    'water': water_live,
    'stress': mood_stress_map[mood_live],   # mood influences stress
    'diet_score': diet_map[food_live]
}

st.success("Live simulation active — adjust inputs to see real-time impact")


# ── Session state ──────────────────────────────────────────────────────────────
if 'health_log' not in st.session_state:
    st.session_state.health_log = []
if 'sensor_history' not in st.session_state:
    now = datetime.now(IST)
    hist = []
    for i in range(60):
        t = now - timedelta(minutes=60-i)
        hist.append({
            'time': t,
            'spo2': round(random.gauss(97.5, 0.8), 1),
            'hr':   round(random.gauss(72, 5)),
            'temp': round(random.gauss(36.6, 0.2), 1),
            'ecg':  round(random.gauss(0, 0.3), 3),
            'activity': round(random.gauss(50, 20)),
            'air': round(random.gauss(350, 40))
        })
    st.session_state.sensor_history = hist
if 'wellness_history' not in st.session_state:
    st.session_state.wellness_history = []
    
    


# ── Simulated live sensor read ─────────────────────────────────────────────────
def read_sensors(IST):
    last = st.session_state.sensor_history[-1] if st.session_state.sensor_history else {}
    spo2 = round(max(88, min(100, random.gauss(last.get('spo2', 97.5), 0.4))), 1)
    hr   = round(max(45, min(160, random.gauss(last.get('hr', 72), 3))))
    temp = round(max(35.0, min(39.5, random.gauss(last.get('temp', 36.6), 0.1))), 1)
    ecg  = round(random.gauss(0, 0.25), 3)
    act  = round(max(0, min(100, random.gauss(last.get('activity', 50), 8))))
    air  = round(max(200, min(800, random.gauss(last.get('air', 350), 25))))
    new = {'time': datetime.now(IST), 'spo2': spo2, 'hr': hr, 'temp': temp,
           'ecg': ecg, 'activity': act, 'air': air}
    st.session_state.sensor_history.append(new)
    if len(st.session_state.sensor_history) > 120:
        st.session_state.sensor_history = st.session_state.sensor_history[-120:]
    return new


# ── Wellness score engine ──────────────────────────────────────────────────────
def compute_wellness(sensors, inputs):
    score = 100.0

    # SpO2 (max 25 pts)
    s = sensors['spo2']
    if s >= 97: score -= 0
    elif s >= 95: score -= 5
    elif s >= 92: score -= 15
    else: score -= 25

    # Heart rate (max 15 pts)
    hr = sensors['hr']
    if 60 <= hr <= 90: score -= 0
    elif 50 <= hr <= 100: score -= 5
    else: score -= 15

    # Body temp (max 10 pts)
    t = sensors['temp']
    if 36.1 <= t <= 37.2: score -= 0
    elif 35.5 <= t <= 37.8: score -= 5
    else: score -= 10

    # Sleep (max 15 pts)
    sl = inputs.get('sleep', 7)
    if sl >= 7: score -= 0
    elif sl >= 6: score -= 5
    elif sl >= 5: score -= 10
    else: score -= 15

    # Water (max 10 pts)
    w = inputs.get('water', 8)
    if w >= 8: score -= 0
    elif w >= 5: score -= 5
    else: score -= 10

    # Stress (max 15 pts)
    st_lvl = inputs.get('stress', 3)
    score -= min(15, st_lvl * 1.5)

    # Diet quality (max 10 pts)
    diet = inputs.get('diet_score', 7)
    score -= max(0, (10 - diet))

    return max(0, min(100, round(score)))


def wellness_color(score):
    if score >= 80: return '#10b981'
    if score >= 60: return '#f59e0b'
    if score >= 40: return '#f97316'
    return '#ef4444'

def wellness_label(score):
    if score >= 80: return 'Excellent'
    if score >= 60: return 'Good'
    if score >= 40: return 'Fair'
    return 'Poor'

def spo2_status(v):
    if v >= 95: return 'Normal', 'normal'
    if v >= 92: return 'Low', 'warning'
    return 'Critical', 'danger'

def hr_status(v):
    if 60 <= v <= 90: return 'Normal', 'normal'
    if 50 <= v <= 100: return 'Borderline', 'warning'
    return 'Abnormal', 'danger'

def temp_status(v):
    if 36.1 <= v <= 37.2: return 'Normal', 'normal'
    if v > 37.2: return 'Elevated', 'warning'
    return 'Low', 'warning'


# ── Anomaly detection ──────────────────────────────────────────────────────────
def run_anomaly_detection():
    if len(st.session_state.sensor_history) < 20:
        return []
    df = pd.DataFrame(st.session_state.sensor_history)
    X = df[['spo2', 'hr', 'temp', 'activity']].values
    clf = IsolationForest(contamination=0.05, random_state=42)
    preds = clf.fit_predict(X)
    anomalies = []
    for i, p in enumerate(preds):
        if p == -1:
            anomalies.append(df.iloc[i])
    return anomalies[-3:]


# ── Sidebar ────────────────────────────────────────────────────────────────────
if st.session_state.sidebar_open:
    with st.sidebar:
        st.markdown("""
        <div style='padding: 8px 0 20px;'>
            <div style='font-size:22px; font-weight:700; color:#00d4aa; letter-spacing:-0.5px;'>VitaIQ</div>
            <div style='font-size:11px; color:#64748b; letter-spacing:0.08em; text-transform:uppercase;'>Wellness Intelligence</div>
        </div>
        """, unsafe_allow_html=True)
    
        st.markdown('<div class="section-header">Daily Health Log</div>', unsafe_allow_html=True)
    
        with st.form("daily_log", clear_on_submit=False):
            sleep_hrs = st.slider("Sleep last night (hrs)", 0.0, 12.0, 7.0, 0.5)
            water     = st.slider("Water intake (glasses)", 0, 16, 8, 1)
            stress    = st.slider("Stress level (1=none, 10=max)", 1, 10, 3, 1)
    
            st.markdown("**Meal quality today**")
            meals = st.selectbox("Overall diet", [
                "Balanced (veggies, protein, grains)",
                "Mostly healthy",
                "Mixed / average",
                "Mostly junk food",
                "Skipped meals"
            ])
            diet_score_map = {
                "Balanced (veggies, protein, grains)": 10,
                "Mostly healthy": 8,
                "Mixed / average": 6,
                "Mostly junk food": 3,
                "Skipped meals": 1
            }
    
            symptoms = st.multiselect("Any symptoms today?", [
                "Headache", "Fatigue", "Chest pain",
                "Shortness of breath", "Dizziness", "Nausea", "None"
            ], default=["None"])
    
            submitted = st.form_submit_button("Log Today's Data", use_container_width=True)
            if submitted:
                entry = {
                    'timestamp': datetime.now().isoformat(),
                    'sleep': sleep_hrs,
                    'water': water,
                    'stress': stress,
                    'diet_score': diet_score_map[meals],
                    'symptoms': symptoms
                }
                st.session_state.health_log.append(entry)
                st.success("Logged successfully!")
    
        st.markdown("---")
        st.markdown('<div class="section-header">Device Status</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:12px; line-height:2;'>
        <span style='color:#10b981;'>●</span> ESP32 connected (simulated)<br>
        <span style='color:#10b981;'>●</span> MAX30102 SpO2/HR active<br>
        <span style='color:#10b981;'>●</span> AD8232 ECG active<br>
        <span style='color:#10b981;'>●</span> MLX90614 temp active<br>
        <span style='color:#10b981;'>●</span> MPU6050 activity active<br>
        <span style='color:#f59e0b;'>●</span> MQTT stream (local)
        </div>
        """, unsafe_allow_html=True)
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()        
        
           

# ── Main content ───────────────────────────────────────────────────────────────
sensors = read_sensors(IST)
# ─────────────────────────────────────────────
# 🫀 PATIENT / CLIENT VIEW LAYER
# ─────────────────────────────────────────────
st.title("🫀 VitalQ Smart Health Assistant")

st.markdown("""
This system monitors health data, analyzes patterns, and provides simple insights.

✔ Real-time vitals  
✔ AI-based analysis  
✔ Actionable recommendations  
""")

# ─────────────────────────────────────────────
# 📥 USER INPUT (MORE REALISTIC PARAMETERS)
# ─────────────────────────────────────────────

st.subheader("📋 Enter Daily Health Data")

col1, col2, col3 = st.columns(3)

with col1:
    sleep = st.slider("Sleep (hours)", 0, 12, 7)

with col2:
    water = st.slider("Water intake (glasses)", 0, 15, 8)

with col3:
    stress = st.slider("Stress level", 1, 10, 3)

col4, col5 = st.columns(2)

with col4:
    steps = st.slider("Daily activity (steps)", 0, 15000, 5000)

with col5:
    screen_time = st.slider("Screen time (hours)", 0, 12, 4)

# ─────────────────────────────────────────────
# ▶️ ANALYZE BUTTON
# ─────────────────────────────────────────────

if st.button("Analyze Health"):

    # simulate vitals from your system
    hr = sensors['hr']
    spo2 = sensors['spo2']
    temp = sensors['temp']

    inputs = {
        'sleep': sleep,
        'water': water,
        'stress': stress,
        'diet_score': 7
    }

    score = compute_wellness(sensors, inputs)

    # ─────────────────────────────────────────────
    # 🧠 HEALTH RESULT
    # ─────────────────────────────────────────────

    st.subheader("🧠 Health Status")

    if score >= 80:
        st.success("You are in good health condition")
    elif score >= 60:
        st.warning("Moderate health condition — some improvement needed")
    else:
        st.error("Health risk detected — please take care")

    st.write(f"Overall Score: {score}/100")

    # ─────────────────────────────────────────────
    # 📊 VISUAL GRAPH (CLIENT FRIENDLY)
    # ─────────────────────────────────────────────

    st.subheader("📊 Vital Trends")

    df = pd.DataFrame(st.session_state.sensor_history[-20:])
    st.line_chart(df[['spo2', 'hr', 'temp']])

    # ─────────────────────────────────────────────
    # 📈 SIMULATION (IMPACT OF INPUTS)
    # ─────────────────────────────────────────────

    st.subheader("🔄 Simulation: Impact of Lifestyle")

    sim_scores = []
    for s in range(3, 10):
        sim_inputs = {'sleep': s, 'water': water, 'stress': stress, 'diet_score': 7}
        sim_scores.append(compute_wellness(sensors, sim_inputs))

    sim_df = pd.DataFrame({
        "Sleep Hours": list(range(3,10)),
        "Wellness Score": sim_scores
    })

    st.line_chart(sim_df.set_index("Sleep Hours"))

    # ─────────────────────────────────────────────
    # 💡 INSIGHTS (SMART RESPONSES)
    # ─────────────────────────────────────────────

    st.subheader("💡 Personalized Insights")

    insights = []

    if spo2 < 95:
        insights.append("Low oxygen level — ensure proper breathing and rest")

    if hr > 100:
        insights.append("High heart rate — reduce stress and avoid exertion")

    if temp > 37.5:
        insights.append("Body temperature is high — monitor for fever")

    if sleep < 6:
        insights.append("Low sleep — aim for at least 7 hours")

    if water < 5:
        insights.append("Low hydration — increase water intake")

    if stress > 6:
        insights.append("High stress — consider relaxation techniques")

    if steps < 3000:
        insights.append("Low physical activity — increase daily movement")

    if screen_time > 6:
        insights.append("High screen time — reduce for better health")

    if not insights:
        st.success("All parameters look good — maintain your lifestyle")
    else:
        for i in insights:
            st.write(f"- {i}")

    # ─────────────────────────────────────────────
    # 📊 SUMMARY DASHBOARD
    # ─────────────────────────────────────────────

    st.subheader("📌 Key Metrics")

    c1, c2, c3 = st.columns(3)
    c1.metric("Heart Rate", f"{hr} BPM")
    c2.metric("Oxygen Level", f"{spo2}%")
    c3.metric("Temperature", f"{temp} °C")
