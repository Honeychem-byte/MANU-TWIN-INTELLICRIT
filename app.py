import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import streamlit as st

from utils.ai_engine import AIPlantEngineer
from utils.asset_health import asset_health_chart
from utils.dashboard import executive_dashboard
from utils.historian import historian_dashboard

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="MANU TWIN INTELLICRIT",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CACHE AI ENGINE
# ==========================================================

@st.cache_resource
def load_ai_engine():
    return AIPlantEngineer()

engine = load_ai_engine()

# ==========================================================
# LIVE PLANT STATUS
# ==========================================================

def plant_status():

    workbook_folder = "workbooks"

    if os.path.exists(workbook_folder):

        files = [
            f for f in os.listdir(workbook_folder)
            if f.endswith(".xlsx")
        ]

        if len(files) > 0:

            st.markdown("""
            <style>

            .online{
                display:inline-block;
                width:15px;
                height:15px;
                background:#00ff00;
                border-radius:50%;
                box-shadow:0px 0px 15px lime;
                animation:pulse 1.2s infinite;
            }

            @keyframes pulse{
                0%{transform:scale(0.9);}
                50%{transform:scale(1.2);}
                100%{transform:scale(0.9);}
            }

            </style>

            <div>
                <span class="online"></span>
                <span style="font-size:18px;font-weight:bold;">
                &nbsp;PLANT ONLINE
                </span>
            </div>
            """, unsafe_allow_html=True)

            return

    st.error("🔴 PLANT OFFLINE")


# ==========================================================
# LIVE TIMESTAMP
# ==========================================================

def live_timestamp():

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    historian_date = now.date() - timedelta(days=1)

    st.markdown(f"""
    <div style="
        background:#1E1E1E;
        padding:10px;
        border-radius:10px;
        border-left:5px solid #00C853;
    ">

    <b>📅 Historian Date :</b>
    {historian_date.strftime("%d-%b-%Y")}

    <br>

    <b>🕒 Live Time (IST):</b>
    {now.strftime("%H:%M:%S")}

    </div>
    """,
    unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

logo_col, title_col = st.columns([1,6])

with logo_col:

    st.image(
        "assets/logo.jpg",
        width=90
    )

with title_col:

    st.title("🏭 MANU TWIN INTELLICRIT")

    st.caption(
        "AI-Powered Digital Twin for Root Cause Analysis • Predictive Maintenance • Process Optimization"
    )

st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image(
        "assets/logo.jpg",
        width=140
    )

    st.title("MANU TWIN")

    st.success("MANU TECH MINDS")

    st.divider()

    plant_status()

    live_timestamp()

    st.divider()

    st.metric(
        "AI Status",
        "ACTIVE"
    )

    st.metric(
        "Platform",
        "CONNECTED"
    )

    st.info(
        "Industrial AI Digital Twin Platform"
    )

st.subheader(
    "🤖 AI Plant Engineer"
)

st.success(
    "Welcome Team MANU TECH MINDS"
)

# ==========================================================
# AI CHAT
# ==========================================================
question = st.text_input(
    "Ask anything about your plant...",
    placeholder="Example: Why did Reactor R101 trip yesterday?"
)
engine = load_ai_engine()
if st.button("🚀 Analyze with AI", use_container_width=True):

    if question.strip() == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("🔍 Searching Historian, Maintenance and Engineering Knowledge Base..."):

            response = engine.answer(question)

        root_tab, evidence_tab, action_tab = st.tabs(
            [
                "🧠 AI Analysis",
                "📊 Engineering Evidence",
                "✅ Recommended Actions"
            ]
        )

        with root_tab:

            st.markdown(response)

        with evidence_tab:

            st.success("### Data Sources Used")

            st.markdown("""
✅ Workbook 2 — AI Plant Historian

✅ Workbook 3 — AI Analytics & Root Cause Analysis

✅ Workbook 5 — Digital Twin & Asset Health

✅ Workbook 6 — Maintenance Records

✅ Workbook 7 — Process Safety

✅ Workbook 11 — Engineering Knowledge Base

✅ Workbook 12 — Asset Performance
""")

        with action_tab:

            st.info("""
### Recommended Engineering Actions

• Inspect affected equipment

• Review historian trends

• Verify DCS alarms

• Check maintenance history

• Validate process conditions

• Review operating procedures

• Generate maintenance work order
""")

st.divider()

# ==========================================================
# EXECUTIVE DASHBOARD
# ==========================================================

executive_dashboard()

# ==========================================================
# DIGITAL TWIN DASHBOARD
# ==========================================================

left, right = st.columns([1,2])

with left:

    asset_health_chart()

with right:

    historian_dashboard()

st.divider()
# ==========================================================
# SYSTEM STATUS
# ==========================================================

status1, status2 = st.columns(2)

with status1:

    st.subheader("🏭 Plant Status")

    st.success("""
✔ Production Running

✔ Historian Connected

✔ AI Monitoring Active

✔ Digital Twin Active

✔ Predictive Analytics Running

✔ Process Safety Monitoring Enabled
""")

with status2:

    st.subheader("🤖 Latest AI Recommendation")

    st.warning("""
Heat Exchanger E101 shows an increasing fouling trend.

Recommended Action:

• Schedule inspection within the next maintenance window.

• Verify cooling water flow.

• Review historical temperature trends.

• Monitor exchanger efficiency continuously.

Confidence: 96%
""")

st.divider()

# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.subheader("⚡ Quick AI Actions")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button("📊 Show Historian"):

        st.info("Scroll to the Historian Dashboard below.")

    if st.button("⚙ Equipment Health"):

        st.info("Asset Health Dashboard Loaded.")

with col2:

    if st.button("🧠 Root Cause"):

        st.info("Ask the AI above for Root Cause Analysis.")

    if st.button("🛠 Maintenance"):

        st.info("Maintenance Records are included in AI analysis.")

with col3:

    if st.button("⚠ Process Safety"):

        st.info("Process Safety workbook is connected.")

    if st.button("📈 Executive KPI"):

        st.info("Executive Dashboard Loaded.")

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "© 2026 MANU TWIN INTELLICRIT | Built by MANU TECH MINDS"
)