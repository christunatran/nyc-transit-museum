"""
Clean Rapid Transit Ridership 1932-1935.csv and 1934-1937.csv.

Both are simple: label column + year columns + increase/decrease columns.
Normalize label name, strip footnotes, drop _page_desc.
"""
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("archival-ridership-data/cleaned_data")
OUTPUT_DIR.mkdir(exist_ok=True)

def clean_rapid_transit(input_path, output_path, label_col):
    df = pd.read_csv(input_path)

    df = df.rename(columns={label_col: "label"})
    df["label"] = (
        df["label"].astype(str)
        .str.replace(r"\s*\([a-z]\)$", "", regex=True)
        .str.strip()
        .replace("nan", pd.NA)
    )

    # Normalize year and numeric columns
    numeric_cols = [c for c in df.columns if c not in ("label", "_page", "_page_desc")]
    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False).str.strip(),
            errors="coerce"
        )

    df = df.drop(columns=["_page_desc"], errors="ignore")
    df = df.dropna(subset=[c for c in numeric_cols if c != "_page"], how="all")

    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")
    print(f"Columns: {list(df.columns)}")

clean_rapid_transit(
    "archival-ridership-data/csv/Rapid Transit Ridership 1932-1935.csv",
    OUTPUT_DIR / "rapid_transit_1932-1935_clean.csv",
    label_col="Line/System"
)

clean_rapid_transit(
    "archival-ridership-data/csv/Rapid Transit Ridership 1934-1937.csv",
    OUTPUT_DIR / "rapid_transit_1934-1937_clean.csv",
    label_col="Line/Category"
)
