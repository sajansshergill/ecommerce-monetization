import pandas as pd
from src.config import OUT_DIR, CLEAN_PARQUET, RFM_PARQUET


def score_quintiles(series: pd.Series, higher_is_better: bool) -> pd.Series:
    """
    Returns 1..5 scores by quintile.
    If higher_is_better=False (e.g., Recency days), low values should score higher.

    Robust to duplicate values / low cardinality by using duplicates='drop'
    and falling back to rank-based bins if needed.
    """
    s = series.copy()

    # Ensure numeric + fill missing defensively
    s = pd.to_numeric(s, errors="coerce").fillna(s.median())

    # Rank to avoid qcut tie issues
    ranked = s.rank(method="first")

    try:
        q = pd.qcut(ranked, 5, labels=[1, 2, 3, 4, 5], duplicates="drop")
        # If duplicates dropped and bins < 5, qcut returns fewer categories
        # We'll remap to 1..5 using rank-based cut.
        if q.isna().any() or q.cat.categories.size < 5:
            q = pd.cut(ranked, bins=5, labels=[1, 2, 3, 4, 5], include_lowest=True)
    except ValueError:
        # Fallback if qcut still fails
        q = pd.cut(ranked, bins=5, labels=[1, 2, 3, 4, 5], include_lowest=True)

    q = q.astype(int)
    return q if higher_is_better else (6 - q)


def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    # Validate expected columns exist
    required = ["InvoiceNo", "CustomerID", "InvoiceDate", "Revenue", "IsLeakage"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in clean dataset: {missing}")

    # Snapshot date = day after last transaction (standard approach)
    snapshot = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    # Keep only positive revenue purchases for RFM (leakage handled separately)
    purchases = df[(~df["IsLeakage"]) & (df["Revenue"] > 0)].copy()

    # Drop null CustomerID just in case
    purchases = purchases.dropna(subset=["CustomerID", "InvoiceDate", "Revenue"])

    rfm = purchases.groupby("CustomerID").agg(
        RecencyDays=("InvoiceDate", lambda x: (snapshot - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Revenue", "sum"),
        FirstPurchase=("InvoiceDate", "min"),
        LastPurchase=("InvoiceDate", "max"),
    ).reset_index()

    # Scores
    rfm["R_Score"] = score_quintiles(rfm["RecencyDays"], higher_is_better=False)
    rfm["F_Score"] = score_quintiles(rfm["Frequency"], higher_is_better=True)
    rfm["M_Score"] = score_quintiles(rfm["Monetary"], higher_is_better=True)

    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str)
        + rfm["F_Score"].astype(str)
        + rfm["M_Score"].astype(str)
    )

    # Simple business-friendly segments
    def segment(row):
        r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        if r >= 4 and f >= 3 and m >= 3:
            return "Loyal"
        if r >= 4 and f <= 2:
            return "New/Promising"
        if r <= 2 and f >= 3 and m >= 3:
            return "At Risk (High Value)"
        if r <= 2 and f <= 2:
            return "Hibernating"
        return "Regular"

    rfm["Segment"] = rfm.apply(segment, axis=1)

    # Basic LTV-ish proxy: avg monthly revenue since first purchase
    tenure_months = (
        (rfm["LastPurchase"] - rfm["FirstPurchase"]).dt.days / 30.0
    ).clip(lower=1)

    rfm["AvgMonthlyRevenue"] = rfm["Monetary"] / tenure_months

    return rfm


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(CLEAN_PARQUET)
    rfm = build_rfm(df)

    rfm.to_parquet(RFM_PARQUET, index=False)

    print(f"✅ Saved RFM dataset -> {RFM_PARQUET} | customers={len(rfm):,}")
    print("\nTop segments:")
    print(rfm["Segment"].value_counts().head(10))


if __name__ == "__main__":
    main()
