# NYC Transit Archival Ridership OCR Pipeline

Extracts tabular ridership data from scanned historical NYC Transit Commission PDFs using Claude Vision API, outputting clean CSVs.

## How it works

1. **Render** — Each PDF page is rendered to a grayscale PNG image using PyMuPDF (`fitz`)
2. **Extract** — Each image is sent to the Claude Vision API with a prompt asking for structured JSON containing the table headers and rows
3. **Flatten** — All extracted pages are merged into a single list of row dicts
4. **Save** — Output is written to CSV (and a raw JSON file for debugging)

## Requirements

```bash
pip install pymupdf anthropic
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
python3 ocr_pipline.py --pdf "1930-1939 Ridership.pdf" --output "csv/1930-1939 Ridership.csv" --dpi 150
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--pdf` | required | Path to input PDF |
| `--output` | `output.csv` | Path to output CSV |
| `--dpi` | 300 | Render resolution. Use 150 to stay under Claude's 5MB image limit |
| `--max-pages` | None | Limit pages processed (useful for testing) |
| `--start-page` | 1 | Resume from a specific page; merges with existing JSON so already-extracted pages are not re-billed |
| `--json-output` | auto | Path to raw JSON (used as merge source when `--start-page` > 1) |

## Configuration (top of script)

| Variable | Value | Notes |
|----------|-------|-------|
| `DPI` | 150 | 300 DPI exceeds Claude's 5MB/image limit on dense pages |
| `MAX_PAGES` | None | Set to an integer to test on a subset |
| `MODEL` | `claude-sonnet-4-6` | Sonnet is ~5x cheaper than Opus with comparable OCR accuracy |
| `max_tokens` | 16384 | Must be high enough for large tables — 4096 causes JSON truncation |

## Output files

Each PDF produces two files:
- `csv/<name>.csv` — flattened rows with `_page` and `_page_desc` metadata columns
- `json/<name>_raw.json` — full per-page extraction results for debugging

---

## Source documents & data dictionary

All fiscal years end June 30 unless otherwise noted. "Registrations" = fare-paying passengers counted at turnstiles.

---

### `1920-1929 Ridership.pdf` → `csv/1920-1929_ridership.csv`

**Coverage:** Fiscal years ending June 30, 1920–1929  
**Granularity:** Station-by-station fare collection, organized by line and borough  
**Operators covered:** IRT (Interborough Rapid Transit) subway and elevated divisions, BMT (New York Rapid Transit Corporation), company-owned surface lines in Brooklyn and Queens  
**Key columns:** Station name, annual passenger counts per year (1920–1929), line/division, borough recap totals

**What to know:**
- Grand total grows from ~2.4 billion passengers in 1920 to ~3.2 billion in 1929 (~33% increase)
- Subway division alone: ~955 million → ~1.28 billion
- New stations appear mid-decade as new lines opened — expansion is physically visible in the data
- Times Square, Grand Central, and major transfer hubs consistently show the highest individual station counts
- Elevated lines declining relative to subway as the decade progresses — the system was already shifting underground

---

### `1930-1939 Ridership.pdf` → `csv/1930-1939 Ridership.csv`

**Coverage:** Fiscal years ending June 30, 1930–1939  
**Granularity:** Station-by-station fare collection, same format as 1920s  
**Operators covered:** IRT subway/elevated, BMT (New York Rapid Transit Corp), IND (Independent System, opened Sept 1932)  
**Key columns:** Station name, annual passenger counts per year (1930–1939), line/division

**What to know:**
- Grand total drops from ~1.33 billion (rapid transit only) in 1930 to a Depression low around 1932–1933, then partially recovers by 1939
- IND starts from zero and grows steadily — you can watch a new transit system being born in the data
- 1939 World's Fair causes a notable spike in May/June ridership, explicitly flagged in source notes
- Surface/street railway lines in visible decline as buses take over

---

### `1940-1995-Ridership-Part1.pdf` + `1940-1995-Ridership-Part2.pdf` → `csv/1940-1995-Ridership-Part1.csv`, `csv/1940-1995-Ridership-Part2.csv`

**Coverage:** Annual station registrations, 1940–1995 (55 years continuous)  
**Granularity:** Every subway station, organized by line segment and geographic sector: North Manhattan/Bronx, Northern Queens, Southern Queens/Brooklyn, Manhattan CBD  
**Source:** MTA Office of Management and Budget  
**Key columns:** Station name, annual registration counts per year, sector grouping

**What to know:**
- Most granular document in the collection — station-level data for every year across 55 years
- Peak ~2 billion system-wide riders in 1946; long collapse to under 1 billion by mid-1970s; slow recovery through 80s–90s
- Includes a fare chronology: nickel fare held until 1948, then dime, tokens introduced 1953, rising to $1.50 by 1995
- Stations that closed mid-century show up as zeros — entire lines disappear (2nd Ave El, 3rd Ave El, various Brooklyn elevated lines)
- New stations appear when opened: Rockaways 1956, Archer Ave 1988, etc.
- Introductory notes explain the shift from IRT/BMT/IND private operators to unified city ownership in 1940

---

### `1940-2011 Historical Ridership.pdf` → `csv/1940-2011 Historical Ridership.csv`

**Coverage:** Calendar years 1940–2011  
**Granularity:** System-wide annual totals — no station breakdown  
**Key columns:** Year, subway ridership, bus ridership, combined total, average weekday ridership

**What to know:**
- The cleanest, most usable document for system-wide totals and timeline visualization
- Inline notes flag every major contextual event: fare increases, strikes (1966, 1980, 2005), 9/11, MetroCard launch 1994, free intermodal transfers 1997, bonus MetroCard 1998
- Subway ridership bottoms out around 976 million in 1976–1977 (height of NYC fiscal crisis)
- Recovery accelerates sharply after MetroCard and bonus fares launch in late 90s
- By 2008 ridership hits ~1.62 billion — approaching but not reaching the postwar peak

---

### `Rapid Transit Ridership 1932-1935.pdf` → `csv/Rapid Transit Ridership 1932-1935.csv`

**Coverage:** 1932–1935  
**Granularity:** System-level totals by operator  
**Source:** NYC Transit Commission  
**Key columns:** Operator name (IRT, BMT, IND, surface lines, H&M), annual ridership totals

**What to know:**
- Focused on the transition period when the IND was brand new
- IND grows from ~zero in 1932 to ~202 million by 1935
- IRT and BMT showing modest Depression-era declines
- Hudson & Manhattan Railroad (PATH predecessor) also tracked — relatively stable ~75–76 million
- Shows the city actively building new infrastructure during the Depression

---

### `Rapid Transit Ridership 1934-1937.pdf` → `csv/Rapid Transit Ridership 1934-1937.csv`

**Coverage:** 1934–1937  
**Granularity:** System-level totals by operator and borough  
**Source:** NYC Transit Commission  
**Key columns:** Operator/mode (rapid transit, bus by borough, surface rail), annual ridership totals, rides per capita

**What to know:**
- Bus ridership growing explosively — total bus trips nearly double from ~314 million (1934) to ~588 million (1937)
- Manhattan, Brooklyn, Queens, and Bronx bus lines broken out separately
- Rapid transit holding relatively steady while surface rail declines and buses take over
- Rides per capita included: ~377 in 1934, ~388 in 1937

---

## Coverage gaps

| Gap | Years | Notes |
|-----|-------|-------|
| Missing recent data | 2012–present | MTA publishes annual ridership on the [MTA Open Data portal](https://data.ny.gov) |
| Notable events in gap | 2012 Superstorm Sandy, 2020 COVID-19 | Both caused dramatic ridership drops visible in public data |

---

## Extracted data summary

| File | Rows |
|------|------|
| `1920-1929_ridership.csv` | 24 |
| `1930-1939 Ridership.csv` | 879 |
| `1940-1995-Ridership-Part1.csv` | 3,976 |
| `1940-1995-Ridership-Part2.csv` | 1,294 |
| `1940-2011 Historical Ridership.csv` | 72 |
| `Rapid Transit Ridership 1932-1935.csv` | 25 |
| `Rapid Transit Ridership 1934-1937.csv` | 23 |
| **Total** | **6,293** |

---

## Known issues

- Pages with `✗ parse_error` indicate Claude returned malformed JSON — usually means `max_tokens` is too low or the table is unusually dense. Check the `_raw.json` file for the truncated response. Use `--start-page` to reprocess only those pages without re-billing clean ones.
- Pages with image size errors indicate the rendered PNG exceeded 5MB — lower `--dpi` to fix.
- Cover pages, intro text, and chart-only pages are skipped with `— No data`.
