"""
pages/1_🏠_Home.py
Professional healthcare-style home page for MedScan AI.
"""

import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MedScan AI | Breast Screening Support",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Shared CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global ─────────────────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: #F4F8FB;
}
[data-testid="stSidebar"] {
    background: #EAF2F7;
    border-right: 1px solid #DCE6EE;
}
.block-container {
    padding: 2rem 3rem;
    max-width: 1200px;
}

/* ── Hero Banner ────────────────────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0F6CBD 0%, #1E88E5 55%, #14B8A6 100%);
    border: 1px solid #BFD9EA;
    border-radius: 18px;
    padding: 3rem 3.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(30, 136, 229, 0.10);
}
.hero-banner::before {
    content: "🩺";
    position: absolute;
    right: 3rem;
    top: 2rem;
    font-size: 5rem;
    opacity: 0.12;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #FFFFFF;
    margin: 0 0 0.5rem 0;
    line-height: 1.2;
}
.hero-subtitle {
    font-size: 1.08rem;
    color: #EAF4FB;
    margin: 0;
    max-width: 760px;
}
.hero-pill {
    display: inline-block;
    background: rgba(255,255,255,0.16);
    color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.28);
    border-radius: 999px;
    padding: 0.35rem 1rem;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

/* ── Stat Cards ─────────────────────────────────────────────────────────── */
.stat-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.stat-card {
    flex: 1;
    min-width: 160px;
    background: #FFFFFF;
    border: 1px solid #DCE6EE;
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    text-align: center;
    box-shadow: 0 6px 20px rgba(15, 108, 189, 0.05);
}
.stat-number {
    font-size: 2rem;
    font-weight: 800;
    color: #0F6CBD;
}
.stat-label {
    font-size: 0.85rem;
    color: #6B7280;
    margin-top: 0.2rem;
}

/* ── Section Cards ──────────────────────────────────────────────────────── */
.section-card {
    background: #FFFFFF;
    border: 1px solid #DCE6EE;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 6px 20px rgba(15, 108, 189, 0.05);
}
.section-card h3 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1F2937;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-card p, .section-card li {
    color: #4B5563;
    font-size: 0.95rem;
    line-height: 1.7;
}

/* ── Risk / symptom tags ───────────────────────────────────────────────── */
.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.8rem;
}
.tag {
    background: #EFF6FB;
    border: 1px solid #D4E6F3;
    border-radius: 8px;
    padding: 0.35rem 0.85rem;
    font-size: 0.85rem;
    color: #0F6CBD;
}
.tag-red {
    border-color: #F3C2C2;
    color: #B42318;
    background: #FEF3F2;
}
.tag-green {
    border-color: #B7E4C7;
    color: #15803D;
    background: #F0FDF4;
}
.tag-pink {
    border-color: #BFD9EA;
    color: #0F6CBD;
    background: #EFF6FB;
}

/* ── Stage cards ───────────────────────────────────────────────────────── */
.stage-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
}
.stage-item {
    background: #F9FCFE;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    border-left: 4px solid;
    border: 1px solid #E3EDF5;
}
.stage-0 { border-color: #22C55E; }
.stage-1 { border-color: #1E88E5; }
.stage-2 { border-color: #F59E0B; }
.stage-3 { border-color: #F97316; }
.stage-4 { border-color: #EF4444; }
.stage-item strong {
    color: #1F2937;
    font-size: 0.95rem;
}
.stage-item p {
    color: #6B7280;
    font-size: 0.82rem;
    margin: 0.3rem 0 0 0;
}

/* ── Treatment cards ───────────────────────────────────────────────────── */
.treatment-card {
    background: #F9FCFE;
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid #E3EDF5;
}
.treatment-card p {
    color: #6B7280;
    font-size: 0.82rem;
    margin: 0.4rem 0 0 0;
}

/* ── CTA Box ───────────────────────────────────────────────────────────── */
.cta-box {
    background: linear-gradient(135deg, #EAF4FB, #DDF4F1);
    border: 1px solid #C9E7E2;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-top: 2rem;
}
.cta-box h3 {
    color: #1F2937;
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
}
.cta-box p {
    color: #4B5563;
    margin-bottom: 1.2rem;
}

/* ── Button ────────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #0F6CBD, #14B8A6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.4rem;
    font-weight: 600;
}
.stButton > button:hover {
    filter: brightness(1.05);
}

/* ── Footer text ───────────────────────────────────────────────────────── */
.medical-note {
    color: #6B7280;
    font-size: 0.8rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-pill">🏥 Clinical Screening Support</div>
  <h1 class="hero-title">AI-Assisted Breast Screening Platform</h1>
  <p class="hero-subtitle">
    MedScan AI combines clinical education, awareness, and AI-supported imaging
    analysis to support early breast screening in an accessible healthcare-style interface.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Global Stats ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-row">
  <div class="stat-card">
    <div class="stat-number">2.3M</div>
    <div class="stat-label">New cases worldwide per year</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">685K</div>
    <div class="stat-label">Deaths annually</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">99%</div>
    <div class="stat-label">5-year survival (Stage 0-1)</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">1 in 8</div>
    <div class="stat-label">Women affected in lifetime risk estimates</div>
  </div>
  <div class="stat-card">
    <div class="stat-number">~30%</div>
    <div class="stat-label">Mortality reduction with screening</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── What is Breast Cancer ─────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
  <h3>🔬 What is Breast Cancer?</h3>
  <p>
    Breast cancer is a disease in which cells in the breast grow abnormally and
    uncontrollably. It most commonly begins in the milk ducts
    (<em>ductal carcinoma</em>) or lobules (<em>lobular carcinoma</em>).
    These abnormal cells may form a tumor, invade nearby tissue, or spread to
    other parts of the body through the lymphatic system or bloodstream.
  </p>
  <p>
    Although it mainly affects women, it can also occur in men.
    Early identification, regular screening, and timely clinical follow-up are
    important for improving outcomes.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Types & Stages ────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="section-card" style="height:100%">
      <h3>🧬 Common Types</h3>
      <ul>
        <li><strong style="color:#0F6CBD;">Invasive Ductal Carcinoma (IDC)</strong> — the most common type.</li>
        <li><strong style="color:#14B8A6;">Ductal Carcinoma In Situ (DCIS)</strong> — non-invasive and confined to ducts.</li>
        <li><strong style="color:#F59E0B;">Invasive Lobular Carcinoma (ILC)</strong> — begins in the milk-producing lobules.</li>
        <li><strong style="color:#EF4444;">Triple-Negative Breast Cancer</strong> — more aggressive and harder to target hormonally.</li>
        <li><strong style="color:#22C55E;">HER2-Positive</strong> — associated with HER2 protein overexpression; targeted therapy may help.</li>
        <li><strong style="color:#7C3AED;">Inflammatory Breast Cancer</strong> — rare but fast progressing.</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="section-card" style="height:100%">
      <h3>📊 Stages of Breast Cancer</h3>
      <div class="stage-grid">
        <div class="stage-item stage-0">
          <strong>Stage 0</strong>
          <p>Non-invasive disease such as DCIS; highly treatable.</p>
        </div>
        <div class="stage-item stage-1">
          <strong>Stage I</strong>
          <p>Small localized tumor with limited spread.</p>
        </div>
        <div class="stage-item stage-2">
          <strong>Stage II</strong>
          <p>Larger tumor or nearby lymph node involvement.</p>
        </div>
        <div class="stage-item stage-3">
          <strong>Stage III</strong>
          <p>Locally advanced disease involving surrounding structures.</p>
        </div>
        <div class="stage-item stage-4">
          <strong>Stage IV</strong>
          <p>Metastatic disease that has spread to distant organs.</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Warning Signs ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
  <h3>⚠️ Warning Signs & Symptoms</h3>
  <p>Early breast cancer may not always cause pain. Key warning signs can include:</p>
  <div class="tag-row">
    <span class="tag tag-red">Lump or thickening in breast or underarm</span>
    <span class="tag tag-red">Change in breast shape or size</span>
    <span class="tag tag-red">Dimpling or puckering of skin</span>
    <span class="tag tag-red">Nipple inversion or unusual discharge</span>
    <span class="tag tag-red">Redness or scaling of nipple/breast skin</span>
    <span class="tag tag-red">Persistent localized breast pain</span>
    <span class="tag tag-red">Swelling in part of the breast</span>
    <span class="tag tag-red">Peeling or flaking skin changes</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Risk Factors / Preventive Measures ───────────────────────────────────────
col3, col4 = st.columns(2, gap="large")

with col3:
    st.markdown("""
    <div class="section-card">
      <h3>🔴 Risk Factors</h3>
      <div class="tag-row">
        <span class="tag tag-pink">Age over 50</span>
        <span class="tag tag-pink">BRCA1 / BRCA2 mutation</span>
        <span class="tag tag-pink">Family history</span>
        <span class="tag tag-pink">Dense breast tissue</span>
        <span class="tag tag-pink">Prior radiation exposure</span>
        <span class="tag tag-pink">Hormone replacement therapy</span>
        <span class="tag tag-pink">Obesity after menopause</span>
        <span class="tag tag-pink">Alcohol use</span>
        <span class="tag tag-pink">Late first pregnancy</span>
        <span class="tag tag-pink">Not breastfeeding</span>
        <span class="tag tag-pink">Early menstruation / late menopause</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="section-card">
      <h3>🟢 Preventive Measures</h3>
      <div class="tag-row">
        <span class="tag tag-green">Routine mammogram screening</span>
        <span class="tag tag-green">Breast self-awareness</span>
        <span class="tag tag-green">Healthy body weight</span>
        <span class="tag tag-green">Regular exercise</span>
        <span class="tag tag-green">Limit alcohol intake</span>
        <span class="tag tag-green">Breastfeeding when possible</span>
        <span class="tag tag-green">Avoid smoking</span>
        <span class="tag tag-green">Genetic counselling when needed</span>
        <span class="tag tag-green">Regular medical follow-up</span>
        <span class="tag tag-green">Balanced nutrition</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Screening Guidelines ──────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
  <h3>🩺 Screening Guidance</h3>
  <ul>
    <li><strong style="color:#0F6CBD;">Ages 20-39:</strong> Clinical breast exam based on risk profile and medical advice.</li>
    <li><strong style="color:#14B8A6;">Ages 40-44:</strong> May begin annual mammogram screening based on preference and risk.</li>
    <li><strong style="color:#F59E0B;">Ages 45-54:</strong> Annual mammograms are commonly recommended.</li>
    <li><strong style="color:#1E88E5;">Ages 55+:</strong> Mammograms every 1-2 years depending on clinical guidance and risk level.</li>
    <li><strong style="color:#EF4444;">High-risk individuals:</strong> Additional MRI and specialist consultation may be recommended.</li>
  </ul>
</div>
""", unsafe_allow_html=True)

# ── Treatment Overview ────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
  <h3>💊 Treatment Overview</h3>
  <p>Treatment depends on cancer type, stage, biomarkers, and individual patient factors. Common treatment approaches include:</p>
  <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap:0.8rem; margin-top:1rem;">
    <div class="treatment-card" style="border-top:3px solid #1E88E5;">
      <strong style="color:#0F6CBD;">Surgery</strong>
      <p>Lumpectomy or mastectomy to remove cancerous tissue.</p>
    </div>
    <div class="treatment-card" style="border-top:3px solid #7C3AED;">
      <strong style="color:#7C3AED;">Radiation Therapy</strong>
      <p>High-energy treatment used to destroy remaining cancer cells.</p>
    </div>
    <div class="treatment-card" style="border-top:3px solid #EF4444;">
      <strong style="color:#B42318;">Chemotherapy</strong>
      <p>Drug-based systemic treatment for rapidly dividing cells.</p>
    </div>
    <div class="treatment-card" style="border-top:3px solid #F59E0B;">
      <strong style="color:#B45309;">Hormone Therapy</strong>
      <p>Used for hormone receptor-positive cancers.</p>
    </div>
    <div class="treatment-card" style="border-top:3px solid #22C55E;">
      <strong style="color:#15803D;">Targeted Therapy</strong>
      <p>Treatments aimed at specific cancer markers such as HER2.</p>
    </div>
    <div class="treatment-card" style="border-top:3px solid #14B8A6;">
      <strong style="color:#0F766E;">Immunotherapy</strong>
      <p>Supports the immune system in identifying and fighting cancer cells.</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cta-box">
  <h3>🔬 Start AI-Based Image Screening</h3>
  <p>Upload a breast imaging sample to receive AI-assisted screening support for educational and research use.</p>
</div>
""", unsafe_allow_html=True)

if st.button("🚀 Go to AI Detection →", use_container_width=False, type="primary"):
    st.switch_page("pages/2_🔬_Detection.py")

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
---
<p class="medical-note">
⚕️ <strong>Medical Disclaimer:</strong> This platform is intended for
<strong>educational and research purposes only</strong>. It does not replace
professional medical advice, diagnosis, or treatment. Always consult a
qualified healthcare provider regarding medical concerns.
</p>
""", unsafe_allow_html=True)