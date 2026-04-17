"""
Link archival ridership station labels to modern subway station IDs.

Reads master_ridership_long.csv and station-neighbors.csv, then adds a
station_id column to each row in the master CSV.  Stations whose label
contains "closed" (case-insensitive) get station_id = -1.  All others
are matched to the closest modern station via normalized name + borough
fuzzy matching.

Outputs:
  - master_ridership_linked.csv   (the full linked dataset)
  - station_id_map.csv            (unique label -> station_id mapping for review)
"""

import csv
import os
import re
from difflib import SequenceMatcher

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_CSV = os.path.join(
    SCRIPT_DIR,
    "..",
    "archival-ridership-data",
    "cleaned_data",
    "master_ridership_long.csv",
)
MODERN_CSV = os.path.join(SCRIPT_DIR, "station-neighbors.csv")
OUTPUT_CSV = os.path.join(
    SCRIPT_DIR,
    "..",
    "archival-ridership-data",
    "cleaned_data",
    "master_ridership_linked.csv",
)
MAP_CSV = os.path.join(SCRIPT_DIR, "station_id_map.csv")

# Borough normalization: archival -> modern abbreviation
BOROUGH_MAP = {
    "manhattan": "M",
    "brooklyn": "Bk",
    "bronx": "Bx",
    "queens": "Q",
}

# Common abbreviation expansions for normalization
ABBREVIATIONS = [
    (r"\bst\b", "street"),
    (r"\bsts\b", "streets"),
    (r"\bave?\b", "avenue"),
    (r"\baves\b", "avenues"),
    (r"\bblvd\b", "boulevard"),
    (r"\bpkwy\b", "parkway"),
    (r"\bpky\b", "parkway"),
    (r"\brd\b", "road"),
    (r"\bpl\b", "place"),
    (r"\bsq\b", "square"),
    (r"\bct\b", "court"),
    (r"\bbway\b", "broadway"),
    (r"\b7av\b", "7 avenue"),
    (r"\b3av\b", "3 avenue"),
    (r"\b10av\b", "10 avenue"),
    (r"\bjct\b", "junction"),
    (r"\bpk\b", "park"),
    (r"\bconc\b", "concourse"),
    (r"\bft\b", "fort"),
    (r"\bhts\b", "heights"),
    (r"\bterm\b", "terminal"),
    (r"\buniv\b", "university"),
    (r"\bel\b", ""),
    (r"\bctr\b", "center"),
    (r"\blvl\b", "level"),
]

# Ordinal suffixes attached to the number: 42nd, 103rd, 1st (no space)
ORDINAL_ATTACHED_RE = re.compile(r"(\d+)(?:st|nd|rd|th|d)\b")
# "103 St." pattern — number + space + "st" at end or before punctuation
# This is "103rd Street", not an ordinal to strip
STREET_ORDINAL_RE = re.compile(r"(\d+)\s+st\b")


def normalize(name):
    """Normalize a station name for comparison."""
    s = name.lower().strip()
    # Remove leading asterisks
    s = s.lstrip("*")
    # Remove parenthetical notes (opened/from/closed dates, etc.)
    s = re.sub(r"\(.*?\)", "", s)
    # Remove quotes
    s = s.replace('"', "")
    # Replace dashes and slashes with spaces
    s = re.sub(r"[/\-\u2014\u2013]", " ", s)
    # Remove all remaining punctuation except spaces and digits
    s = re.sub(r"[^a-z0-9\s]", "", s)
    # "103 st" -> "103 street" (this is an abbreviated street name, not ordinal)
    s = STREET_ORDINAL_RE.sub(r"\1 street", s)
    # Strip attached ordinal suffixes: "42nd" -> "42", "103rd" -> "103"
    s = ORDINAL_ATTACHED_RE.sub(r"\1", s)
    # Expand abbreviations
    for pattern, replacement in ABBREVIATIONS:
        s = re.sub(pattern, replacement, s)
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_modern_stations():
    """Load modern stations, deduplicated by station_id."""
    stations = {}
    with open(MODERN_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["station_id"]
            if sid not in stations:
                stations[sid] = {
                    "station_id": sid,
                    "station_name": row["station_name"],
                    "borough": row["borough"],
                    "normalized": normalize(row["station_name"]),
                }
    return list(stations.values())


LEADING_NUMBER_RE = re.compile(r"^(\d+)\b")
ALL_NUMBERS_RE = re.compile(r"\d+")


def extract_numbers(norm_name):
    """Extract all numbers from a normalized name."""
    return set(ALL_NUMBERS_RE.findall(norm_name))


def extract_leading_number(norm_name):
    """Extract the leading street number if present."""
    m = LEADING_NUMBER_RE.match(norm_name)
    return m.group(1) if m else None


def match_score(archival_norm, modern_norm):
    """
    Compute similarity between two normalized station names.
    Numbers are critical identifiers — if both names start with a street
    number and they differ, heavily penalize the score.
    """
    base = SequenceMatcher(None, archival_norm, modern_norm).ratio()

    a_num = extract_leading_number(archival_norm)
    m_num = extract_leading_number(modern_norm)

    if a_num and m_num:
        if a_num == m_num:
            # Matching street numbers — boost
            base += 0.15
        else:
            # Different street numbers — heavy penalty
            base *= 0.3

    return base


def find_best_match(label, borough, modern_stations):
    """
    Find the best matching modern station for an archival label + borough.
    Returns (station_id, station_name, score).
    """
    norm = normalize(label)
    borough_code = BOROUGH_MAP.get(borough.lower().strip(), "")

    best_id = None
    best_name = ""
    best_score = 0.0

    for ms in modern_stations:
        same_borough = ms["borough"] == borough_code
        score = match_score(norm, ms["normalized"])
        # Borough bonus
        effective_score = score + (0.1 if same_borough else 0.0)

        if effective_score > best_score:
            best_score = effective_score
            best_id = ms["station_id"]
            best_name = ms["station_name"]

    return best_id, best_name, best_score


def main():
    modern_stations = load_modern_stations()
    print(f"Loaded {len(modern_stations)} modern stations")

    # Build unique (label, borough) pairs from master CSV
    label_borough_pairs = set()
    rows = []
    with open(MASTER_CSV, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)
            label_borough_pairs.add((row["label"], row["borough"]))

    print(f"Loaded {len(rows)} rows, {len(label_borough_pairs)} unique (label, borough) pairs")

    # Build mapping: (label, borough) -> station_id
    mapping = {}
    closed_count = 0
    matched_count = 0
    low_confidence = []

    for label, borough in sorted(label_borough_pairs):
        if "closed" in label.lower():
            mapping[(label, borough)] = (-1, "CLOSED", 1.0)
            closed_count += 1
        else:
            sid, sname, score = find_best_match(label, borough, modern_stations)
            mapping[(label, borough)] = (sid, sname, score)
            matched_count += 1
            if score < 0.5:
                low_confidence.append((label, borough, sid, sname, score))

    print(f"Closed stations: {closed_count}")
    print(f"Matched stations: {matched_count}")
    print(f"Low confidence matches (score < 0.5): {len(low_confidence)}")
    if low_confidence:
        print("\nSample low-confidence matches:")
        for label, borough, sid, sname, score in low_confidence[:20]:
            print(f"  '{label}' ({borough}) -> {sid} '{sname}' (score: {score:.3f})")

    # Write station_id_map.csv for review
    with open(MAP_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "borough", "station_id", "modern_station_name", "match_score"])
        for (label, borough), (sid, sname, score) in sorted(mapping.items()):
            writer.writerow([label, borough, sid, sname, f"{score:.4f}"])
    print(f"\nWrote station ID map to {MAP_CSV}")

    # Write linked master CSV
    out_fieldnames = fieldnames + ["station_id"]
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()
        for row in rows:
            sid, _, _ = mapping[(row["label"], row["borough"])]
            row["station_id"] = sid
            writer.writerow(row)
    print(f"Wrote linked dataset to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
