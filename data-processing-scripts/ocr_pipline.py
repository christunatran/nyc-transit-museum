"""
NYC Transit Ridership OCR Pipeline
-----------------------------------
Renders each PDF page at high DPI, sends to Claude Vision API,
and extracts tabular data as structured CSV.

Usage:
    python ocr_pipeline.py --pdf path/to/file.pdf --output results.csv

Requirements:
    pip install anthropic pymupdf
    export ANTHROPIC_API_KEY=your_key_here
"""

import fitz  # PyMuPDF
import anthropic
import base64
import csv
import json
import argparse
import os
import sys
from pathlib import Path


# ── Configuration ─────────────────────────────────────────────────────────────

DPI = 300          # Higher = better accuracy, slower + more tokens
MAX_PAGES = None   # Set to an integer to limit pages during testing e.g. 3
MODEL = "claude-sonnet-4-6"  # ~5x cheaper than opus, still accurate for tabular OCR


# ── Prompts ───────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a precise data extraction assistant specializing in 
historical transit documents. Your job is to extract tabular ridership data from 
scanned NYC Transit Commission reports and return it as clean structured JSON.

Rules:
- Extract ALL rows and columns you can read, even if some cells are unclear
- For unclear values, use null rather than guessing
- Preserve original column headers exactly as written
- If a page has no tabular data (cover page, notes page), return {"type": "no_data", "content": "description of page"}
- Numbers should be integers with no commas or formatting
- Return ONLY valid JSON, no markdown, no explanation
"""

TABLE_PROMPT = """Extract all tabular data from this page of a historical NYC 
transit ridership report. 

Return JSON in this format:
{
  "type": "table",
  "page_description": "brief description of what this page covers",
  "headers": ["col1", "col2", ...],
  "rows": [
    {"col1": value, "col2": value, ...},
    ...
  ]
}

If there are multiple separate tables on the page, return:
{
  "type": "multiple_tables", 
  "tables": [ ...array of table objects... ]
}

Extract every row you can see. Numbers should be plain integers (no commas).
"""


# ── Core Functions ─────────────────────────────────────────────────────────────

def pdf_to_images(pdf_path: str, dpi: int = DPI, start_page: int = 1) -> list[bytes]:
    """Render PDF pages to PNG images at specified DPI, starting from start_page (1-indexed)."""
    doc = fitz.open(pdf_path)
    images = []

    total = len(doc)
    start_idx = start_page - 1  # convert to 0-indexed
    end_idx = min(start_idx + MAX_PAGES, total) if MAX_PAGES else total
    pages_to_process = range(start_idx, end_idx)

    print(f"  Rendering {len(pages_to_process)} pages at {dpi} DPI (pages {start_page}–{end_idx})...")

    for i in pages_to_process:
        page = doc[i]
        # Scale matrix for desired DPI (72 is base DPI)
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)  # Grayscale saves tokens
        images.append(pix.tobytes("png"))
        print(f"    Page {i+1}/{total} rendered ({len(pix.tobytes('png')) // 1024}KB)")

    doc.close()
    return images


def extract_table_from_image(client: anthropic.Anthropic, image_bytes: bytes, page_num: int) -> dict:
    """Send a page image to Claude and extract structured table data."""
    
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=16384,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": TABLE_PROMPT
                        }
                    ],
                }
            ],
        )
        
        raw = response.content[0].text.strip()
        
        # Strip any accidental markdown code fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        result = json.loads(raw)
        result["page_number"] = page_num
        return result
        
    except json.JSONDecodeError as e:
        print(f"    WARNING: Could not parse JSON on page {page_num}: {e}")
        return {"type": "parse_error", "page_number": page_num, "raw": raw}
    except Exception as e:
        print(f"    ERROR on page {page_num}: {e}")
        return {"type": "error", "page_number": page_num, "error": str(e)}


def flatten_to_rows(extracted_pages: list[dict]) -> list[dict]:
    """Flatten all extracted page data into a single list of row dicts."""
    all_rows = []
    
    for page_data in extracted_pages:
        page_num = page_data.get("page_number", "?")
        
        if page_data.get("type") == "table":
            for row in page_data.get("rows", []):
                row["_page"] = page_num
                row["_page_desc"] = page_data.get("page_description", "")
                all_rows.append(row)
                
        elif page_data.get("type") == "multiple_tables":
            for table in page_data.get("tables", []):
                for row in table.get("rows", []):
                    row["_page"] = page_num
                    row["_page_desc"] = table.get("page_description", "")
                    all_rows.append(row)
        
        # Skip no_data, parse_error, error pages
    
    return all_rows


def save_csv(rows: list[dict], output_path: str):
    """Save extracted rows to CSV."""
    if not rows:
        print("  No rows to save.")
        return
    
    # Collect all unique keys across all rows for headers
    all_keys = []
    seen = set()
    for row in rows:
        for k in row.keys():
            if k not in seen:
                all_keys.append(k)
                seen.add(k)
    
    # Move metadata cols to end
    meta_cols = ["_page", "_page_desc"]
    data_cols = [k for k in all_keys if k not in meta_cols]
    final_cols = data_cols + [c for c in meta_cols if c in seen]
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=final_cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"  Saved {len(rows)} rows to {output_path}")


def save_json(data: list[dict], output_path: str):
    """Save raw extracted JSON for debugging."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved raw JSON to {output_path}")


# ── Main ───────────────────────────────────────────────────────────────────────

def process_pdf(pdf_path: str, output_csv: str, start_page: int = 1, json_output: str = None):

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: Set ANTHROPIC_API_KEY environment variable first.")
        print("  export ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    if json_output is None:
        json_output = output_csv.replace(".csv", "_raw.json")

    print(f"\n{'='*60}")
    print(f"Processing: {pdf_path}")
    if start_page > 1:
        print(f"Resuming from page {start_page}")
    print(f"{'='*60}")

    # Load existing results for pages outside the range being reprocessed
    existing = {}
    if start_page > 1 and os.path.exists(json_output):
        prior = json.load(open(json_output))
        end_page = start_page + MAX_PAGES - 1 if MAX_PAGES else None
        existing = {
            p["page_number"]: p for p in prior
            if p.get("page_number", 0) < start_page
            or (end_page is not None and p.get("page_number", 0) > end_page)
        }
        print(f"  Keeping {len(existing)} already-extracted pages from {json_output}")

    # Step 1: Render pages from start_page onward
    print("\n[1/3] Rendering PDF pages...")
    images = pdf_to_images(pdf_path, DPI, start_page)

    # Step 2: Extract tables via Claude Vision
    total_pages = start_page - 1 + len(images)
    print(f"\n[2/3] Extracting tables from {len(images)} pages via Claude Vision...")
    new_results = {}

    for i, img_bytes in enumerate(images):
        page_num = start_page + i
        print(f"  Processing page {page_num}/{total_pages}...")
        result = extract_table_from_image(client, img_bytes, page_num)
        new_results[page_num] = result

        page_type = result.get("type", "unknown")
        if page_type == "table":
            n_rows = len(result.get("rows", []))
            print(f"    ✓ Extracted {n_rows} rows")
        elif page_type == "multiple_tables":
            n_tables = len(result.get("tables", []))
            print(f"    ✓ Found {n_tables} tables")
        elif page_type == "no_data":
            print(f"    — No data ({result.get('content', '')})")
        else:
            print(f"    ✗ {page_type}")

    # Merge existing + new, sorted by page number
    merged = {**existing, **new_results}
    extracted = [merged[k] for k in sorted(merged)]

    # Step 3: Save outputs
    print(f"\n[3/3] Saving outputs...")
    save_json(extracted, json_output)

    rows = flatten_to_rows(extracted)
    save_csv(rows, output_csv)

    print(f"\nDone! Files saved:")
    print(f"  CSV:  {output_csv}")
    print(f"  JSON: {json_output}")

    return extracted


def main():
    parser = argparse.ArgumentParser(description="Extract tabular data from transit ridership PDFs")
    parser.add_argument("--pdf", required=True, help="Path to input PDF file")
    parser.add_argument("--output", default="output.csv", help="Path to output CSV file")
    parser.add_argument("--dpi", type=int, default=300, help="Render DPI (default 300, higher=better)")
    parser.add_argument("--max-pages", type=int, default=None, help="Limit pages for testing")
    parser.add_argument("--start-page", type=int, default=1, help="Resume from this page (1-indexed); merges with existing JSON")
    parser.add_argument("--json-output", type=str, default=None, help="Path to raw JSON output (and existing JSON to merge from)")
    args = parser.parse_args()

    global DPI, MAX_PAGES
    DPI = args.dpi
    MAX_PAGES = args.max_pages

    if not os.path.exists(args.pdf):
        print(f"ERROR: File not found: {args.pdf}")
        sys.exit(1)

    process_pdf(args.pdf, args.output, start_page=args.start_page, json_output=args.json_output)


if __name__ == "__main__":
    main()