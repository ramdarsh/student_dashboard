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
df["NAME"] = df["Name"].str.upper()

INTEREST_COLUMNS = [
    "Area_of_Interest_1",
    "Area_of_Interest_2",
    "Area_of_Interest_3",
    "Mention_Other_Area"
]

# ----------------------------------
# NORMALIZATION MAP (FINAL)
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

    # WEB
    "Web developer": "WEB DEVELOPMENT",
    "WEB DEVELOPER": "WEB DEVELOPMENT",
    "FRONTEND": "WEB DEVELOPMENT",
    "FRONTEND DEVELOPER": "WEB DEVELOPMENT",
    "BACKEND": "WEB DEVELOPMENT",
    "BACKEND DEVELOPER": "WEB DEVELOPMENT",
    "FULL STACK": "WEB DEVELOPMENT",
    "FULL STACK DEVELOPER": "WEB DEVELOPMENT",
    "FRONTEND OR BACKEND DEVELOPER": "WEB DEVELOPMENT",

    # GAME
    "Game developer": "GAME DEVELOPMENT",
    "GAME DEVELOPER": "GAME DEVELOPMENT",
    "Game Designer": "GAME DEVELOPMENT",
    "GAME DESIGNER": "GAME DEVELOPMENT",

    # DATA
    "Data analyst": "DATA ANALYTICS",
    "Data Analyst": "DATA ANALYTICS",
    "DATA ANALYST": "DATA ANALYTICS",
    "Data analytics": "DATA ANALYTICS",
    "DATA ANALYTICS": "DATA ANALYTICS",
    "Data scientist": "DATA ANALYTICS / AI",
    "DATA SCIENTIST": "DATA ANALYTICS / AI",

    # SOFTWARE DEVELOPMENT
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
rows = []

for _, row in df.iterrows():
    interests = []

    for col in INTEREST_COLUMNS:
        value = str(row[col]) if pd.notna(row[col]) else ""
        for item in value.split(","):
            item = item.strip()
            if item:
                interests.append(
                    NORMALIZATION_MAP.get(item, item).upper()
                )

    rows.append({
        "NAME": row["NAME"],
        "INTERESTS": ", ".join(sorted(set(interests)))
    })

student_interest_df = pd.DataFrame(rows)

# ----------------------------------
# INTEREST COUNTS
# ----------------------------------
all_interests = []
for interests in student_interest_df["INTERESTS"]:
    all_interests.extend([i.strip() for i in interests.split(",")])

interest_counts = (
    pd.Series(all_interests)
    .value_counts()
    .reset_index()
)

interest_counts.columns = ["INTEREST", "STUDENT COUNT"]

# ----------------------------------
# SIDEBAR
# ----------------------------------
st.sidebar.header("FILTER OPTIONS")

selected_interest = st.sidebar.selectbox(
    "SELECT ROLE / INTEREST",
    ["ALL"] + interest_counts["INTEREST"].tolist()
)

st.sidebar.divider()
st.sidebar.markdown("### 📌 STUDENT COUNT BY INTEREST")

for _, r in interest_counts.iterrows():
    st.sidebar.metric(
        r["INTEREST"],
        r["STUDENT COUNT"]
    )

# ----------------------------------
# TOP-N + OTHER (LAYOUT FIX)
# ----------------------------------
TOP_N = 7

top_interests = interest_counts.head(TOP_N)
other_count = interest_counts.iloc[TOP_N:]["STUDENT COUNT"].sum()

if other_count > 0:
    other_row = pd.DataFrame([{
        "INTEREST": "OTHER",
        "STUDENT COUNT": other_count
    }])
    chart_counts = pd.concat([top_interests, other_row], ignore_index=True)
else:
    chart_counts = top_interests

# ----------------------------------
# CHARTS (FIXED & READABLE)
# ----------------------------------
st.subheader("📊 INTEREST DISTRIBUTION")

col_bar, col_pie = st.columns([1.3, 1])

# ---- HORIZONTAL BAR CHART ----
fig_bar = px.bar(
    chart_counts,
    x="STUDENT COUNT",
    y="INTEREST",
    text="STUDENT COUNT",
    orientation="h",
    title="TOP INTERESTS BY NUMBER OF STUDENTS"
)

fig_bar.update_layout(
    height=500,
    margin=dict(l=140, r=40, t=60, b=40),
    xaxis=dict(title="NUMBER OF STUDENTS"),
    yaxis=dict(title="INTEREST")
)

fig_bar.update_traces(textposition="outside")

col_bar.plotly_chart(fig_bar, use_container_width=True)

# ---- PIE CHART (CLEAN) ----
fig_pie = px.pie(
    chart_counts,
    names="INTEREST",
    values="STUDENT COUNT",
    hole=0.4,
    title="INTEREST SHARE (TOP CATEGORIES)"
)

fig_pie.update_layout(
    height=500,
    margin=dict(l=20, r=20, t=60, b=20),
    legend=dict(
        orientation="v",
        x=1.05,
        y=0.5
    )
)

col_pie.plotly_chart(fig_pie, use_container_width=True)

# ----------------------------------
# STUDENT DETAILS
# ----------------------------------
st.subheader("👨‍🎓 STUDENT DETAILS")

if selected_interest == "ALL":
    st.info("SELECT A ROLE FROM THE SIDEBAR TO VIEW STUDENT DETAILS.")
else:
    filtered = student_interest_df[
        student_interest_df["INTERESTS"].str.contains(selected_interest)
    ]
    st.dataframe(
        filtered.reset_index(drop=True),
        height=320,
        use_container_width=True
    )

# ----------------------------------
# RAW DATA
# ----------------------------------
with st.expander("VIEW RAW DATA"):
    st.dataframe(df)
