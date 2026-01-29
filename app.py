import pandas as pd
import streamlit as st
import plotly.express as px

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="STUDENT INTEREST DASHBOARD",
    layout="wide"
)

st.title("🎓 STUDENT AREA OF INTEREST DASHBOARD")

# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("student_interests.csv")
    return df

df = load_data()

# ----------------------------------
# CLEAN & FORMAT DATA
# ----------------------------------
df["NAME"] = df["Name"].str.upper()

INTEREST_COLUMNS = [
    "Area_of_Interest_1",
    "Area_of_Interest_2",
    "Area_of_Interest_3",
    "Mention_Other_Area"
]

ALL_INTERESTS = []

for col in INTEREST_COLUMNS:
    df[col] = df[col].fillna("")
    for value in df[col]:
        for item in str(value).split(","):
            item = item.strip()
            if item:
                ALL_INTERESTS.append(item)

interest_df = pd.DataFrame(ALL_INTERESTS, columns=["INTEREST"])

# ----------------------------------
# NORMALIZE INTEREST NAMES
# ----------------------------------
NORMALIZATION_MAP = {
    "Ai/ML": "AI/ML",
    "AI/ml": "AI/ML",
    "ai/ml": "AI/ML",
    "cloud computing": "CLOUD COMPUTING",
    "Cloud computing": "CLOUD COMPUTING",
    "Cyber security": "CYBER SECURITY",
    "Web developer": "WEB DEVELOPMENT",
    "Game developer": "GAME DEVELOPMENT",
    "Data analyst": "DATA ANALYTICS",
    "Big Data": "BIG DATA"
}

interest_df["INTEREST"] = (
    interest_df["INTEREST"]
    .replace(NORMALIZATION_MAP)
    .str.upper()
)

# ----------------------------------
# COUNT INTERESTS
# ----------------------------------
interest_counts = (
    interest_df["INTEREST"]
    .value_counts()
    .reset_index()
)

interest_counts.columns = ["INTEREST", "STUDENT COUNT"]

# ----------------------------------
# SIDEBAR FILTER
# ----------------------------------
st.sidebar.header("FILTER OPTIONS")

selected_interests = st.sidebar.multiselect(
    "FILTER BY INTEREST",
    options=interest_counts["INTEREST"].unique(),
    default=interest_counts["INTEREST"].unique()
)

filtered_counts = interest_counts[
    interest_counts["INTEREST"].isin(selected_interests)
]

# ----------------------------------
# METRICS
# ----------------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric("TOTAL STUDENTS", df["NAME"].nunique())

with col2:
    st.metric("TOTAL UNIQUE INTERESTS", interest_df["INTEREST"].nunique())

# ----------------------------------
# BAR CHART
# ----------------------------------
fig = px.bar(
    filtered_counts,
    x="INTEREST",
    y="STUDENT COUNT",
    text="STUDENT COUNT",
    title="STUDENT INTEREST DISTRIBUTION"
)

fig.update_layout(
    xaxis_title="INTEREST",
    yaxis_title="NUMBER OF STUDENTS",
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# RAW DATA VIEW
# ----------------------------------
with st.expander("VIEW RAW STUDENT DATA"):
    st.dataframe(df)
