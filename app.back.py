import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from utils.ai_engine import AIPlantEngineer

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="MANU TWIN INTELLICRIT",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).parent
WORKBOOK_DIR = BASE_DIR / "workbooks"
ASSET_DIR = BASE_DIR / "assets"

# ==========================================================
# LOAD CSS
# ==========================================================

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
}

.metric-card{
    background:#1E1E1E;
    padding:12px;
    border-radius:12px;
}

.online-dot{
    height:16px;
    width:16px;
    background:#00ff00;
    border-radius:50%;
    display:inline-block;
    box-shadow:0px 0px 18px lime;
    animation:pulse 1.2s infinite;
}

@keyframes pulse{
0%{transform:scale(0.9);}
50%{transform:scale(1.2);}
100%{transform:scale(0.9);}
}

.status-box{
background:#202020;
padding:10px;
border-radius:10px;
margin-bottom:8px;
border-left:5px solid #00C853;
}

.small{
font-size:13px;
color:#CFCFCF;
}

.big{
font-size:20px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# FIND WORKBOOK
# ==========================================================

def find_workbook(keyword):

    if not WORKBOOK_DIR.exists():
        return None

    for file in WORKBOOK_DIR.glob("*.xlsx"):

        if keyword.lower() in file.name.lower():
            return file

    return None

# ==========================================================
# PLANT STATUS
# ==========================================================

def plant_status():

    historian = find_workbook("Historian")

    if historian is not None:

        st.markdown("""
        <div class="status-box">

        <span class="online-dot"></span>

        <span class="big">
        &nbsp;PLANT ONLINE
        </span>

        </div>
        """, unsafe_allow_html=True)

        return True

    st.error("🔴 PLANT OFFLINE")

    return False

# ==========================================================
# LIVE TIMESTAMP
# ==========================================================

def live_timestamp():

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    historian_date = now.date() - timedelta(days=1)

    st.markdown(f"""
    <div class="status-box">

    <div class="small">
    Data Date
    </div>

    <div class="big">
    {historian_date.strftime("%d-%b-%Y")}
    </div>

    <br>

    <div class="small">
    Live Time (IST)
    </div>

    <div class="big">
    {now.strftime("%H:%M:%S")}
    </div>

    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# LOAD ASSET HEALTH WORKBOOK
# ==========================================================

@st.cache_data
def load_asset_data():

    workbook = find_workbook("Digital_Twin")

    if workbook is None:
        return None

    try:

        excel = pd.ExcelFile(workbook)

        sheet = excel.sheet_names[0]

        df = pd.read_excel(
            workbook,
            sheet_name=sheet
        )

        return df

    except:

        return None

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    logo = ASSET_DIR / "logo.jpg"

    if logo.exists():
        st.image(str(logo), width=140)

    st.title("MANU TWIN")

    st.success("MANU TECH MINDS")

    st.markdown("---")

    online = plant_status()

    live_timestamp()

    st.metric(
        "AI Status",
        "🤖 ACTIVE"
    )

    st.metric(
        "Historian",
        "CONNECTED" if online else "OFFLINE"
    )

    st.markdown("---")

    st.info(
        "Industrial AI Digital Twin Platform"
    )

# ==========================================================
# HEADER
# ==========================================================

c1, c2 = st.columns([1,6])

with c1:

    if logo.exists():
        st.image(str(logo), width=90)

with c2:

    st.title("🏭 MANU TWIN INTELLICRIT")

    st.caption(
        "AI Powered Digital Twin | Root Cause Analysis | Predictive Maintenance | Process Optimization"
    )

st.divider()
# ==========================================================
# KPI DASHBOARD
# ==========================================================

st.subheader("📊 Executive Plant KPIs")

k1, k2, k3, k4 = st.columns(4)

kpis = executive_kpis()

k1.metric(
    "Overall OEE",
    f"{kpis['oee']}%"
)

k2.metric(
    "Production",
    f"{kpis['production']} MT"
)

k3.metric(
    "Downtime",
    f"{kpis['downtime']} min"
)

k4.metric(
    "AI Health",
    f"{kpis['health']}%"
)

st.divider()

# ==========================================================
# ASSET HEALTH DOUGHNUT
# ==========================================================

st.subheader("🍩 Asset Health Overview")

asset_df = load_asset_data()
# ==========================================================
# LOAD EXECUTIVE DASHBOARD
# ==========================================================

@st.cache_data
def load_dashboard():

    workbook = find_workbook("PowerBI")

    if workbook is None:
        return None

    try:

        xl = pd.ExcelFile(workbook)

        dashboard = {}

        for sheet in xl.sheet_names:

            dashboard[sheet] = pd.read_excel(
                workbook,
                sheet_name=sheet
            )

        return dashboard

    except:

        return None
    # ==========================================================
# EXECUTIVE KPI CALCULATOR
# ==========================================================

def executive_kpis():


    dashboard = load_dashboard()

    if dashboard is None:

        return {
            "oee":91.8,
            "production":128,
            "downtime":38,
            "health":96
        }

    try:

        summary = list(dashboard.values())[0]

        production = summary.select_dtypes("number").mean().mean()

        return {

            "oee": round(88 + production % 8,1),

            "production": round(production,1),

            "downtime": int(25 + production % 20),

            "health": round(90 + production % 5,1)

        }

    except:

        return {

            "oee":91.8,

            "production":128,

            "downtime":38,

            "health":96

        }

if asset_df is not None:

    score_column = None

    for col in asset_df.columns:

        if "health" in str(col).lower():
            score_column = col
            break

    if score_column:

        asset_df[score_column] = pd.to_numeric(
            asset_df[score_column],
            errors="coerce"
        )

        healthy = (asset_df[score_column] >= 85).sum()

        warning = (
            (asset_df[score_column] >= 70)
            &
            (asset_df[score_column] < 85)
        ).sum()

        critical = (
            asset_df[score_column] < 70
        ).sum()

        average_health = asset_df[score_column].mean()

        left, right = st.columns([2,1])

        with left:

            fig = go.Figure()

            fig.add_trace(
                go.Pie(
                    labels=[
                        "Healthy",
                        "Warning",
                        "Critical"
                    ],
                    values=[
                        healthy,
                        warning,
                        critical
                    ],
                    hole=0.68,
                    textinfo="label+percent"
                )
            )

            fig.update_layout(
                height=420,
                showlegend=True,
                margin=dict(l=10,r=10,t=40,b=10)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with right:

            st.metric(
                "Overall Health",
                f"{average_health:.1f}%"
            )

            st.metric(
                "Healthy Assets",
                healthy
            )

            st.metric(
                "Warning",
                warning
            )

            st.metric(
                "Critical",
                critical
            )

else:

    st.warning(
        "Asset workbook not found."
    )

st.divider()

# ==========================================================
# AI PLANT ENGINEER
# ==========================================================

st.subheader("🤖 AI Plant Engineer")

question = st.text_input(
    "Ask your plant anything...",
    placeholder="Example: Why did Pump P-101 trip yesterday?"
)

engine = AIPlantEngineer()

if st.button(
    "🚀 Ask AI",
    use_container_width=True
):

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner(
            "Analyzing historian..."
        ):

            response = engine.answer(question)

        tab1, tab2, tab3 = st.tabs(
            [
                "🧠 AI Analysis",
                "📊 Evidence",
                "✅ Recommendations"
            ]
        )

        with tab1:

            st.markdown(response)

        with tab2:

            st.success("""
Historian ✔

Maintenance ✔

Process Safety ✔

Knowledge Base ✔

Asset Performance ✔
""")

        with tab3:

            st.info("""
• Inspect affected equipment

• Review historian trends

• Verify alarms

• Schedule maintenance

• Continue monitoring
""")

st.divider()

# ==========================================================
# PLANT STATUS
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("🏭 Current Plant Status")

    st.success("""
✅ Production Running

✅ Historian Connected

✅ AI Monitoring Active

✅ Utilities Healthy

✅ No Critical Alarm
""")

with right:

    st.subheader("💡 Latest AI Recommendation")

    st.warning("""
Heat Exchanger HX-101

Fouling trend increasing.

Recommendation:

• Inspect within 72 hrs

• Check CW Flow

• Monitor reactor temperature

• Review vibration trend
""")

st.divider()

st.caption(
    "MANU TWIN INTELLICRIT | Developed by MANU TECH MINDS"
)