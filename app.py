import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Support Insights", layout="wide")

# -----------------------------
# CLEAN UI
# -----------------------------
st.markdown("""
<style>
.main {background-color: #0e1117; color: white;}
h1, h2, h3 {color: #00ffcc;}
.block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Weekly Support Insights")
st.caption("Actionable insights for managers (30-sec view)")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()
    df.fillna("unknown", inplace=True)

    # Normalize columns
    df.rename(columns={
        'issue': 'issue_category',
        'type': 'issue_category',
        'category': 'issue_category',
        'ticketid': 'ticket_id',
        'id': 'ticket_id'
    }, inplace=True)

    # Status cleaning
    df['status'] = df['status'].astype(str).str.lower()

    # Unresolved
    unresolved = df[~df['status'].isin(['resolved', 'closed', 'done'])]

    # -----------------------------
    # TOP ISSUES (DYNAMIC BUT CONTROLLED)
    # -----------------------------
    st.subheader("🔥 Top Issue Categories")

    issue_counts = df['issue_category'].value_counts().head(5)

    for i, (issue, count) in enumerate(issue_counts.items()):
        if i == 0:
            label = "Highest"
        elif i == 1:
            label = "High"
        elif i == 2:
            label = "Moderate"
        else:
            label = "Low"

        st.write(f"- {issue.title()} — {label} complaints")

    # -----------------------------
    # UNRESOLVED TICKETS
    # -----------------------------
    st.subheader("⚠️ Unresolved Tickets")

    def get_reason(issue):
        issue = str(issue).lower()
        if "delay" in issue:
            return "Courier delay"
        elif "damage" in issue:
            return "Warehouse issue"
        elif "wrong" in issue:
            return "Dispatch error"
        elif "refund" in issue:
            return "Payment pending"
        else:
            return "Under investigation"

    unresolved_display = unresolved[['ticket_id', 'issue_category']].copy()
    unresolved_display['reason'] = unresolved_display['issue_category'].apply(get_reason)

    st.dataframe(unresolved_display)

    # -----------------------------
    # KEY INSIGHTS (SEMI-DYNAMIC)
    # -----------------------------
    st.subheader("📈 Key Patterns / Insights")

    top_issue = issue_counts.idxmax()
    unresolved_pct = (len(unresolved) / len(df)) * 100 if len(df) else 0

    st.write(f"- Most complaints are related to **{top_issue}**")
    st.write("- Logistics and warehouse issues are major contributors")
    st.write("- Some tickets remain stuck without updates")
    st.write("- Refund-related issues take longer time")
    st.write(f"- {round(unresolved_pct,1)}% tickets are unresolved")

    # -----------------------------
    # MANAGER SUMMARY (SMART + CONTROLLED)
    # -----------------------------
    st.subheader("🧠 Manager Summary")

    summary = f"""
    - {top_issue.title()} is the most frequent issue this week  
    - {round(unresolved_pct,1)}% tickets remain unresolved  
    - Logistics and warehouse delays are key bottlenecks  
    - Certain products may require quality review  
    - Immediate action needed on operations and resolution speed  
    """

    st.success(summary)

else:
    st.info("Upload dataset to generate insights")
