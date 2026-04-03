import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="AQKA-PINN Platform", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CINEMATIC CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=Roboto+Mono:wght@300;500&display=swap');
    
    :root {
        --glass: rgba(10, 14, 20, 0.85);
        --cyan: #00F2FF;
        --border: rgba(0, 242, 255, 0.3);
    }

    .stApp {
        background: radial-gradient(circle at center, #0B1118 0%, #05070A 100%);
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism Panels */
    div[data-testid="stVerticalBlock"] > div.element-container {
        background: var(--glass);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0, 242, 255, 0.1);
        margin-bottom: 10px;
    }

    /* Header Styling */
    .main-header {
        text-align: center;
        border-bottom: 2px solid var(--cyan);
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    .status-text {
        font-family: 'Roboto Mono', monospace;
        color: var(--cyan);
        font-size: 0.9rem;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: var(--cyan) !important;
        font-family: 'Roboto Mono', monospace;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: transparent;
        color: var(--cyan);
        border: 1px solid var(--cyan);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: var(--cyan);
        color: black;
        box-shadow: 0 0 15px var(--cyan);
    }
    </style>
    """, unsafe_placeholder=True)

# --- HEADER SECTION ---
col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
with col_h1:
    st.markdown("<h2 style='margin:0;'>AQKA-PINN <span style='color:#00F2FF;'>Intelligent Diagnostic Platform</span></h2>", unsafe_placeholder=True)
    st.markdown("<p class='status-text'>SYSTEM STATUS: <span style='color:#00FF41;'>● ACTIVE</span> | NODE: QUANTUM-A14</p>", unsafe_placeholder=True)

with col_h2:
    st.metric("AI Confidence", "92.4%", "+0.2%")
with col_h3:
    st.metric("Latency", "32ms", "-4ms")

st.markdown("---")

# --- MAIN LAYOUT ---
left_col, center_col, right_col = st.columns([1, 2, 1])

# --- LEFT PANEL: CLINICAL INPUT ---
with left_col:
    st.subheader("📋 Clinical Input")
    uploaded_file = st.file_uploader("Upload DICOM/Scan", type=['png', 'jpg', 'jpeg'])
    
    st.info("Patient ID: **XP-9920** | Age: 54 | Sex: M")
    
    st.slider("Thermal Sensitivity (PINN)", 0.0, 1.0, 0.85)
    st.slider("Vibration Frequency (Hz)", 0, 1000, 440)
    
    st.write("Annotation Tools")
    btn_col1, btn_col2 = st.columns(2)
    btn_col1.button("🔍 Zoom")
    btn_col2.button("📏 Measure")

# --- CENTER PANEL: AI ANALYSIS ---
with center_col:
    st.subheader("🧠 Neural Analysis Core")
    
    # Simulate a PINN Heatmap Overlay on a scan
    img_data = np.random.rand(100, 100)
    fig = go.Figure(data=[go.Heatmap(
        z=img_data,
        colorscale='Viridis',
        showscale=False,
        hoverinfo='z'
    )])
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)
    
    layers = st.multiselect("Toggle Analysis Layers", ["Raw Scan", "Segmentation", "PINN Risk Overlay"], default=["Raw Scan", "Segmentation"])

# --- RIGHT PANEL: CLINICAL INSIGHTS ---
with right_col:
    st.subheader("📊 Clinical Insights")
    st.error("RISK LEVEL: HIGH")
    
    st.markdown("""
    **Primary Prediction:**  
    *Metastatic Abnormality (Zone A)*
    
    **Calculated Metrics:**
    - Lesion Size: `4.2mm`
    - Tissue Density: `1.04 g/cm³`
    - Growth Rate: `+1.2% / month`
    """)
    
    st.progress(0.92, text="Model Convergence")
    st.button("Generate Medical Report")
    st.button("🚨 EMERGENCY ALERT", type="primary")

# --- BOTTOM PANEL: PHYSICS EXPLAINABILITY ---
st.markdown("---")
bot_col1, bot_col2 = st.columns([2, 1])

with bot_col1:
    st.subheader("🧬 PINN Physics Explainability")
    st.latex(r'''
    \frac{\partial T}{\partial t} = \alpha \left( \frac{\partial^2 T}{\partial x^2} + \frac{\partial^2 T}{\partial y^2} \right) + S
    ''')
    st.caption("AI solving Bio-heat Transfer Equation for Tissue Anomalies")
    
    # Feature importance chart
    features = ['Density', 'Thermal', 'Mass', 'Gradient']
    scores = [45, 30, 15, 10]
    feat_fig = go.Figure([go.Bar(x=features, y=scores, marker_color='#00F2FF')])
    feat_fig.update_layout(height=150, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(feat_fig, use_container_width=True)

with bot_col2:
    st.subheader("📈 Time-Series Projection")
    chart_data = np.random.randn(20, 1).cumsum()
    st.line_chart(chart_data)

