import pandas as pd
import joblib
from pathlib import Path
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# ---------------------------------------------------
# Resolve base directories
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "synthetic" / "transactions.csv"
MODEL_DIR = BASE_DIR / "src" / "models"
MODEL_PATH = MODEL_DIR / "fraud_model.pkl"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------
# Load dataset
# ---------------------------------------------------
df = pd.read_csv(DATA_PATH)

# ---------------------------------------------------
# Explicit feature selection (CRITICAL)
# ---------------------------------------------------
FEATURES = [
    "transaction_amount",
    "is_new_merchant",
    "user_txn_count_1h",
    "user_txn_count_24h",
    "user_avg_amount_24h",
    "amount_vs_user_avg",
    "is_night_for_user",
]

X = df[FEATURES].astype(float)
y = df["is_fraud"].astype(int)

# ---------------------------------------------------
# Train / test split (stratified)
# ---------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# ---------------------------------------------------
# XGBoost model
# ---------------------------------------------------
model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=42
)

# ---------------------------------------------------
# Train model
# ---------------------------------------------------
model.fit(X_train, y_train)

# ---------------------------------------------------
# Save trained model
# ---------------------------------------------------
joblib.dump(model, MODEL_PATH)

print("======================================")
print("Behavioral fraud model trained successfully")
print(f"Model saved at: {MODEL_PATH}")
print("======================================")
