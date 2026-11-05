# ==================================================
# IMPORTS
# ==================================================

import streamlit as st
import pandas as pd


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="PMO Insight Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# DATA LOADING
# Load project portfolio data from CSV file
# ==================================================

df = pd.read_csv("data/sample_projects.csv")

# Sidebar filters
st.sidebar.header("Filters")

selected_status = st.sidebar.multiselect(
    "Project Status",
    df["Status"].unique(),
    default=df["Status"].unique()
)


selected_department = st.sidebar.multiselect(
    "Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

filtered_df = df[
    (df["Status"].isin(selected_status)) &
    (df["Department"].isin(selected_department))
]

# ==================================================
# HEALTH STATUS CALCULATION
# Classify projects based on risk and status
# ==================================================

def calculate_health(row):
    if row["Status"] == "Delayed" or row["Risk Level"] == "High":
        return "🔴 Critical"
    elif row["Risk Level"] == "Medium":
        return "🟡 Warning"
    else:
        return "🟢 Healthy"


df["Health Status"] = df.apply(calculate_health, axis=1)


# ==================================================
# PORTFOLIO KPI CALCULATIONS
# ==================================================

total_projects = len(df)
on_track = len(df[df["Status"] == "On Track"])
at_risk = len(df[df["Status"] == "At Risk"])
delayed = len(df[df["Status"] == "Delayed"])
completed = len(df[df["Status"] == "Completed"])
high_risk = len(df[df["Risk Level"] == "High"])

average_progress = round(df["Progress"].mean(), 1)


# ==================================================
# DASHBOARD HEADER
# ==================================================

st.title("📊 PMO Insight Dashboard")

st.subheader("Portfolio Overview")


# ==================================================
# KPI CARDS
# ==================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Projects", total_projects)
col2.metric("On Track", on_track)
col3.metric("At Risk", at_risk)
col4.metric("Delayed", delayed)
col5.metric("Avg Progress", f"{average_progress}%")


# ==================================================
# PROJECTS TABLE
# Display complete project portfolio
# ==================================================

st.subheader("Projects")

st.dataframe(filtered_df)

# ==================================================
# STATUS DISTRIBUTION
# Project status overview
# ==================================================

status_counts = filtered_df["Status"].value_counts()

st.subheader("Status Distribution")

st.bar_chart(status_counts)


# ==================================================
# RISK DISTRIBUTION
# Risk level overview
# ==================================================

risk_counts = filtered_df["Risk Level"].value_counts()

st.subheader("Risk Distribution")

st.bar_chart(risk_counts)


# ==================================================
# FINANCIAL METRICS
# ==================================================

total_budget = df["Budget"].sum()
total_spend = df["Actual Spend"].sum()

budget_utilization = round(
    (total_spend / total_budget) * 100,
    1
)

st.subheader("Financial Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Budget", f"${total_budget:,.0f}")
col2.metric("Total Spend", f"${total_spend:,.0f}")
col3.metric("Budget Utilization", f"{budget_utilization}%")


# ==================================================
# PROJECTS REQUIRING ATTENTION
# Delayed projects or high-risk initiatives
# ==================================================

attention_projects = df[
    (df["Status"] == "Delayed") |
    (df["Risk Level"] == "High")
]

st.subheader("Projects Requiring Attention")

st.dataframe(
    attention_projects[
        [
            "Project Name",
            "Project Manager",
            "Status",
            "Risk Level",
            "Health Status",
            "Progress",
        ]
    ]
)


