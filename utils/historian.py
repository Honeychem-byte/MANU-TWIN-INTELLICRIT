import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# WORKBOOK LOCATION
# =========================================================

WORKBOOK_FOLDER = Path("workbooks")

# =========================================================
# EQUIPMENT MAPPING
# =========================================================

EQUIPMENT_MAP = {

    "Reactor R101": [
        "Reactor Temperature",
        "Reactor Pressure",
        "Reactor Level",
        "Production Rate"
    ],

    "Pump P101": [
        "Pump Current",
        "Pump Vibration",
        "Motor RPM"
    ],

    "Heat Exchanger E101": [
        "Cooling Water Flow",
        "Heat Exchanger Fouling Index"
    ],

    "Distillation Column C101": [
        "Column Top Temp",
        "Column Bottom Temp",
        "Final Product Purity"
    ],

    "Plant Performance": [
        "Yield",
        "OEE",
        "Alarm Count",
        "Downtime",
        "AI Health Score",
        "Risk Score"
    ]

}

# =========================================================
# LOAD HISTORIAN
# =========================================================

def get_historian_data():

    workbook = None

    for file in WORKBOOK_FOLDER.glob("*.xlsx"):

        if "Historian" in file.name:

            workbook = file
            break

    if workbook is None:
        return None

    sheets = pd.read_excel(
        workbook,
        sheet_name=None
    )

    if "Historian" not in sheets:
        return None

    df = sheets["Historian"]

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    return df

# =========================================================
# HISTORIAN DASHBOARD
# =========================================================

def historian_dashboard():

    df = get_historian_data()

    if df is None:

        st.error("Historian Workbook Not Found")

        return

    st.subheader("📈 Live Digital Twin Historian")

    equipment = st.selectbox(
        "🏭 Equipment",
        list(EQUIPMENT_MAP.keys())
    )

    available_parameters = [

        p for p in EQUIPMENT_MAP[equipment]

        if p in df.columns

    ]

    if len(available_parameters) == 0:

        st.warning("No parameters found.")

        return

    parameter = st.selectbox(

        "📊 Parameter",

        available_parameters

    )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=df["Timestamp"],

            y=df[parameter],

            mode="lines",

            name=parameter,

            line=dict(width=2)

        )

    )

    fig.update_layout(

        title=f"{equipment} - {parameter}",

        xaxis_title="Time",

        yaxis_title=parameter,

        hovermode="x unified",

        height=450

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(

        "Current",

        f"{df[parameter].iloc[-1]:.2f}"

    )

    c2.metric(

        "Maximum",

        f"{df[parameter].max():.2f}"

    )

    c3.metric(

        "Minimum",

        f"{df[parameter].min():.2f}"

    )

    c4.metric(

        "Average",

        f"{df[parameter].mean():.2f}"

    )

    st.markdown("---")

    st.info(f"""
### 🤖 AI Observation

**Equipment:** {equipment}

**Parameter:** {parameter}

• Current Value : **{df[parameter].iloc[-1]:.2f}**

• Average Value : **{df[parameter].mean():.2f}**

• Maximum Value : **{df[parameter].max():.2f}**

• Minimum Value : **{df[parameter].min():.2f}**

Recommendation:

- Continue monitoring the selected asset.
- Review abnormal spikes if observed.
- Compare with maintenance history.
- Use AI Root Cause Analysis for detailed diagnostics.
""")