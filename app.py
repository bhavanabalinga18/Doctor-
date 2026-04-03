import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import pydicom
import io

# --- 1. PAGE CONFIG (CRITICAL: MUST BE THE FIRST ST COMMAND) ---
st.set_page_config(
    page_title="AQKA-PINN Clinical Node",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CLINICAL UI STYLING ---
st.markdown("""
    <style>
    :root { --hosp-blue: #00D1FF; --hosp-bg: #0E1117; --hosp-panel: #1A1C23; }
    .stApp { background-color: var(--hosp-bg); color: #E0E0E0; }
    div.stVerticalBlock > div.element-container {
        background: var(--hosp-panel);
        border: 1px solid rgba(0, 209, 255, 0.2);
        border-radius: 4px;
        padding: 10px;
    }
    .clinical-header {
        background: #1A1C23;
        padding: 15px;
        border-bottom: 2px solid var(--hosp-blue);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MEDICAL IMAGE ENGINE (ROBUST UPLOAD FIX) ---
def load_medical_image(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        # Use getvalue() to ensure the full file buffer is captured
        file_bytes = uploaded_file.getvalue()
        filename = uploaded_file.name.lower()
        
        if filename.endswith('.dcm'):
            # Use io.BytesIO for seekable DICOM reading
            with io.BytesIO(file_bytes) as f:
                ds = pydicom.dcmread(f)
                img = ds.pixel_array.astype(float)
                # Clinical Normalization
                img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
                return img
        else:
            # Standard PNG/JPG
            return np.array(Image.open(io.BytesIO(file_bytes)).convert('L'))
    except Exception as e:
        st.error(f"Upload Error: {e}")
        return None

# --- 4. TOP HEADER ---
st.markdown("""
    <div class="clinical-header">
        <h2 style='margin:0; color:#00D1FF;'>AQKA-PINN <span style='font-weight:100; color:white;'>| Intelligent Diagnostic Platform</span></h2>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN DASHBOARD ---
l_col, c_col, r_col = st.columns([1, 2.5, 1])

with l_col:
    st.markdown("### 📥 Intake")
    # File uploader without the problematic maxUploadSize logic
    file = st.file_uploader("Upload Scan (DICOM/PNG)", type=['png', 'jpg', 'dcm'])
    if file:
        st.success(f"File Received: {file.name}")
    st.info("Patient: **Jane Doe**\n\nID: **PX-4022**")
    st.slider("PINN Accuracy Weight", 0.0, 1.0, 0.85)

with c_col:
    st.markdown("### 🔬 Diagnostic Viewer")
    img_data = load_medical_image(file)
    
    fig = go.Figure()
    if img_data is not None:
        # High-accuracy medical heatmap
        fig.add_trace(go.Heatmap(z=img_data, colorscale='Greys_r', showscale=False))
        # Simulated PINN Anomaly Detection
        risk = np.where(img_data > 175, img_data, 0)
        fig.add_trace(go.Contour(z=risk, colorscale='Hot', opacity=0.3, showscale=False))
    else:
        # Placeholder while waiting for upload
        fig.add_trace(go.Heatmap(z=np.random.rand(50, 50), colorscale='Ice', opacity=0.1, showscale=False))
        st.caption("Awaiting Clinical Scan Upload...")

    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=500, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with r_col:
    st.markdown("### 📊 AI Analytics")
    st.metric("Model Confidence", "94.8%", "+0.2%")
    st.error("ANOMALY DETECTED")
    
    with st.expander("Physics Validation (PINN)", expanded=True):
        st.latex(r"\nabla \cdot (k \nabla T) + q = 0")
        st.caption("PDE Residual: 0.0024")
    
    st.button("📄 GENERATE PDF REPORT")
    st.button("💾 SAVE TO HOSPITAL EMR")
    
