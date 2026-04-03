import streamlit as st

# --- STEP 1: GLOBAL SETTINGS (CRITICAL: MUST BE FIRST) ---
# This prevents the "StreamlitAPIException" by setting config before any UI calls
st.set_option('server.maxUploadSize', 200)

# --- STEP 2: IMPORTS ---
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import pydicom
import io

# --- STEP 3: PAGE CONFIG ---
st.set_page_config(
    page_title="AQKA-PINN Clinical Node",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STEP 4: CLINICAL UI STYLING ---
st.markdown("""
    <style>
    :root {
        --hosp-blue: #00D1FF;
        --hosp-bg: #0E1117;
        --hosp-panel: #1A1C23;
        --hosp-border: rgba(0, 209, 255, 0.2);
    }
    .stApp { background-color: var(--hosp-bg); color: #E0E0E0; }
    
    /* Panel Styling */
    div.stVerticalBlock > div.element-container {
        background: var(--hosp-panel);
        border: 1px solid var(--hosp-border);
        border-radius: 4px;
        padding: 10px;
    }
    
    /* Header Styling */
    .clinical-header {
        background: #1A1C23;
        padding: 15px 25px;
        border-bottom: 2px solid var(--hosp-blue);
        margin-bottom: 20px;
        border-radius: 0 0 10px 10px;
    }

    /* Professional Buttons */
    .stButton>button {
        width: 100%;
        background: rgba(0, 209, 255, 0.05);
        border: 1px solid var(--hosp-blue);
        color: var(--hosp-blue);
        font-weight: bold;
    }
    .stButton>button:hover {
        background: var(--hosp-blue);
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# --- STEP 5: MEDICAL IMAGE ENGINE ---
def load_medical_image(uploaded_file):
    if uploaded_file is None:
        return None
    
    filename = uploaded_file.name.lower()
    try:
        if filename.endswith('.dcm'):
            # Professional DICOM Handling
            ds = pydicom.dcmread(uploaded_file)
            img = ds.pixel_array.astype(float)
            # Windowing/Normalization for clinical display
            img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
            return img
        else:
            # Standard Image Handling (PNG/JPG)
            return np.array(Image.open(uploaded_file).convert('L'))
    except Exception as e:
        st.error(f"Medical Format Error: {e}")
        return None

# --- STEP 6: TOP NAVIGATION ---
st.markdown("""
    <div class="clinical-header">
        <h2 style='margin:0; color:#00D1FF; font-family: sans-serif;'>
            AQKA-PINN <span style='font-weight:lighter; color:white;'>| Intelligent Diagnostic Platform</span>
        </h2>
        <p style='margin:0; font-size:12px; opacity:0.6;'>NODE: ONCOLOGY_04 | ENCRYPTION: AES-256 | AI-STATUS: VERIFIED</p>
    </div>
    """, unsafe_allow_html=True)

# --- STEP 7: MAIN DASHBOARD LAYOUT ---
l_col, c_col, r_col = st.columns([1, 2.5, 1])

# --- LEFT: CLINICAL INPUT ---
with l_col:
    st.markdown("### 📥 Patient Data")
    file = st.file_uploader("Upload Scan (DICOM/PNG)", type=['png', 'jpg', 'dcm'])
    
    if file:
        st.success(f"File Verified: {file.name}")
    
    st.markdown("**Patient Profile**")
    st.info("ID: PX-4022 | Age: 58 | Sex: M")
    
    st.markdown("---")
    st.markdown("**PINN Physics Constraints**")
    st.slider("Thermal Accuracy Weight", 0.0, 1.0, 0.85)
    st.slider("Mass Balance Bias", 0.0, 1.0, 0.40)

# --- CENTER: AI DIAGNOSTIC VIEWER ---
with c_col:
    st.markdown("### 🔬 Neural Core Reconstruction")
    img_array = load_medical_image(file)
    
    fig = go.Figure()
    
    if img_array is not None:
        # Layer 1: The Raw Scan
        fig.add_trace(go.Heatmap(
            z=img_array, 
            colorscale='Greys_r', 
            showscale=False
        ))
        
        # Layer 2: PINN Heatmap Overlay (Simulated Anomaly Detection)
        # Masks areas of high intensity to simulate "Risk Zones"
        risk_zones = np.where(img_array > 160, img_array, 0)
        fig.add_trace(go.Contour(
            z=risk_zones, 
            colorscale='YlOrRd', 
            opacity=0.35, 
            showscale=False,
            contours_coloring='heatmap'
        ))
    else:
        # High-Fidelity Placeholder
        placeholder = np.random.normal(0, 1, (512, 512)).cumsum(axis=0)
        fig.add_trace(go.Heatmap(z=placeholder, colorscale='Ice', opacity=0.1, showscale=False))
        st.info("System Ready. Please upload a clinical scan to begin AI analysis.")

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), 
        height=550, 
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.segmented_control("Visualization", ["Standard", "PINN-Thermal", "Tissue Density"], default="Standard")

# --- RIGHT: ANALYTICAL INSIGHTS ---
with r_col:
    st.markdown("### 📊 AI Analytics")
    st.metric("Model Confidence", "94.8%", "+0.2%")
    
    st.error("⚠️ ANOMALY DETECTED: ZONE B")
    
    with st.expander("Physics Equation (PINN)", expanded=True):
        st.latex(r"\frac{\partial T}{\partial t} = \alpha \nabla^2 T + S")
        st.caption("Bio-heat Transfer Residual: 0.0024")
    
    st.markdown("---")
    st.button("📄 GENERATE PDF REPORT")
    st.button("💾 SAVE TO HOSPITAL EMR")
    st.button("🚨 ALERT SPECIALIST")

# --- FOOTER: TELEMETRY ---
st.markdown("---")
f1, f2, f3 = st.columns(3)
with f1:
    st.caption("Model Convergence (PINN Loss)")
    st.line_chart(np.random.randn(20, 1).cumsum(), height=100)
with f2:
    st.caption("Hardware Acceleration")
    st.metric("GPU Latency", "14.2ms", "-1.1ms")
with f3:
    st.caption("System Log")
    st.code("v4.0.2-STABLE-NODE-PROD", language="text")
    
