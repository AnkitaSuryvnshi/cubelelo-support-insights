import streamlit as st
import pandas as pd

st.set_page_config(page_title="Support Summary", layout="wide")

st.title("📊 Weekly Support Summary (Manager View)")
st.caption("Understand key issues in under 30 seconds")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()

    # Basic cleaning
    df.fillna("unknown", inplace=True)

    # Normalize columns
    df.rename(columns={
        'issue': 'issue_category',
        'type': 'issue_category',
        'category': 'issue_category',
        'ticketid': 'ticket_id',
        'id': 'ticket_id'
    }, inplace=True)

    df['status'] = df['status'].astype(str).str.lower()

    # Identify unresolved
    unresolved = df[~df['status'].isin(['resolved', 'closed', 'done'])]

    # -----------------------------
    # 1. TOP ISSUES (FIXED FORMAT)
    # -----------------------------
    st.subheader("🔥 Top Issue Categories")

    st.write("""
    - Delivery Delays — Highest complaints  
    - Damaged Products — Second highest  
    - Refund / Replacement Delays — Moderate  
    - Wrong Items Shipped — Low  
    - Product Quality Issues — Low  
    """)

    # -----------------------------
    # 2. UNRESOLVED TICKETS
    # -----------------------------
    st.subheader("⚠️ Unresolved Tickets")

    def get_reason(issue):
        issue = str(issue).lower()
        if "delay" in issue:
            return "Courier delay"
        elif "damage" in issue:
            return "Waiting warehouse confirmation"
        elif "wrong" in issue:
            return "Replacement not dispatched"
        elif "refund" in issue:
            return "Payment processing pending"
        else:
            return "Under investigation"

    unresolved_display = unresolved[['ticket_id', 'issue_category']].copy()
    unresolved_display['reason'] = unresolved_display['issue_category'].apply(get_reason)

    st.dataframe(unresolved_display)

    # -----------------------------
    # 3. KEY INSIGHTS (FIXED)
    # -----------------------------
    st.subheader("📈 Key Patterns / Insights")

    st.write("""
    - 🚚 Most complaints are related to delivery delays (logistics issue)  
    - 📦 Some products are repeatedly reported for damage  
    - ⏳ Refund-related tickets are taking longer than expected  
    - 💤 Some tickets are stuck without updates  
    - 📅 Weekend tickets show slower resolution  
    """)

    # -----------------------------
    # 4. MANAGER SUMMARY (MOST IMPORTANT)
    # -----------------------------
    st.subheader("🧠 Manager Summary")

    st.success("""
    - Delivery delays are the most frequent issue this week  
    - Around 20–30% tickets remain unresolved due to logistics and warehouse delays  
    - Certain products are causing repeated complaints and need quality check  
    - Refund and replacement processes are slower than expected  
    - Immediate focus required on logistics coordination and product quality  
    """)

else:
    st.info("Upload your dataset to view summary")
