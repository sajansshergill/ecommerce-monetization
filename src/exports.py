import pandas as pd
from src.config import OUT_DIR, CLEAN_PARQUET, RFM_PARQUET


def export_segment_summary(rfm: pd.DataFrame) -> pd.DataFrame:
    seg = (
        rfm.groupby("Segment")
        .agg(
            customers=("CustomerID", "count"),
            total_revenue=("Monetary", "sum"),
            avg_revenue=("Monetary", "mean"),
            avg_recency_days=("RecencyDays", "mean"),
            avg_frequency=("Frequency", "mean"),
            avg_monthly_revenue=("AvgMonthlyRevenue", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )
    seg["revenue_share"] = seg["total_revenue"] / seg["total_revenue"].sum()
    return seg


def export_monthly_kpis(clean: pd.DataFrame) -> pd.DataFrame:
    df = clean.copy()
    df["month"] = df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()

    purchases = df[(~df["IsLeakage"]) & (df["Revenue"] > 0)]

    monthly = (
        purchases.groupby("month")
        .agg(
            revenue=("Revenue", "sum"),
            orders=("InvoiceNo", "nunique"),
            active_customers=("CustomerID", "nunique"),
            units=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values("month")
    )

    monthly["aov"] = monthly["revenue"] / monthly["orders"]
    monthly["arpc"] = monthly["revenue"] / monthly["active_customers"]
    return monthly


def export_leakage_monthly(clean: pd.DataFrame) -> pd.DataFrame:
    df = clean.copy()
    df["month"] = df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()

    leak = (
        df.groupby("month")
        .agg(
            net_revenue=("Revenue", "sum"),
            leakage_revenue=("Revenue", lambda s: s[df.loc[s.index, "IsLeakage"]].sum()),
            positive_revenue=("Revenue", lambda s: s[(~df.loc[s.index, "IsLeakage"]) & (s > 0)].sum()),
            leakage_rows=("IsLeakage", "sum"),
            total_rows=("IsLeakage", "count"),
        )
        .reset_index()
        .sort_values("month")
    )

    leak["leakage_rate_rows"] = leak["leakage_rows"] / leak["total_rows"]
    return leak


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Output filenames (match your structure exactly)
    SEGMENT_SUMMARY_CSV = OUT_DIR / "segment_summary.csv"
    RFM_CUSTOMERS_CSV = OUT_DIR / "rfm_customers.csv"
    MONTHLY_KPIS_CSV = OUT_DIR / "monthly_kpis.csv"
    LEAKAGE_MONTHLY_CSV = OUT_DIR / "leakage_monthly.csv"

    clean = pd.read_parquet(CLEAN_PARQUET)
    rfm = pd.read_parquet(RFM_PARQUET)

    segment_summary = export_segment_summary(rfm)
    monthly_kpis = export_monthly_kpis(clean)
    leakage_monthly = export_leakage_monthly(clean)

    segment_summary.to_csv(SEGMENT_SUMMARY_CSV, index=False)
    rfm.to_csv(RFM_CUSTOMERS_CSV, index=False)
    monthly_kpis.to_csv(MONTHLY_KPIS_CSV, index=False)
    leakage_monthly.to_csv(LEAKAGE_MONTHLY_CSV, index=False)

    print("✅ CSV exports saved to outputs/:")
    print(f" - {SEGMENT_SUMMARY_CSV.name}")
    print(f" - {RFM_CUSTOMERS_CSV.name}")
    print(f" - {MONTHLY_KPIS_CSV.name}")
    print(f" - {LEAKAGE_MONTHLY_CSV.name}")


if __name__ == "__main__":
    main()
