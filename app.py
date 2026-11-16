# ==================================================
# IMPORTS
# ==================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="PMO Insight Dashboard",
    page_icon="📊",
    layout="wide"
)


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


# ==================================================
# DATA LOADING
# Load project portfolio data from CSV file
# ==================================================

df = pd.read_csv("data/sample_projects.csv")

# Health status needs df to exist first, and must be added
# before filtering so it shows up in every table
df["Health Status"] = df.apply(calculate_health, axis=1)


# ==================================================
# SIDEBAR FILTERS
# ==================================================

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

# Stop early if the filters leave no projects (avoids division by zero)
if filtered_df.empty:
    st.warning("No hay proyectos con los filtros seleccionados.")
    st.stop()


# ==================================================
# PORTFOLIO KPI CALCULATIONS
# ==================================================

total_projects = len(filtered_df)
on_track = len(filtered_df[filtered_df["Status"] == "On Track"])
at_risk = len(filtered_df[filtered_df["Status"] == "At Risk"])
delayed = len(filtered_df[filtered_df["Status"] == "Delayed"])
completed = len(filtered_df[filtered_df["Status"] == "Completed"])
high_risk = len(filtered_df[filtered_df["Risk Level"] == "High"])

average_progress = round(filtered_df["Progress"].mean(), 1)


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
status_counts = filtered_df["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Projects"]

st.subheader("Status Distribution")

fig_status = px.pie(status_counts, names="Status", values="Projects")
st.plotly_chart(fig_status)
# ==================================================
# RISK DISTRIBUTION
# Risk level overview
# ==================================================

risk_counts = filtered_df["Risk Level"].value_counts().reset_index()
risk_counts.columns = ["Risk Level", "Projects"]

st.subheader("Risk Distribution")

fig_risk = px.pie(risk_counts, names="Risk Level", values="Projects", hole=0.5)
st.plotly_chart(fig_risk)




# ==================================================
# FINANCIAL METRICS
# ==================================================

total_budget = filtered_df["Budget"].sum()
total_spend = filtered_df["Actual Spend"].sum()

budget_utilization = round(
    (total_spend / total_budget) * 100,
    1
) if total_budget > 0 else 0

st.subheader("Financial Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Budget", f"${total_budget:,.0f}")
col2.metric("Total Spend", f"${total_spend:,.0f}")
col3.metric("Budget Utilization", f"{budget_utilization}%")


# ==================================================
# PROJECTS REQUIRING ATTENTION
# Delayed projects or high-risk initiatives
# ==================================================

attention_projects = filtered_df[
    (filtered_df["Status"] == "Delayed") |
    (filtered_df["Risk Level"] == "High")
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
    ] )