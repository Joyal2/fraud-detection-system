def create_features(df):
    df["amount_log"] = df["transaction_amount"].apply(lambda x: np.log1p(x))
    df["is_night"] = df["transaction_hour"].between(0, 6).astype(int)
    return df
