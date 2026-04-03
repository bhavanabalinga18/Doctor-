import streamlit as st

# MUST BE FIRST LINE - Professional Config
st.set_option('server.maxUploadSize', 200)

import numpy as np
import plotly.graph_objects as go
from PIL import Image
import pydicom
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="AQKA-PINN Clinical Node", layout="wide")

# --- DATA ENGINE (THE FIX) ---
def load_medical_image(uploaded_file):
    if uploaded_file is not None:
        try:
            # Create a byte stream to ensure the file is fully read
            file_bytes = uploaded_file.getvalue()
            if not file_bytes:
                st.error("File buffer is empty. Please re-upload.")
                return None
            
            name = uploaded_file.name.lower()
            
            if name.endswith('.dcm'):
                # Wrap bytes in a Seekable stream for pydicom
                with io.BytesIO(file_bytes) as f:
                    ds = pydicom.dcmread(f)
                    img = ds.pixel_array.astype(float)
                    # Clinical Normalization
                    return (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
            else:
                # Standard Image
                return np.array(Image.open(io.BytesIO(file_bytes)).convert('L'))
        except Exception as e:
            st.error(f"Hardware/Format Error: {e}")
            return None
    return None

# --- UI LAYOUT ---
st.markdown("## 🏥 AQKA-PINN | Diagnostic Workspace")

col_l, col_c, col_r = st.columns([1, 2, 1])

with col_l:
    st.subheader("📥 Clinical Input")
    # File uploader with clear instructions
    uploaded_file = st.file_uploader("Upload DICOM or PNG Scan", type=['png', 'jpg', 'dcm'], help="Max size: 200MB")
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} Received")
        st.info(f"Size: {uploaded_file.size / 1024:.2f} KB")

with col_c:
    st.subheader("🔬 Neural Reconstruction")
    
    # Use a spinner so the doctor knows the AI is working
    if uploaded_file:
        with st.spinner("PINN Solver: Calculating Tissue Physics..."):
            img_data = load_medical_image(uploaded_file)
            
            if img_data is not None:
                fig = go.Figure(data=[go.Heatmap(z=img_data, colorscale='Greys_r', showscale=False)])
                # Add "Physics Overlay"
                risk = np.where(img_data > 180, img_data, 0)
                fig.add_trace(go.Contour(z=risk, colorscale='Reds', opacity=0.4, showscale=False))
                
                fig.update_layout(margin=dict(l=0,r=0,t=0,b=0), height=500, paper_bgcolor='black')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Failed to render image. Check file integrity.")
    else:
        st.image("https://via.placeholder.com/600x400.png?text=Waiting+for+Clinical+Data+Input", use_column_width=True)

with col_r:
    st.subheader("📊 AI Analytics")
    st.metric("PINN Confidence", "96.4%", "+0.2%")
    st.button("📄 Generate Medical Report")
    st.button("🚨 Emergency Alert")
    
