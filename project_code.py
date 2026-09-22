"""
Emergency Room Operations & Patient Experience Analytics
Interactive Streamlit dashboard.

Run:
    pip install -r requirements.txt
    streamlit run project_code.py
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "cleaned_dataset.csv"

st.set_page_config(
    page_title="Emergency Room Operations & Patient Experience Analytics",
    page_icon="🏥",
    layout="wide",
)

@st.cache_data

def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE.name}. Keep cleaned_dataset.csv in the same folder as project_code.py."
        )
    df = pd.read_csv(DATA_FILE, parse_dates=["patient_admission_datetime"])
    required = {
        "patient_admission_datetime", "patient_gender", "patient_age", "patient_race",
        "department_referral", "admission_status", "patient_satisfaction_score",
        "patient_wait_time", "admission_month", "admission_hour", "day_of_week",
        "age_group", "wait_time_group", "satisfaction_available"
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    return df

try:
    df = load_data()
except Exception as exc:
    st.error(str(exc))
    st.stop()

st.title("🏥 Emergency Room Operations & Patient Experience Analytics")
st.caption("Data → Information → Insight → Risk / Opportunity → Action")

# Sidebar filters
st.sidebar.header("Dashboard Filters")
min_date = df["patient_admission_datetime"].min().date()
max_date = df["patient_admission_datetime"].max().date()
date_range = st.sidebar.date_input(
    "Admission date", (min_date, max_date), min_value=min_date, max_value=max_date
)

gender_options = sorted(df["patient_gender"].dropna().unique())
gender = st.sidebar.multiselect("Gender", gender_options, default=gender_options)

race_options = sorted(df["patient_race"].dropna().unique())
race = st.sidebar.multiselect("Race", race_options, default=race_options)

dept_options = sorted(df["department_referral"].dropna().unique())
dept = st.sidebar.multiselect("Department referral", dept_options, default=dept_options)

filtered = df[
    (df["patient_admission_datetime"].dt.date >= date_range[0])
    & (df["patient_admission_datetime"].dt.date <= date_range[1])
    & (df["patient_gender"].isin(gender))
    & (df["patient_race"].isin(race))
    & (df["department_referral"].isin(dept))
].copy()

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# Executive KPIs
visits = len(filtered)
admission_rate = (filtered["admission_status"].eq("Admitted").mean()) * 100
avg_wait = filtered["patient_wait_time"].mean()
sat = filtered["patient_satisfaction_score"].mean()
sat_coverage = filtered["patient_satisfaction_score"].notna().mean() * 100

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total ER Visits", f"{visits:,}")
c2.metric("Admission Rate", f"{admission_rate:.1f}%")
c3.metric("Average Wait Time", f"{avg_wait:.1f} min")
c4.metric("Average Satisfaction", "N/A" if pd.isna(sat) else f"{sat:.2f}/10")
c5.metric("Satisfaction Coverage", f"{sat_coverage:.1f}%")

st.divider()

# Operational Analysis
st.subheader("Operational Analysis")

filtered["month"] = filtered["patient_admission_datetime"].dt.to_period("M").astype(str)
monthly = filtered.groupby("month", as_index=False).agg(
    visits=("patient_admission_datetime", "size"),
    admission_rate=("admission_status", lambda s: s.eq("Admitted").mean() * 100),
)

hourly = filtered.groupby("admission_hour", as_index=False).agg(
    visits=("patient_admission_datetime", "size"),
    avg_wait=("patient_wait_time", "mean"),
)

hourly["hour_label"] = hourly["admission_hour"].map(lambda h: f"{int(h):02d}:00")

dept_summary = filtered.groupby("department_referral", as_index=False).agg(
    visits=("patient_admission_datetime", "size"),
    avg_wait=("patient_wait_time", "mean"),
    admission_rate=("admission_status", lambda s: s.eq("Admitted").mean() * 100),
).sort_values("visits", ascending=False)

age_summary = filtered.groupby("age_group", observed=False, as_index=False).agg(
    visits=("patient_age", "size"),
    admission_rate=("admission_status", lambda s: s.eq("Admitted").mean() * 100),
)

r1, r2 = st.columns(2)
with r1:
    fig = px.line(monthly, x="month", y="visits", markers=True, title="Monthly ER Visit Volume")
    fig.update_layout(xaxis_title="Month", yaxis_title="Visits")
    st.plotly_chart(fig, use_container_width=True)
with r2:
    fig = px.bar(hourly, x="hour_label", y="visits", title="Patient Volume by Hour")
    fig.update_layout(xaxis_title="Hour", yaxis_title="Visits")
    st.plotly_chart(fig, use_container_width=True)

r3, r4 = st.columns(2)
with r3:
    fig = px.line(hourly, x="hour_label", y="avg_wait", markers=True, title="Average Wait Time by Hour")
    fig.update_layout(xaxis_title="Hour", yaxis_title="Average Wait (minutes)")
    st.plotly_chart(fig, use_container_width=True)
with r4:
    fig = px.bar(dept_summary, x="department_referral", y="visits", title="Department Referral Analysis")
    fig.update_layout(xaxis_title="Referral", yaxis_title="Visits")
    st.plotly_chart(fig, use_container_width=True)

r5, r6 = st.columns(2)
with r5:
    fig = px.bar(
        age_summary, x="age_group", y="admission_rate",
        title="Admission Rate by Age Group", text_auto=".1f"
    )
    fig.update_layout(xaxis_title="Age Group", yaxis_title="Admission Rate (%)")
    st.plotly_chart(fig, use_container_width=True)
with r6:
    outcome = filtered["admission_status"].value_counts().rename_axis("Outcome").reset_index(name="Visits")
    fig = px.pie(outcome, names="Outcome", values="Visits", title="Admission Distribution")
    st.plotly_chart(fig, use_container_width=True)

# Patient experience
st.subheader("Patient Experience")
sat_df = filtered.dropna(subset=["patient_satisfaction_score"]).copy()

if sat_df.empty:
    st.info("No satisfaction responses are available for the current filters.")
else:
    wait_sat = sat_df.groupby("wait_time_group", observed=False, as_index=False).agg(
        responses=("patient_satisfaction_score", "size"),
        avg_satisfaction=("patient_satisfaction_score", "mean"),
    )
    p1, p2 = st.columns(2)
    with p1:
        fig = px.histogram(
            sat_df, x="patient_satisfaction_score", nbins=11,
            title="Satisfaction Score Distribution"
        )
        fig.update_layout(xaxis_title="Satisfaction Score (0–10)", yaxis_title="Responses")
        st.plotly_chart(fig, use_container_width=True)
    with p2:
        fig = px.scatter(
            sat_df, x="patient_wait_time", y="patient_satisfaction_score",
            opacity=0.45, trendline="ols",
            title="Wait Time vs Satisfaction (Recorded Responses Only)"
        )
        fig.update_layout(xaxis_title="Wait Time (minutes)", yaxis_title="Satisfaction (0–10)")
        st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        wait_sat, x="wait_time_group", y="avg_satisfaction",
        title="Average Satisfaction by Wait-Time Group", text_auto=".2f"
    )
    fig.update_layout(xaxis_title="Wait-Time Group", yaxis_title="Average Satisfaction (0–10)")
    st.plotly_chart(fig, use_container_width=True)

# Data quality and BI interpretation
st.subheader("Data Quality, Risks & Business Actions")
known_referrals = (~filtered["department_referral"].eq("Unknown / Not Recorded")).mean() * 100

st.markdown(
    f"""
**What is happening?**  
The current filter contains **{visits:,} ER visits**, with an observed admission rate of **{admission_rate:.1f}%** and an average wait of **{avg_wait:.1f} minutes**.

**Data quality / limitations**  
- Satisfaction responses cover **{sat_coverage:.1f}%** of records. Satisfaction findings therefore apply only to records with a recorded response.
- **{100-known_referrals:.1f}%** of records have department referral marked **Unknown / Not Recorded**. Referral comparisons should distinguish recorded referrals from missing referral information.
- The dataset is observational. The dashboard describes patterns and associations; it does **not** establish that wait time causes dissatisfaction or admission.

**Operational risk / opportunity**  
Hourly demand and wait-time patterns can help management identify periods that merit staffing or workflow review. Department and age-group differences can guide further investigation, but should be interpreted alongside volume and data completeness.

**Recommended actions**  
1. Review peak-volume hours alongside average wait before adjusting staffing or workflow coverage.
2. Investigate departments with higher observed waits while considering their case volume and referral-data completeness.
3. Improve satisfaction-response capture so patient-experience KPIs represent a larger share of visits.
4. Standardize referral documentation and monitor the **Unknown / Not Recorded** rate as a data-quality KPI.
5. Add staffing, triage severity, queue size and treatment timestamps in future data collection to support stronger root-cause analysis.
"""
)
