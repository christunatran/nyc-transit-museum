import pandas as pd
from pathlib import Path

INPUT = "archival-ridership-data/csv/1920-1929_ridership.csv"
OUTPUT_DIR = Path("archival-ridership-data/cleaned_data")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT = OUTPUT_DIR / "1920-1929_ridership_clean.csv"

df = pd.read_csv(INPUT)

# 1. Name the unnamed first column, then merge with STATIONS column
#    (page 2 uses the first column for names; pages 3+ use "STATIONS")
df = df.rename(columns={df.columns[0]: "label"})
if "STATIONS" in df.columns:
    df["label"] = df["label"].combine_first(df["STATIONS"])
    df = df.drop(columns=["STATIONS"])

# 2. Merge "Year Ended June 30" into "1920"
#    (page 2 stores the 1920 value under "Year Ended June 30" due to the original header)
if "Year Ended June 30" in df.columns:
    if "1920" not in df.columns:
        df = df.rename(columns={"Year Ended June 30": "1920"})
    else:
        df["1920"] = df["1920"].combine_first(df["Year Ended June 30"])
    df = df.drop(columns=["Year Ended June 30"], errors="ignore")

# 3. Drop the verbose page description
df = df.drop(columns=["_page_desc"], errors="ignore")

# 4. Strip footnote markers like (a), (b) from labels
df["label"] = df["label"].str.replace(r"\s*\([a-z]\)$", "", regex=True).str.strip()

# 5. Clean "Est." prefixes from numeric columns
year_cols = [c for c in df.columns if str(c).isdigit()]
for col in year_cols:
    df[col] = df[col].astype(str).str.replace("Est.", "", regex=False).str.strip()
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 6. Sort year columns in order
meta_cols = ["label", "_page"]
sorted_years = sorted(year_cols, key=int)
df = df[[c for c in meta_cols if c in df.columns] + sorted_years]

# 7. Drop rows where all year values are null (section headers)
df = df.dropna(subset=sorted_years, how="all")

df.to_csv(OUTPUT, index=False)
print(f"Saved {len(df)} rows to {OUTPUT}")
print(f"Columns: {list(df.columns)}")
