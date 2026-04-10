"""
app.py  ←  Entry point for MedScan AI.
Loads the AI model ONCE into the global cache before redirecting to Home.
Every subsequent page (Detection etc.) gets the model instantly from cache.

Run with:
    streamlit run app.py
"""

import os
import sys
import streamlit as st

st.set_page_config(
    page_title="MedScan AI — Breast Cancer Detection",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Allow model_utils import from project root ────────────────────────────────
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from model_utils import load_model

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "breast_cancer_model_final_kp.pth")

# ── Load model ONCE — cached globally for the lifetime of the server process ──
# Any page that calls get_model() gets the already-loaded model from RAM.
@st.cache_resource(show_spinner=False)
def get_model():
    return load_model(MODEL_PATH)

# Trigger the load now, while the splash/redirect screen is showing.
# All subsequent calls from any page return instantly from the cache.
with st.spinner("⏳ Starting MedScan AI — loading model…"):
    get_model()

# ── Global sidebar branding ───────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #F4F8FB; }
[data-testid="stSidebar"]          { background: #EAF2F7; border-right: 1px solid #DCE6EE; }

.brand-box {
    background: linear-gradient(135deg, #0F6CBD, #14B8A6);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.5rem;
    text-align: center;
}
.brand-icon  { font-size: 2.5rem; }
.brand-title { font-size: 1.15rem; font-weight: 800; color: #fff; margin: 0.4rem 0 0.2rem; }
.brand-sub   { font-size: 0.78rem; color: #E0F2FE; letter-spacing: 0.06em; text-transform: uppercase; }

[data-testid="stSidebarNav"] a {
    color: #374151 !important;
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    transition: background 0.2s;
}
[data-testid="stSidebarNav"] a:hover { background: #DBEAFE !important; color: #0F6CBD !important; }
[data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: #DBEAFE !important;
    color: #0F6CBD !important;
    font-weight: 600;
}

.sidebar-disclaimer {
    font-size: 0.73rem;
    color: #6B7280;
    text-align: center;
    margin-top: 2rem;
    line-height: 1.5;
    border-top: 1px solid #DCE6EE;
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="brand-box">
      <div class="brand-icon">🎗️</div>
      <div class="brand-title">MedScan AI</div>
      <div class="brand-sub">Breast Cancer Screening</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-disclaimer">
      For educational &amp; research use only.<br>
      Not a substitute for medical advice.
    </div>
    """, unsafe_allow_html=True)

# ── Redirect to Home ──────────────────────────────────────────────────────────
st.switch_page("pages/1_🏠_Home.py")