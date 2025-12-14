from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"

RAW_CSV = DATA_DIR / "online_retail_ii.csv"
CLEAN_PARQUET = OUT_DIR / "clean.parquet"
CUSTOMER_DAILY_PARQUET = OUT_DIR / "customer_daily.parquet"
RFM_PARQUET = OUT_DIR / "rfm.parquet"
