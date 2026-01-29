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
    return pd.read_csv("student_interests.csv")

df = load_data()

# ----------------------------------
# FORMAT NAMES
# ----------------------------------
df["NAME"] = df["Name"].str.upper()

INTEREST_COLUMNS = [
    "Area_of_Interest_1",
    "Area_of_Interest_2",
    "Area_of_Interest_3",
    "Mention_Other_Area"
]

# ----------------------------------
# NORMALIZATION MAP
# ----------------------------------
NORMALIZATION_MAP = {
    # AI / ML
    "Ai/ML": "AI/ML",
    "AI/ml": "AI/ML",
    "ai/ml": "AI/ML",

    # CLOUD
    "cloud computing": "CLOUD COMPUTING",
    "Cloud computing": "CLOUD COMPUTING",
    "DEVOPS": "CLOUD COMPUTING",
    "Devops": "CLOUD COMPUTING",
    "DEVOPS ENGINEER": "CLOUD COMPUTING",
    "CLOUD ENGINEER": "CLOUD COMPUTING",

    # CYBER
    "Cyber security": "CYBER SECURITY",
    "CYBER SECURITY": "CYBER SECURITY",

    # WEB (MERGED)
    "Web developer": "WEB DEVELOPMENT",
    "WEB DEVELOPER": "WEB DEVELOPMENT",
    "FRONTEND": "WEB DEVELOPMENT",
    "FRONTEND DEVELOPER": "WEB DEVELOPMENT",
    "BACKEND": "WEB DEVELOPMENT",
    "BACKEND DEVELOPER": "WEB DEVELOPMENT",
    "FULL STACK": "WEB DEVELOPMENT",
    "FULL STACK DEVELOPER": "WEB DEVELOPMENT",
    "FRONTEND OR BACKEND DEVELOPER": "WEB DEVELOPMENT",
    "FULL STACK WEB DEVELOPMENT": "WEB DEVELOPMENT",

    # GAME
    "Game developer": "GAME DEVELOPMENT",
    "GAME DEVELOPER": "GAME DEVELOPMENT",
    "Game Designer": "GAME DEVELOPMENT",
    "GAME DESIGNER": "GAME DEVELOPMENT",

    # DATA (MERGED)
    "Data analyst": "DATA ANALYTICS",
    "Data Analyst": "DATA ANALYTICS",
    "DATA ANALYST": "DATA ANALYTICS",
    "Data analytics": "DATA ANALYTICS",
    "DATA ANALYTICS": "DATA ANALYTICS",
    "DATA SCIENTIST": "DATA SCIENTIST",
    "Data scientist": "DATA SCIENTIST",

    # SOFTWARE DEVELOPMENT (MERGED)
    "SDE": "SOFTWARE DEVELOPMENT",
    "JR SDE": "SOFTWARE DEVELOPMENT",
    "Jr SDE": "SOFTWARE DEVELOPMENT",
    "SOFTWARE DEVELOPER": "SOFTWARE DEVELOPMENT",
    "SOFTWARE ENGINEER": "SOFTWARE DEVELOPMENT",
    "SOFTWARE DEVELOPMENT ENGINEER": "SOFTWARE DEVELOPMENT",

    # BIG DATA
    "Big Data": "BIG DATA",
    "BIG DATA": "BIG DATA"
}


# ----------------------------------
# BUILD STUDENT → INTEREST MAPPING
# ----------------------------------
student_interest_rows = []

for _, row in df.iterrows():
    interests = []

    for col in INTEREST_COLUMNS:
        value = str(row[col]) if pd.notna(row[col]) else ""
        for item in value.split(","):
            item = item.strip()
            if item:
                item = NORMALIZATION_MAP.get(item, item).upper()
                interests.append(item)

    student_interest_rows.append({
        "NAME": row["NAME"],
        "INTERESTS": ", ".join(sorted(set(interests)))
    })

student_interest_df = pd.DataFrame(student_interest_rows)

# ----------------------------------
# CREATE INTEREST COUNT DATA
# ----------------------------------
all_interests = []

for interests in student_interest_df["INTERESTS"]:
    for i in interests.split(","):
        all_interests.append(i.strip())

interest_counts = (
    pd.Series(all_interests)
    .value_counts()
    .reset_index()
)

interest_counts.columns = ["INTEREST", "STUDENT COUNT"]

# ----------------------------------
# SIDEBAR FILTER
# ----------------------------------
st.sidebar.header("FILTER OPTIONS")

selected_interest = st.sidebar.selectbox(
    "SELECT ROLE / INTEREST",
    options=["ALL"] + interest_counts["INTEREST"].tolist()
)
# ----------------------------------
# SIDEBAR: STUDENT COUNT BY INTEREST
# ----------------------------------
st.sidebar.markdown("### 📌 STUDENT COUNT BY INTEREST")

for _, row in interest_counts.iterrows():
    st.sidebar.metric(
        label=row["INTEREST"],
        value=row["STUDENT COUNT"]
    )


# ----------------------------------
# METRICS
# ----------------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric("TOTAL STUDENTS", student_interest_df["NAME"].nunique())

with col2:
    st.metric("TOTAL UNIQUE INTERESTS", interest_counts["INTEREST"].nunique())

# ----------------------------------
# CHARTS SECTION
# ----------------------------------
st.subheader("📊 INTEREST DISTRIBUTION")

if selected_interest == "ALL":
    chart_data = interest_counts
else:
    chart_data = interest_counts[interest_counts["INTEREST"] == selected_interest]

col_bar, col_pie = st.columns(2)

# ---- BAR CHART ----
fig_bar = px.bar(
    chart_data,
    x="INTEREST",
    y="STUDENT COUNT",
    text="STUDENT COUNT",
    title="STUDENT INTEREST COUNT"
)

fig_bar.update_layout(
    xaxis_title="INTEREST",
    yaxis_title="NUMBER OF STUDENTS",
    xaxis_tickangle=-45
)

col_bar.plotly_chart(fig_bar, use_container_width=True)

# ---- PIE CHART ----
fig_pie = px.pie(
    interest_counts if selected_interest == "ALL" else chart_data,
    names="INTEREST",
    values="STUDENT COUNT",
    title="ROLE DISTRIBUTION (PERCENTAGE)",
    hole=0.4
)

fig_pie.update_traces(textposition="inside", textinfo="percent+label")

col_pie.plotly_chart(fig_pie, use_container_width=True)

# ----------------------------------
# STUDENT DETAILS FOR SELECTED ROLE
# ----------------------------------
st.subheader("👨‍🎓 STUDENT DETAILS")

if selected_interest == "ALL":
    st.info("SELECT A ROLE FROM THE SIDEBAR TO VIEW STUDENT DETAILS.")
else:
    filtered_students = student_interest_df[
        student_interest_df["INTERESTS"].str.contains(selected_interest, case=False)
    ]

    st.write(f"TOTAL STUDENTS INTERESTED IN {selected_interest}: {len(filtered_students)}")

    st.dataframe(
        filtered_students.reset_index(drop=True),
        use_container_width=True
    )

# ----------------------------------
# RAW DATA VIEW
# ----------------------------------
with st.expander("VIEW RAW DATA"):
    st.dataframe(df)








