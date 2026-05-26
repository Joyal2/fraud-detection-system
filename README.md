🚨 Fraud Detection System

Behavioral Fraud Detection using ML, FastAPI & Streamlit








📌 Project Overview

This project implements a real-time behavioral fraud detection system that evaluates financial transactions and classifies them into:

✅ APPROVE

⚠️ REVIEW

🚫 BLOCK

Unlike simple rule-based systems, this solution uses user-level behavioral patterns and a machine learning model (XGBoost) to make decisions.
Fraud risk scores are intentionally hidden from the UI to reflect real-world banking systems.

🧠 Key Features

Behavioral fraud detection (not static rules)

User transaction velocity analysis

Spending deviation detection

Night-time & new-merchant risk modeling

REST API using FastAPI

Interactive frontend using Streamlit

Reproducible ML pipeline (data & model regenerated via code)


🏗️ System Architecture

                ┌────────────────────┐
                │  Streamlit Frontend │
                │  (Decision Only UI) │
                └─────────▲──────────┘
                          │ HTTP POST
                          │
                ┌─────────┴──────────┐
                │   FastAPI Backend   │
                │  Feature Engineering│
                │  + ML Inference     │
                └─────────▲──────────┘
                          │
                ┌─────────┴──────────┐
                │  XGBoost Model      │
                │  (fraud_model.pkl)  │
                └─────────▲──────────┘
                          │
                ┌─────────┴──────────┐
                │ Synthetic Data Gen  │
                │ Behavioral Features │
                └────────────────────┘


⚙️ Tech Stack

Python 3.14

Pandas / NumPy

XGBoost

Scikit-learn

FastAPI

Uvicorn

Streamlit


🚀 How to Run the Project (Windows)

1️⃣ Create & Activate Virtual Environment : 
python -m venv venv 
venv\Scripts\activate

2️⃣ Install Dependencies : 
pip install -r requirements.txt

3️⃣ Generate Synthetic Behavioral Data : 
python src/data/generate_data.py


Expected:

Fraud rate: ~35–40%

4️⃣ Train the Fraud Detection Model : 
python src/models/train.py


Output:

Model saved to src/models/fraud_model.pkl

5️⃣ Start Backend API (FastAPI): 
uvicorn src.api.main:app


API available at:

http://127.0.0.1:8000

6️⃣ Start Frontend (Streamlit)
streamlit run frontend/app.py


Frontend opens at:

http://localhost:8501

🧪 Sample Test Cases
High Risk (BLOCK)
{
  "transaction_amount": 1200,
  "is_new_merchant": 1,
  "user_txn_count_1h": 6,
  "user_txn_count_24h": 15,
  "user_avg_amount_24h": 140,
  "is_night_for_user": 1
}

Low Risk (APPROVE)
{
  "transaction_amount": 80,
  "is_new_merchant": 0,
  "user_txn_count_1h": 1,
  "user_txn_count_24h": 3,
  "user_avg_amount_24h": 100,
  "is_night_for_user": 0
}


🔐 Design Decisions

Fraud scores are hidden to prevent system gaming

Backend controls feature engineering (trusted layer)

Data & models excluded from GitHub for reproducibility

Fraud prevalence increased for demo & learning purposes

📈 Future Improvements

Cost-based decision thresholds

SHAP-based explainability

Kafka streaming ingestion

User-level long-term profiling

Cloud deployment (Render + Streamlit Cloud)

👤 Author

Joyal Jomon
Aspiring Data Scientist | ML Engineer
GitHub: https://github.com/Joyal2

⭐ If You Like This Project

Give it a star ⭐ 
