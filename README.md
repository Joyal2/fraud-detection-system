1. Project Overview
This project implements a real-time behavioral fraud detection system using synthetic transaction data,
machine learning, and a modern API + frontend stack. The system classifies transactions into APPROVE,
REVIEW, or BLOCK without exposing internal fraud scores, mimicking real financial systems.
2. Project Structure
fraud-detection-system/
 data/synthetic/transactions.csv
 src/data/generate_data.py
 src/models/train.py
 src/models/fraud_model.pkl
 src/api/main.py
 frontend/app.py
 requirements.txt
3. Environment Setup
Create and activate a virtual environment, then install dependencies using pip and the provided
requirements file.
Commands:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
4. Data Generation
The data generator creates user-level transaction histories with behavioral features such as velocity,
spending deviation, night activity, and merchant novelty. Fraud prevalence is intentionally increased
(~40%) for demonstration purposes.
Command:
python src/data/generate_data.py
5. Model Training
An XGBoost classifier is trained using behavioral features. The trained model is saved as fraud_model.pkl
and later loaded by the API.
Command:
python src/models/train.py
6. Backend API (FastAPI)
The FastAPI service exposes a /predict endpoint. It receives raw transaction details, computes derived
behavioral features internally, and returns a decision without exposing the fraud score.
Command:
uvicorn src.api.main:app
7. Frontend (Streamlit)
The Streamlit frontend provides a simple UI for entering transaction details and displaying the fraud
decision (APPROVE, REVIEW, BLOCK).
Command:
streamlit run frontend/app.py
8. End-to-End Run Order
1. Activate virtual environment
2. Generate data
3. Train model
4. Start FastAPI backend
5. Start Streamlit frontend
9. Notes
Fraud scores are intentionally hidden from the frontend to reflect real-world fraud system design.
Thresholds and fraud prevalence can be adjusted easily via the data generation and API logic