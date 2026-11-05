import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="PMO Insight Dashboard",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv("data/sample_projects.csv")

def calculate_health(row):
    if row["Status"] == "Delayed" or row["Risk Level"] == "High":
        return "🔴 Critical"
    elif row["Risk Level"] == "Medium":
        return "🟡 Warning"
    else:
        return "🟢 Healthy"

df["Health Status"] = df.apply(calculate_health, axis=1)

st.title("📊 PMO Insight Dashboard")

st.subheader("Portfolio Overview")
total_projects = len(df)
on_track = len(df[df["Status"] == "On Track"])
at_risk = len(df[df["Status"] == "At Risk"])
delayed = len(df[df["Status"] == "Delayed"])

average_progress = round(df["Progress"].mean(), 1)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Projects", total_projects)
col2.metric("On Track", on_track)
col3.metric("At Risk", at_risk)
col4.metric("Delayed", delayed)
col5.metric("Avg Progress", f"{average_progress}%")

st.subheader("Projects")

st.dataframe(df)

status_counts = df["Status"].value_counts()

st.bar_chart(status_counts)

completed = len(df[df["Status"] == "Completed"])

risk_counts = df["Risk Level"].value_counts()

st.subheader("Risk Distribution")

st.bar_chart(risk_counts)

average_progress = round(df["Progress"].mean(), 1)

st.metric("Average Progress", f"{average_progress}%")

total_budget = df["Budget"].sum()
total_spend = df["Actual Spend"].sum()
budget_utilization = round((total_spend / total_budget) * 100, 1)

st.subheader("Financial Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Budget", f"${total_budget:,.0f}")
col2.metric("Total Spend", f"${total_spend:,.0f}")
col3.metric("Budget Utilization", f"{budget_utilization}%")

st.subheader("Projects Requiring Attention")

attention_projects = df[
    (df["Status"] == "Delayed") |
    (df["Risk Level"] == "High")
]

st.dataframe(
    attention_projects[
        ["Project Name",
         "Project Manager",
         "Status",
         "Risk Level",
         "Progress"]
    ]
)

high_risk = len(df[df["Risk Level"] == "High"])

