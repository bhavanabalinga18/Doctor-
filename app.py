import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AQKA-PINN Platform", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CORRECTED CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=Roboto+Mono:wght@300;500&display=swap');
    
    :root {
        --glass: rgba(10, 14, 20, 0.9);
        --cyan: #00F2FF;
        --border: rgba(0, 242, 255, 0.3);
    }

    .stApp {
        background: radial-gradient(circle at center, #0B1118 0%, #05070A 100%);
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphism Panels */
    div.stVerticalBlock > div {
        background: var(--glass);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0, 242, 255, 0.1);
        margin-bottom: 15px;
    }

    .status-text {
        font-family: 'Roboto Mono', monospace;
        color: var(--cyan);
        font-size: 0.85rem;
        letter-spacing: 1px;
    }

    [data-testid="stMetricValue"] {
        color: var(--cyan) !important;
        font-family: 'Roboto Mono', monospace;
    }
    
    .stButton>button {
        width: 100%;
        background: rgba(0, 242, 255, 0.05);
        color: var(--cyan);
        border: 1px solid var(--cyan);
        transition: 0.3s ease;
        text-transform: uppercase;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: var(--cyan);
        color: #000;
        box-shadow: 0 0 20px var(--cyan);
    }
    </style>
    """, unsafe_allow_html=True) # FIXED PARAMETER

# --- HEADER SECTION ---
col_h1, col_h2, col_h3 = st.columns([2.5, 1, 1])
with col_h1:
    st.markdown("<h1 style='margin:0; font-weight:700;'>AQKA-PINN <span style='color:#00F2FF;'>Intelligent Diagnostic Platform</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='status-text'>SYSTEM: ACTIVE | ENCRYPTED LINK: SECURE | MODE: CLINICAL AI</p>", unsafe_allow_html=True)

with col_h2:
    st.metric("AI Confidence", "94.2%", "+0.5%")
with col_h3:
    st.metric("Processing", "28ms", "-2ms")

st.markdown("<hr style='border: 1px solid rgba(0, 242, 255, 0.2);'>", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
left_col, center_col, right_col = st.columns([1, 2, 1])

# --- LEFT PANEL: CLINICAL INPUT ---
with left_col:
    st.markdown("### 📋 Clinical Input")
    st.file_uploader("Upload Diagnostic Scan", type=['png', 'jpg', 'jpeg', 'dcm'])
    
    with st.container():
        st.write("**Patient Metadata**")
        st.caption("ID: PX-4022 | Age: 62 | Sex: F")
        st.caption("Type: Contrast Enhanced CT")
    
    st.slider("Physics Constraint Weight (PINN)", 0.0, 1.0, 0.75)
    st.slider("Scanning Resolution", 128, 1024, 512)
    
    st.write("**Manual Annotation**")
    b1, b2 = st.columns(2)
    b1.button("Highlight")
    b2.button("Crosshair")

# --- CENTER PANEL: AI ANALYSIS ---
with center_col:
    st.markdown("### 🧠 Neural Core Visualization")
    
    # Generate dummy high-res medical heatmap
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2)/2) + 0.1 * np.random.normal(size=X.shape)
    
    fig = go.Figure(data=[go.Heatmap(
        z=Z, x=x, y=y,
        colorscale='IceFire',
        reversescale=True,
        showscale=False
    )])
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.multiselect("Active Layers", ["PINN Gradient", "Vascular Segmentation", "Density Map"], default=["PINN Gradient"])

# --- RIGHT PANEL: CLINICAL INSIGHTS ---
with right_col:
    st.markdown("### 📊 Clinical Insights")
    st.markdown("<div style='padding:10px; border-radius:5px; background:rgba(255, 49, 49, 0.2); border:1px solid #FF3131; color:#FF3131; text-align:center; font-weight:bold;'>CRITICAL ANOMALY DETECTED</div>", unsafe_allow_html=True)
    
    st.write("")
    st.markdown("""
    - **Detection:** Pulmonary Nodule
    - **Probability:** 91.8%
    - **Location:** Segment 4 (Upper Lobe)
    - **Estimated Size:** 12.4mm
    """)
    
    st.progress(0.91, text="Structural Risk Analysis")
    st.button("Export DICOM Report")
    st.button("Request Senior Review")

# --- BOTTOM PANEL: PHYSICS ---
st.markdown("<hr style='border: 1px solid rgba(0, 242, 255, 0.1);'>", unsafe_allow_html=True)
bot_l, bot_r = st.columns([2, 1])

with bot_l:
    st.markdown("### 🧬 PINN Governing Equations")
    st.latex(r"L(u) = f(x, t), \quad x \in \Omega, t \in [0, T]")
    st.latex(r"MSE_{pinn} = MSE_u + MSE_f + MSE_{bc}")
    st.caption("Minimizing physical residuals through deep neural operators.")

with bot_r:
    st.markdown("### 📈 Progression Forecast")
    chart_data = np.random.randn(20, 1).cumsum()
    st.line_chart(chart_data)
    
