# 📚 Library Answer Assistant

> A retrieval-based library Q&A analytics system for evaluating **answer quality, citation accuracy, retrieval performance, and peak-load degradation** across university library content.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQL](https://img.shields.io/badge/SQL-Analytics-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

---

## 📌 Overview

The **Library Answer Assistant** analyzes how effectively a retrieval-based question-answering system answers questions using university library content.

The project works with a synthetic dataset containing **60,000 questions across 90 days**, covering **8 departments** and **3 document types**:

- 📄 Papers
- 🎓 Theses
- 📚 Course Materials

The system evaluates whether answers are:

- Correctly retrieved
- Properly supported by citations
- Helpful to students
- Generated within acceptable response times
- Reliable during peak-load periods

The results are presented through an interactive **Streamlit dashboard** for students, librarians, analysts, and project reviewers.

---

## 🎯 Problem

The existing library workflow relies heavily on keyword search.

Students receive lists of documents and must manually search through them to find an answer.

According to the project dataset:

- **11 documents** — median number of documents opened per answer
- **22 minutes** — median time spent finding an answer

The project investigates whether a retrieval-based answer system can reduce this effort while maintaining evidence-backed answers.

---

## 💡 What This Project Does

```text
Student Question
       ↓
   Retrieval
       ↓
Relevant Passages
       ↓
  Answer Generation
       ↓
   Citation Check
       ↓
 Quality Evaluation
       ↓
 Streamlit Dashboard
```

The analytics pipeline evaluates the system at three levels:

### 🔹 Source Level

Compare performance across:

- Papers
- Theses
- Course Materials

### 🔹 Department Level

Identify differences in answer quality across all **8 departments**.

### 🔹 Peak-Load Level

Compare system performance during normal and high-volume days.

---

## ❓ Business Questions

The project answers eight core questions:

| # | Question |
|---|---|
| 1 | Which sources produce the best answers? |
| 2 | Which departments have the weakest answer quality? |
| 3 | What happens to answer quality on peak-load days? |
| 4 | Which departments degrade the most on peak-load days? |
| 5 | How does retrieval coverage relate to citation accuracy? |
| 6 | How often does the system refuse to answer, and in which departments? |
| 7 | Are scanned or metadata-incomplete documents associated with lower retrieval hit rates? |
| 8 | What are the most common failure reasons? |

---

## 📊 Key Metrics

The dashboard tracks:

| Metric | Purpose |
|---|---|
| **Retrieval Hit Rate** | Measures retrieval effectiveness |
| **Citation Accuracy** | Measures citation correctness |
| **Unsupported Answer Rate** | Measures unsupported generated answers |
| **Refusal Rate** | Measures questions the system refuses |
| **Helpfulness** | Measures user ratings |
| **Time-to-Answer** | Measures student effort |
| **Documents Opened** | Measures search effort |
| **P95 Response Time** | Measures system latency |
| **Answer Quality Score** | Composite quality measure |
| **Peak-Day Degradation** | Measures quality decline during peak load |

---

## ⭐ Answer Quality Score

The project uses a composite score between **0 and 1**:

```text
Answer Quality Score =
    0.4 × Citation Accuracy
  + 0.3 × Retrieval Hit Rate
  + 0.2 × Helpfulness
  + 0.1 × (1 − Normalised Response Time)
```

The dashboard also displays the individual metrics so that the composite score does not hide specific weaknesses.

---

## 🚦 Peak-Load Analysis

A department-day is considered a **peak day** when its query volume exceeds that department's **80th percentile**.

```text
Daily Department Queries
          ↓
Department-specific 80th Percentile
          ↓
Queries > 80th Percentile
          ↓
      Peak Day
```

This department-specific approach prevents larger departments from dominating the analysis.

### Peak-Day Degradation

```text
Peak-Day Degradation =
Normal-Day Quality Score
−
Peak-Day Quality Score
```

---

## 📈 Dashboard

The Streamlit dashboard provides:

### KPI Overview

- Total questions
- Retrieval hit rate
- Citation accuracy
- Refusal rate
- Helpfulness
- Time-to-answer
- P95 response time

### Source Comparison

Compare Paper, Thesis, and Course Material performance.

### Department Analysis

Compare:

- Normal quality
- Peak quality
- Quality degradation

### Failure Analysis

Investigate common failure reasons such as:

- No supported source
- Wrong citation
- OCR gap
- Metadata issues

### Interactive Filters

- Department
- Source type
- Date range
- Peak / Normal
- Rating
- Failure reason

---

## 🗂️ Dataset

The project uses a synthetic **Library Q&A dataset**.

| Property | Value |
|---|---|
| Rows | 60,000 |
| Time Period | 90 days |
| Departments | 8 |
| Source Types | 3 |
| Grain | One row per question |
| Primary Key | `query_id` |
| Format | CSV |
| Timezone | IST |

### Important Fields

```text
query_id
department
request_timestamp
source_type
retrieved_passage_count
retrieval_hit
answer_generated
refused
answer_word_count
claim_count
supported_claim_count
citation_count
response_time_seconds
docs_opened
time_to_answer_minutes
rating
failure_reason
audited
audit_correct
department_daily_queries
```

---

## 🏗️ Project Architecture

```text
                 ┌──────────────────────┐
                 │   Library Q&A CSV    │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ Data Validation      │
                 │ & Cleaning           │
                 └──────────┬───────────┘
                            ↓
              ┌─────────────────────────────┐
              │     SQL + Python Analysis   │
              └──────────────┬──────────────┘
                             ↓
        ┌────────────────────────────────────────┐
        │                                        │
        ↓                                        ↓
┌──────────────────┐                    ┌──────────────────┐
│ KPI Calculation  │                    │ Peak Analysis   │
└────────┬─────────┘                    └────────┬─────────┘
         │                                      │
         └────────────────┬─────────────────────┘
                          ↓
                ┌──────────────────────┐
                │ Streamlit Dashboard  │
                └──────────────────────┘
```

---

## 🛠️ Tech Stack

- **Python** — Data processing and analysis
- **SQL** — Analytical queries and validation
- **Streamlit** — Interactive dashboard
- **Pandas** — Data manipulation
- **CSV** — Dataset storage

> The exact implementation libraries may evolve during development.

---

## 📁 Project Structure

```text
library-answer-assistant/
│
├── data/
│   └── library_qa_log.csv
│
├── src/
│   ├── data_validation.py
│   ├── metrics.py
│   ├── analysis.py
│   └── peak_analysis.py
│
├── sql/
│   ├── source_analysis.sql
│   ├── department_analysis.sql
│   └── peak_analysis.sql
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│   └── analysis.ipynb
│
├── tests/
│   └── test_metrics.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd library-answer-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Place the dataset at:

```text
data/library_qa_log.csv
```

### 5. Start the dashboard

```bash
streamlit run dashboard/app.py
```

---

## 🧪 Data Validation

Before calculating KPIs, the pipeline validates:

- `query_id` uniqueness
- Missing values
- Data types
- Boolean relationships
- Timestamps and IST
- Refusal/answer logic
- Claim counts
- Retrieval counts
- Response-time ranges
- Audit fields
- Failure reasons
- Null `source_type`

Invalid records are logged and excluded from affected KPI calculations where appropriate.

---

## 📌 Project Scope

### V1 Includes

- Question input
- Retrieval across library sources
- Inline citations
- Source filtering
- Department filtering
- Year filtering
- Source comparison
- Department ranking
- Peak vs normal analysis
- Answer Quality Score
- Failure analysis
- Interactive dashboard
- CSV export

### V1 Does Not Include

- Mobile application
- Multi-turn conversation memory
- Essay generation
- Literature-review generation
- Plagiarism detection
- Real-time indexing
- Live data refresh
- Multi-language support
- Personalised recommendations
- Email alerts
- Predictive forecasting

---

## ⚠️ Important Analytical Considerations

This project treats observed relationships as **associations, not causation**.

Other considerations include:

- Small audit samples may affect citation-accuracy estimates.
- Composite scores can hide individual metric weaknesses.
- Peak-day thresholds are department-specific.
- Invalid or incomplete records may affect individual KPIs.

---

## 📄 Documentation

The complete product requirements are documented in the project PRD.

The PRD contains the detailed:

- Business requirements
- Dataset definitions
- KPI definitions
- Answer-quality formula
- Peak-load methodology
- User stories
- Dashboard requirements
- Risk analysis
- Validation requirements
- Final success criteria

---

## 📌 Project Status

**🚧 V1 — In Development**

The implementation is being developed against the requirements defined in the Product Requirements Document.

---

## 🎯 Final Product Question

> **Which sources and departments produce the weakest cited answers, and which behaviours — retrieval coverage, citation support, refusals, and response time — are most associated with that weakness, especially on peak-load days?**

---

### Built for

**Library Analytics • Retrieval Evaluation • Data Analysis • Streamlit • SQL • Python**
