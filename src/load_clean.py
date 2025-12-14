import pandas as pd
from src.config import RAW_CSV, OUT_DIR, CLEAN_PARQUET

# Canonical columns we want AFTER normalization
CANONICAL_COLS = ["InvoiceNo", "CustomerID", "InvoiceDate", "Quantity", "UnitPrice", "Country"]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize messy raw column names into canonical names used across the project.

    Handles common variants like:
      - 'Invoice No' -> 'InvoiceNo'
      - 'Customer ID' -> 'CustomerID'
      - 'Unit Price'  -> 'UnitPrice'
      - 'InvoiceDate' or 'Invoice Date' -> 'InvoiceDate'
    """
    # Create a normalized key for each original column:
    #  - strip whitespace
    #  - remove spaces/underscores
    #  - lowercase
    original_cols = df.columns.tolist()
    normalized = (
        pd.Index(original_cols)
        .astype(str)
        .str.strip()
        .str.replace(" ", "", regex=False)
        .str.replace("_", "", regex=False)
        .str.lower()
    )

    # Map normalized names -> canonical names
    rename_map = {
        "invoiceno": "InvoiceNo",
        "invoice": "InvoiceNo",          # sometimes invoice is used
        "invoiceid": "InvoiceNo",
        "customerid": "CustomerID",
        "customer": "CustomerID",        # rare
        "invoicedate": "InvoiceDate",
        "date": "InvoiceDate",           # rare, but seen in exports
        "quantity": "Quantity",
        "qty": "Quantity",
        "unitprice": "UnitPrice",
        "price": "UnitPrice",            # rare
        "country": "Country",
    }

    # Build a dict original_col -> canonical_col if we recognize it
    fixed = {}
    for orig, norm in zip(original_cols, normalized):
        if norm in rename_map:
            fixed[orig] = rename_map[norm]

    # Rename recognized columns
    df = df.rename(columns=fixed)

    return df


def load_raw(path=RAW_CSV) -> pd.DataFrame:
    """
    Load raw CSV and normalize column names into canonical schema.
    """
    df = pd.read_csv(path, encoding="ISO-8859-1")

    # Normalize column names
    df = _normalize_columns(df)

    # Validate we have what we need
    missing = [c for c in CANONICAL_COLS if c not in df.columns]
    if missing:
        # Helpful debug output
        raise ValueError(
            "Missing required columns after normalization: "
            f"{missing}\n\nColumns found:\n{df.columns.tolist()}"
        )

    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataset:
      - parse dates
      - coerce types
      - drop critical nulls
      - compute Revenue
      - flag cancellations/refunds (leakage)
    """
    df = df.copy()

    # Parse datetime safely
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    # CustomerID often loads as float due to NaNs, so keep it nullable int
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce").astype("Int64")

    # Numeric fields
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    # Drop critical nulls
    df = df.dropna(subset=["InvoiceDate", "CustomerID", "Quantity", "UnitPrice", "Country"])

    # Revenue at line-item level
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    # Leakage flags
    # Many cancellations have InvoiceNo starting with 'C'
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["IsCancel"] = df["InvoiceNo"].str.startswith("C")

    df["IsNegativeQty"] = df["Quantity"] < 0
    df["IsNegativeRevenue"] = df["Revenue"] < 0

    # Broad leakage definition (good for portfolio)
    df["IsLeakage"] = df["IsCancel"] | df["IsNegativeQty"] | df["IsNegativeRevenue"]

    # Clean up country strings
    df["Country"] = df["Country"].astype(str).str.strip()

    return df


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_raw()
    df = clean(df)

    keep = [
        "InvoiceNo",
        "CustomerID",
        "InvoiceDate",
        "Quantity",
        "UnitPrice",
        "Revenue",
        "Country",
        "IsCancel",
        "IsNegativeQty",
        "IsNegativeRevenue",
        "IsLeakage",
    ]

    df[keep].to_parquet(CLEAN_PARQUET, index=False)

    print(f"✅ Saved clean dataset -> {CLEAN_PARQUET}")
    print(f"✅ Rows: {len(df):,}")
    print("✅ Date range:",
          df["InvoiceDate"].min().date(),
          "to",
          df["InvoiceDate"].max().date())


if __name__ == "__main__":
    main()
