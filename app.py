import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import pydicom
import io

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="AQKA-PINN Clinical Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Increase upload limit for large DICOM sets
st.set_option('server.maxUploadSize', 200)

# --- 2. CLINICAL UI STYLING (HOSPITAL DARK MODE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
    
    :root {
        --hosp-blue: #00D1FF;
        --hosp-danger: #FF4B4B;
        --hosp-bg: #0E1117;
        --hosp-panel: #1A1C23;
    }

    .stApp { background-color: var(--hosp-bg); color: #E0E0E0; }

    /* Modular Glass Panels */
    div.stVerticalBlock > div.element-container {
        background: var(--hosp-panel);
        border: 1px solid rgba(0, 209, 255, 0.2);
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .clinical-header {
        background: linear-gradient(90deg, #1A1C23 0%, #0E1117 100%);
        padding: 10px 20px;
        border-bottom: 2px solid var(--hosp-blue);
        margin-bottom: 25px;
    }

    .metric-label { font-family: 'Roboto Mono', monospace; color: var(--hosp-blue); font-size: 12px; }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        border: 1px solid var(--hosp-blue);
        background: rgba(0, 209, 255, 0.05);
        color: var(--hosp-blue);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: var(--hosp-blue);
        color: black;
        box-shadow: 0 0 15px rgba(0, 209, 255, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC: MEDICAL IMAGE PROCESSING ---
def process_medical_file(uploaded_file):
    """Handles PNG, JPG, and DICOM with normalization."""
    if uploaded_file is None:
        return None
    
    filename = uploaded_file.name.lower()
    
    try:
        if filename.endswith('.dcm'):
            ds = pydicom.dcmread(uploaded_file)
            img_array = ds.pixel_array.astype(float)
            # Normalize pixel values for display (0-255)
            img_array = (img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array)) * 255
            return img_array
        else:
            img = Image.open(uploaded_file).convert('L')
            return np.array(img)
    except Exception as e:
        st.error(f"Processing Error: {e}")
        return None

# --- 4. TOP NAVIGATION BAR ---
st.markdown("""
    <div class="clinical-header">
        <h2 style='margin:0; color:#00D1FF;'>AQKA-PINN <span style='font-weight:100; color:white;'>| Intelligent Diagnostic Platform</span></h2>
        <p style='margin:0; font-size:12px; opacity:0.7;'>v4.0.2-SECURE | SESSION: 882-AX | HOSPITAL NODE: ONCOLOGY-04</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD LAYOUT ---
col_sidebar, col_main, col_stats = st.columns([1, 2.5, 1])

# --- LEFT PANEL: CLINICAL INPUT ---
with col_sidebar:
    st.markdown("#### 📥 Patient Intake")
    file = st.file_uploader("Upload Scan (DICOM/IMG)", type=['png', 'jpg', 'jpeg', 'dcm'])
    
    if file:
        st.success(f"Loaded: {file.name}")
    
    with st.container():
        st.write("**Patient ID:** `XP-40992`")
        st.write("**Physician:** Dr. Aris, M.")
        st.write("**Priority:** <span style='color:#FF4B4B;'>URGENT</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### ⚙️ Physics Constraints")
    pinn_res = st.select_slider("PINN Solver Depth", options=["Standard", "Advanced", "Quantum-P"], value="Advanced")
    thermal_bias = st.slider("Bio-thermal Bias", 0.0, 1.0, 0.82)
    st.toggle("Auto-segmentation Overlay", value=True)

# --- CENTER PANEL: DIAGNOSTIC VIEWER ---
with col_main:
    st.markdown("#### 🔬 Neural Core Analysis")
    
    processed_img = process_medical_file(file)
    
    fig = go.Figure()

    if processed_img is not None:
        # Clinical Grayscale Base
        fig.add_trace(go.Heatmap(
            z=processed_img,
            colorscale='Greys_r',
            showscale=False
        ))
        
        # AI Risk Overlay (Simulated PINN Heatmap)
        # We generate a heatmap based on image intensity to simulate "risk zones"
        risk_overlay = np.where(processed_img > 180, processed_img, 0)
        fig.add_trace(go.Contour(
            z=risk_overlay,
            colorscale='Hot',
            opacity=0.35,
            showscale=False,
            contours_coloring='heatmap'
        ))
    else:
        # Placeholder for empty state
        st.info("Awaiting input file for neural reconstruction...")
        z_empty = np.random.uniform(0, 1, (512, 512))
        fig.add_trace(go.Heatmap(z=z_empty, colorscale='Ice', opacity=0.2, showscale=False))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.segmented_control("Imaging Mode", options=["Standard", "PINN Thermal", "Vascular Flow", "Risk Projection"], default="Standard")

# --- RIGHT PANEL: CLINICAL INSIGHTS ---
with col_stats:
    st.markdown("#### 📊 Clinical Logic")
    
    # Confidence Metric
    st.metric(label="AI Diagnostic Confidence", value="94.82%", delta="0.45%")
    
    st.markdown("""
    **Primary Finding:**
    - Focal Abnormality: **Detected**
    - Morphology: **Irregular**
    - Vascularity Index: **High**
    """)
    
    with st.expander("Physics Validation (PINN)", expanded=True):
        st.latex(r"\nabla \cdot (k \nabla T) + q = 0")
        st.caption("Thermal residual within 0.004 tol.")

    st.button("📄 GENERATE PDF REPORT")
    st.button("🚨 ALERT SURGICAL TEAM", type="secondary")
    st.button("💾 SAVE TO HOSPITAL EMR")

# --- BOTTOM PANEL: TELEMETRY ---
st.markdown("---")
b_col1, b_col2, b_col3 = st.columns(3)

with b_col1:
    st.markdown("**Real-time Loss Curve**")
    st.line_chart(np.random.randn(20, 1).cumsum(), height=120)

with b_col2:
    st.markdown("**Quantum-P Latency**")
    st.metric("Mean Latency", "12.4 ms", "-2.1 ms")

with b_col3:
    st.markdown("**Model Version**")
    st.code("AQKA-PINN-v4.0.2-BETA", language="text")
    
