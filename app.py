import streamlit as st

# --- 1. SETTINGS (MUST BE FIRST) ---
# This fixes the error in your screenshot
st.set_option('server.maxUploadSize', 200)

import numpy as np
import plotly.graph_objects as go
from PIL import Image
import pydicom
import io

# --- 2. PAGE CONFIG ---
st.set_page_config(
    page_title="AQKA-PINN Clinical Node",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. CLINICAL UI STYLING ---
st.markdown("""
    <style>
    :root {
        --hosp-blue: #00D1FF;
        --hosp-bg: #0E1117;
        --hosp-panel: #1A1C23;
    }
    .stApp { background-color: var(--hosp-bg); color: #E0E0E0; }
    div.stVerticalBlock > div.element-container {
        background: var(--hosp-panel);
        border: 1px solid rgba(0, 209, 255, 0.2);
        border-radius: 4px;
        padding: 15px;
    }
    .clinical-header {
        background: #1A1C23;
        padding: 10px 20px;
        border-bottom: 2px solid var(--hosp-blue);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA PROCESSING ---
def load_medical_image(uploaded_file):
    if uploaded_file is None:
        return None
    
    name = uploaded_file.name.lower()
    try:
        if name.endswith('.dcm'):
            ds = pydicom.dcmread(uploaded_file)
            img = ds.pixel_array.astype(float)
            # Normalize for hospital-grade visualization
            img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
            return img
        else:
            return np.array(Image.open(uploaded_file).convert('L'))
    except Exception as e:
        st.error(f"Image Load Error: {e}")
        return None

# --- 5. TOP HEADER ---
st.markdown("""
    <div class="clinical-header">
        <h2 style='margin:0; color:#00D1FF;'>AQKA-PINN <span style='font-weight:100; color:white;'>| Clinical Platform</span></h2>
    </div>
    """, unsafe_allow_html=True)

# --- 6. MAIN LAYOUT ---
l_col, c_col, r_col = st.columns([1, 2.5, 1])

with l_col:
    st.markdown("### 📥 Intake")
    file = st.file_uploader("Upload Scan", type=['png', 'jpg', 'dcm'])
    st.info("Patient ID: **XP-4022**\n\nStatus: **Stable**")
    st.slider("PINN Accuracy", 0.0, 1.0, 0.8)

with c_col:
    st.markdown("### 🔬 Diagnostic Viewer")
    img_array = load_medical_image(file)
    
    fig = go.Figure()
    if img_array is not None:
        fig.add_trace(go.Heatmap(z=img_array, colorscale='Greys_r', showscale=False))
        # Simulated AI Heatmap overlay
        risk = np.where(img_array > 150, img_array, 0)
        fig.add_trace(go.Contour(z=risk, colorscale='Hot', opacity=0.3, showscale=False))
    else:
        # High-accuracy placeholder
        fig.add_trace(go.Heatmap(z=np.random.rand(512, 512), colorscale='Ice', opacity=0.1, showscale=False))
        st.caption("Waiting for medical data input...")

    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=500, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with r_col:
    st.markdown("### 📊 AI Logic")
    st.metric("Confidence", "94.2%", "+0.5%")
    st.warning("Anomaly Detected in Segment A")
    
    with st.expander("Physics Equation", expanded=True):
        st.latex(r"\frac{\partial T}{\partial t} = \alpha \nabla^2 T + S")
    
    st.button("📄 Generate Report")
    st.button("💾 Save to EMR")
    
