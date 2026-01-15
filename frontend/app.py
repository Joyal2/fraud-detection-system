import streamlit as st
import requests

# -------------------------------------------------
# App configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 Fraud Detection System")
st.write("Real-time behavioral fraud decision system")

st.info(
    "This system evaluates transaction risk using behavioral patterns. "
    "Internal risk scores are hidden to simulate real-world fraud systems."
)

API_URL = "http://127.0.0.1:8000/predict"

# -------------------------------------------------
# Input fields (RAW FEATURES ONLY)
# -------------------------------------------------
st.subheader("Transaction Details")

transaction_amount = st.number_input(
    "Transaction Amount",
    min_value=0.0,
    value=500.0,
    step=10.0
)

is_new_merchant = st.selectbox(
    "New Merchant?",
    options=[0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

user_txn_count_1h = st.number_input(
    "User Transactions (Last 1 Hour)",
    min_value=0,
    value=1
)

user_txn_count_24h = st.number_input(
    "User Transactions (Last 24 Hours)",
    min_value=0,
    value=5
)

user_avg_amount_24h = st.number_input(
    "User Average Amount (Last 24 Hours)",
    min_value=0.0,
    value=120.0,
    step=10.0
)

is_night_for_user = st.selectbox(
    "Night Transaction?",
    options=[0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

# -------------------------------------------------
# Submit
# -------------------------------------------------
if st.button("Evaluate Transaction"):
    payload = {
        "transaction_amount": transaction_amount,
        "is_new_merchant": is_new_merchant,
        "user_txn_count_1h": user_txn_count_1h,
        "user_txn_count_24h": user_txn_count_24h,
        "user_avg_amount_24h": user_avg_amount_24h,
        "is_night_for_user": is_night_for_user
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        st.divider()
        st.subheader("Fraud Decision")

        decision = result["decision"]

        if decision == "BLOCK":
            st.error("🚫 TRANSACTION BLOCKED")
            st.caption("This transaction shows high-risk behavioral patterns.")

        elif decision == "REVIEW":
            st.warning("⚠️ TRANSACTION UNDER REVIEW")
            st.caption("This transaction requires additional verification.")

        else:
            st.success("✅ TRANSACTION APPROVED")
            st.caption("This transaction matches normal user behavior.")

    except Exception:
        st.error("❌ Unable to reach fraud detection service.")
