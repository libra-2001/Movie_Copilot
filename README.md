# 🎬 Netflix Content Strategy Copilot (AI-Driven Analytics)

An end-to-end data science project that transforms raw streaming data into actionable business intelligence. This tool helps streaming executives optimize content spend and identify technical friction using Generative AI.

---

## 🚀 Project Overview
This project solves the "Blind Spend" problem in streaming. By merging viewership logs with financial data, the Copilot identifies high-value content and uses a **PandasAI (LLM)** agent to allow stakeholders to query millions of rows in plain English.

### 🧠 The "AI Brain"
Unlike standard dashboards, this project features an **AI Strategy Consultant**. 
* **Natural Language Querying:** Ask "Which director has the best ROI?" or "Show me Gen Z watch trends."
* **Automated Insights:** The agent writes and executes Python code on the fly to answer complex business questions.

---

## 🛠️ Tech Stack & Skills
* **Language:** Python 3.10
* **Interface:** Streamlit (Interactive Web App)
* **AI Engine:** PandasAI + OpenAI GPT-3.5/4
* **Analysis:** Pandas, NumPy
* **Visualization:** Plotly (Interactive Charts)
* **Statistics:** SciPy (Hypothesis Testing)
* **Deployment:** Git, GitHub

---

## 📊 Key Business Insights & Features

### 1. Executive Dashboard
* **Views vs. Retention:** Identifies "Clickbait" content (high views, low completion).
* **Market Penetration:** Geospatial analysis of global user activity.
* **Technical Friction Audit:** Analysis of 4K content performance across different device types.

### 2. Statistical Validation (Hypothesis Testing)
We tested the assumption that **4K content on Mobile** leads to higher churn. 
* **Method:** Two-Sample T-Test.
* **Finding:** P-Value of 0.26 (No significant difference).
* **Business Impact:** Saved engineering resources by pivoting focus away from mobile 4K optimization toward content acquisition.

---

## 📦 Installation & Setup

1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/libra-2001/Movie_Copilot.git](https://github.com/libra-2001/Movie_Copilot.git)
   cd Movie_Copilot
