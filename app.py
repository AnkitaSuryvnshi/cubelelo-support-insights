import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Support Insights", layout="wide")

# -----------------------------
# CUSTOM UI
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #00ffcc;
}
.stMetric {
    background-color: #1c1f26;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Support Insights Dashboard")
st.caption("Turn raw support tickets into actionable insights in <30 seconds")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("📂 Upload CSV file", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()

    # -----------------------------
    # REQUIRED COLUMN CHECK
    # -----------------------------
    required_cols = ['ticket_id', 'issue_category', 'status']
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            st.stop()

    # -----------------------------
    # SIDEBAR FILTERS
    # -----------------------------
    st.sidebar.header("🔍 Filters")

    issue_filter = st.sidebar.multiselect(
        "Issue Type",
        df['issue_category'].unique(),
        default=df['issue_category'].unique()
    )

    status_filter = st.sidebar.multiselect(
        "Status",
        df['status'].unique(),
        default=df['status'].unique()
    )

    df = df[
        (df['issue_category'].isin(issue_filter)) &
        (df['status'].isin(status_filter))
    ]

    # -----------------------------
    # UNRESOLVED LOGIC
    # -----------------------------
    df['status'] = df['status'].astype(str)
    unresolved = df[df['status'].str.lower() != 'resolved']

    total = len(df)
    unresolved_pct = (len(unresolved) / total * 100) if total else 0

    # -----------------------------
    # METRICS
    # -----------------------------
    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", total)
    col2.metric("Unresolved", len(unresolved))
    col3.metric("Unresolved %", f"{round(unresolved_pct,2)}%")

    # -----------------------------
    # TOP ISSUES
    # -----------------------------
    st.subheader("🔥 Top Issue Categories")

    top_issues = df['issue_category'].value_counts()

    fig, ax = plt.subplots()
    top_issues.plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # -----------------------------
    # REASON ENGINE
    # -----------------------------
    def get_reason(issue):
        issue = str(issue).lower()
        if "delay" in issue:
            return "Logistics delay"
        elif "damage" in issue:
            return "Warehouse issue"
        elif "wrong" in issue:
            return "Dispatch error"
        elif "refund" in issue:
            return "Payment processing delay"
        else:
            return "Needs investigation"

    unresolved['reason'] = unresolved['issue_category'].apply(get_reason)

    # -----------------------------
    # PRIORITY ENGINE
    # -----------------------------
    def get_priority(issue):
        issue = str(issue).lower()
        if "delay" in issue or "refund" in issue:
            return "High 🔴"
        elif "damage" in issue or "wrong" in issue:
            return "Medium 🟠"
        else:
            return "Low 🟢"

    df['priority'] = df['issue_category'].apply(get_priority)

    # -----------------------------
    # SLA CHECK (ADVANCED FEATURE)
    # -----------------------------
    if 'date_created' in df.columns:
        df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')
        df['days_open'] = (pd.Timestamp.now() - df['date_created']).dt.days

        df['sla_breach'] = df['days_open'].apply(
            lambda x: "Yes ❌" if x > 3 else "No ✅"
        )

        st.subheader("⏱ SLA Breach Check")
        st.write(df[['ticket_id', 'days_open', 'sla_breach']].head(10))

    # -----------------------------
    # UNRESOLVED TABLE
    # -----------------------------
    st.subheader("⚠️ Unresolved Tickets with Reasons")
    st.dataframe(unresolved[['ticket_id', 'issue_category', 'reason']])

    # -----------------------------
    # PRODUCT INSIGHTS
    # -----------------------------
    if 'product_name' in df.columns:
        st.subheader("📦 Product Issue Analysis")
        st.write(df['product_name'].value_counts().head(5))

    # -----------------------------
    # KEY INSIGHTS
    # -----------------------------
    st.subheader("📈 Key Insights")

    if len(top_issues) > 0:
        top_issue = top_issues.idxmax()
    else:
        top_issue = "N/A"

    st.write(f"• Most common issue: **{top_issue}**")
    st.write(f"• {round(unresolved_pct,2)}% tickets unresolved")

    # -----------------------------
    # MANAGER SUMMARY
    # -----------------------------
    st.subheader("🧠 Manager Summary")

    summary = f"""
    - {top_issue} is the most frequent issue  
    - {round(unresolved_pct,2)}% tickets are unresolved  
    - Logistics & warehouse delays are major contributors  
    - Some products show repeated complaints  
    - Immediate action required on operations and quality control  
    """

    st.success(summary)

    # -----------------------------
    # DOWNLOAD REPORT
    # -----------------------------
    st.subheader("⬇️ Download Report")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Full Report", csv, "support_report.csv")

else:
    st.info("📂 Upload your dataset to begin")
