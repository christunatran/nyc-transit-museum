"""
Clean 1940-2011 Historical Ridership.csv.

Page 1: annual totals (subway + bus) with avg weekday — columns named Annual_*/AvgWeekday_*
Page 2: different column naming (Subway, Bus, Total, Avg Weekday/Weekend/Daily)
Both pages have Year and Notes. Normalize into one consistent schema.
"""
import pandas as pd
from pathlib import Path

INPUT = "archival-ridership-data/csv/1940-2011 Historical Ridership.csv"
OUTPUT_DIR = Path("archival-ridership-data/cleaned_data")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT = OUTPUT_DIR / "1940-2011_historical_ridership_clean.csv"

df = pd.read_csv(INPUT)

p1 = df[df["_page"] == 1].copy()
p2 = df[df["_page"] == 2].copy()

# ── Normalize page 1 ──────────────────────────────────────────────────────────
p1 = p1.rename(columns={
    "Annual_Subway":      "annual_subway",
    "Annual_Bus":         "annual_bus",
    "Annual_Total":       "annual_total",
    "AvgWeekday_Subway":  "avg_weekday_subway",
    "AvgWeekday_Bus":     "avg_weekday_bus",
    "AvgWeekday_Total":   "avg_weekday_total",
})

# ── Normalize page 2 ──────────────────────────────────────────────────────────
p2 = p2.rename(columns={
    "Subway":      "annual_subway",
    "Bus":         "annual_bus",
    "Total":       "annual_total",
    "Avg Weekday": "avg_weekday_total",
    "Avg Weekend": "avg_weekend_total",
    "Avg Daily":   "avg_daily_total",
})

# ── Combine ───────────────────────────────────────────────────────────────────
combined = pd.concat([p1, p2], ignore_index=True)

numeric_cols = [
    "annual_subway", "annual_bus", "annual_total",
    "avg_weekday_subway", "avg_weekday_bus", "avg_weekday_total",
    "avg_weekend_total", "avg_daily_total",
]
for col in numeric_cols:
    if col in combined.columns:
        combined[col] = pd.to_numeric(combined[col], errors="coerce")

# Drop rows with no data
combined = combined.dropna(subset=["annual_subway", "annual_total"], how="all")

# Sort by year
combined = combined.sort_values("Year").reset_index(drop=True)

# Final column order
keep = ["Year", "Notes", "_page",
        "annual_subway", "annual_bus", "annual_total",
        "avg_weekday_subway", "avg_weekday_bus", "avg_weekday_total",
        "avg_weekend_total", "avg_daily_total"]
combined = combined[[c for c in keep if c in combined.columns]]

combined.to_csv(OUTPUT, index=False)
print(f"Saved {len(combined)} rows to {OUTPUT}")
print(f"Columns: {list(combined.columns)}")
