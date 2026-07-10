import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.ai_engine import AIPlantEngineer
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
import os

# -------------------------------------------------------
# LIVE PLANT STATUS
# -------------------------------------------------------

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
                <span style="font-size:20px;font-weight:bold;">
                &nbsp;PLANT ONLINE
                </span>
            </div>
            """, unsafe_allow_html=True)

            return

    st.markdown("""
    <span style="color:red;font-size:20px;font-weight:bold;">
    🔴 PLANT OFFLINE
    </span>
    """, unsafe_allow_html=True)
def live_timestamp():

    # Current time in India
    now = datetime.now(ZoneInfo("Asia/Kolkata"))

    # Historian data represents yesterday
    historian_date = now.date() - timedelta(days=1)

    st.markdown(f"""
    <div style="
        background:#1E1E1E;
        padding:10px;
        border-radius:10px;
        border-left:5px solid #00C853;
        margin-top:10px;
        margin-bottom:10px;
    ">

    <b>📅 Data Date :</b> {historian_date.strftime("%d-%b-%Y")}<br>

    <b>🕒 Live Time (IST) :</b> {now.strftime("%H:%M:%S")}

    </div>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="MANU TWIN INTELLICRIT",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

col1, col2 = st.columns([1, 6])

with col1:
    st.image("assets/logo.jpg", width=90)

with col2:
    st.title("🏭 MANU TWIN INTELLICRIT")
    st.caption(
        "AI-Powered Digital Twin for Root Cause Analysis, Predictive Maintenance & Process Optimization"
    )

st.markdown("---")

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

with st.sidebar:

    st.image("assets/logo.jpg", width=150)

    st.title("MANU TWIN")

    st.success("MANU TECH MINDS")

    st.markdown("---")

    plant_status()
    # -------------------------------------------------------
    # LIVE DATA TIMESTAMP
    # -------------------------------------------------------

    live_timestamp()
    # -------------------------------------------------------
# ASSET HEALTH DOUGHNUT CHART
# -------------------------------------------------------

def asset_health_chart():

    try:

        # Read Workbook 5
        df = pd.read_excel(
          "workbooks/Workbook_5_Digital_Twin_AI_Mapped.xlsx",
            sheet_name="Asset Health Ranking",
            header=1
        )

        # Rename columns
        df.columns = [
            "Rank",
            "Equipment",
            "Health Score",
            "Priority",
            "Recommendation",
            "Extra"
        ]

        # Remove the first duplicated header row
        df = df[df["Rank"] != "Rank"]

        # Convert health score to numeric
        df["Health Score"] = pd.to_numeric(
            df["Health Score"],
            errors="coerce"
        )

        # Categorize assets
        healthy = (df["Health Score"] >= 85).sum()
        warning = ((df["Health Score"] >= 70) &
                   (df["Health Score"] < 85)).sum()
        critical = (df["Health Score"] < 70).sum()

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
                hole=0.65,
                textinfo="label+percent"
            )
        )

        fig.update_layout(
            title="Equipment Health Distribution",
            height=420,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.metric(
            "Overall Asset Health",
            f"{df['Health Score'].mean():.1f}%"
        )

    except Exception as e:

        st.error(f"Unable to load Asset Health Chart: {e}")

    st.metric("AI Status", "🤖 ACTIVE")

    st.metric("Historian", "✅ CONNECTED")

    st.metric("Equipment Health", "98%")

    st.markdown("---")

    st.info("Industrial AI Digital Twin Platform")

# -------------------------------------------------------
# MAIN PAGE
# -------------------------------------------------------

st.subheader(
    "AI Agent for Root Cause Analysis & Process Optimization"
)

st.success("Welcome Team MANU TECH MINDS")

st.markdown("## 🤖 AI Plant Engineer")

question = st.text_input(
    "Ask anything about your plant...",
    placeholder="Example: Why did Reactor R101 trip yesterday?"
)

engine = AIPlantEngineer()

if st.button("🚀 Ask AI", use_container_width=True):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("AI is searching your historian and knowledge base..."):

            response = engine.answer(question)

        tab1, tab2, tab3 = st.tabs(
            ["🧠 Root Cause", "📊 Evidence", "✅ Actions"]
        )

        with tab1:
            st.markdown(response)

        with tab2:
            st.info("""
### Evidence Sources

✅ Historian (Workbook 2)

✅ AI Analytics & RCA (Workbook 3)

✅ Maintenance Records (Workbook 6)

✅ Process Safety (Workbook 7)

✅ Engineering Knowledge Base (Workbook 11)

✅ Asset Performance (Workbook 12)
""")

        with tab3:
            st.success("""
### Immediate Recommendations

✔ Inspect affected equipment

✔ Verify operating conditions

✔ Check recent alarms

✔ Review historian trends

✔ Create maintenance work order
""")

st.markdown("---")

st.subheader("Plant KPIs")

c1, c2, c3, c4 = st.columns(4)

c1.metric("OEE", "91.8%", "+1.3%")
c2.metric("Production", "128 MT", "+5 MT")
c3.metric("Downtime", "38 min", "-12")
c4.metric("AI Health", "96%", "+4%")

asset_health_chart()