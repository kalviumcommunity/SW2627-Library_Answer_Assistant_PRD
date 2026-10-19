**Library Answer Assistant**

Product Requirements Document

Product: Library Answer Assistant

# 1\. Business Problem

## Problem

The university library holds research papers, theses, and course materials across 8 departments. Students currently search by keyword and receive lists of full documents.

In the project dataset, a student opens a median of 11 documents and spends a median of 22 minutes finding one answer, without receiving a concise, citation-backed explanation.

The product will determine whether a retrieval-based answer system can provide short, correctly cited answers and whether answer quality changes during peak-load days.

## Goal

Identify:

- Which document sources produce the weakest cited answers.
- Which departments produce the weakest answers.
- Which behaviours (retrieval coverage, citation support, refusal rate, and response time) are associated with weak answers.
- Whether answer quality decreases during peak-load days.

## Primary Users

Undergraduate and postgraduate students using library content for assignments, theses, and exam preparation.

## Success Criteria

- All 8 business questions can be answered.
- All 3 source types can be compared.
- All 8 departments can be ranked.
- The 3 weakest departments can be identified.
- Every displayed answer has at least one traceable citation.
- Dashboard results match validated Python/SQL analysis.

# 2\. Stakeholders

| **Stakeholder Type** | **Who**                           | **Responsibility**                             |
| -------------------- | --------------------------------- | ---------------------------------------------- |
| Primary Users        | Students                          | Ask questions, read answers, verify sources    |
| Secondary Users      | Subject Librarians, Data Analysts | Review answer quality and investigate problems |
| Data Owner           | Dataset/Data Dictionary Owner     | Confirm data fields, quality, and definitions  |
| Approvers            | Head Librarian, Project Reviewer  | Approve business and technical requirements    |

# 3\. Business Impact

## Operational Impact

The current keyword-search workflow requires a median of 11 opened documents per answer. The product provides one concise answer with citations and gives librarians visibility into weak sources and departments.

## Cost Impact

The dataset contains no verified licensing-cost or monetary-loss information. Therefore, no financial impact is claimed.

Instead, the product measures:

- Documents opened per answer.
- Unanswered/refused questions.
- Source-level performance.
- Department-level performance.

## User Experience Impact

The product measures changes in:

- Time-to-answer: baseline 22 minutes median.
- Documents opened: baseline 11 median.
- Citation accuracy.
- Helpfulness rating.

# 4\. Dataset & Data Source Documentation

## Dataset Overview

| **Property** | **Details**                    |
| ------------ | ------------------------------ |
| Source       | Synthetic Library Q&A dataset  |
| Size         | 60,000 rows                    |
| Time Period  | 90 days                        |
| Departments  | 8                              |
| Sources      | Paper, Thesis, Course Material |
| Grain        | One row per question           |
| Primary Key  | query_id                       |
| Format       | CSV                            |
| Refresh      | Static, pre-generated          |
| Timezone     | IST                            |

## Important Fields

| **Field**                | **Description**                       |
| ------------------------ | ------------------------------------- |
| query_id                 | Unique question identifier            |
| student_hash             | Hashed student identifier             |
| department               | Student's department                  |
| request_timestamp        | Question timestamp                    |
| source_type              | Paper, thesis, or course material     |
| retrieved_passage_count  | Number of passages retrieved          |
| retrieval_hit            | Whether expected source was retrieved |
| answer_generated         | Whether an answer was generated       |
| refused                  | Whether the system refused            |
| answer_word_count        | Answer length                         |
| claim_count              | Number of claims                      |
| supported_claim_count    | Claims supported by evidence          |
| citation_count           | Number of citations                   |
| response_time_seconds    | System response time                  |
| docs_opened              | Documents opened by student           |
| time_to_answer_minutes   | Time taken to reach an answer         |
| rating                   | Up/down helpfulness rating            |
| failure_reason           | Reason for low-quality answer         |
| audited                  | Whether answer was audited            |
| audit_correct            | Whether audited answer was correct    |
| department_daily_queries | Daily department query volume         |

## Derived Fields

- is_peak_day
- supported_claim_ratio
- citation_accuracy
- low_quality_flag
- answer_quality_score
- source_rank
- department_rank

The dataset fields are documented and verified against the project's data dictionary.

# 5\. KPIs & Success Metrics

| **KPI**                 | **Measurement**                          | **Target**                  |
| ----------------------- | ---------------------------------------- | --------------------------- |
| Retrieval Hit Rate      | Successful retrievals ÷ total questions  | Flag below 85%              |
| Citation Accuracy       | Correct audited citations ÷ audited rows | Flag below 90%              |
| Unsupported Answer Rate | Unsupported answers ÷ generated answers  | Flag above 5%               |
| Refusal Rate            | Refused questions ÷ total questions      | Flag above 25%              |
| Helpfulness             | Up ratings ÷ rated answers               | Flag below 75%              |
| Median Time-to-Answer   | Median time_to_answer_minutes            | Flag if peak is >50% higher |
| Documents Opened        | Mean docs_opened                         | Flag above median 11        |
| P95 Response Time       | 95th percentile response time            | Flag above 5 seconds        |
| Answer Quality Score    | Composite score                          | Flag below 0.7              |
| Peak-Day Degradation    | Normal score − peak score                | Rank departments            |

## Answer Quality Score

```
Answer Quality Score =
    0.4 × citation_accuracy
  + 0.3 × retrieval_hit_rate
  + 0.2 × helpfulness_rate
  + 0.1 × (1 − normalised_response_time)
```

The score ranges from 0 to 1.

## Peak-Day Degradation Score

```
Peak-Day Degradation Score =
  Answer Quality Score (Normal Days)
− Answer Quality Score (Peak Days)
```

A higher positive value indicates a larger quality decline during peak days.

# 6\. Peak-Load Day Definition

A department-day is classified as a peak day when:

```
Department Daily Queries
        >
80th Percentile of that Department's Daily Queries
Daily Department Volume
          ↓
Calculate Department-specific 80th Percentile
          ↓
Volume > 80th Percentile
          ↓
is_peak_day = TRUE
```

Each department is evaluated against its own query-volume pattern so that larger departments do not dominate the analysis.

# 7\. Business Questions

| **ID** | **Business Question**                                                                   |
| ------ | --------------------------------------------------------------------------------------- |
| BQ1    | Which sources produce the best answers?                                                 |
| BQ2    | Which departments have the weakest answer quality?                                      |
| BQ3    | What happens to answer quality on peak-load days?                                       |
| BQ4    | Which departments degrade the most on peak-load days?                                   |
| BQ5    | How does retrieval coverage relate to citation accuracy?                                |
| BQ6    | How often does the product refuse, and in which departments?                            |
| BQ7    | Are scanned or metadata-incomplete documents associated with lower retrieval hit rates? |
| BQ8    | What are the most common failure reasons?                                               |

# 8\. Answer Quality Model

Answer quality is evaluated using:

- Retrieval hit rate
- Citation accuracy
- Supported claim ratio
- Helpfulness
- Response time
- Refusal rate

The dashboard will display the individual metrics alongside the Answer Quality Score so that the composite score does not hide the underlying performance signals.

# 9\. User Stories

**US-01:** As a student, I want to ask a question in plain language and receive an answer of ≤150 words, so that I can understand a topic without opening many documents.

**US-02:** As a student, I want every claim to include source details, so that I can verify and cite the information.

**US-03:** As a student, I want to filter by document type and year, so that I can find sources relevant to my assignment.

**US-04:** As a student, I want the system to say "No supported answer found" when evidence is insufficient, so that I do not use unsupported information.

**US-05:** As a student, I want to open the cited passage, so that I can verify the context.

**US-06:** As a subject librarian, I want to compare sources and departments, so that I can identify areas requiring improvement.

**US-07:** As a subject librarian, I want to compare normal and peak days, so that I can identify periods when answer quality decreases.

**US-08:** As a Data Analyst, I want to filter results by source, department, and date, so that I can investigate quality patterns.

# 10\. Product Scope

## In Scope: V1

- Plain-language question input
- Answers up to 150 words
- Inline citations
- Retrieval across papers, theses, and course materials
- Document-type filter
- Year filter
- Department filter
- "No supported answer found" behaviour
- Source comparison
- Department ranking
- Peak vs normal analysis
- Answer Quality Score
- Peak-Day Degradation Score
- Failure-reason analysis
- Department drill-down
- Interactive dashboard
- CSV export

## Out of Scope: V1

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
- Automated acquisition decisions

# 11\. Data Workflow Architecture

```
1. INGESTION
      ↓
2. CLEANING & VALIDATION
      ↓
3. SQL / PYTHON ANALYSIS
      ↓
4. VISUALISATION
      ↓
5. DELIVERY
```

## Stage 1: Ingestion

Load library_qa_log.csv.

## Stage 2: Cleaning & Validation

Validate:

- Boolean relationships
- Claim counts
- Answer length
- Retrieval counts
- Response time
- Audit fields
- Failure reasons

## Stage 3: Analysis

Generate:

- Source-level summaries
- Department-level summaries
- Peak vs normal comparisons
- Refusal analysis
- Failure reasons
- Answer Quality Score
- Peak-Day Degradation Score
- Rankings

## Stage 4: Visualisation

Create the Streamlit dashboard.

## Stage 5: Delivery

Deliver the dashboard to librarians, analysts, and the Head Librarian.

# 12\. Dashboard Requirements

## Dashboard Layout

```
┌─────────────────────────────────────────────────────┐
│              LIBRARY ANSWER ASSISTANT               │
│                ANSWER QUALITY DASHBOARD             │
├─────────────────────────────────────────────────────┤
│ Questions | Hit Rate | Citation | Refusal | Helpful │
│ Time-to-Answer | P95 Response Time                  │
├─────────────────────────────────────────────────────┤
│                 SOURCE COMPARISON                   │
│ Source | Hit Rate | Citation | Refusal | Quality    │
├─────────────────────────────────────────────────────┤
│                 DEPARTMENT RANKING                  │
│ Dept | Normal Quality | Peak Quality | Degradation  │
├─────────────────────────────────────────────────────┤
│                 PEAK vs NORMAL                      │
│ Hit Rate | Citation | Refusal | Time | Helpfulness  │
├──────────────────────────┬──────────────────────────┤
│ ANSWER PATH              │ FAILURE REASONS          │
│ Query → Retrieval        │ No supported source      │
│ → Passage → Citation     │ Wrong citation           │
│ → Rating                 │ OCR gap / Metadata       │
└──────────────────────────┴──────────────────────────┘
```

## Filters

- Department
- Source type
- Date range
- Peak / Normal
- Rating
- Failure reason

## Interactions

- Selecting a department filters the dashboard.
- Selecting a source filters the dashboard.
- Hovering shows exact values and sample size.
- Reset button clears filters.

# 13\. Risk & Assumption Analysis

| **Risk**                              | **Likelihood** | **Impact** | **Mitigation**                                |
| ------------------------------------- | -------------- | ---------- | --------------------------------------------- |
| Correlation interpreted as causation  | Medium         | Medium     | Label findings as associations                |
| Composite score hides weak metrics    | Medium         | High       | Show component metrics                        |
| Small audit samples affect accuracy   | Medium         | Medium     | Show sample size                              |
| Dataset contains invalid records      | Low            | High       | Run validation checks                         |
| Peak threshold changes with dataset   | Low            | Medium     | Use documented department-specific percentile |
| Students skip original sources        | High           | Medium     | Provide highlighted source passages           |
| Null sources affect source comparison | High           | Medium     | Exclude refusals from source metrics          |

## Key Assumptions

- Dataset contains 60,000 questions over 90 days.
- There are 8 departments and 3 source types.
- Each row represents one question.
- Peak days use the department-specific 80th percentile.
- Correlation is not treated as causation.
- KPI thresholds and score formulas are the working V1 definitions.
- Baselines of 11 documents and 22 minutes come from the project dataset.

# 14\. Data Quality & Validation Requirements

Before KPI calculations:

- Check query_id uniqueness.
- Check missing values.
- Validate data types.
- Validate Boolean fields.
- Validate timestamps and IST.
- Validate refusal/answer logic.
- Validate claim counts.
- Validate response-time range.
- Validate audit fields.
- Analyse null source_type.

## Invalid Data Handling

```
Invalid Record
      ↓
Log Validation Failure
      ↓
Determine Metric Impact
      ↓
Exclude From Affected KPI
      ↓
Document Impact
```

# 15\. Final Success Criteria

The product is ready for final review when:

- All 8 business questions are answerable.
- All 3 sources are compared and ranked.
- All 8 departments are ranked.
- The 3 most degraded departments are identified.
- Peak days use the department-specific 80th percentile.
- KPI calculations match validated Python/SQL results.
- Users can filter by source, department, and date.
- Selecting a department/source updates dependent dashboard sections.
- Failure reasons can be analysed.
- Every displayed answer has a traceable citation.
- Dashboard results can be traced to the underlying dataset.

# 16\. Final Product Question

Which sources and departments produce the weakest cited answers, and which behaviours (retrieval coverage, citation support, refusals, and response time) are most associated with that weakness, especially on peak-load days?