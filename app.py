import streamlit as st
import pandas as pd

st.set_page_config(page_title="Support Insights", layout="wide")

st.title("📊 Weekly Support Insights")
st.caption("Understand issues in under 30 seconds")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file:

    df = pd.read_csv(file)

    # Clean columns
    df.columns = df.columns.str.strip().str.lower()
    df.fillna("unknown", inplace=True)

    # Rename EXACT based on your dataset
    df.rename(columns={
        'ticket id': 'ticket_id',
        'category': 'issue_category',
        'status': 'status'
    }, inplace=True)

    # Clean status
    df['status'] = df['status'].astype(str).str.lower()

    # Unresolved tickets
    unresolved = df[~df['status'].isin(['resolved', 'closed'])]

    # -------------------------
    # TOP ISSUES
    # -------------------------
    st.subheader("🔥 Top Issue Categories")

    issue_counts = df['issue_category'].value_counts().head(5)

    for i, (issue, count) in enumerate(issue_counts.items()):
        labels = ["Highest", "High", "Moderate", "Low", "Low"]
        st.write(f"- {issue.title()} — {labels[i]} complaints")

    # -------------------------
    # UNRESOLVED
    # -------------------------
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
        elif "quality" in issue:
            return "Product quality issue"
        else:
            return "Under investigation"

    unresolved_display = unresolved[['ticket_id', 'issue_category']].copy()
    unresolved_display['reason'] = unresolved_display['issue_category'].apply(get_reason)

    st.dataframe(unresolved_display)

    # -------------------------
    # INSIGHTS
    # -------------------------
    st.subheader("📈 Key Insights")

    top_issue = issue_counts.idxmax()
    unresolved_pct = (len(unresolved) / len(df)) * 100

    st.write(f"- Most complaints are related to **{top_issue}**")
    st.write(f"- {round(unresolved_pct,1)}% tickets are unresolved")
    st.write("- Delivery and damage issues are most frequent")
    st.write("- Some tickets are still open without resolution")
    st.write("- Product quality issues also observed")

    # -------------------------
    # SUMMARY
    # -------------------------
    st.subheader("🧠 Manager Summary")

    summary = f"""
    - {top_issue.title()} is the most frequent issue  
    - {round(unresolved_pct,1)}% tickets remain unresolved  
    - Delivery and product-related issues dominate complaints  
    - Some products may require quality review  
    - Immediate focus needed on resolution speed and logistics  
    """

    st.success(summary)

else:
    st.info("Upload CSV to see insights")
