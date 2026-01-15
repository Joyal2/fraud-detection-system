import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_transactions(n=30000, n_users=2000):
    np.random.seed(42)

    user_ids = np.random.randint(1, n_users + 1, size=n)

    start_time = datetime.now() - timedelta(days=30)
    timestamps = [
        start_time + timedelta(minutes=np.random.randint(0, 60 * 24 * 30))
        for _ in range(n)
    ]

    # Heavier-tailed amount distribution
    transaction_amount = np.random.lognormal(mean=4.8, sigma=1.0, size=n)

    df = pd.DataFrame({
        "user_id": user_ids,
        "timestamp": pd.to_datetime(timestamps),
        "transaction_amount": transaction_amount,
        "is_new_merchant": np.random.binomial(1, 0.5, size=n),
    })

    df["transaction_hour"] = df["timestamp"].dt.hour
    df = df.sort_values(["user_id", "timestamp"])
    df = df.set_index("timestamp")

    # Wider velocity
    df["user_txn_count_1h"] = (
        df.groupby("user_id")["transaction_amount"]
        .rolling("1h")
        .count()
        .reset_index(level=0, drop=True)
    )

    df["user_txn_count_24h"] = (
        df.groupby("user_id")["transaction_amount"]
        .rolling("24h")
        .count()
        .reset_index(level=0, drop=True)
    )

    df["user_avg_amount_24h"] = (
        df.groupby("user_id")["transaction_amount"]
        .rolling("24h")
        .mean()
        .reset_index(level=0, drop=True)
    )

    df["is_night_for_user"] = df["transaction_hour"].between(0, 5).astype(int)

    df = df.fillna(0).reset_index()

    # Derived feature (now wide)
    df["amount_vs_user_avg"] = (
        df["transaction_amount"] / (df["user_avg_amount_24h"] + 1)
    )

    # Strong fraud logic
    high_amount = df["amount_vs_user_avg"] > 4
    high_velocity = df["user_txn_count_1h"] > 3
    risky_context = (df["is_new_merchant"] == 1) | (df["is_night_for_user"] == 1)

    fraud_core = high_amount | (high_velocity & risky_context)

    # Noise to reach ~40%
    noise = np.random.rand(len(df)) < 0.25

    df["is_fraud"] = (fraud_core | noise).astype(int)

    print("Fraud rate:", round(df["is_fraud"].mean(), 4))
    print("Max amount_vs_user_avg:", df["amount_vs_user_avg"].max())
    print("Max user_txn_count_1h:", df["user_txn_count_1h"].max())

    return df


if __name__ == "__main__":
    df = generate_transactions()
    df.to_csv("data/synthetic/transactions.csv", index=False)
    print("Synthetic behavioral fraud data generated")
