from fastapi import FastAPI
import joblib
import numpy as np
from pathlib import Path

app = FastAPI(title="Fraud Detection API")

# -------------------------------------------------
# Load model
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "src" / "models" / "fraud_model.pkl"
model = joblib.load(MODEL_PATH)

# -------------------------------------------------
# Health check
# -------------------------------------------------
@app.get("/")
def health():
    return {"status": "Fraud Detection API running"}

# -------------------------------------------------
# Prediction endpoint (BACKEND CONTROLS FEATURES)
# -------------------------------------------------
@app.post("/predict")
def predict(transaction: dict):

    # -----------------------------
    # RAW INPUTS (trusted)
    # -----------------------------
    transaction_amount = float(transaction["transaction_amount"])
    is_new_merchant = int(transaction["is_new_merchant"])
    user_txn_count_1h = int(transaction["user_txn_count_1h"])
    user_txn_count_24h = int(transaction["user_txn_count_24h"])
    user_avg_amount_24h = float(transaction["user_avg_amount_24h"])
    is_night_for_user = int(transaction["is_night_for_user"])

    # -----------------------------
    # DERIVED FEATURES (AUTHORITATIVE)
    # -----------------------------
    amount_vs_user_avg = transaction_amount / (user_avg_amount_24h + 1)

    # -----------------------------
    # Feature vector (EXACT training order)
    # -----------------------------
    features = np.array([[
        transaction_amount,
        is_new_merchant,
        user_txn_count_1h,
        user_txn_count_24h,
        user_avg_amount_24h,
        amount_vs_user_avg,
        is_night_for_user
    ]], dtype=float)

    # -----------------------------
    # Model inference
    # -----------------------------
    fraud_score = float(model.predict_proba(features)[0][1])

    # -----------------------------
    # Decision policy
    # -----------------------------
    if fraud_score >= 0.75:
        decision = "BLOCK"
    elif fraud_score >= 0.40:
        decision = "REVIEW"
    else:
        decision = "APPROVE"

    return {
        "fraud_score": round(fraud_score, 4),
        "decision": decision
    }
