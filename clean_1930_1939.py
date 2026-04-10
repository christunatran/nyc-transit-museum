import pandas as pd
from pathlib import Path

INPUT = "archival-ridership-data/csv/1930-1939 Ridership.csv"
OUTPUT_DIR = Path("archival-ridership-data/cleaned_data")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT = OUTPUT_DIR / "1930-1939_ridership_clean.csv"

df = pd.read_csv(INPUT)

# ── 1. Normalize label column ──────────────────────────────────────────────────
# Pages 3-6,8-11 use STATIONS; page 7 uses Station; page 1 uses Line Type
df["label"] = (
    df.get("STATIONS", pd.Series(dtype=str))
    .combine_first(df.get("Station", pd.Series(dtype=str)))
    .combine_first(df.get("Line Type", pd.Series(dtype=str)))
)

# ── 2. Normalize line and borough columns ──────────────────────────────────────
df["line"] = df.get("Line", pd.Series(dtype=str)).combine_first(
    df.get("LINE", pd.Series(dtype=str))
)
df["borough"] = df.get("Borough", pd.Series(dtype=str)).combine_first(
    df.get("BOROUGH", pd.Series(dtype=str))
)

# ── 3. Map page 2's fiscal year columns into 1938/1939 ────────────────────────
# Page 2 has "Fiscal Year 1939" and "Fiscal Year 1938" instead of year columns
if "Fiscal Year 1939" in df.columns:
    if "1939" not in df.columns:
        df["1939"] = pd.NA
    df["1939"] = df["1939"].combine_first(df["Fiscal Year 1939"])

if "Fiscal Year 1938" in df.columns:
    if "1938" not in df.columns:
        df["1938"] = pd.NA
    df["1938"] = df["1938"].combine_first(df["Fiscal Year 1938"])

# ── 4. Map page 1's annual total into 1939 ────────────────────────────────────
# Page 1 has "Number of Fare Passengers Carried During Fiscal Year 1939"
annual_col = "Number of Fare Passengers Carried During Fiscal Year 1939"
if annual_col in df.columns:
    if "1939" not in df.columns:
        df["1939"] = pd.NA
    df["1939"] = df["1939"].combine_first(df[annual_col])

# Keep Month and Year from page 1 as metadata
month_col = "Month" if "Month" in df.columns else None
year_col = "Year" if "Year" in df.columns else None

# ── 5. Clean "Est." and footnote markers ──────────────────────────────────────
year_cols = [str(y) for y in range(1930, 1940) if str(y) in df.columns]
for col in year_cols:
    df[col] = df[col].astype(str).str.replace("Est.", "", regex=False).str.strip()
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["label"] = df["label"].astype(str).str.replace(r"\s*\([a-z]\)$", "", regex=True).str.strip()
df["label"] = df["label"].replace("nan", pd.NA)

# ── 6. Build final column order ───────────────────────────────────────────────
meta = ["label", "line", "borough", "_page"]
if month_col:
    meta.append("Month")
if year_col:
    meta.append("Year")

sorted_years = sorted(year_cols, key=int)
keep = [c for c in meta if c in df.columns] + sorted_years
df = df[keep]

# ── 7. Drop rows with no year data at all ─────────────────────────────────────
df = df.dropna(subset=sorted_years, how="all")

# ── 8. Drop rows where label is null AND no line/borough (truly empty rows) ───
df = df[~(df["label"].isna() & df["line"].isna() & df["borough"].isna())]

df.to_csv(OUTPUT, index=False)
print(f"Saved {len(df)} rows to {OUTPUT}")
print(f"Columns: {list(df.columns)}")
print(f"\nRows per page:")
print(df.groupby("_page").size().to_string())
