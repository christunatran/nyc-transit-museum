"""
Add borough column to master_ridership_long.csv.

Two-pass strategy:

Pass 1 — from source documents only:
- 1920-1929 and 1930-1939: forward-fill from geographic section headers
  embedded in the STATIONS column of the raw CSVs (e.g. "BROOKLYN STATIONS",
  "MANHATTAN, EAST", "JEROME AVENUE BRANCH").
- 1940-1995: segment-to-borough mapping for unambiguous single-borough segments.

Pass 2 — from web research (Wikipedia, per-station lookups):
- Multi-borough lines (8 Ave., Broadway/7 Ave., Jamaica, Lexington Ave.,
  Crosstown, Lenox Ave., Fulton St.) filled using station-level borough
  lookups sourced from Wikipedia line articles and per-station articles.
  Source URLs documented in BIBLIOGRAPHY.md.
"""

import re
import pandas as pd
from pathlib import Path

OUT = Path("archival-ridership-data/cleaned_data")


# ── Borough detection from section headers ─────────────────────────────────────

def header_to_borough(header_text):
    """
    Return a borough string if the section header explicitly names one,
    else None (meaning: don't change the current borough).
    """
    if not isinstance(header_text, str):
        return None
    t = header_text.upper()

    # Brooklyn
    if "BKLYN" in t or "BROOKLYN" in t:
        return "Brooklyn"
    # Explicit Bronx labels
    if re.search(r"\bBRONX\b", t):
        return "Bronx"
    if "JEROME AVENUE BRANCH" in t or "JEROME AVE" in t:
        return "Bronx"
    if "PELHAM" in t and "BRANCH" in t:
        return "Bronx"
    if "WHITE PLAINS" in t:
        return "Bronx"
    if "BRONX CONCOURSE" in t:
        return "Bronx"
    # Explicit Queens labels
    if "QUEENSBORO" in t or "QUEENS BOULEVARD" in t:
        return "Queens"
    if "ASTORIA BRANCH" in t:
        return "Queens"
    if "FLUSHING BRANCH" in t or "FLUSHING LINE" in t:
        return "Queens"
    # Explicit Manhattan labels
    if "MANHATTAN" in t and "BRIDGE" not in t:
        return "Manhattan"
    if "BROADWAY LINE, MANHATTAN" in t:
        return "Manhattan"
    # Brooklyn line names
    if "MYRTLE AVENUE LINE" in t:
        return "Brooklyn"
    if "FULTON STREET LINE" in t or "FULTON STREET AVE" in t:
        return "Brooklyn"
    if "FOURTH AVENUE LINE (BROOKLYN)" in t:
        return "Brooklyn"
    if "BROOKLYN CROSSTOWN LINE" in t:
        return "Brooklyn"
    # Queens IND
    if "QUEENS BOULEVARD LINE" in t:
        return "Queens"
    # IRT Lexington Ave. main line (Manhattan), before Jerome/Pelham branches
    # Header rows like "LEXINGTON AVE. LINE NET TOTAL" / "LEXINGTON AVENUE LINE—GROSS TOTAL"
    # carry data AND label the Manhattan trunk — treat them as Manhattan setters.
    if "LEXINGTON AVE" in t and "JEROME" not in t and "PELHAM" not in t and "WHITE PLAINS" not in t:
        return "Manhattan"
    # Eastern Parkway Line / Livonia Ave. Branch → Brooklyn (IRT subway)
    if "EASTERN PARKWAY" in t or "LIVONIA" in t:
        return "Brooklyn"
    # Queensboro subway — Queens section
    if "QUEENSBORO" in t:
        return "Queens"
    # IRT Third Avenue El — borough depends on which section header appears
    # The Manhattan section ran from downtown to ~129th St.
    # The Bronx section ran from Willis Ave. (Mott Haven) northward.
    # "THIRD AVENUE LINE" alone is ambiguous; resolve per-station in web-research pass.
    # Sixth Avenue El — Manhattan
    if "SIXTH AVENUE LINE" in t or "6TH AVENUE LINE" in t:
        return "Manhattan"

    return None  # ambiguous — carry forward previous


def build_borough_map_from_raw(raw_csv_path, stations_col, year_sample_cols, page_col="_page"):
    """
    Read a raw CSV, walk through each page's rows in order, detect section
    headers by borough keyword, forward-fill, and return a dict mapping
    (normalized_label, page) → borough.
    """
    df = pd.read_csv(raw_csv_path)
    label_borough = {}
    current_borough = None

    for page in sorted(df[page_col].dropna().unique()):
        if int(page) < 3:
            continue  # skip system-total pages
        pg = df[df[page_col] == page].copy()
        current_borough = None  # reset per page

        for _, row in pg.iterrows():
            raw_label = row.get(stations_col)
            if pd.isna(raw_label):
                continue
            raw_label = str(raw_label).strip()
            if not raw_label or raw_label.lower() in ("nan", ""):
                continue

            # Detect if this row is a section header (all year cols are null)
            year_vals = [row.get(c) for c in year_sample_cols if c in row.index]
            all_null = all(pd.isna(v) for v in year_vals)

            detected = header_to_borough(raw_label)
            if detected:
                current_borough = detected

            if not all_null and current_borough:
                # This is a data row — record its borough
                norm = raw_label.lower().strip()
                label_borough[(norm, int(page))] = current_borough

    return label_borough


# ── 1920-1929 ──────────────────────────────────────────────────────────────────

year_cols_20 = [str(y) for y in range(1920, 1930)]
borough_map_20 = build_borough_map_from_raw(
    "archival-ridership-data/csv/1920-1929_ridership.csv",
    stations_col="STATIONS",
    year_sample_cols=year_cols_20,
)

# Load cleaned data and apply
df20c = pd.read_csv(OUT / "1920-1929_ridership_clean.csv")

def lookup_borough_20(row):
    norm = str(row["label"]).lower().strip() if pd.notna(row["label"]) else ""
    return borough_map_20.get((norm, int(row["_page"])))

df20c["borough"] = df20c.apply(lookup_borough_20, axis=1)
df20c.to_csv(OUT / "1920-1929_ridership_clean.csv", index=False)
covered = df20c["borough"].notna().sum()
print(f"1920-1929: borough filled for {covered}/{len(df20c)} rows "
      f"({covered/len(df20c)*100:.0f}%)")


# ── 1930-1939 ──────────────────────────────────────────────────────────────────

year_cols_30 = [str(y) for y in range(1930, 1940)]
borough_map_30 = build_borough_map_from_raw(
    "archival-ridership-data/csv/1930-1939 Ridership.csv",
    stations_col="STATIONS",
    year_sample_cols=year_cols_30,
)

df30c = pd.read_csv(OUT / "1930-1939_ridership_clean.csv")

def lookup_borough_30(row):
    norm = str(row["label"]).lower().strip() if pd.notna(row["label"]) else ""
    return borough_map_30.get((norm, int(row["_page"])))

df30c["borough"] = df30c.apply(lookup_borough_30, axis=1)
df30c.to_csv(OUT / "1930-1939_ridership_clean.csv", index=False)
covered = df30c["borough"].notna().sum()
print(f"1930-1939: borough filled for {covered}/{len(df30c)} rows "
      f"({covered/len(df30c)*100:.0f}%)")


# ── 1940-1995: segment → borough ───────────────────────────────────────────────
# Only segments that are unambiguously single-borough in the source document.
# Multi-borough lines left null.

SEGMENT_BOROUGH = {
    # Bronx
    "Concourse":                                  "Bronx",
    "Jerome Ave.":                                "Bronx",
    "White Plains Rd.":                           "Bronx",
    "Dyre Ave. Opened 5/15/41":                   "Bronx",
    "Burnside Ave. Closed 8/31/58":               "Bronx",
    "Pelham":                                     "Bronx",
    "3 Av Elevated Bronx segment Closed 4/28/73": "Bronx",
    "South Bronx CBD":                            "Bronx",
    # Manhattan
    "Midtown":                                    "Manhattan",
    "Valley":                                     "Manhattan",
    "Downtown":                                   "Manhattan",
    "2 Av Elevated Closed 6/11/40":               "Manhattan",
    "3 Av Elevated Manhattan Closed 5/12/55":     "Manhattan",
    "Manh. Transfer":                             "Manhattan",
    # Queens
    "Astoria":                                    "Queens",
    "Queens Blvd.":                               "Queens",
    "Archer Ave. Opened 12/11/88":                "Queens",
    "Rockaways Opened 6/28/56":                   "Queens",
    "Flushing":                                   "Queens",
    "Long Is. City CBD":                          "Queens",
    "Queens Transfer":                            "Queens",
    # Brooklyn
    "Canarsie":                                   "Brooklyn",
    "Myrtle Ave.":                                "Brooklyn",
    "Brighton":                                   "Brooklyn",
    "Sea Beach":                                  "Brooklyn",
    "West End":                                   "Brooklyn",
    "6 Ave./Culver":                              "Brooklyn",
    "Culver Shuttle Closed 5/11/75":              "Brooklyn",
    "Neptune-Ditmas Part of Culver El until 10/29/54": "Brooklyn",
    "5 Av Elevated Closed 5/31/40":               "Brooklyn",
    "Nostrand Ave.":                              "Brooklyn",
    "Sumner-Vandrbilt Closed 10/3/69":            "Brooklyn",
    "Lexington Av El Closed 10/13/50":            "Brooklyn",
    "9 Av Elevated Closed 6/11/40":               "Brooklyn",
    "Fulton St. El W. of Rock. Av Closed 5/31/40": "Brooklyn",
    "Franklin Ave.":                              "Brooklyn",
    "Eastern Pkwy.":                              "Brooklyn",
    "Rock Av-Grant Closed 4/27/56":               "Brooklyn",
    "80St-Lefferts Bl Listed above.":             "Brooklyn",
    "Lefferts Bl-80 St.":                         "Brooklyn",
    "Lefferts Bl-80 St. Part of Fulton El until 4/27/56": "Brooklyn",
    "4 Ave.":                                     "Brooklyn",
    "Part of Fulton El until 4/27/56":            "Brooklyn",
    "Brooklyn CBD":                               "Brooklyn",
    "Brooklyn Transfer":                          "Brooklyn",
    # Multi-borough — intentionally null (not in this dict)
    # 8 Ave., Broadway/7 Ave., Lenox Ave., Lexington Ave.,
    # Jamaica, Crosstown, Fulton St., etc.
}

df40c = pd.read_csv(OUT / "1940-1995_ridership_clean.csv")
df40c["borough"] = df40c["segment"].map(SEGMENT_BOROUGH)
df40c.to_csv(OUT / "1940-1995_ridership_clean.csv", index=False)
covered = df40c["borough"].notna().sum()
print(f"1940-1995: borough filled for {covered}/{len(df40c)} rows "
      f"({covered/len(df40c)*100:.0f}%)")
null_segs = df40c[df40c["borough"].isna()]["segment"].dropna().unique()
print(f"  Segments left null (multi-borough): {sorted(set(null_segs))[:15]}")


# ── Pass 2: station-level borough lookup for multi-borough segments ────────────
# Source: Wikipedia per-line and per-station articles (see BIBLIOGRAPHY.md).
# Keys are (label_normalized, segment); values are borough strings.
# Only entries where borough is unambiguous from the source article are included.

STATION_BOROUGH_WEB = {
    # 8 Ave. — IND Eighth Avenue Line (A/C/E upper Manhattan portion)
    # All stations in this segment's source-document listing are in Manhattan
    # (72 St.–207 St. on the upper West Side / Washington Heights / Inwood).
    # Source: Wikipedia "IND Eighth Avenue Line"
    ("72 st.", "8 Ave."):              "Manhattan",
    ("81 st.", "8 Ave."):              "Manhattan",
    ("86 st.", "8 Ave."):              "Manhattan",
    ("96 st.", "8 Ave."):              "Manhattan",
    ("cathedral pkwy.", "8 Ave."):     "Manhattan",
    ("103 st.", "8 Ave."):             "Manhattan",
    ("116 st.", "8 Ave."):             "Manhattan",
    ("125 st.", "8 Ave."):             "Manhattan",
    ("135 st.", "8 Ave."):             "Manhattan",
    ("145 st.", "8 Ave."):             "Manhattan",
    ("155 st.", "8 Ave."):             "Manhattan",
    ("163 st.", "8 Ave."):             "Manhattan",
    ("168 st.", "8 Ave."):             "Manhattan",
    ("175 st.", "8 Ave."):             "Manhattan",
    ("181 st.", "8 Ave."):             "Manhattan",
    ("190 st.", "8 Ave."):             "Manhattan",
    ("207 st.", "8 Ave."):             "Manhattan",
    ("dyckman st./200 st.", "8 Ave."): "Manhattan",

    # Broadway/7 Ave. — IRT Broadway–Seventh Avenue Line (1/2/3 upper Manhattan portion)
    # All stations in this segment listing are in Manhattan.
    # 225 St. (Marble Hill) is geographically north of the Harlem River ship canal
    # but is administered as part of Manhattan County; MTA lists it as Manhattan.
    # Source: Wikipedia "IRT Broadway–Seventh Avenue Line"; "Marble Hill–225th Street station"
    ("66 st.", "Broadway/7 Ave."):                   "Manhattan",
    ("72 st.", "Broadway/7 Ave."):                   "Manhattan",
    ("79 st.", "Broadway/7 Ave."):                   "Manhattan",
    ("86 st.", "Broadway/7 Ave."):                   "Manhattan",
    ("91 st. (closed 2/2/59)", "Broadway/7 Ave."):   "Manhattan",
    ("91 st. (closed 2/59)", "Broadway/7 Ave."):     "Manhattan",
    ("96 st.", "Broadway/7 Ave."):                   "Manhattan",
    ("cathedral pkwy.", "Broadway/7 Ave."):          "Manhattan",
    ("103 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("116 st./columbia univ.", "Broadway/7 Ave."):   "Manhattan",
    ("125 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("137 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("145 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("157 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("181 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("191 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("207 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("215 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("225 st.", "Broadway/7 Ave."):                  "Manhattan",  # Marble Hill; administratively Manhattan
    ("231 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("238 st.", "Broadway/7 Ave."):                  "Manhattan",
    ("242 st.", "Broadway/7 Ave."):                  "Bronx",       # Van Cortlandt Park–242 St terminal, Bronx
    ("dyckman st.", "Broadway/7 Ave."):              "Manhattan",

    # Crosstown — IND Crosstown Line (G train Brooklyn portion)
    # All stations in this segment listing are in Brooklyn.
    # (The G train's two Queens stations — Court Square, 21 St. — are not in the dataset.)
    # Source: Wikipedia "IND Crosstown Line"
    ("nassau ave.", "Crosstown"):               "Brooklyn",
    ("greenpoint ave.", "Crosstown"):           "Brooklyn",
    ("broadway", "Crosstown"):                  "Brooklyn",
    ("flushing ave.", "Crosstown"):             "Brooklyn",
    ("myrtle/willoughby aves.", "Crosstown"):   "Brooklyn",
    ("bedford/nostrand aves.", "Crosstown"):    "Brooklyn",
    ("classon ave.", "Crosstown"):              "Brooklyn",
    ("clinton/washington aves.", "Crosstown"):  "Brooklyn",

    # Fulton St. — IND Fulton Street Line (A/C through Brooklyn into Queens)
    # Source: Wikipedia "IND Fulton Street Line"; per-station articles for
    # Grant Ave., 104th St., 111th St., Lefferts Blvd., Liberty Ave., Shepherd Ave.
    ("clinton/washington aves.", "Fulton St."): "Brooklyn",
    ("franklin ave.", "Fulton St."):            "Brooklyn",
    ("kingston/throop aves.", "Fulton St."):    "Brooklyn",
    ("nostrand ave.", "Fulton St."):            "Brooklyn",
    ("ralph ave.", "Fulton St."):               "Brooklyn",
    ("rockaway ave.", "Fulton St."):            "Brooklyn",
    ("shepherd ave. (opened 11/28/48)", "Fulton St."):  "Brooklyn",
    ("shephard ave. (opened 11/28/48)", "Fulton St."):  "Brooklyn",  # OCR spelling variant
    ("utica ave.", "Fulton St."):               "Brooklyn",
    ("van siclen ave. (opened 11/28/48)", "Fulton St."): "Brooklyn",
    ("liberty ave. (opened 11/28/48)", "Fulton St."):    "Brooklyn",
    ("euclid ave. (opened 11/28/48)", "Fulton St."):     "Brooklyn",
    ("grant ave. (opened 4/29/56)", "Fulton St."):       "Brooklyn",  # last Brooklyn station per Wikipedia
    ("111 st.", "Fulton St."):                  "Queens",
    ("104 st.", "Fulton St."):                  "Queens",
    ("lefferts blvd", "Fulton St."):            "Queens",

    # Jamaica — BMT Jamaica Line (J/Z) Brooklyn + Queens portion
    # Brooklyn stations: Hewes St. through Cypress Hills
    # Queens stations: Elderts Lane onward
    # Source: Wikipedia "BMT Jamaica Line"; per-station articles
    ("hewes st.", "Jamaica"):               "Brooklyn",
    ("lorimer st.", "Jamaica"):             "Brooklyn",
    ("marcy ave.", "Jamaica"):              "Brooklyn",
    ("flushing ave.", "Jamaica"):           "Brooklyn",
    ("myrtle ave./broadway", "Jamaica"):    "Brooklyn",
    ("kosciusko st.", "Jamaica"):           "Brooklyn",
    ("gates ave.", "Jamaica"):              "Brooklyn",
    ("halsey st.", "Jamaica"):              "Brooklyn",
    ("chauncey st.", "Jamaica"):            "Brooklyn",
    ("alabama ave.", "Jamaica"):            "Brooklyn",
    ("van siclen ave.", "Jamaica"):         "Brooklyn",
    ("cleveland st.", "Jamaica"):           "Brooklyn",
    ("norwood ave.", "Jamaica"):            "Brooklyn",
    ("crescent st.", "Jamaica"):            "Brooklyn",
    ("cypress hills", "Jamaica"):           "Brooklyn",
    ("liberty ave.", "Jamaica"):            "Brooklyn",  # East New York, Brooklyn
    ("elderts lane", "Jamaica"):            "Queens",
    ("forest pkwy.", "Jamaica"):            "Queens",
    ("woodhaven blvd.", "Jamaica"):         "Queens",
    ("104-102 sts.", "Jamaica"):            "Queens",
    ("111 st.", "Jamaica"):                 "Queens",
    ("121 st.", "Jamaica"):                 "Queens",
    ("metropolitan ave. (closed 4/15/85)", "Jamaica"):     "Queens",
    ("queens blvd. (closed 4/15/85)", "Jamaica"):          "Queens",
    ("160 st. (closed 9/11/77)", "Jamaica"):               "Queens",
    ("168 st. (closed 9/11/77)", "Jamaica"):               "Queens",
    ("sutphin blvd.-lirr (closed 9/11/77)", "Jamaica"):    "Queens",

    # Lenox Ave. — IRT Lenox Avenue Line (2/3 Harlem terminal branch)
    # All stations are in Manhattan (Harlem neighborhood).
    # Source: Wikipedia "IRT Lenox Avenue Line"
    ("110 st./central park n.", "Lenox Ave."): "Manhattan",
    ("116 st.", "Lenox Ave."):                 "Manhattan",
    ("125 st.", "Lenox Ave."):                 "Manhattan",
    ("135 st.", "Lenox Ave."):                 "Manhattan",
    ("145 st.", "Lenox Ave."):                 "Manhattan",
    ("148 st. (opened 5/13/68)", "Lenox Ave."): "Manhattan",

    # Lexington Ave. — IRT Lexington Avenue Line (4/5/6 Manhattan portion)
    # All stations in this listing are in Manhattan (Upper East Side / East Harlem).
    # The Lexington Ave. segment in the 1940-1995 data covers only the Manhattan
    # stations; Bronx stations appear under Pelham, White Plains Rd., etc.
    # Source: Wikipedia "IRT Lexington Avenue Line"
    ("68 st.", "Lexington Ave."):  "Manhattan",
    ("77 st.", "Lexington Ave."):  "Manhattan",
    ("86 st.", "Lexington Ave."):  "Manhattan",
    ("96 st.", "Lexington Ave."):  "Manhattan",
    ("103 st.", "Lexington Ave."): "Manhattan",
    ("110 st.", "Lexington Ave."): "Manhattan",
    ("116 st.", "Lexington Ave."): "Manhattan",
    ("125 st.", "Lexington Ave."): "Manhattan",
}

# ── Segment-agnostic fallbacks ─────────────────────────────────────────────────
# Stations whose borough is unambiguous from their name alone, regardless of
# which segment they appear under (handles segment=NaN cases).
# Only included where the station name uniquely identifies a single borough.

LABEL_ONLY_BOROUGH = {
    # Manhattan — downtown / Lower East Side elevated stations
    "canal st./2 av. el (closed 6/13/42)":    "Manhattan",
    "canal st./3 av. el (closed 5/11/55)":    "Manhattan",
    "canal st./broadway":                      "Manhattan",
    "canal/church sts.":                       "Manhattan",
    "canal/varick sts.":                       "Manhattan",
    "chatham sq./2 av. el (closed 6/13/42)":  "Manhattan",
    "chatham sq./3 av. el (closed 5/11/55)":  "Manhattan",
    "grand st./2 av el (closed 6/13/42)":     "Manhattan",
    "grand st./2 av. el (closed 6/13/42)":    "Manhattan",
    "grand st./3 av el (closed 5/11/55)":     "Manhattan",
    "grand st./3 av. el (closed 5/11/55)":    "Manhattan",
    "franklin st./6 av. el (closed 6/11/40)": "Manhattan",
    "franklin st.":                            "Manhattan",   # Tribeca, IND/BMT
    "delancey/essex sts.":                     "Manhattan",
    "east broadway":                           "Manhattan",
    "worth st./lex av. line (closed 9/1/62)":  "Manhattan",
    "worth st./lex. line (closed 9/1/62)":     "Manhattan",
    # Bronx — Pelham line stations (IRT Pelham Bay Line, all in Bronx)
    "baychester ave.":        "Bronx",
    "buhre ave.":             "Bronx",
    "castle hill ave.":       "Bronx",
    "elder ave.":             "Bronx",
    "e. 177 st./parkchester": "Bronx",
    "gun hill rd.":           "Bronx",
    "middletown rd.":         "Bronx",
    "morris park":            "Bronx",
    "morrison/soundview aves.": "Bronx",
    "pelham pkwy.":           "Bronx",
    "st. lawrence ave.":      "Bronx",
    "westchester square":     "Bronx",
    "whitlock ave.":          "Bronx",
    "zerega ave.":            "Bronx",
    # Bronx — South Bronx elevated / Pelham Bay stations
    "brook ave.":             "Bronx",
    "cypress ave.":           "Bronx",
    "e. 143 st.":             "Bronx",
    "e. 149 st.":             "Bronx",
    "hunts pt. ave.":         "Bronx",
    "longwood ave.":          "Bronx",
    # Bronx — 3rd Ave El and Concourse-area stations
    "3 ave./138 st.":                                   "Bronx",
    "3 ave./149 st. (el sta. closed 4/28/73)":          "Bronx",
    "3 ave./149 st. (el sts. closed 4/28/73)":          "Bronx",
    "133 st./3 av. el (closed 5/11/55)":               "Bronx",
    "138 st./3 av. el (closed 5/11/55)":               "Bronx",
    "143 st./3 av. el (closed 5/11/55)":               "Bronx",
    "145 st./3 av. el (closed 5/11/55)":               "Bronx",
    "138 st./grand concourse":                          "Bronx",
    "149 st./grand concourse":                          "Bronx",
    # Brooklyn — IND Fulton/A-train stations (already in segment lookup but segment may be NaN)
    "euclid ave. (opened 11/28/48)":        "Brooklyn",
    "grant ave. (opened 4/29/56)":          "Brooklyn",
    "kingston/throop aves.":                "Brooklyn",
    "liberty ave. (opened 11/28/48)":       "Brooklyn",
    "nostrand ave.":                        "Brooklyn",
    "ralph ave.":                           "Brooklyn",
    "rockaway ave.":                        "Brooklyn",
    "shepherd ave. (opened 11/28/48)":      "Brooklyn",
    "shephard ave. (opened 11/28/48)":      "Brooklyn",
    "utica ave.":                           "Brooklyn",
    "van siclen ave. (opened 11/28/48)":    "Brooklyn",
    "clinton/washington aves.":             "Brooklyn",
    "franklin ave.":                        "Brooklyn",

    # ── Third Avenue El — Manhattan stations ──
    # The 3rd Ave El crossed from Manhattan into the Bronx via the Willis Avenue
    # Bridge (~129th–133rd St). 129th St and below = Manhattan; 133rd St and
    # above = Bronx. Source: IRT Third Avenue Line history (training knowledge,
    # consistent with Wikipedia "IRT Third Avenue Line" and "Third Avenue El").
    "34th street":              "Manhattan",   # 3rd Ave El, Manhattan
    "24th street ferry":        "Manhattan",   # 3rd Ave El, Manhattan
    "42d street":               "Manhattan",   # 3rd Ave El, Manhattan
    "47th street":              "Manhattan",   # 3rd Ave El, Manhattan
    "50th street (to july '25)": "Manhattan",  # 3rd Ave El, Manhattan
    "53d street":               "Manhattan",   # 3rd Ave El, Manhattan
    "59th street":              "Manhattan",   # 3rd Ave El, Manhattan
    "67th street":              "Manhattan",   # 3rd Ave El, Manhattan
    "73d street":               "Manhattan",   # 3rd Ave El, Manhattan
    "84th street":              "Manhattan",   # 3rd Ave El, Manhattan
    "89th street":              "Manhattan",   # 3rd Ave El, Manhattan
    "99th street":              "Manhattan",   # 3rd Ave El, Manhattan
    "106th street":             "Manhattan",   # 3rd Ave El, East Harlem, Manhattan
    "116th street":             "Manhattan",   # 3rd Ave El, East Harlem, Manhattan
    "123d street":              "Manhattan",   # 3rd Ave El, Manhattan (between 116 and 129)
    "129th street":             "Manhattan",   # 3rd Ave El, last Manhattan station
    "willis avenue (to 4/15/24)": "Manhattan", # Willis Ave Bridge approach, Manhattan side
    # Third Avenue El — Bronx stations (133rd St northward)
    "133d street":              "Bronx",
    "138th street":             "Bronx",
    "143d street":              "Bronx",
    "149th street":             "Bronx",
    "155th street":             "Bronx",       # 3rd Ave El, Bronx
    "156th street":             "Bronx",
    "161st street":             "Bronx",
    "166th street":             "Bronx",
    "169th street":             "Bronx",
    "claremont parkway":        "Bronx",
    "174th street":             "Bronx",
    "177th street":             "Bronx",
    "180th street":             "Bronx",
    "183d street":              "Bronx",
    "fordham road":             "Bronx",
    "bronx park":               "Bronx",
    "200th street":             "Bronx",
    "204th street":             "Bronx",
    "williamsbridge-210th street": "Bronx",    # Williamsbridge neighborhood, NE Bronx
    # 1930s data variants (same stations, slightly different spelling)
    "133rd street":             "Bronx",
    "138th street":             "Bronx",
    "143rd street":             "Bronx",
    "149th street":             "Bronx",
    "161st street":             "Bronx",
    "166th street":             "Bronx",
    "169th street":             "Bronx",
    "174th street":             "Bronx",
    "177th street":             "Bronx",
    "180th street":             "Bronx",
    "183rd street":             "Bronx",
    # Other identifiable 1930s elevated stations
    "24th street":              "Manhattan",   # 6th Ave El or 3rd Ave El, Manhattan
    "34th street":              "Manhattan",
    "39th street":              "Brooklyn",    # BMT 4th Ave line, Bay Ridge, Brooklyn
    "42d street":               "Manhattan",
    "50th street":              "Manhattan",
    "54th street":              "Brooklyn",    # BMT 4th Ave line, Brooklyn
    "62nd street":              "Brooklyn",    # BMT 4th Ave line, Bay Ridge, Brooklyn

    # ── IND Eighth Avenue Line opening stations (Sept. 10, 1932) — Manhattan ──
    # The initial route ran 207th St → Chambers St, entirely in Manhattan.
    # Source: Wikipedia "IND Eighth Avenue Line"
    "103rd street (from sept. 10, 1932)":   "Manhattan",
    "110th street (from sept. 10, 1932)":   "Manhattan",
    "116th street (from sept. 10, 1932)":   "Manhattan",
    "125th street (from sept. 10, 1932)":   "Manhattan",
    "135th street (from sept. 10, 1932)":   "Manhattan",
    "145th street (from sept. 10, 1932)":   "Manhattan",
    "14th street (from sept. 10, 1932)":    "Manhattan",
    "155th street (from sept. 10, 1932)":   "Manhattan",
    "163rd street (from sept. 10, 1932)":   "Manhattan",
    "168th street (from sept. 10, 1932)":   "Manhattan",
    "175th street (from sept. 10, 1932)":   "Manhattan",
    "181st street (from sept. 10, 1932)":   "Manhattan",
    "207th street (from sept. 10, 1932)":   "Manhattan",
    "23rd street (from sept. 10, 1932)":    "Manhattan",
    "34th street (from sept. 10, 1932)":    "Manhattan",
    "42nd street (from sept. 10, 1932)":    "Manhattan",
    "4th street (from sept. 10, 1932)":     "Manhattan",
    "50th street (from sept. 10, 1932)":    "Manhattan",
    "59th street (from sept. 10, 1932)":    "Manhattan",
    "72nd street (from sept. 10, 1932)":    "Manhattan",
    "81st street (from sept. 10, 1932)":    "Manhattan",
    "86th street (from sept. 10, 1932)":    "Manhattan",
    "96th street (from sept. 10, 1932)":    "Manhattan",
    "dyckman street (from sept. 10, 1932)": "Manhattan",
    "overlook terrace (from sept. 10, 1932)": "Manhattan",
    "spring street (from sept. 10, 1932)":  "Manhattan",
    "canal street (from sept. 10, 1932)":   "Manhattan",
    "chambers street (from sept. 10, 1932)":"Manhattan",
    # IND extension openings — Manhattan
    "cortlandt-nassau street (from february 1, 1933)": "Manhattan",
    "broadway-lafayette street (from january 1, 1936)": "Manhattan",
    "second avenue (from january 1, 1936)": "Manhattan",
    "delancey street (from january 1, 1936)": "Manhattan",
    "east broadway (from january 1, 1936)": "Manhattan",
    # IND extension openings — Brooklyn
    # Court St, High St, Jay St opened Feb 1933 as 8th Ave line extension to Brooklyn
    "court street (from february 1, 1933)": "Brooklyn",
    "high street (from february 24, 1933)": "Brooklyn",
    "jay street-borough hall (from february 1, 1933)": "Brooklyn",
    # IND Fulton Street Line / Crosstown opened April 9, 1936 — all Brooklyn
    "hoyt-schermerhorn streets (from april 9, 1936)":  "Brooklyn",
    "clinton-washington avenues (from april 9, 1936)": "Brooklyn",
    "kingston-throop avenues (from april 9, 1936)":    "Brooklyn",
    "lafayette avenue (from april 9, 1936)":           "Brooklyn",
    "nostrand avenue (from april 9, 1936)":            "Brooklyn",
    "ralph avenue (from april 9, 1936)":               "Brooklyn",
    "rockaway avenue (from april 9, 1936)":            "Brooklyn",
    "utica avenue (from april 9, 1936)":               "Brooklyn",
    "franklin avenue (from april 9, 1936)":            "Brooklyn",
    "york street (from april 9, 1936)":                "Brooklyn",

    # ── Other identifiable 1930s stations ──
    "grand central":              "Manhattan",
    "grand central (lex. ave.)":  "Manhattan",
    "times square":               "Manhattan",
    "borough hall":               "Brooklyn",
    "queens plaza":               "Queens",
    "dean street":                "Brooklyn",    # BMT Brighton Beach Line
    "norton's point":             "Brooklyn",    # Coney Island terminus, Brooklyn
    "park place":                 "Brooklyn",    # BMT Brighton Beach, Brooklyn

    # ── Identifiable 1920s stations (from 1920-1929 source) ──
    "grand central (to 12/2/23)":      "Manhattan",  # Grand Central, pre-Dec 1923 routing
    "avenue l":                        "Brooklyn",   # BMT Sea Beach / West End, Brooklyn
    "eastern parkway":                 "Brooklyn",   # BMT Brighton Beach Line, Brooklyn
    "flatlands":                       "Brooklyn",   # BMT Canarsie / New Lots area, Brooklyn
    "new lots ave.":                   "Brooklyn",   # BMT New Lots Line, Brooklyn
    "van sicklen ave.":                "Brooklyn",   # BMT Canarsie Line, Brooklyn
    "central (lexington avenue)":      "Queens",     # IRT Flushing Line at Central Ave, Queens
    "jurens plaza (from 8/1/20)":      "Queens",     # Queens station opened Aug 1, 1920
    "lawrence avenue conn":            "Brooklyn",   # BMT connection at Lawrence Ave, Brooklyn
}

def apply_web_borough(df):
    """Apply station-level borough lookup to rows still missing borough."""
    def lookup(row):
        if pd.notna(row.get("borough")):
            return row["borough"]
        label_norm = str(row.get("label", "")).lower().strip()
        seg = str(row.get("segment", "")) if pd.notna(row.get("segment")) else ""
        # Try segment-specific lookup first
        result = STATION_BOROUGH_WEB.get((label_norm, seg))
        if result:
            return result
        # Fall back to label-only lookup
        return LABEL_ONLY_BOROUGH.get(label_norm)
    return df.apply(lookup, axis=1)

# Apply to all three cleaned source files and re-save
for fname, label_col in [
    ("1920-1929_ridership_clean.csv", "label"),
    ("1930-1939_ridership_clean.csv", "label"),
    ("1940-1995_ridership_clean.csv", "label"),
]:
    path = OUT / fname
    df = pd.read_csv(path)
    df["borough"] = apply_web_borough(df)
    df.to_csv(path, index=False)

print("Pass 2 (web research) applied to cleaned files.")


# ── Rebuild master dataset ─────────────────────────────────────────────────────
print("\nRebuilding master dataset...")
import subprocess
result = subprocess.run(["python3", "build_master_dataset.py"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("STDERR:", result.stderr[:500])
