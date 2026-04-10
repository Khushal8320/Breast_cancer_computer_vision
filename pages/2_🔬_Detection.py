"""
pages/2_🔬_Detection.py
Breast cancer image evaluation page for MedScan AI.
Model is already loaded by app.py — this page gets it instantly from cache.
"""

import sys, os, io
import streamlit as st
from PIL import Image

# ── Import shared get_model() from app.py so cache is shared ─────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from model_utils import load_model, predict, CLASS_NAMES

MODEL_PATH = os.path.join(ROOT, "breast_cancer_model_final_kp.pth")

@st.cache_resource(show_spinner=False)   # same key as app.py → hits cache, no reload
def get_model():
    return load_model(MODEL_PATH)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MedScan AI | Detection",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #F4F8FB; }
[data-testid="stSidebar"]          { background: #EAF2F7; border-right: 1px solid #DCE6EE; }
.block-container                   { padding: 2rem 3rem; max-width: 1200px; }

.hero-banner {
    background: linear-gradient(135deg, #0F6CBD 0%, #1E88E5 55%, #14B8A6 100%);
    border-radius: 18px;
    padding: 2.4rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(30,136,229,0.12);
}
.hero-banner::before {
    content: "🔬";
    position: absolute; right: 3rem; top: 1.5rem;
    font-size: 5rem; opacity: 0.12;
}
.hero-pill {
    display: inline-block;
    background: rgba(255,255,255,0.18); color: #fff;
    border: 1px solid rgba(255,255,255,0.30); border-radius: 999px;
    padding: 0.3rem 1rem; font-size: 0.82rem; font-weight: 700;
    letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.8rem;
}
.hero-title { font-size: 2.2rem; font-weight: 800; color: #fff; margin: 0 0 0.4rem; }
.hero-sub   { font-size: 1rem; color: #EAF4FB; margin: 0; }

.panel {
    background: #fff; border: 1px solid #DCE6EE; border-radius: 16px;
    padding: 1.6rem 1.8rem; margin-bottom: 1.2rem;
    box-shadow: 0 6px 20px rgba(15,108,189,0.05);
}
.panel h3 {
    font-size: 1.1rem; font-weight: 700; color: #1F2937;
    margin: 0 0 0.8rem; display: flex; align-items: center; gap: 0.5rem;
}
.panel p { color: #4B5563; font-size: 0.92rem; line-height: 1.7; margin: 0; }

.result-box    { border-radius: 14px; padding: 1.6rem 2rem; text-align: center; border: 2px solid; margin-bottom: 1.2rem; }
.result-normal { background: #F0FDF4; border-color: #86EFAC; }
.result-cancer { background: #FEF2F2; border-color: #FCA5A5; }
.result-icon   { font-size: 3rem; margin-bottom: 0.3rem; }
.result-label  { font-size: 1.9rem; font-weight: 800; margin: 0; }
.result-conf   { font-size: 1rem; color: #6B7280; margin-top: 0.3rem; }

.prob-row   { display:flex; justify-content:space-between; margin-bottom:0.3rem; }
.prob-label { font-size:0.88rem; color:#374151; font-weight:600; }
.prob-val   { font-size:0.88rem; color:#6B7280; font-weight:600; }

.upload-hint {
    background: #EFF6FB; border: 2px dashed #7EC8E3; border-radius: 12px;
    padding: 0.9rem 1rem; text-align: center; color: #0F6CBD;
    font-size: 0.88rem; margin-bottom: 0.8rem;
}
.img-meta     { font-size:0.8rem; color:#6B7280; text-align:center; margin-top:0.4rem; }
.medical-note { color:#6B7280; font-size:0.8rem; text-align:center; }

.stButton > button {
    background: linear-gradient(135deg, #0F6CBD, #14B8A6);
    color: white; border: none; border-radius: 10px;
    padding: 0.65rem 1.4rem; font-weight: 600; font-size: 0.95rem;
}
.stButton > button:hover { filter: brightness(1.05); }
</style>
""", unsafe_allow_html=True)

# ── Get model from cache (loaded by app.py — zero wait time here) ─────────────
model = get_model()

# ── Session state: image bytes + result survive across reruns ─────────────────
for key, default in [("img_bytes", None), ("img_name", None), ("result", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-pill">🔬 AI Evaluation</div>
  <h1 class="hero-title">Breast Cancer Image Detection</h1>
  <p class="hero-sub">
    Upload a breast imaging scan, preview it at full quality,
    then run the AI analysis to get an instant prediction.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
left, right = st.columns([1, 1.2], gap="large")

# ════════════════════════════ LEFT ═══════════════════════════════════════════
with left:

    st.markdown("""
    <div class="panel">
      <h3>📁 Upload Scan Image</h3>
      <p>Supported formats: JPG, JPEG, PNG, BMP, TIFF</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-hint">
      Drag &amp; drop your image here, or click <strong>Browse files</strong>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload image",
        type=["jpg", "jpeg", "png", "bmp", "tiff", "tif"],
        label_visibility="collapsed",
    )

    # Save bytes immediately — survives the button-click rerun
    if uploaded is not None:
        raw = uploaded.read()
        if st.session_state.img_name != uploaded.name or st.session_state.img_bytes != raw:
            st.session_state.img_bytes = raw
            st.session_state.img_name  = uploaded.name
            st.session_state.result    = None   # clear old result for new image

    st.markdown("<br>", unsafe_allow_html=True)

    run = st.button(
        "🚀 Run AI Analysis",
        use_container_width=True,
        type="primary",
        disabled=(st.session_state.img_bytes is None),
    )

    if run:
        with st.spinner("🧠 Analysing image…"):
            pil = Image.open(io.BytesIO(st.session_state.img_bytes)).convert("RGB")
            st.session_state.result = predict(model, pil)

    if st.session_state.img_bytes is None:
        st.info("⬆️ Upload an image to enable analysis.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="panel" style="padding:1rem 1.4rem;">
      <h3 style="margin-bottom:0.3rem;">🤖 Model</h3>
      <p style="font-size:0.84rem; color:#0F6CBD; font-weight:600;">
        ResNet-18 &nbsp;·&nbsp; breast_cancer_model_final_kp.pth
      </p>
      <p style="font-size:0.78rem; color:#22C55E; font-weight:600; margin-top:0.4rem;">
        ✅ Loaded &amp; ready
      </p>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════ RIGHT ══════════════════════════════════════════
with right:

    if st.session_state.img_bytes is not None:
        pil_img = Image.open(io.BytesIO(st.session_state.img_bytes)).convert("RGB")
        w, h    = pil_img.size
        size_kb = len(st.session_state.img_bytes) / 1024

        # ── Full-quality image preview ─────────────────────────────────────
        st.markdown("""
        <div class="panel">
          <h3>🖼️ Uploaded Image — Full Quality</h3>
        </div>
        """, unsafe_allow_html=True)

        st.image(pil_img, use_container_width=True)
        st.markdown(
            f'<p class="img-meta">{st.session_state.img_name} &nbsp;·&nbsp; '
            f'{w} × {h} px &nbsp;·&nbsp; {size_kb:.1f} KB</p>',
            unsafe_allow_html=True,
        )

        mc = st.columns(3)
        mc[0].metric("Width",  f"{w} px")
        mc[1].metric("Height", f"{h} px")
        mc[2].metric("Size",   f"{size_kb:.1f} KB")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Prediction results ─────────────────────────────────────────────
        if st.session_state.result is not None:
            res       = st.session_state.result
            is_cancer = res["class_id"] == 1
            box_cls   = "result-cancer" if is_cancer else "result-normal"
            lbl_color = "#B42318"       if is_cancer else "#15803D"

            st.markdown(f"""
            <div class="result-box {box_cls}">
              <div class="result-icon">{res['icon']}</div>
              <p class="result-label" style="color:{lbl_color};">{res['label']}</p>
              <p class="result-conf">Confidence &nbsp;<strong>{res['confidence']:.2f}%</strong></p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="panel">
              <h3>📊 Probability Breakdown</h3>
            </div>
            """, unsafe_allow_html=True)

            for cid, cname in CLASS_NAMES.items():
                prob = res["probabilities"][cid]
                st.markdown(f"""
                <div class="prob-row">
                  <span class="prob-label">{cname}</span>
                  <span class="prob-val">{prob:.2f}%</span>
                </div>
                """, unsafe_allow_html=True)
                st.progress(prob / 100)

            if is_cancer:
                st.markdown("""
                <div style="background:#FEF2F2; border-left:4px solid #EF4444;
                    border-radius:8px; padding:1rem 1.2rem; margin-top:1rem;
                    color:#7F1D1D; font-size:0.88rem;">
                  <strong>⚠️ Note:</strong> Potential abnormality flagged.
                  For <strong>research &amp; educational use only</strong>.
                  Please consult a qualified radiologist or oncologist.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#F0FDF4; border-left:4px solid #22C55E;
                    border-radius:8px; padding:1rem 1.2rem; margin-top:1rem;
                    color:#14532D; font-size:0.88rem;">
                  <strong>✅ Note:</strong> No abnormality detected.
                  Continue routine screening as advised by your healthcare provider.
                  For <strong>research &amp; educational use only</strong>.
                </div>
                """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="panel" style="text-align:center; padding:3rem 2rem;">
              <p style="font-size:2.5rem; margin-bottom:0.5rem;">🧠</p>
              <p style="font-size:1rem; color:#6B7280;">
                Click <strong>Run AI Analysis</strong> to see the prediction.
              </p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="panel" style="text-align:center; padding:5rem 2rem;">
          <p style="font-size:3rem; margin-bottom:0.6rem;">🖼️</p>
          <p style="font-size:1.05rem; color:#6B7280;">
            Your image preview and AI prediction will appear here.
          </p>
        </div>
        """, unsafe_allow_html=True)

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
---
<p class="medical-note">
⚕️ <strong>Medical Disclaimer:</strong> For educational &amp; research purposes only.
Not a substitute for professional medical advice, diagnosis, or treatment.
</p>
""", unsafe_allow_html=True)