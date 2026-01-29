import pandas as pd
import streamlit as st
import plotly.express as px

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Student Interest Dashboard",
    layout="wide"
)

st.title("🎓 Student Area of Interest Dashboard")

# ----------------------------
# Load data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("student_interests.csv")
    return df

df = load_data()

# ----------------------------
# Combine interest columns
# ----------------------------
interest_cols = [
    "Area_of_Interest_1",
    "Area_of_Interest_2",
    "Area_of_Interest_3",
    "Mention_Other_Area"
]

all_interests = []

for col in interest_cols:
    df[col] = df[col].fillna("")
    for val in df[col]:
        for item in val.split(","):
            item = item.strip()
            if item:
                all_interests.append(item)

interest_df = pd.DataFrame(all_interests, columns=["Interest"])

# ----------------------------
# Normalize labels (critical)
# ----------------------------
normalization_map = {
    "Ai/ML": "AI/ML",
    "AI/ml": "AI/ML",
    "ai/ml": "AI/ML",
    "cloud computing": "Cloud Computing",
    "Cloud computing": "Cloud Computing",
    "Cyber security": "Cyber Security",
    "Web developer": "Web Development",
    "Game developer": "Game Development",
    "Data analyst": "Data Analytics",
    "Big Data": "Big Data"
}

interest_df["Interest"] = interest_df["Interest"].replace(normalization_map)

# ----------------------------
# Count interests
# ----------------------------
interest_counts = (
    interest_df["Interest"]
    .value_counts()
    .reset_index()
)
interest_counts.columns = ["Interest", "Student Count"]

# ----------------------------
# Sidebar filter
# ----------------------------
selected_interest = st.sidebar.multiselect(
    "Filter by Interest",
    options=interest_counts["Interest"].unique(),
    default=interest_counts["Interest"].unique()
)

filtered_counts = interest_counts[
    interest_counts["Interest"].isin(selected_interest)
]

# ----------------------------
# KPI metrics
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Students", df["Name"].nunique())

with col2:
    st.metric("Total Unique Interests", interest_df["Interest"].nunique())

# ----------------------------
# Bar chart
# ----------------------------
fig = px.bar(
    filtered_counts,
    x="Interest",
    y="Student Count",
    text="Student Count",
    title="Student Interest Distribution",
)

fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Raw table (optional)
# ----------------------------
with st.expander("View Raw Data"):
    st.dataframe(df)
