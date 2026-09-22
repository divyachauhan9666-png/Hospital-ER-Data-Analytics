# Emergency Room Operations & Patient Experience Analytics

## Project Overview
This project analyzes hospital emergency-room operations and patient experience using visit volume, admission patterns, wait time, referral categories, age groups, satisfaction responses, and time-based patterns. The BI storyline is **Data → Information → Insight → Risk / Opportunity → Action**.

## Business Problem
Emergency-room managers need a clear view of demand, admission patterns, waiting-time pressure, referral workload, and patient experience. The project turns visit-level data into practical KPIs and operational observations that can support further investigation and resource planning.

## Objectives
- Measure ER visit volume and admission rate.
- Identify monthly and hourly demand patterns.
- Analyze wait time across hours and recorded referral categories.
- Compare admission rates across age groups.
- Evaluate patient satisfaction while making response coverage explicit.
- Surface data-quality gaps, risks, opportunities, and possible management actions.

## Dataset Description
The dataset contains **9,216 ER visit records** covering **01 Apr 2023 to 30 Oct 2024**. It includes admission timestamp, gender, age, race, department referral, admission status, satisfaction score, and wait time.

### Dataset Source
Hospital Emergency Dataset by **Xavier Berge**, available on Kaggle. The dataset page identifies the license as **CC0: Public Domain**.

Source: https://www.kaggle.com/datasets/xavierberge/hospital-emergency-dataset

## Data Cleaning & Privacy
- Removed direct identifiers from the final analysis-ready/public dataset: Patient ID, Patient First Initial, and Patient Last Name.
- Removed the redundant duplicate admission-status field from the source.
- Standardized gender to `M` / `F`.
- Standardized admission status to `Admitted` / `Not Admitted`.
- Parsed the admission timestamp into a proper datetime.
- Converted age, wait time, and satisfaction to numeric types.
- Missing department referral values are represented as `Unknown / Not Recorded`; they are not treated as a confirmed referral category.
- Missing satisfaction scores remain missing; no satisfaction value was fabricated.
- The source contained **0 exact duplicate rows**, so no rows were removed for exact duplication.
- Derived fields include month, hour, weekday, age group, wait-time group, and satisfaction-response availability.

## Key KPIs
- **Total ER Visits:** 9,216
- **Admission Rate:** 50.0%
- **Average Wait Time:** 35.3 minutes
- **Average Satisfaction:** 4.99/10, among recorded responses
- **Satisfaction Response Coverage:** 27.3%

## Key Analytical Findings
- **23:00** is the highest-volume hour in this dataset, with **436 visits**.
- The **30–39** age group has the highest visit volume (**1,200 visits**).
- Recorded referral volume is highest for **General Practice (1,840)**; **5,400 records (58.6%)** have no recorded referral.
- Satisfaction is available for only **27.3%** of visits, so satisfaction findings apply only to recorded responses.
- The linear association between wait time and satisfaction among recorded responses is **weak (r = -0.021)**. This should be interpreted as an observed association, not evidence that wait time causes dissatisfaction.

## Data Limitations
- Satisfaction scores are missing for **6,699 records (72.7%)**.
- Department referral is missing for **5,400 records (58.6%)**.
- The dataset does not include staffing levels, queue size, triage severity, provider availability, or treatment timestamps, so root-cause analysis of waiting time is limited.
- The analysis is observational and does not establish causal relationships.

## Technologies Used
Python, Pandas, Streamlit, Plotly.

## Project Structure
```text
Hospital_ER_Data_Analytics_Project/
├── project_code.py
├── requirements.txt
├── .gitignore
├── README.md
├── Project_Report.docx
├── cleaned_dataset.csv
└── charts/
    ├── 01_monthly_visits.png
    ├── 02_wait_by_department.png
    ├── 03_visits_by_department.png
    ├── 04_admission_mix.png
    ├── 05_satisfaction_distribution.png
    ├── 06_age_group_admission.png
    ├── 07_hourly_volume.png
    ├── 08_hourly_wait.png
    ├── 09_wait_vs_satisfaction.png
    ├── 10_satisfaction_by_wait_group.png
    └── dashboard_screenshot.png
```

## Installation
```bash
pip install -r requirements.txt
```

## Run the Dashboard
From the project folder:
```bash
streamlit run project_code.py
```

The app uses a project-relative path and expects `cleaned_dataset.csv` in the same folder as `project_code.py`.

## Business Actions
1. Review peak-hour visit volume together with wait-time patterns before changing staffing or workflow coverage.
2. Investigate departments with higher observed waits while considering case volume and referral completeness.
3. Improve satisfaction-response capture and monitor response coverage as a data-quality KPI.
4. Standardize referral documentation and track the `Unknown / Not Recorded` rate.
5. Add staffing, triage, queue, and treatment-timestamp data in future iterations for stronger operational diagnosis.

## Prediction / ML Assessment
A machine-learning model was intentionally not added to the final submission. The current project is primarily descriptive and BI-focused, and the available operational fields are insufficient for a meaningful production prediction. Future enriched data could support forecasting or wait-time modeling.

## Privacy Note
The final `cleaned_dataset.csv` is designed for public/project use and contains **no direct patient identifiers**. The raw source file should not be uploaded to a public repository.

## Author
**Divya Chauhan**

## Submission Note
This repository is structured for GitHub and internship submission. The dashboard, cleaned dataset, report, and documentation are intended to remain consistent with one another.
