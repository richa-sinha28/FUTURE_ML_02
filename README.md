<div align="center">

# 🎯 TicketAI — Support Intelligence System

### Automated Customer Support Ticket Classification & Priority Routing

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://futureml02-nwy83g4rnrsmco6kf9ama2.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)




---

## 📌 Overview

Real-world customer support teams receive **hundreds of tickets daily** — billing issues, crashes, login problems, hardware failures. Manually sorting them is slow, error-prone, and delays critical resolutions.

**TicketAI** is an end-to-end Machine Learning system that:

- 📂 **Classifies** support tickets into 8 categories automatically
- 🚨 **Prioritizes** each ticket as High / Medium / Low
- 📊 **Compares** 3 ML models side-by-side with live confidence scores
- ⚡ **Deploys** as an interactive Streamlit web dashboard

> This is not a chatbot — it's a **decision-support system** used in real SaaS and IT operations.

---

## 🚀 Live Demo

👉 **[https://futureml02-nwy83g4rnrsmco6kf9ama2.streamlit.app/](https://futureml02-nwy83g4rnrsmco6kf9ama2.streamlit.app/)**

Paste any support ticket text and instantly get:
- Predicted category from all 3 models
- Priority level (High / Medium / Low)
- Confidence scores & probability radar chart

---

## 📊 Dashboard Preview

| Feature | Description |
|---|---|
| 🔍 **Ticket Analyzer** | Input any support ticket, get instant ML predictions |
| 🤖 **3-Model Comparison** | LR, SVM & Naive Bayes results side-by-side |
| 🕸️ **Radar Chart** | Probability distribution across all 8 categories |
| 📈 **Accuracy Bar Chart** | Visual model performance comparison |
| 📋 **Category Distribution** | Dataset class balance visualization |
| ⚙️ **ML Pipeline Details** | Full preprocessing → model → output breakdown |

---

## 🗂️ Ticket Categories

The system classifies tickets into **8 categories**:

| # | Category | Example Ticket |
|---|---|---|
| 1 | 💻 **Hardware** | "My laptop screen is cracked and won't turn on" |
| 2 | 🔐 **Access** | "I can't log into the company portal" |
| 3 | 🗄️ **Storage** | "The shared drive is full and inaccessible" |
| 4 | 🛒 **Purchase** | "Need to order 5 monitors for the new team" |
| 5 | 👥 **HR Support** | "Question about my payroll and leave balance" |
| 6 | 🔑 **Administrative rights** | "Need admin permissions for the dev server" |
| 7 | 📁 **Internal Project** | "Requesting access to the Q3 roadmap repo" |
| 8 | 🗒️ **Miscellaneous** | General queries not fitting other categories |

---

## 🚨 Priority Assignment

Priority is assigned using a keyword-rule system layered on top of ML classification:

```
🔴 HIGH    →  urgent, error, down, crash, fail, issue, broken, critical, outage
🟡 MEDIUM  →  password, login, reset, slow, delay, cannot, unable
🟢 LOW     →  everything else
```

This hybrid approach (ML + rules) mirrors production support systems used by real SaaS companies.

---

## 🧠 How It Works

### Full Pipeline

```
Raw Ticket Text
      │
      ▼
┌─────────────────────────────┐
│     Text Preprocessing      │
│  • Lowercase                │
│  • Remove special chars     │
│  • Tokenize                 │
│  • Remove stopwords (NLTK)  │
│  • Lemmatize (WordNet)      │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│     TF-IDF Vectorizer       │
│  • max_features = 10,000    │
│  • ngram_range  = (1, 2)    │
│  • min_df       = 3         │
└─────────────┬───────────────┘
              │
      ┌───────┼───────┐
      ▼       ▼       ▼
  [ LR ]   [SVM]   [ NB ]
      └───────┼───────┘
              │
              ▼
    Category Label + Priority
```

### Models & Accuracy

| Model | Accuracy | Notes |
|---|---|---|
| 🟢 **Linear SVM** | **85.83%** | Best performer — excellent for high-dimensional text |
| 🟣 **Logistic Regression** | 85.46% | Strong baseline, supports probability outputs |
| 🔴 **Naive Bayes** | 78.72% | Fastest, most interpretable |

> Linear SVM is used as the **primary classifier** in the live dashboard.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| ML Framework | scikit-learn |
| NLP | NLTK (stopwords, WordNetLemmatizer) |
| Feature Extraction | TF-IDF Vectorizer |
| Dashboard | Streamlit |
| Charts | Plotly |
| Deployment | Streamlit Community Cloud |

---

## 📁 Project Structure

```
ticketai/
│
├── app.py                          # Main Streamlit dashboard
│
├── models/
│   ├── tfidf.pkl                   # Trained TF-IDF vectorizer
│   ├── lr_model.pkl                # Logistic Regression model
│   ├── nb_model.pkl                # Naive Bayes model
│   └── svm_model.pkl              # Linear SVM model (primary)
│
├── notebooks/
│   └── ticket_classification.ipynb # Full training notebook
│
├── data/
│   └── all_tickets_processed_improved_v3.csv
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ticketai.git
cd ticketai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the dashboard
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## 📦 Requirements

```txt
streamlit
scikit-learn
nltk
plotly
numpy
```

Or install directly:
```bash
pip install streamlit scikit-learn nltk plotly numpy
```

---

## 📓 Model Training (Summary)

The models were trained on `all_tickets_processed_improved_v3.csv` with an **80/20 train-test split**.

```python
# Text cleaning
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    tokens = [lemmatizer.lemmatize(w) for w in text.split()
              if w not in stop_words]
    return " ".join(tokens)

# Vectorization
tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1,2), min_df=3)

# Models trained
models = {
    "Logistic Regression": LogisticRegression(max_iter=2000),
    "Linear SVM":          LinearSVC(),
    "Naive Bayes":         MultinomialNB()
}
```

---

## 💡 Business Value

| Problem | TicketAI Solution |
|---|---|
| Tickets not categorized | Auto-classifies into 8 structured categories |
| Urgent issues delayed | Keyword-based priority routing (High/Med/Low) |
| Support team sorts manually | ML handles sorting instantly at scale |
| No insight into ticket trends | Dashboard shows category distribution & model confidence |

This system reduces **mean time to response (MTTR)** and improves **customer satisfaction scores** by ensuring the right tickets reach the right team — immediately.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

<div align="center">

⭐ Star this repo if you found it useful!

</div>
