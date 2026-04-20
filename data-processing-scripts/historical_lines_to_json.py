"""Convert nyc-historical-lines/*.numbers to visualization/data/historical-lines.json.

Headers vary across files (mixed capitalization, occasional typos, column order).
We match by header name where possible and fall back to the filename prefix for
the company field so a spreadsheet typo (e.g. "BTM") doesn't propagate.
"""

import glob
import json
import os
import re

from numbers_parser import Document

SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "nyc-historical-lines")
OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "visualization", "data", "historical-lines.json"
)


def parse_year(s):
    if not s:
        return None
    m = re.search(r"\b(18|19|20)\d{2}\b", str(s))
    return int(m.group(0)) if m else None


def clean(s):
    if s is None:
        return None
    s = str(s).replace("\xa0", " ").strip()
    return s or None


def main():
    files = sorted(glob.glob(os.path.join(SRC_DIR, "*.numbers")))
    lines_out = []
    for f in files:
        base = os.path.basename(f).replace(".numbers", "")
        company_tag = base.split("_")[0].upper()
        doc = Document(f)
        for sheet in doc.sheets:
            for tbl in sheet.tables:
                rows = list(tbl.rows(values_only=True))
                if not rows:
                    continue
                headers = [
                    (h.strip().lower() if isinstance(h, str) else None) for h in rows[0]
                ]
                idx = {h: i for i, h in enumerate(headers) if h}

                def find(*names):
                    for n in names:
                        if n in idx:
                            return idx[n]
                    return None

                i_station = find("station", "name", "names")
                i_opened = find("opened", "opening date")
                i_closed = find("closed", "closing date")
                i_lat = find("latitude")
                i_lng = find("longitude", "longitide")
                i_company = find("company")
                i_services = find("services")
                i_notes = find("transfers and notes", "transfers  and notes", "notes")

                stations = []
                for r in rows[1:]:
                    if not r or all(v is None for v in r):
                        continue
                    name = clean(r[i_station]) if i_station is not None else None
                    if not name:
                        continue
                    lat = r[i_lat] if i_lat is not None else None
                    lng = r[i_lng] if i_lng is not None else None
                    try:
                        lat = float(lat) if lat is not None else None
                    except (TypeError, ValueError):
                        lat = None
                    try:
                        lng = float(lng) if lng is not None else None
                    except (TypeError, ValueError):
                        lng = None
                    # Some spreadsheets have the lat/lng column headers swapped
                    # relative to the values. NYC sits near lat≈40, lng≈-74, so
                    # swap when the values clearly belong in the other slot.
                    if lat is not None and lng is not None:
                        lat_ok = 24 <= lat <= 50
                        lng_ok = -125 <= lng <= -65
                        swap_ok = 24 <= lng <= 50 and -125 <= lat <= -65
                        if not (lat_ok and lng_ok) and swap_ok:
                            lat, lng = lng, lat
                        # Positive-longitude typo (e.g. 73.88 instead of -73.88).
                        if 24 <= lat <= 50 and 65 <= lng <= 125:
                            lng = -lng
                    opened_raw = clean(r[i_opened]) if i_opened is not None else None
                    closed_raw = clean(r[i_closed]) if i_closed is not None else None
                    co_raw = clean(r[i_company]) if i_company is not None else None
                    co = (co_raw or company_tag).upper()
                    if co not in ("IRT", "BMT", "IND"):
                        co = company_tag
                    stations.append({
                        "station": name,
                        "latitude": lat,
                        "longitude": lng,
                        "opened_year": parse_year(opened_raw),
                        "opened_raw": opened_raw,
                        "closed_year": parse_year(closed_raw),
                        "closed_raw": closed_raw,
                        "company": co,
                        "services": clean(r[i_services]) if i_services is not None else None,
                        "notes": clean(r[i_notes]) if i_notes is not None else None,
                    })
                lines_out.append({
                    "line": base,
                    "company": company_tag,
                    "stations": stations,
                })

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as fh:
        json.dump(lines_out, fh, indent=2)
    total = sum(len(l["stations"]) for l in lines_out)
    located = sum(
        1 for l in lines_out for s in l["stations"]
        if s["latitude"] is not None and s["longitude"] is not None
    )
    print(f"Wrote {OUT_PATH}: {len(lines_out)} lines, {total} stations ({located} with coords)")


if __name__ == "__main__":
    main()
