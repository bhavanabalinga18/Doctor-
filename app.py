import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import pydicom

# --- 1. PAGE CONFIG (MUST BE THE VERY FIRST ST COMMAND) ---
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

# --- 3. MEDICAL IMAGE ENGINE ---
def load_medical_image(uploaded_file):
    if uploaded_file is None: return None
    try:
        if uploaded_file.name.lower().endswith('.dcm'):
            ds = pydicom.dcmread(uploaded_file)
            img = ds.pixel_array.astype(float)
            return (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
        else:
            return np.array(Image.open(uploaded_file).convert('L'))
    except Exception as e:
        st.error(f"Format Error: {e}")
        return None

# --- 4. HEADER ---
st.markdown('<div class="clinical-header"><h2 style="color:#00D1FF; margin:0;">AQKA-PINN | Clinical Platform</h2></div>', unsafe_allow_html=True)

# --- 5. DASHBOARD ---
l, c, r = st.columns([1, 2.5, 1])

with l:
    st.markdown("### 📥 Intake")
    file = st.file_uploader("Upload Scan", type=['png', 'jpg', 'dcm'])
    st.info("ID: PX-4022 | Age: 58")
    st.slider("Physics Accuracy", 0.0, 1.0, 0.85)

with c:
    st.markdown("### 🔬 Diagnostic Viewer")
    img = load_medical_image(file)
    fig = go.Figure()
    if img is not None:
        fig.add_trace(go.Heatmap(z=img, colorscale='Greys_r', showscale=False))
        # Simulated Anomaly Overlay
        risk = np.where(img > 170, img, 0)
        fig.add_trace(go.Contour(z=risk, colorscale='Hot', opacity=0.3, showscale=False))
    else:
        fig.add_trace(go.Heatmap(z=np.random.rand(50,50), colorscale='Ice', opacity=0.1, showscale=False))
    
    fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=500, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with r:
    st.markdown("### 📊 AI Logic")
    st.metric("Confidence", "94.8%", "+0.2%")
    st.error("ANOMALY DETECTED")
    with st.expander("Physics Validation"):
        st.latex(r"\nabla \cdot (k \nabla T) + q = 0")
    st.button("📄 GENERATE REPORT")
    st.button("💾 SAVE TO EMR")
    
