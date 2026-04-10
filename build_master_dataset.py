"""
Build master long-format ridership dataset spanning 1920-1995.

Sources:
- 1920-1929: IRT/BMT subway station data (pages 3-10, station level)
- 1930-1939: IRT/BMT/IND subway station data (pages 3-12, station level)
- 1940-1995: Unified city system, all stations (MTA/Board of Transportation)

Strategy:
- Melt each source to long format: one row per station-year
- Normalize station names for cross-decade matching
- Tag each row with source so data provenance is always visible
- No interpolation or fabrication — NaN means no data for that year

Output:
- cleaned_data/master_ridership_long.csv
"""

import pandas as pd
import re
from pathlib import Path

OUTPUT_DIR = Path("archival-ridership-data/cleaned_data")
OUTPUT_DIR.mkdir(exist_ok=True)


# ── Name normalization ─────────────────────────────────────────────────────────

def normalize_name(name):
    """Lowercase, strip punctuation noise, expand abbreviations."""
    if pd.isna(name) or str(name).strip() in ("", "nan"):
        return None
    n = str(name).lower().strip()
    n = re.sub(r"\s*\([a-z]\)$", "", n)           # remove (a), (b) footnotes
    n = re.sub(r"\(.*?\)", "", n)                  # remove all parentheticals
    n = re.sub(r"\b(st\.?)\b", "st", n)
    n = re.sub(r"\bave\.?\b", "ave", n)
    n = re.sub(r"\bblvd\.?\b", "blvd", n)
    n = re.sub(r"\bpkwy\.?\b", "pkwy", n)
    n = re.sub(r"[/\-–—]", " ", n)                # normalize separators
    n = re.sub(r"[.,]", "", n)                     # strip punctuation
    n = re.sub(r"\s+", " ", n).strip()
    return n


# ── System-total detection ─────────────────────────────────────────────────────

SYSTEM_TOTAL_KEYWORDS = [
    "total", "division", "corp.", "co.", "company", "lines:", "lines,",
    "surface", "bus lines", "ferry", "grand total", "hudson tubes",
    "rapid transit lines", "bklyn stas", "brooklyn stations",
    "net total", "gross total", "adjustment", "miscellaneous",
    "subtotal", "sub-total",
    # metadata rows that leaked through OCR cleaning
    "conductor's collection", "number of station", "system route mile",
    "route miles",
]

# OCR-corrupted all-caps header strings that are line names, not stations
HEADER_FRAGMENTS = [
    "adway-fourth ave. line", "adway line", "atbush avenue conn",
    "astoria branch", "flushing branch", "broadway-fourth avenue line",
    "flatbush avenue conn", "brighton beach line", "houston-essex street line",
    "fth avenue - bay ridge", "sea beach line",
]

def is_system_total(label):
    if pd.isna(label):
        return True
    l = str(label).lower()
    if any(kw in l for kw in SYSTEM_TOTAL_KEYWORDS):
        return True
    if any(h in l for h in HEADER_FRAGMENTS):
        return True
    # All-caps strings longer than 6 chars are almost always section headers
    if str(label) == str(label).upper() and len(str(label).strip()) > 6:
        return True
    return False


# ── Load and melt 1920-1929 ────────────────────────────────────────────────────

df20 = pd.read_csv("archival-ridership-data/cleaned_data/1920-1929_ridership_clean.csv")

# Pages 3-10 are station-level (IRT Contract 1/2/3 stations)
# Page 2 is system-level totals — exclude
station_20 = df20[df20["_page"] >= 3].copy()
station_20 = station_20[~station_20["label"].apply(is_system_total)]

year_cols_20 = [c for c in station_20.columns if c.isdigit()]
id_vars_20 = ["label", "_page"] + (["borough"] if "borough" in station_20.columns else [])
melted_20 = station_20.melt(
    id_vars=id_vars_20,
    value_vars=year_cols_20,
    var_name="year",
    value_name="ridership"
).dropna(subset=["ridership"])

melted_20["segment"] = None
if "borough" not in melted_20.columns:
    melted_20["borough"] = None
melted_20["source"] = "IRT/BMT (1920s)"
melted_20["era"] = "private_operators"
print(f"1920-1929: {len(melted_20)} station-year rows ({melted_20['label'].nunique()} stations)")


# ── Load and melt 1930-1939 ────────────────────────────────────────────────────

df30 = pd.read_csv("archival-ridership-data/cleaned_data/1930-1939_ridership_clean.csv")

# Pages 3-12 are station-level
# Pages 1-2 are system-level / monthly totals
station_30 = df30[df30["_page"] >= 3].copy()
station_30 = station_30[~station_30["label"].apply(is_system_total)]

year_cols_30 = [c for c in station_30.columns if c.isdigit() and 1930 <= int(c) <= 1939]
melted_30 = station_30.melt(
    id_vars=["label", "line", "borough", "_page"],
    value_vars=year_cols_30,
    var_name="year",
    value_name="ridership"
).dropna(subset=["ridership"])

melted_30["segment"] = melted_30["line"]
melted_30["source"] = "IRT/BMT/IND (1930s)"
melted_30["era"] = "private_operators"
print(f"1930-1939: {len(melted_30)} station-year rows ({melted_30['label'].nunique()} stations)")


# ── Load and melt 1940-1995 ────────────────────────────────────────────────────

df40 = pd.read_csv("archival-ridership-data/cleaned_data/1940-1995_ridership_clean.csv")
df40 = df40[~df40["label"].apply(is_system_total)]

year_cols_40 = [c for c in df40.columns if c.isdigit()]
id_vars_40 = ["label", "segment", "_page"] + (["borough"] if "borough" in df40.columns else [])
melted_40 = df40.melt(
    id_vars=id_vars_40,
    value_vars=year_cols_40,
    var_name="year",
    value_name="ridership"
).dropna(subset=["ridership"])

# Each station appears on 4 pages per segment (14-yr chunks, non-overlapping years).
# After melt + dropna, year ranges don't overlap so there are no true duplicates —
# EXCEPT for 6 station-segment pairs that appear in two geographic sections of the
# source document with conflicting values. We keep ALL rows and flag conflicts.
dup_mask = melted_40.duplicated(subset=["label", "segment", "year"], keep=False)
melted_40["conflict"] = dup_mask

def classify_era(year):
    y = int(year)
    if y < 1968:
        return "board_of_transportation"
    return "mta"

melted_40["era"] = melted_40["year"].apply(classify_era)
melted_40["source"] = "Unified System (1940-1995)"
if "borough" not in melted_40.columns:
    melted_40["borough"] = None
print(f"1940-1995: {len(melted_40)} station-year rows ({melted_40['label'].nunique()} stations)")


# ── Combine all sources ────────────────────────────────────────────────────────

melted_20["conflict"] = False
melted_30["conflict"] = False

cols = ["label", "segment", "borough", "year", "ridership", "source", "era", "_page", "conflict"]

master = pd.concat([
    melted_20.reindex(columns=cols),
    melted_30.reindex(columns=cols),
    melted_40.reindex(columns=cols),
], ignore_index=True)

master["year"] = master["year"].astype(int)
master["ridership"] = pd.to_numeric(master["ridership"], errors="coerce")
master = master.sort_values(["label", "segment", "year"]).reset_index(drop=True)


# ── Add normalized name for cross-decade matching ──────────────────────────────

master["label_normalized"] = master["label"].apply(normalize_name)

# Flag stations that appear in multiple source eras (cross-decade matches)
name_sources = master.groupby("label_normalized")["source"].nunique()
master["cross_decade_match"] = master["label_normalized"].map(name_sources) > 1


# ── Save ───────────────────────────────────────────────────────────────────────

out = OUTPUT_DIR / "master_ridership_long.csv"
master.to_csv(out, index=False)

print(f"\nMaster dataset: {len(master)} rows")
print(f"Year range: {master['year'].min()} – {master['year'].max()}")
print(f"Unique stations (normalized): {master['label_normalized'].nunique()}")
print(f"Cross-decade matches: {master['cross_decade_match'].sum()} rows "
      f"({master[master['cross_decade_match']]['label_normalized'].nunique()} stations)")
print(f"\nSaved to {out}")
print(f"\nRows per era:")
print(master.groupby("era")["ridership"].count().to_string())
