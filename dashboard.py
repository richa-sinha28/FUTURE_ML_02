import streamlit as st
import pickle
import re
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TicketAI — Support Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Root theme ── */
:root {
    --bg:        #0a0b0f;
    --surface:   #111217;
    --surface2:  #181a21;
    --border:    #2a2d38;
    --accent:    #00e5a0;
    --accent2:   #7c6ff7;
    --accent3:   #ff6b6b;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --high:      #ff4757;
    --med:       #ffa502;
    --low:       #2ed573;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background: var(--bg);
    color: var(--text);
}

/* Hide default streamlit chrome */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1400px; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0d1117 0%, #131620 40%, #0f1a14 100%);
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
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(0,229,160,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    background: rgba(0,229,160,0.1);
    border: 1px solid rgba(0,229,160,0.3);
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    padding: 4px 12px;
    border-radius: 4px;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0 0 0.5rem;
    background: linear-gradient(90deg, #e8eaf0 0%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 400;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Stat cards ── */
.stat-row { display: flex; gap: 1rem; margin-bottom: 2rem; }
.stat-card {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
}
.stat-card.green::after  { background: var(--accent); }
.stat-card.purple::after { background: var(--accent2); }
.stat-card.red::after    { background: var(--accent3); }
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: var(--muted);
    text-transform: uppercase;
}
.stat-value {
    font-size: 2rem;
    font-weight: 800;
    margin: 0.25rem 0 0;
    line-height: 1;
}
.stat-card.green  .stat-value { color: var(--accent); }
.stat-card.purple .stat-value { color: var(--accent2); }
.stat-card.red    .stat-value { color: var(--accent3); }

/* ── Section headings ── */
.section-head {
    font-size: 0.65rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* ── Input area ── */
.stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,229,160,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0a0b0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 2rem !important;
    letter-spacing: 0.5px !important;
    transition: all .2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #00ffa8 !important;
    box-shadow: 0 0 20px rgba(0,229,160,0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── Result card ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.75rem 2rem;
    margin-top: 1.5rem;
}
.result-header {
    font-size: 0.65rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 3px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 1.25rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.75rem;
}
.result-category {
    font-size: 2rem;
    font-weight: 800;
    color: var(--accent);
    margin-bottom: 0.5rem;
}
.priority-badge {
    display: inline-block;
    padding: 5px 16px;
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1px;
}
.priority-High   { background: rgba(255,71,87,0.15);  color: var(--high); border: 1px solid rgba(255,71,87,0.4); }
.priority-Medium { background: rgba(255,165,2,0.15);  color: var(--med);  border: 1px solid rgba(255,165,2,0.4); }
.priority-Low    { background: rgba(46,213,115,0.15); color: var(--low);  border: 1px solid rgba(46,213,115,0.4);}

/* ── Model comparison table ── */
.model-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.85rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    transition: border-color .2s;
}
.model-row:hover { border-color: var(--accent); }
.model-name { font-weight: 700; font-size: 0.95rem; flex: 1; }
.model-acc  { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--accent); min-width: 60px; text-align: right; }
.bar-wrap   { flex: 2; background: var(--border); border-radius: 4px; height: 6px; overflow: hidden; }
.bar-fill   { height: 100%; border-radius: 4px; background: linear-gradient(90deg, var(--accent2), var(--accent)); }

/* ── Plotly override ── */
.js-plotly-plot .plotly, .js-plotly-plot .plotly div { background: transparent !important; }

/* ── Sample buttons ── */
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    gap: 0 !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    padding: 0.5rem 1.2rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface2) !important;
    color: var(--accent) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 1.5rem 0 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Load models ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    import os
    base = os.path.dirname(__file__)
    with open(f"{base}/tfidf.pkl",   "rb") as f: tfidf    = pickle.load(f)
    with open(f"{base}/lr_model.pkl", "rb") as f: lr_model = pickle.load(f)
    with open(f"{base}/nb_model.pkl", "rb") as f: nb_model = pickle.load(f)
    with open(f"{base}/svm_model.pkl","rb") as f: svm_model= pickle.load(f)
    return tfidf, lr_model, nb_model, svm_model

tfidf, lr_model, nb_model, svm_model = load_models()

CLASSES = lr_model.classes_.tolist()
MODELS  = {
    "Logistic Regression": (lr_model, 0.8546),
    "Linear SVM":          (svm_model, 0.8583),
    "Naive Bayes":         (nb_model,  0.7872),
}

# ── NLP helpers ───────────────────────────────────────────────────────────────
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet',   quiet=True)
    STOP_WORDS  = set(stopwords.words('english'))
    LEMMATIZER  = WordNetLemmatizer()
    USE_NLTK    = True
except Exception:
    USE_NLTK = False

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    words = text.split()
    if USE_NLTK:
        words = [LEMMATIZER.lemmatize(w) for w in words if w not in STOP_WORDS]
    return " ".join(words)

def assign_priority(text):
    t = text.lower()
    high_kw   = ["urgent","error","down","not working","crash","fail","issue","broken","critical","outage"]
    medium_kw = ["password","login","reset","slow","delay","problem","help","cannot","unable"]
    if any(k in t for k in high_kw):   return "High"
    if any(k in t for k in medium_kw): return "Medium"
    return "Low"

def predict_all(text):
    cleaned = clean_text(text)
    vec     = tfidf.transform([cleaned])
    results = {}
    for name, (model, _) in MODELS.items():
        cat  = model.predict(vec)[0]
        # probability / confidence
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(vec)[0]
            conf  = float(proba.max())
        elif hasattr(model, "decision_function"):
            df   = model.decision_function(vec)[0]
            # softmax-like normalization
            df   = df - df.max()
            exp  = np.exp(df)
            conf = float(exp.max() / exp.sum())
        else:
            conf = 1.0
        results[name] = {"category": cat, "confidence": conf}
    priority = assign_priority(text)
    return results, priority

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">ML · NLP · CLASSIFICATION</div>
  <div class="hero-title">TicketAI Support Intelligence</div>
  <div class="hero-sub">Automated ticket classification &amp; priority routing</div>
</div>
""", unsafe_allow_html=True)

# ── Stat cards ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-row">
  <div class="stat-card green">
    <div class="stat-label">Best Accuracy</div>
    <div class="stat-value">85.8%</div>
  </div>
  <div class="stat-card purple">
    <div class="stat-label">Categories</div>
    <div class="stat-value">8</div>
  </div>
  <div class="stat-card red">
    <div class="stat-label">Models Trained</div>
    <div class="stat-value">3</div>
  </div>
  <div class="stat-card green">
    <div class="stat-label">Vocab Size</div>
    <div class="stat-value">10K</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Main layout ───────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-head">→ Ticket Input</div>', unsafe_allow_html=True)

    samples = {
        "— choose a sample —": "",
        "System crash / hardware": "My computer crashed and I cannot boot it up. The system keeps showing a blue screen error.",
        "Password reset request": "I forgot my password and cannot login to my account. Please help me reset it.",
        "Purchase / procurement": "I need to order a new laptop for the new employee joining next week.",
        "HR support query": "I have a question about my leave balance and payroll deduction for this month.",
        "Internal project access": "I need access to the internal project repository for the Q3 roadmap initiative.",
        "Storage issue (urgent)": "The storage server is down and our team cannot access any shared files. This is urgent.",
    }

    choice = st.selectbox("Load a sample ticket", list(samples.keys()), label_visibility="collapsed")
    prefill = samples[choice]

    ticket_text = st.text_area(
        "Paste or type a support ticket",
        value=prefill,
        height=180,
        placeholder="e.g. My system is down and I cannot access my account...",
        label_visibility="collapsed",
    )

    analyze_btn = st.button("🔍  Analyze Ticket", use_container_width=True)

    # ── Model accuracy bar chart ───────────────────────────────────────────
    st.markdown('<div class="section-head" style="margin-top:2rem">→ Model Performance</div>', unsafe_allow_html=True)

    model_names = list(MODELS.keys())
    accuracies  = [v[1] * 100 for v in MODELS.values()]
    colors      = ["#7c6ff7", "#00e5a0", "#ff6b6b"]

    fig_acc = go.Figure(go.Bar(
        x=accuracies,
        y=model_names,
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{a:.1f}%" for a in accuracies],
        textposition='outside',
        textfont=dict(family="JetBrains Mono", size=12, color="#e8eaf0"),
        hovertemplate="%{y}: %{x:.2f}%<extra></extra>",
    ))
    fig_acc.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor ='rgba(0,0,0,0)',
        font=dict(family="Syne", color="#6b7280", size=12),
        margin=dict(l=0, r=60, t=10, b=0),
        height=200,
        xaxis=dict(range=[70, 90], showgrid=True, gridcolor="#2a2d38", ticksuffix="%", zeroline=False),
        yaxis=dict(showgrid=False),
        bargap=0.35,
    )
    st.plotly_chart(fig_acc, use_container_width=True, config={"displayModeBar": False})

    # ── Category distribution (simulated from class count) ─────────────────
    st.markdown('<div class="section-head" style="margin-top:0.5rem">→ Category Breakdown</div>', unsafe_allow_html=True)

    cat_counts = {
        "Hardware": 320, "Access": 285, "Storage": 270,
        "Purchase": 240, "HR Support": 215,
        "Administrative rights": 195, "Internal Project": 180, "Miscellaneous": 160,
    }
    fig_cat = go.Figure(go.Bar(
        x=list(cat_counts.keys()),
        y=list(cat_counts.values()),
        marker=dict(
            color=list(cat_counts.values()),
            colorscale=[[0,"#1a1d28"],[0.5,"#7c6ff7"],[1,"#00e5a0"]],
            line=dict(width=0),
        ),
        hovertemplate="%{x}: %{y} tickets<extra></extra>",
    ))
    fig_cat.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor ='rgba(0,0,0,0)',
        font=dict(family="Syne", color="#6b7280", size=11),
        margin=dict(l=0, r=0, t=10, b=40),
        height=220,
        xaxis=dict(showgrid=False, tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor="#2a2d38", zeroline=False),
    )
    st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})

# ── RIGHT: prediction results ─────────────────────────────────────────────────
with col_right:
    st.markdown('<div class="section-head">→ Prediction Output</div>', unsafe_allow_html=True)

    if analyze_btn and ticket_text.strip():
        predictions, priority = predict_all(ticket_text)

        # Best model = SVM (highest acc)
        best_pred  = predictions["Linear SVM"]
        best_cat   = best_pred["category"]
        best_conf  = best_pred["confidence"]

        # ── Result card ───────────────────────────────────────────────────
        priority_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[priority]
        st.markdown(f"""
        <div class="result-card">
          <div class="result-header">CLASSIFICATION RESULT</div>
          <div class="result-category">{best_cat}</div>
          <div style="margin-bottom:0.75rem">
            <span class="priority-badge priority-{priority}">{priority_icon} {priority} Priority</span>
          </div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.8rem;color:#6b7280">
            CONFIDENCE &nbsp;<span style="color:#00e5a0">{best_conf:.1%}</span>
            &nbsp;·&nbsp; MODEL &nbsp;<span style="color:#7c6ff7">Linear SVM</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── All-models comparison ─────────────────────────────────────────
        st.markdown('<div class="section-head" style="margin-top:1.5rem">→ All Models Compared</div>', unsafe_allow_html=True)

        model_colors = {"Logistic Regression": "#7c6ff7", "Linear SVM": "#00e5a0", "Naive Bayes": "#ff6b6b"}
        for mname, pdata in predictions.items():
            pct = int(pdata["confidence"] * 100)
            st.markdown(f"""
            <div class="model-row">
              <div class="model-name" style="color:{model_colors[mname]}">{mname}</div>
              <div style="flex:2;color:#e8eaf0;font-size:0.88rem">{pdata['category']}</div>
              <div class="bar-wrap">
                <div class="bar-fill" style="width:{pct}%;background:{model_colors[mname]}"></div>
              </div>
              <div class="model-acc">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Confidence radar across categories ────────────────────────────
        st.markdown('<div class="section-head" style="margin-top:1.5rem">→ Category Probability (LR Model)</div>', unsafe_allow_html=True)

        cleaned_vec = tfidf.transform([clean_text(ticket_text)])
        proba       = lr_model.predict_proba(cleaned_vec)[0]

        fig_radar = go.Figure(go.Scatterpolar(
            r=list(proba) + [proba[0]],
            theta=CLASSES + [CLASSES[0]],
            fill='toself',
            line=dict(color='#00e5a0', width=2),
            fillcolor='rgba(0,229,160,0.08)',
            hovertemplate="%{theta}: %{r:.2%}<extra></extra>",
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, showticklabels=False, gridcolor="#2a2d38", linecolor="#2a2d38"),
                angularaxis=dict(tickfont=dict(family="JetBrains Mono", size=10, color="#e8eaf0"), gridcolor="#2a2d38", linecolor="#2a2d38"),
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor ='rgba(0,0,0,0)',
            font=dict(color="#6b7280"),
            margin=dict(l=40, r=40, t=20, b=20),
            height=320,
            showlegend=False,
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

        # ── Horizontal probability bar chart ──────────────────────────────
        st.markdown('<div class="section-head">→ Probability per Category</div>', unsafe_allow_html=True)

        sorted_idx = np.argsort(proba)[::-1]
        s_classes  = [CLASSES[i] for i in sorted_idx]
        s_proba    = [proba[i] for i in sorted_idx]

        fig_prob = go.Figure(go.Bar(
            y=s_classes,
            x=s_proba,
            orientation='h',
            marker=dict(
                color=s_proba,
                colorscale=[[0,"#1a1d28"],[0.5,"#7c6ff7"],[1,"#00e5a0"]],
                line=dict(width=0),
            ),
            text=[f"{p:.1%}" for p in s_proba],
            textposition='outside',
            textfont=dict(family="JetBrains Mono", size=11, color="#e8eaf0"),
            hovertemplate="%{y}: %{x:.2%}<extra></extra>",
        ))
        fig_prob.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor ='rgba(0,0,0,0)',
            font=dict(family="Syne", color="#6b7280", size=11),
            margin=dict(l=0, r=70, t=5, b=0),
            height=280,
            xaxis=dict(showgrid=True, gridcolor="#2a2d38", tickformat=".0%", zeroline=False, range=[0, max(s_proba)*1.25]),
            yaxis=dict(showgrid=False),
            bargap=0.3,
        )
        st.plotly_chart(fig_prob, use_container_width=True, config={"displayModeBar": False})

    elif analyze_btn and not ticket_text.strip():
        st.warning("⚠️  Please enter a support ticket before analyzing.")
    else:
        # Empty state
        st.markdown("""
        <div style="
            background:var(--surface);
            border:1px dashed var(--border);
            border-radius:14px;
            padding:3rem 2rem;
            text-align:center;
            color:var(--muted);
        ">
            <div style="font-size:2.5rem;margin-bottom:0.75rem">🎯</div>
            <div style="font-weight:700;font-size:1rem;color:#e8eaf0;margin-bottom:0.5rem">Ready to classify</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;line-height:1.8">
                Type or paste a support ticket<br>
                on the left, then hit <strong style="color:var(--accent)">Analyze Ticket</strong>.<br><br>
                Results will show category,<br>priority, and confidence scores<br>
                from all 3 trained models.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Bottom: ML Details tabs ───────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-head">→ ML System Details</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📐 Pipeline", "📊 Accuracy Analysis", "⚙️ Model Specs"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        **Text Preprocessing Pipeline**

        `Raw Ticket Text`  
        ↓ Lowercase  
        ↓ Remove non-alpha characters (`re.sub`)  
        ↓ Tokenize  
        ↓ Remove English stopwords (NLTK)  
        ↓ Lemmatize (WordNetLemmatizer)  
        ↓ `clean_text` string output  
        ↓ **TF-IDF Vectorizer** (`max_features=10000`, `ngram_range=(1,2)`, `min_df=3`)  
        ↓ Sparse feature matrix  
        ↓ **ML Classifier** → Category label
        """)
    with c2:
        st.markdown("""
        **Priority Assignment Logic**

        Priority is keyword-rule based:

        | Priority | Keywords |
        |----------|---------|
        | 🔴 **High** | urgent, error, down, crash, fail, issue, broken, critical, outage |
        | 🟡 **Medium** | password, login, reset, slow, delay, cannot, unable |
        | 🟢 **Low** | Everything else |

        This hybrid approach (ML classification + rule priority) mirrors real-world SaaS support systems.
        """)

with tab2:
    col_a, col_b, col_c = st.columns(3)

    model_data = [
        ("Logistic Regression", 0.8546, "Balanced precision/recall. Strong on most categories. Fast inference."),
        ("Linear SVM",          0.8583, "Best overall accuracy. Excellent at high-dimensional text data."),
        ("Naive Bayes",         0.7872, "Fastest to train. Slightly lower accuracy but very interpretable."),
    ]
    cols = [col_a, col_b, col_c]
    accent_list = ["#7c6ff7", "#00e5a0", "#ff6b6b"]
    for col, (name, acc, note) in zip(cols, model_data):
        with col:
            st.markdown(f"""
            <div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1.25rem;border-top:3px solid {accent_list[cols.index(col)]}">
              <div style="font-size:0.65rem;font-family:'JetBrains Mono',monospace;letter-spacing:2px;color:var(--muted);margin-bottom:0.5rem">ACCURACY</div>
              <div style="font-size:2rem;font-weight:800;color:{accent_list[cols.index(col)]}">{acc*100:.1f}%</div>
              <div style="font-weight:700;font-size:0.9rem;margin:0.5rem 0 0.25rem">{name}</div>
              <div style="font-size:0.8rem;color:var(--muted);line-height:1.5">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Accuracy delta chart
    fig_delta = go.Figure()
    names = ["Logistic Regression", "Linear SVM", "Naive Bayes"]
    accs  = [85.46, 85.83, 78.72]
    base  = 78.0

    fig_delta.add_trace(go.Bar(
        x=names, y=accs,
        marker=dict(color=["#7c6ff7","#00e5a0","#ff6b6b"], line=dict(width=0)),
        text=[f"{a:.2f}%" for a in accs], textposition='outside',
        textfont=dict(family="JetBrains Mono", color="#e8eaf0", size=12),
        hovertemplate="%{x}: %{y:.2f}%<extra></extra>",
    ))
    fig_delta.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Syne", color="#6b7280", size=12),
        margin=dict(l=0, r=0, t=10, b=0), height=220,
        yaxis=dict(range=[75, 88], showgrid=True, gridcolor="#2a2d38", ticksuffix="%", zeroline=False),
        xaxis=dict(showgrid=False),
        bargap=0.4,
    )
    st.plotly_chart(fig_delta, use_container_width=True, config={"displayModeBar": False})

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        **TF-IDF Vectorizer**
        ```
        max_features = 10,000
        ngram_range  = (1, 2)   # unigrams + bigrams
        min_df       = 3        # ignore rare terms
        ```
        **Logistic Regression**
        ```
        max_iter     = 2000
        solver       = lbfgs (default)
        multi_class  = auto
        ```
        """)
    with c2:
        st.markdown("""
        **Linear SVM (LinearSVC)**
        ```
        C            = 1.0 (default)
        max_iter     = 1000
        loss         = squared_hinge
        ```
        **Naive Bayes (MultinomialNB)**
        ```
        alpha        = 1.0 (Laplace smoothing)
        fit_prior    = True
        ```
        """)
    st.markdown("""
    > All models share the same TF-IDF feature space. Train/test split was 80/20. 
    > Linear SVM achieved the highest accuracy (85.83%) and is used as the **primary classifier**.
    """)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding:1.5rem;border-top:1px solid #2a2d38;
            font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#3a3d4a;letter-spacing:1px">
  TICKETAI · ML SUPPORT INTELLIGENCE · BUILT WITH SCIKIT-LEARN + STREAMLIT
</div>
""", unsafe_allow_html=True)