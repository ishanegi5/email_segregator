import streamlit as st
import json
import time
import pandas as pd
from datetime import datetime

# ── Backend imports (unchanged) ───────────────────────────────────────────────
from classifier import classify_email
from extractors import extract_tonnage, extract_vc, extract_tc

# ── Sample emails (for quick-fill buttons) ────────────────────────────────────
from sample_emails import TONNAGE_EMAIL, VC_EMAIL, TC_EMAIL

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="ShipMind AI",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — dark SaaS dashboard theme
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0f1117;
    --surface:   #181c27;
    --border:    #252a38;
    --accent:    #4f8ef7;
    --accent2:   #38d9a9;
    --warn:      #f5a623;
    --danger:    #ff6b6b;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --card:      #1a1f2e;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1200px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text) !important;
}

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0f1117 0%, #1a2340 60%, #0d1b2a 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(79,142,247,0.15), transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #fff;
    margin: 0 0 0.4rem 0;
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: rgba(79,142,247,0.15);
    color: var(--accent);
    border: 1px solid rgba(79,142,247,0.3);
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ── Metric cards ── */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 140px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    text-align: center;
}
.metric-card .num {
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    font-family: 'DM Mono', monospace;
    line-height: 1;
}
.metric-card .label {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Section headers ── */
.section-header {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.8rem 0 0.7rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Category badge ── */
.cat-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border-radius: 8px;
    padding: 6px 16px;
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.cat-TONNAGE   { background: rgba(79,142,247,0.15); color: #4f8ef7; border: 1px solid rgba(79,142,247,0.3); }
.cat-CARGO_VC  { background: rgba(56,217,169,0.15); color: #38d9a9; border: 1px solid rgba(56,217,169,0.3); }
.cat-CARGO_TC  { background: rgba(245,166,35,0.15);  color: #f5a623; border: 1px solid rgba(245,166,35,0.3); }

/* ── Data field cards ── */
.field-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.9rem; margin-top: 0.8rem; }
.field-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
}
.field-card .fkey {
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
}
.field-card .fval {
    font-size: 0.95rem;
    color: var(--text);
    font-family: 'DM Mono', monospace;
    font-weight: 500;
    word-break: break-word;
}
.field-card .fval.null { color: var(--muted); font-style: italic; font-family: 'DM Sans', sans-serif; }

/* ── Text area ── */
textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.88rem !important;
}
textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; }

/* ── History table ── */
.history-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.88rem;
}
.history-row .ts { color: var(--muted); font-family: 'DM Mono', monospace; font-size: 0.78rem; min-width: 90px; }
.history-row .snippet { flex: 1; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: var(--surface) !important; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 7px !important; color: var(--muted) !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"] { background: var(--card) !important; color: var(--text) !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 10px !important;
}

/* ── Footer ── */
.footer {
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    text-align: center;
    font-size: 0.8rem;
    color: var(--muted);
}
.footer a { color: var(--accent); text-decoration: none; }

/* ── Notification banners ── */
.notif-success {
    background: rgba(56,217,169,0.1);
    border: 1px solid rgba(56,217,169,0.3);
    color: #38d9a9;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}
.notif-error {
    background: rgba(255,107,107,0.1);
    border: 1px solid rgba(255,107,107,0.3);
    color: #ff6b6b;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

/* ── Selectbox / misc inputs ── */
[data-testid="stSelectbox"] > div { background: var(--card) !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "history" not in st.session_state:
    st.session_state.history = []       # list of dicts
if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🚢 ShipMind AI")
    st.markdown("<div style='color:#6b7280;font-size:0.8rem;margin-top:-0.6rem;margin-bottom:1.4rem;'>Shipping Intelligence Platform</div>", unsafe_allow_html=True)

    # Navigation
    page = st.radio(
        "Navigation",
        ["🔍 Analyze Email", "📋 History", "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Quick-fill section
    st.markdown("**⚡ Quick Examples**")
    st.caption("Load a sample email instantly")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⚓", help="Tonnage email"):
            st.session_state.quick_fill = TONNAGE_EMAIL
    with col2:
        if st.button("📦", help="Cargo VC email"):
            st.session_state.quick_fill = VC_EMAIL
    with col3:
        if st.button("⏱️", help="Cargo TC email"):
            st.session_state.quick_fill = TC_EMAIL

    st.markdown("---")

    # Stats panel
    total = len(st.session_state.history)
    tonnage_count = sum(1 for h in st.session_state.history if h["category"] == "TONNAGE")
    vc_count      = sum(1 for h in st.session_state.history if h["category"] == "CARGO_VC")
    tc_count      = sum(1 for h in st.session_state.history if h["category"] == "CARGO_TC")

    st.markdown("**📊 Session Stats**")
    st.markdown(f"""
    <div style='font-size:0.85rem;line-height:2;'>
      <span style='color:#6b7280;'>Total Processed</span> &nbsp;<b style='color:#4f8ef7;'>{total}</b><br>
      <span style='color:#6b7280;'>Tonnage</span> &nbsp;<b style='color:#4f8ef7;'>{tonnage_count}</b><br>
      <span style='color:#6b7280;'>Cargo VC</span> &nbsp;<b style='color:#38d9a9;'>{vc_count}</b><br>
      <span style='color:#6b7280;'>Cargo TC</span> &nbsp;<b style='color:#f5a623;'>{tc_count}</b>
    </div>
    """, unsafe_allow_html=True)

    if total > 0:
        st.markdown("---")
        # Export full session CSV
        df_all = pd.DataFrame([
            {"timestamp": h["timestamp"], "category": h["category"], **h["data"]}
            for h in st.session_state.history
        ])
        st.download_button(
            "⬇ Export Session CSV",
            data=df_all.to_csv(index=False),
            file_name="shipmind_session.csv",
            mime="text/csv",
            use_container_width=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE — ANALYZE EMAIL
# ══════════════════════════════════════════════════════════════════════════════
if page == "🔍 Analyze Email":

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">🤖 AI-Powered NLP</div>
      <div class="hero-title">Shipping Email Intelligence</div>
      <p class="hero-sub">Instantly classify and extract structured data from raw shipping emails — Tonnage, Cargo VC, and Cargo TC.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input section ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📨 Email Input</div>', unsafe_allow_html=True)

    input_tab, upload_tab = st.tabs(["✏️  Paste Email", "📁  Upload .txt File"])

    with input_tab:
        # Pre-fill from quick-fill buttons
        prefill = st.session_state.get("quick_fill", "")
        email_text = st.text_area(
            "Paste your shipping email below",
            value=prefill,
            height=200,
            placeholder="Paste the raw shipping email text here…",
            label_visibility="collapsed",
        )
        # Clear the quick-fill after use so it doesn't persist
        if prefill:
            st.session_state.quick_fill = ""

    with upload_tab:
        uploaded = st.file_uploader("Upload a .txt email file", type=["txt"])
        if uploaded:
            email_text = uploaded.read().decode("utf-8")
            st.markdown('<div class="notif-success">✅ File loaded successfully.</div>', unsafe_allow_html=True)
            st.code(email_text, language="text")

    # ── Process button ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([2, 1.5, 2])
    with btn_col:
        process = st.button("🔍 Analyze Email", use_container_width=True, type="primary")

    # ── Processing logic ──────────────────────────────────────────────────────
    if process:
        if not email_text or not email_text.strip():
            st.markdown('<div class="notif-error">⚠️ Please paste or upload an email before analyzing.</div>', unsafe_allow_html=True)
        else:
            # Loading spinner while running backend
            with st.spinner("Classifying and extracting data…"):
                time.sleep(0.4)  # slight visual delay for UX polish

                # ── BACKEND LOGIC (unchanged) ──────────────────────────────
                category = classify_email(email_text)

                if category == "TONNAGE":
                    data = extract_tonnage(email_text)
                elif category == "CARGO_VC":
                    data = extract_vc(email_text)
                else:
                    data = extract_tc(email_text)
                # ── END BACKEND LOGIC ──────────────────────────────────────

            # Save to session history
            record = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "category": category,
                "data": data,
                "raw": email_text,
            }
            st.session_state.history.insert(0, record)
            st.session_state.last_result = record

            st.markdown('<div class="notif-success">✅ Analysis complete!</div>', unsafe_allow_html=True)

    # ── Results display ───────────────────────────────────────────────────────
    if st.session_state.last_result:
        result = st.session_state.last_result
        category = result["category"]
        data     = result["data"]

        # Category badge
        icons = {"TONNAGE": "⚓", "CARGO_VC": "📦", "CARGO_TC": "⏱️"}
        labels = {"TONNAGE": "Tonnage", "CARGO_VC": "Cargo — Voyage Charter", "CARGO_TC": "Cargo — Time Charter"}
        icon = icons.get(category, "📧")
        label = labels.get(category, category)

        st.markdown('<div class="section-header">📌 Result</div>', unsafe_allow_html=True)

        col_cat, col_fields = st.columns([1, 2])
        with col_cat:
            st.markdown(f"""
            <div style='background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.4rem;text-align:center;'>
              <div style='font-size:2.2rem;margin-bottom:0.5rem;'>{icon}</div>
              <div style='font-size:0.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;'>Detected Category</div>
              <div class='cat-badge cat-{category}'>{icon} {label}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_fields:
            # Metric: fields found vs null
            found = sum(1 for v in data.values() if v is not None)
            total_fields = len(data)
            st.markdown(f"""
            <div class='metric-row'>
              <div class='metric-card'>
                <div class='num'>{total_fields}</div>
                <div class='label'>Fields Targeted</div>
              </div>
              <div class='metric-card'>
                <div class='num' style='color:var(--accent2);'>{found}</div>
                <div class='label'>Fields Extracted</div>
              </div>
              <div class='metric-card'>
                <div class='num' style='color:{"var(--danger)" if (total_fields-found)>0 else "var(--accent2)"};'>{total_fields - found}</div>
                <div class='label'>Not Found</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Extracted field cards
        st.markdown('<div class="section-header">🗂 Extracted Fields</div>', unsafe_allow_html=True)

        cards_html = '<div class="field-grid">'
        for key, val in data.items():
            display_key = key.replace("_", " ").title()
            if val:
                cards_html += f"""
                <div class='field-card'>
                  <div class='fkey'>{display_key}</div>
                  <div class='fval'>{val}</div>
                </div>"""
            else:
                cards_html += f"""
                <div class='field-card'>
                  <div class='fkey'>{display_key}</div>
                  <div class='fval null'>— not found</div>
                </div>"""
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

        # Download / export row
        st.markdown('<div class="section-header">⬇ Export</div>', unsafe_allow_html=True)
        col_j, col_c, _ = st.columns([1, 1, 2])

        json_str = json.dumps({"category": category, "extracted_data": data}, indent=2)
        with col_j:
            st.download_button(
                "⬇ Download JSON",
                data=json_str,
                file_name=f"shipmind_{category.lower()}_{datetime.now().strftime('%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )
        with col_c:
            df_single = pd.DataFrame([{"category": category, **data}])
            st.download_button(
                "⬇ Download CSV",
                data=df_single.to_csv(index=False),
                file_name=f"shipmind_{category.lower()}_{datetime.now().strftime('%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        # Raw JSON (collapsible)
        with st.expander("🔢 View Raw JSON"):
            st.code(json_str, language="json")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE — HISTORY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋 History":

    st.markdown("""
    <div class="hero" style="padding:1.8rem 2.5rem;">
      <div class="hero-title" style="font-size:1.8rem;">Processing History</div>
      <p class="hero-sub">All emails analyzed in this session</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("No emails analyzed yet. Head to **🔍 Analyze Email** to get started.")
    else:
        icons = {"TONNAGE": "⚓", "CARGO_VC": "📦", "CARGO_TC": "⏱️"}

        for i, rec in enumerate(st.session_state.history):
            icon = icons.get(rec["category"], "📧")
            snippet = rec["raw"][:80].replace("\n", " ").strip() + "…"
            st.markdown(f"""
            <div class='history-row'>
              <span class='ts'>{rec['timestamp']}</span>
              <span class='cat-badge cat-{rec["category"]}' style='font-size:0.78rem;padding:3px 10px;'>{icon} {rec['category']}</span>
              <span class='snippet'>{snippet}</span>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"View details — Entry #{len(st.session_state.history) - i}"):
                st.json({"category": rec["category"], "extracted_data": rec["data"]})


# ══════════════════════════════════════════════════════════════════════════════
# PAGE — ABOUT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "ℹ️ About":

    st.markdown("""
    <div class="hero">
      <div class="hero-badge">Open Source Project</div>
      <div class="hero-title">About ShipMind AI</div>
      <p class="hero-sub">An AI-powered shipping email intelligence tool built with Python, Scikit-learn, and Streamlit.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🛠 Tech Stack")
        for item in [
            ("🐍", "Python 3.x", "Core language"),
            ("🤖", "Scikit-learn", "Naive Bayes ML classifier"),
            ("🔍", "Regex / NLP", "Information extraction"),
            ("📊", "Pandas", "Data export & CSV"),
            ("🎨", "Streamlit", "Frontend UI"),
        ]:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:0.8rem;background:var(--card);border:1px solid var(--border);
            border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.5rem;'>
              <span style='font-size:1.3rem;'>{item[0]}</span>
              <div>
                <div style='font-weight:600;font-size:0.9rem;'>{item[1]}</div>
                <div style='color:var(--muted);font-size:0.78rem;'>{item[2]}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📌 Email Categories")
        for cat, icon, desc in [
            ("TONNAGE", "⚓", "Vessel availability announcements — name, port, DWT, type"),
            ("CARGO_VC", "📦", "Voyage charter cargo offers — cargo, load/discharge ports, laycan"),
            ("CARGO_TC", "⏱️", "Time charter requests — delivery, redelivery, duration"),
        ]:
            st.markdown(f"""
            <div style='background:var(--card);border:1px solid var(--border);border-radius:8px;
            padding:0.9rem 1rem;margin-bottom:0.5rem;'>
              <div style='font-weight:600;margin-bottom:0.3rem;'>{icon} {cat}</div>
              <div style='color:var(--muted);font-size:0.85rem;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 🚀 How to Run")
    st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  Built with ❤️ using Python · Scikit-learn · Streamlit &nbsp;|&nbsp;
  <b>ShipMind AI</b> — Shipping Email Intelligence Platform
</div>
""", unsafe_allow_html=True)
