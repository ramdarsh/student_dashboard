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
    "Ai/ML": "AI/ML", "AI/ml": "AI/ML", "ai/ml": "AI/ML",

    "cloud computing": "CLOUD COMPUTING", "Cloud computing": "CLOUD COMPUTING",
    "DEVOPS": "CLOUD COMPUTING", "DEVOPS ENGINEER": "CLOUD COMPUTING",
    "CLOUD ENGINEER": "CLOUD COMPUTING",

    "Cyber security": "CYBER SECURITY", "CYBER SECURITY": "CYBER SECURITY",

    "Web developer": "WEB DEVELOPMENT", "WEB DEVELOPER": "WEB DEVELOPMENT",
    "FRONTEND": "WEB DEVELOPMENT", "BACKEND": "WEB DEVELOPMENT",
    "FULL STACK": "WEB DEVELOPMENT",
    "FRONTEND OR BACKEND DEVELOPER": "WEB DEVELOPMENT",

    "Game developer": "GAME DEVELOPMENT", "Game Designer": "GAME DEVELOPMENT",

    "Data analyst": "DATA ANALYTICS", "DATA ANALYST": "DATA ANALYTICS",
    "DATA ANALYTICS": "DATA ANALYTICS",
    "Data scientist": "DATA ANALYTICS / AI",

    "SDE": "SOFTWARE DEVELOPMENT", "JR SDE": "SOFTWARE DEVELOPMENT",
    "SOFTWARE DEVELOPER": "SOFTWARE DEVELOPMENT",
    "SOFTWARE ENGINEER": "SOFTWARE DEVELOPMENT",

    "Big Data": "BIG DATA"
}

# ----------------------------------
# BUILD STUDENT → INTEREST TABLE
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
    st.sidebar.metric(r["INTEREST"], r["STUDENT COUNT"])

# ----------------------------------
# FILTER CHART DATA
# ----------------------------------
chart_data = (
    interest_counts if selected_interest == "ALL"
    else interest_counts[interest_counts["INTEREST"] == selected_interest]
)

# ----------------------------------
# FIXED LAYOUT CHARTS (DESKTOP SAFE)
# ----------------------------------
st.subheader("📊 INTEREST DISTRIBUTION")

col_bar, col_pie = st.columns([1.3, 1])

# ---- BAR CHART (LAYOUT FIXED) ----
fig_bar = px.bar(
    chart_data,
    x="INTEREST",
    y="STUDENT COUNT",
    text="STUDENT COUNT"
)

fig_bar.update_traces(textposition="outside")

fig_bar.update_layout(
    height=500,
    margin=dict(l=40, r=40, t=40, b=140),
    xaxis=dict(
        title="INTEREST",
        tickangle=-35,
        tickfont=dict(size=11)
    ),
    yaxis=dict(title="NUMBER OF STUDENTS")
)

col_bar.plotly_chart(fig_bar, use_container_width=True)

# ---- PIE CHART (STABLE SIZE) ----
fig_pie = px.pie(
    interest_counts,
    names="INTEREST",
    values="STUDENT COUNT",
    hole=0.4
)

fig_pie.update_layout(
    height=500,
    margin=dict(l=20, r=20, t=40, b=20)
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
    st.dataframe(filtered, height=320, use_container_width=True)

# ----------------------------------
# RAW DATA
# ----------------------------------
with st.expander("VIEW RAW DATA"):
    st.dataframe(df)
