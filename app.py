import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Student Analytics Dashboard", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e3f2fd, #fce4ec);
}

/* Center Heading */
h1, h2, .stCaption {
    text-align: center;
}

/* KPI Cards */
.kpi-box {
    background: linear-gradient(135deg,#667eea,#764ba2);
    padding:18px;
    border-radius:12px;
    color:white;
    text-align:center;
    font-size:18px;
    font-weight:bold;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Student Career Counselling Dashboard")


# ---------------- GOOGLE SHEET ----------------
SHEET_ID = "1TQn9yVdfuBCOx8OVrzDm4jEUtv0nuPAR2Udg2190shc"
SHEET_NAME = "Dashboard_Data"

@st.cache_data(ttl=60)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/1TQn9yVdfuBCOx8OVrzDm4jEUtv0nuPAR2Udg2190shc/gviz/tq?tqx=out:csv&sheet=Dashboard_Data"
    return pd.read_csv(url)

df = load_data()

# ---------------- TOP FILTERS ----------------
st.subheader("🔍 Filters")
f1, f2, f3 = st.columns(3)

with f1:
    district = st.selectbox("District", ["All"] + sorted(df["District"].dropna().unique().tolist()))
with f2:
    school = st.selectbox("School Name", ["All"] + sorted(df["School Name"].dropna().unique().tolist()))
with f3:
    class_name = st.selectbox("Class", ["All"] + sorted(df["Class"].dropna().unique().tolist()))

filtered_df = df.copy()
if district != "All":
    filtered_df = filtered_df[filtered_df["District"] == district]
if school != "All":
    filtered_df = filtered_df[filtered_df["School Name"] == school]
if class_name != "All":
    filtered_df = filtered_df[filtered_df["Class"] == class_name]

st.divider()

# ---------------- KPI ----------------
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"<div class='kpi-box'>Total Students<br>{len(filtered_df)}</div>", unsafe_allow_html=True)
k2.markdown(f"<div class='kpi-box'>Total Schools<br>{filtered_df['School Name'].nunique()}</div>", unsafe_allow_html=True)
k3.markdown(f"<div class='kpi-box'>Total Districts<br>{filtered_df['District'].nunique()}</div>", unsafe_allow_html=True)
avg_prev = round(filtered_df["% of Previous Class"].mean(), 2)
k4.markdown(f"<div class='kpi-box'>Avg % Previous Class<br>{avg_prev}</div>", unsafe_allow_html=True)

st.divider()

# ---------------- SCHOOL PERFORMANCE ----------------
school_count = filtered_df["School Name"].value_counts().reset_index()
school_count.columns = ["School Name", "Students"]
fig_school = px.bar(school_count, x="School Name", y="Students",
                    title="🏫 School Wise Performance")
st.plotly_chart(fig_school, use_container_width=True)

# ---------------- TAMMANA TEST ----------------
tammana_cols = ["Tammana Test", "Tammana Test-1", "Tammana Test-2"]
tammana_list = []
for c in tammana_cols:
    if c in filtered_df.columns:
        tammana_list += filtered_df[c].dropna().astype(str).tolist()

tammana_list = [x for x in tammana_list if x.strip() != ""]
if tammana_list:
    tammana_count = pd.Series(tammana_list).value_counts().reset_index()
    tammana_count.columns = ["Tammana Test", "Count"]
    fig_tammana = px.bar(tammana_count, x="Tammana Test", y="Count",
                         title="📊 Tammana Test Analysis")
    st.plotly_chart(fig_tammana, use_container_width=True)

# ---------------- TAMMANA STEN SCORE ----------------
sten_cols = [
    "Tammana Sten Score", "Tammana Sten Score1",
    "Tammana Sten Score2", "Tammana Sten Score3",
    "Tammana Sten Score4"
]
sten_list = []
for c in sten_cols:
    if c in filtered_df.columns:
        sten_list += filtered_df[c].dropna().astype(str).tolist()

sten_list = [x for x in sten_list if x.strip() != ""]
if sten_list:
    sten_count = pd.Series(sten_list).value_counts().reset_index()
    sten_count.columns = ["Sten Score", "Count"]
    fig_sten = px.bar(sten_count, x="Sten Score", y="Count",
                      title="🧮 Tammana Sten Score Analysis")
    st.plotly_chart(fig_sten, use_container_width=True)

# ---------------- CII RESULT ----------------
cii_cols = ["Cii Result", "Cii Result1", "Cii Result2"]
cii_list = []
for c in cii_cols:
    if c in filtered_df.columns:
        cii_list += filtered_df[c].dropna().astype(str).tolist()

cii_list = [x for x in cii_list if x.strip() != ""]
if cii_list:
    cii_count = pd.Series(cii_list).value_counts().reset_index()
    cii_count.columns = ["CII Result", "Count"]
    fig_cii = px.bar(cii_count, x="CII Result", y="Count",
                     title="📑 CII Result Analysis")
    st.plotly_chart(fig_cii, use_container_width=True)

# ---------------- CAREER PATH ----------------
career_cols = ["Career-1","Career-2","Career-3","Career-4","Career-5"]
career_list = []
for c in career_cols:
    if c in filtered_df.columns:
        career_list += filtered_df[c].dropna().astype(str).tolist()

career_list = [x for x in career_list if x.strip() != ""]
if career_list:
    career_count = pd.Series(career_list).value_counts().reset_index()
    career_count.columns = ["Career Path", "Students"]
    fig_career = px.pie(career_count, names="Career Path", values="Students",
                        title="🎯 Career Path Distribution")
    st.plotly_chart(fig_career, use_container_width=True)

st.divider()

# ---------------- DOWNLOAD ----------------
st.subheader("📥 Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_student_data.csv", "text/csv")

st.divider()

# ---------------- DATA TABLE ----------------
st.subheader("📋 Live Data Table")
st.dataframe(filtered_df, use_container_width=True)

