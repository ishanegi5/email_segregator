
# 🚢 ShipMind AI — Shipping Email Intelligence Platform

An AI-powered tool that classifies and extracts structured data from raw shipping emails, with a professional SaaS-grade Streamlit UI.

---

## 🎯 What It Does

Classifies shipping emails into three categories and extracts key fields:

| Category | Icon | Extracted Fields |
|---|---|---|
| **TONNAGE** | ⚓ | Vessel name, open port, vessel size, vessel type |
| **CARGO_VC** | 📦 | Cargo name, loading port, discharge port, laycan |
| **CARGO_TC** | ⏱️ | Delivery port, redelivery port, duration |

---

## ✨ Features

### AI / Backend
- ML classification via **Scikit-learn Naive Bayes**
- Regex-based information extraction
- JSON + CSV export
- Batch processing via `main.py`

### UI / UX (Professional SaaS Dashboard)
- 🌑 Dark theme — ChatGPT / Notion inspired
- 📌 Sidebar navigation with live session stats
- ⚡ Quick-fill example buttons (Tonnage, VC, TC)
- 📁 File upload support (`.txt`)
- 🔢 Extracted field cards with found/not-found indicators
- 📊 Metric cards (fields targeted / extracted / missing)
- ⬇ Download as JSON or CSV per analysis
- 📋 Session history with category badges
- 🔍 Raw JSON viewer (collapsible)
- 📱 Responsive layout

---

## 🛠 Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.x |
| ML | Scikit-learn (Naive Bayes + TF-IDF) |
| NLP | Regex |
| Data | Pandas |
| Frontend | Streamlit |

---

## 📦 Install

```bash
pip install -r requirements.txt
```

## 🚀 Run (Streamlit UI)

```bash
streamlit run app.py
```

## 🖥 Run (Batch / CLI)

```bash
python main.py
```
Place `.txt` email files inside an `emails/` folder. Results are saved to `output/` as JSON and `shipping_data.csv`.

---

## 📁 Project Structure

```
shipping_email_project/
│
├── app.py              ← Streamlit UI (main frontend)
├── classifier.py       ← ML email classifier (Naive Bayes)
├── extractors.py       ← Regex extraction logic
├── main.py             ← Batch CLI runner
├── sample_emails.py    ← Sample emails for quick-fill
├── utils.py            ← JSON save utility
├── requirements.txt
└── output/             ← JSON results saved here
```

---

## 📸 UI Preview

> Dark SaaS dashboard — 3-page navigation (Analyze · History · About), category badges, field cards, download buttons, session stats.

---

*Built with Python · Scikit-learn · Streamlit*

