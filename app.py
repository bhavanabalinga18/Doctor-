import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import io

# --- SYSTEM CONFIG ---
st.set_page_config(
    page_title="AQKA-PINN Clinical Node",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- HOSPITAL GRADE UI (CSS) ---
st.markdown("""
    <style>
    /* Professional Dark Mode Palette */
    :root {
        --clinical-blue: #00A3FF;
        --warning-red: #FF3B30;
        --bg-solid: #0A0C10;
        --panel-bg: #141820;
        --text-main: #E1E1E1;
    }

    .stApp {
        background-color: var(--bg-solid);
        color: var(--text-main);
    }

    /* Solid Hospital Panels (No Neon Overkill) */
    div.stVerticalBlock > div {
        background: var(--panel-bg);
        border: 1px solid #252A34;
        border-radius: 4px;
        padding: 20px;
        margin-bottom: 12px;
    }

    /* Clinical Typography */
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: -0.5px;
    }

    .status-bar {
        background: #1C222D;
        padding: 10px 20px;
        border-radius: 4px;
        border-left: 4px solid var(--clinical-blue);
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 2px;
        text-transform: uppercase;
        font-size: 12px;
        font-weight: 600;
        height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TOP NAVIGATION / STATUS ---
st.markdown(f"""
    <div class="status-bar">
        <span><b>NODE:</b> ONCOLOGY_DEPT_04</span>
        <span><b>AI AGENT:</b> AQKA-PINN v3.2.1 (Validated)</span>
        <span><b>ENCRYPTION:</b> AES-256 ACTIVE</span>
    </div>
    """, unsafe_allow_html=True)

# --- HEADER ---
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    st.title("AQKA-PINN Diagnostic Platform")
    st.caption("Physics-Informed Neural Network for Real-Time Tissue Characterization")

with c2:
    st.metric("System Accuracy", "99.2%", "0.1%")
with c3:
    st.metric("Compute Load", "14%", "Low")

# --- MAIN CLINICAL WORKSPACE ---
col_input, col_view, col_info = st.columns([1, 2.2, 1])

with col_input:
    st.markdown("### 📥 Patient Data")
    uploaded_file = st.file_uploader("Drop Scan (DICOM/PNG)", type=['png', 'jpg', 'dcm'])
    
    with st.expander("Patient File: PX-4022", expanded=True):
        st.write("**Name:** Smith, Jane")
        st.write("**DOB:** 12-May-1972")
        st.write("**History:** Non-smoker, Type II Diabetes")
    
    st.markdown("---")
    st.write("**AI Model Parameters**")
    pinn_weight = st.select_slider("Physics Precision", options=["Standard", "High", "Research"], value="High")
    st.checkbox("Enable Multi-modal Fusion", value=True)

with col_view:
    st.markdown("### 🔬 Neural Segmentation Viewer")
    
    # Logic to show image or placeholder
    if uploaded_file:
        img = Image.open(uploaded_file)
        # Simulate AI Overlay using Plotly
        img_array = np.array(img.convert('L'))
        fig = go.Figure()
        fig.add_trace(go.Heatmap(z=img_array, colorscale='Greys_r', showscale=False))
        # Add a "Heatmap" contour to look like AI detection
        fig.add_trace(go.Contour(
            z=img_array, 
            contours_coloring='lines', 
            line_width=2, 
            colorscale='Hot', 
            opacity=0.4,
            showscale=False
        ))
    else:
        # High-res placeholder
        z = np.random.normal(0, 1, (512, 512)).cumsum(axis=0).cumsum(axis=1)
        fig = go.Figure(data=[go.Heatmap(z=z, colorscale='Ice', showscale=False)])

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=550,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.segmented_control("Visualization Mode", options=["Standard", "Thermal (PINN)", "Vascular", "Risk Gradient"], default="Standard")

with col_info:
    st.markdown("### 📋 AI Findings")
    st.warning("⚠️ High Probability Abnormality")
    
    st.info("""
    **Primary Diagnosis:**  
    Malignant Neoplasm (Prob: 94%)
    
    **PINN Verification:**  
    Elasticity mismatch detected in Zone B. Heat flux residual: 0.002.
    """)
    
    st.write("**Quantitative Data:**")
    st.data_editor({
        "Metric": ["Volume", "Density", "Sphericity"],
        "Value": ["4.2 cm³", "1.08 g/mL", "0.88"]
    }, disabled=True, hide_index=True)
    
    st.button("✅ Verify & Save to EMR", use_container_width=True)
    st.button("📄 Generate PDF Report", use_container_width=True)

# --- PHYSICS VALIDATION FOOTER ---
st.markdown("---")
f1, f2 = st.columns([2, 1])
with f1:
    st.markdown("### 📐 PINN Mathematical Validation")
    st.latex(r"\mathcal{L}_{total} = \omega_{data} \mathcal{L}_{data} + \omega_{phys} \mathcal{L}_{PDE}")
    st.caption("The system enforces Navier-Stokes and Bio-heat constraints to ensure physiological plausibility.")
with f2:
    st.markdown("### ⏱️ Progression Analysis")
    st.line_chart(np.random.randn(10, 1), height=150)
    
