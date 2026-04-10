"""
Clean 1940-1995-Ridership-Part1.csv and Part2.csv.

Structure: Station-level data, years split across pages in 14-year chunks.
Each page covers Segment + Station + a range of years.
Page 6 of Part1 is a fare chronology table (Date, Fare, Notes) — kept separately.
Output: two files — station ridership and fare history.
"""
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("archival-ridership-data/cleaned_data")
OUTPUT_DIR.mkdir(exist_ok=True)

part1 = pd.read_csv("archival-ridership-data/csv/1940-1995-Ridership-Part1.csv")
part2 = pd.read_csv("archival-ridership-data/csv/1940-1995-Ridership-Part2.csv")

# ── Fare chronology (Part1 page 6 only) ───────────────────────────────────────
fare_df = part1[part1["_page"] == 6][["Date", "Fare", "Notes", "_page"]].dropna(how="all")
fare_df.to_csv(OUTPUT_DIR / "1940-1995_fare_history.csv", index=False)
print(f"Saved {len(fare_df)} rows to 1940-1995_fare_history.csv")

# ── Station ridership ─────────────────────────────────────────────────────────
# Drop fare page from Part1, combine both parts
ridership = pd.concat([
    part1[part1["_page"] != 6],
    part2
], ignore_index=True)

# Normalize label columns
ridership["label"] = (
    ridership.get("Station", pd.Series(dtype=str))
)
ridership["segment"] = ridership.get("Segment", pd.Series(dtype=str))

# Clean footnote markers
ridership["label"] = (
    ridership["label"].astype(str)
    .str.replace(r"\s*\([a-z]\)$", "", regex=True)
    .str.strip()
    .replace("nan", pd.NA)
)

# Year columns 1940-1995
year_cols = [str(y) for y in range(1940, 1996) if str(y) in ridership.columns]
for col in year_cols:
    ridership[col] = pd.to_numeric(
        ridership[col].astype(str).str.replace("Est.", "", regex=False).str.strip(),
        errors="coerce"
    )

# Drop rows with no year data
ridership = ridership.dropna(subset=year_cols, how="all")

# Final column order
sorted_years = sorted(year_cols, key=int)
keep = ["label", "segment", "_page"] + sorted_years
ridership = ridership[[c for c in keep if c in ridership.columns]]

ridership.to_csv(OUTPUT_DIR / "1940-1995_ridership_clean.csv", index=False)
print(f"Saved {len(ridership)} rows to 1940-1995_ridership_clean.csv")
print(f"Columns: {list(ridership.columns)}")
