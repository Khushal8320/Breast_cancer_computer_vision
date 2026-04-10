# 🎗️ MedScan AI — Breast Cancer Detection App

A production-level Streamlit application for breast cancer awareness and
AI-powered screening using your trained ResNet-18 model.

---

## 📁 Project Structure

```
breast_cancer_app/
├── app.py                  ← Entry point (run this)
├── model_utils.py          ← Model loading & inference logic
├── requirements.txt        ← Python dependencies
├── pages/
│   ├── 1_🏠_Home.py        ← Breast cancer education & awareness page
│   └── 2_🔬_Detection.py   ← AI image upload & detection page
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

The browser will open automatically at `http://localhost:8501`.

---

## 🧠 Using the Detection Page

1. **Load your model** — Upload `breast_cancer_model_final_kp.pth` (or any `.pkl`).
2. **Upload an image** — Accepted formats: PNG, JPG, JPEG, BMP, TIFF.
3. **Click "Run Analysis"** — The AI will return:
   - Prediction label (Normal / Cancer Detected)
   - Confidence score
   - Probability bar for each class

---

## 🔬 Model Details

| Property       | Value                          |
|---------------|-------------------------------|
| Architecture  | ResNet-18 (Transfer Learning) |
| Input size    | 224 × 224 px                  |
| Classes       | 0 = Normal · 1 = Cancer       |
| Weights file  | `.pth` state_dict or `.pkl`   |
| Normalisation | ImageNet mean/std             |

---

## ⚕️ Medical Disclaimer

This tool is for **educational and research purposes only**.  
It is **not** a substitute for professional medical advice, diagnosis, or treatment.  
Always consult a qualified healthcare provider for medical concerns.
