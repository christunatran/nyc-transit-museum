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
python3 ocr_pipline.py --pdf "1930-1939 Ridership.pdf" --output "csv/1930-1939 Ridership.csv"
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--pdf` | required | Path to input PDF |
| `--output` | `output.csv` | Path to output CSV |
| `--dpi` | 300 | Render resolution. Use 150 to stay under Claude's 5MB image limit |
| `--max-pages` | None | Limit pages processed (useful for testing) |

## Configuration (top of script)

| Variable | Value | Notes |
|----------|-------|-------|
| `DPI` | 150 | 300 DPI exceeds Claude's 5MB/image limit on dense pages |
| `MAX_PAGES` | None | Set to an integer to test on a subset |
| `MODEL` | `claude-sonnet-4-6` | Sonnet is ~5x cheaper than Opus with comparable OCR accuracy |
| `max_tokens` | 16384 | Must be high enough for large tables — 4096 causes JSON truncation |

## Output files

Each PDF produces two files in `csv/`:
- `<name>.csv` — flattened rows with `_page` and `_page_desc` metadata columns
- `<name>_raw.json` — full per-page extraction results for debugging

## Extracted data

| File | Rows |
|------|------|
| `1920-1929_ridership.csv` | 393 |
| `1930-1939 Ridership.csv` | 879 |
| `1940-1995-Ridership-Part1.csv` | 3,976 |
| `1940-1995-Ridership-Part2.csv` | 1,294 |
| `1940-2011 Historical Ridership.csv` | 72 |
| `Rapid Transit Ridership 1932-1935.csv` | 25 |
| `Rapid Transit Ridership 1934-1937.csv` | 23 |
| **Total** | **6,662** |

## Known issues

- Pages with parse errors (`✗ parse_error`) indicate Claude returned malformed JSON — usually means `max_tokens` is too low or the table is unusually dense. Check the `_raw.json` file for the truncated response.
- Pages with image errors indicate the rendered PNG exceeded 5MB — lower `--dpi` to fix.
- Cover pages, intro text, and chart-only pages are skipped with `— No data`.
