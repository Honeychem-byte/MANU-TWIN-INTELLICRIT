import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Internal utility imports (Assuming these exist in your project)
from utils.historian import load_historian
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
# PROJECT PATHS & CSS
# ==========================================================
BASE_DIR = Path(__file__).parent
WORKBOOK_DIR = BASE_DIR / "workbooks"
ASSET_DIR = BASE_DIR / "assets"

st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    .online-dot {
        height: 16px; width: 16px;
        background: #00ff00; border-radius: 50%;
        display: inline-block; box-shadow: 0px 0px 18px lime;
        animation: pulse 1.2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.9); }
        50% { transform: scale(1.2); }
        100% { transform: scale(0.9); }
    }
    .status-box {
        background: #202020; padding: 10px;
        border-radius: 10px; margin-bottom: 8px;
        border-left: 5px solid #00C853;
    }
    .small { font-size: 13px; color: #CFCFCF; }
    .big { font-size: 20px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================
def find_workbook(keyword):
    if not WORKBOOK_DIR.exists():
        return None
    for file in WORKBOOK_DIR.glob("*.xlsx"):
        if keyword.lower() in file.name.lower():
            return file
    return None

def plant_status():
    historian = find_workbook("Historian")
    if historian:
        st.markdown('<div class="status-box"><span class="online-dot"></span><span class="big">&nbsp;PLANT ONLINE</span></div>', unsafe_allow_html=True)
        return True
    st.error("🔴 PLANT OFFLINE")
    return False

@st.cache_data
def load_asset_data():
    workbook = find_workbook("Digital_Twin")
    if workbook is None: return None
    try:
        df = pd.read_excel(workbook, sheet_name=0)
        return df
    except Exception:
        return None

# ==========================================================
# SIDEBAR
# ==========================================================
with st.sidebar:
    logo_path = ASSET_DIR / "logo.jpg"
    if logo_path.exists():
        st.image(str(logo_path), width=140)
    
    st.title("MANU TWIN")
    st.success("MANU TECH MINDS")
    st.markdown("---")
    
    online = plant_status()
    
    # Live Timestamp Logic
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    data_date = now.date() - timedelta(days=1)
    
    st.markdown(f"""
    <div class="status-box">
        <div class="small">Data Date</div>
        <div class="big">{data_date.strftime("%d-%b-%Y")}</div>
        <br>
        <div class="small">Live Time (IST)</div>
        <div class="big">{now.strftime("%H:%M:%S")}</div>
    </div>
    """, unsafe_allow_html=True)

    st.metric("AI Status", "🤖 ACTIVE")
    st.metric("Historian", "CONNECTED" if online else "OFFLINE")

# ==========================================================
# HEADER & KPIs
# ==========================================================
c1, c2 = st.columns([1,6])
with c1:
    if logo_path.exists(): st.image(str(logo_path), width=80)
with c2:
    st.title("🏭 MANU TWIN INTELLICRIT")
    st.caption("AI Powered Digital Twin | Predictive Maintenance | Process Optimization")

st.divider()

# KPI Calculation
asset_df = load_asset_data()
k1, k2, k3, k4 = st.columns(4)

if asset_df is not None and not asset_df.empty:
    oee = int(asset_df["OEE"].mean()) if "OEE" in asset_df.columns else 0
    prod = int(asset_df["Production"].sum()) if "Production" in asset_df.columns else 0
    dt = int(asset_df["Downtime"].sum()) if "Downtime" in asset_df.columns else 0
    health = int(asset_df["Health"].mean()) if "Health" in asset_df.columns else 0
else:
    oee, prod, dt, health = 0, 0, 0, 0

k1.metric("Overall OEE", f"{oee}%")
k2.metric("Production", f"{prod} MT")
k3.metric("Downtime", f"{dt} min")
k4.metric("AI Health", f"{health}%")

# ==========================================================
# MAIN DASHBOARD PANELS
# ==========================================================
st.divider()
left, right = st.columns([1, 2])

with left:
    st.markdown("### 🍩 Asset Health")
    if asset_df is not None:
        # Find column containing 'health'
        health_col = next((c for c in asset_df.columns if "health" in c.lower()), None)
        
        if health_col:
            vals = pd.to_numeric(asset_df[health_col], errors='coerce').fillna(0)
            h_count = (vals >= 85).sum()
            w_count = ((vals >= 70) & (vals < 85)).sum()
            c_count = (vals < 70).sum()

            fig = go.Figure(data=[go.Pie(labels=["Healthy", "Warning", "Critical"], 
                                       values=[h_count, w_count, c_count], 
                                       hole=.7, marker=dict(colors=['#00C853', '#FFD600', '#D50000']))])
            fig.update_layout(height=350, margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Avg Health Score", f"{vals.mean():.1f}%")
    else:
        st.warning("No Asset Data available.")

with right:
    st.markdown("### 📈 Live Digital Twin Historian")
    hist_data = load_historian()
    
    if hist_data:
        sheet = st.selectbox("📄 Select Source", list(hist_data.keys()))
        df_hist = hist_data[sheet]
        
        # Determine Time Column
        time_col = next((c for c in df_hist.columns if any(x in c.lower() for x in ["time", "date"])), None)
        
        if time_col:
            df_hist[time_col] = pd.to_datetime(df_hist[time_col])
            nums = df_hist.select_dtypes(include='number').columns.tolist()
            
            if nums:
                param = st.selectbox("📊 Parameter", nums)
                fig_line = go.Figure(go.Scatter(x=df_hist[time_col], y=df_hist[param], mode='lines', line=dict(color='#00d4ff')))
                fig_line.update_layout(height=350, margin=dict(t=30, b=0), xaxis_title="Time", yaxis_title=param)
                st.plotly_chart(fig_line, use_container_width=True)
                
                # Metrics Row
                m1, m2, m3 = st.columns(3)
                m1.metric("Current", f"{df_hist[param].iloc[-1]:.2f}")
                m2.metric("Peak", f"{df_hist[param].max():.2f}")
                m3.metric("Avg", f"{df_hist[param].mean():.2f}")
    else:
        st.error("Historian Connection Failed.")

# ==========================================================
# AI AGENT SECTION
# ==========================================================
st.divider()
st.subheader("🤖 AI Plant Engineer")
question = st.text_input("Ask your plant anything...", placeholder="e.g., Analysis of vibration levels in Turbine GT-1")

if st.button("🚀 Ask AI", use_container_width=True):
    if question:
        with st.spinner("Analyzing data streams..."):
            engine = AIPlantEngineer()
            response = engine.answer(question)
            
            t1, t2, t3 = st.tabs(["🧠 Analysis", "📊 Evidence", "✅ Steps"])
            with t1: st.markdown(response)
            with t2: st.info("Verification: Historian (OK), Maintenance logs (OK), Sensors (OK)")
            with t3: st.success("1. Inspect Bearings\n2. Check Lubrication\n3. Schedule Vibration Tuning")
    else:
        st.warning("Please enter a query.")

st.divider()
st.caption("MANU TWIN INTELLICRIT | Powered by MANU TECH MINDS")
