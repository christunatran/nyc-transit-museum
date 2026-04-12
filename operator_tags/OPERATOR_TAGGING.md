# Operator Tagging & Ridership-Unit Documentation

Processing log for adding operator tagging and accounting-metadata columns
to `master_ridership_long.csv`.

**Input:** `master_ridership_long.csv` (42,662 rows, 1920–1995)
**Output:** `master_ridership_with_operator.csv` (same 42,662 rows + 6 new columns)
**Script:** `build_operator_tags.py`

---

## Six new columns

| Column | Type | Meaning |
|---|---|---|
| `original_operator` | string | IRT / BMT / IND / aggregate / SUMMARY / unknown |
| `original_line` | string, nullable | Line or contract within operator (pre-1940 mainly) |
| `joint_operation` | bool | True if the station had joint IRT/BMT service at the time of the row |
| `is_aggregate_row` | bool | True if the row is an accounting row (conductor colls, ticket credits) rather than a station entry |
| `methodology_note` | string, nullable | Free-text caveat for known comparability issues |
| `unit_of_measurement` | string | What "ridership" actually counts in that row |

---

## What "ridership" actually means (this is important)

The column is called `ridership` but what's being counted differs by era.
Neither era counts "unique humans who rode the subway." Both count
**revenue-event attributions to a station** — and they attribute those
events differently.

### Pre-1940 (`unit_of_measurement = fare_dollars_implied_fare_count`)

9,560 rows. The Transit Commission source documents track **fares
collected in dollars**, at a fixed 5¢ per fare. The numbers represent
revenue that a company booked from that station. At the 5¢ fare this
converts 1:1 to an implicit fare count. What it counts:

- ✓ Revenue-paying turnstile entries at that station
- ✓ Ticket-office sales at that station
- ✗ NOT: unique passengers (same person two rides = two fares)
- ✗ NOT: free transfers
- ✗ NOT: employee or courtesy passes
- ✗ NOT: conductor collections on-train (reported separately)

### Post-1940, pre-1994 (`unit_of_measurement = turnstile_registrations`)

30,796 rows. The source documents use the word "**registrations**" — a
turnstile entry recorded by mechanical counter. What it counts:

- ✓ Token/coin fare-paying entries
- ✗ NOT: unique passengers
- ✗ NOT: free transfers
- ✗ NOT: employee passes
- ✗ NOT: conductor collections

### Post-1994 (`unit_of_measurement = turnstile_registrations_incl_metrocard`)

1,153 rows. MetroCard entries were included starting in 1994 per the
source document. This is a meaningful methodology change — pre-1994 bulk
farecard purchases weren't entry-associated; after 1994 they are.

**Implication for analysis:** When you compare Times Square 1925 to
Times Square 1965, you're comparing "IRT's dollar-revenue at Times
Square turnstiles, at 5¢/fare" to "turnstile-counter registrations at
Times Square." These are conceptually similar but not identical metrics,
and they're subject to different accounting quirks (see below).

---

## Joint IRT/BMT stations (1923-1949)

**567 rows** across all pre-1940 data have `joint_operation = True`.
These are Astoria Line, Flushing Line, and Queensboro Plaza stations.

### Why IRT (not BMT)

Under the Dual Contracts of 1913, the Astoria and Flushing lines east of
Queensboro Plaza were officially **IRT lines** under Contract 3 — the
City built the infrastructure and leased it to the IRT as lessee-of-record.
BMT held "irrevocable and equal trackage rights" granted via Contract 4,
and ran trains on these lines from April 8, 1923 onward, but was not the
lessee. Joint service ended October 17, 1949.

The Transit Commission's accounting followed the contract, not the train.

### What the "ridership" number means at joint stations

From a footnote on the 1930s PDF page 5, verbatim:

> "Ticket sales here shown on Astoria and Flushing branches represent
> net sales for the Interborough Rapid Transit Company after deducting
> portion allocated to the New York Rapid Transit Corporation on account
> of joint traffic over these routes. For ticket sales credited to the
> New York Rapid Transit Corporation, see page 151."

Translation: at joint stations, the fare enters a shared pool and a
contractual formula splits the revenue. The 567 rows in this dataset
show **IRT's net share** of that split. BMT's corresponding share exists
on undigitized pages 149 and 151 of the source document.

**This is a real but narrow caveat.** The row is not a lie — it
accurately reflects IRT's books — but it is also not "total fare activity
at the station." To get that, you'd need both the IRT and BMT sides.

---

## Other accounting patterns baked into the source documents

Going through the source CSVs systematically, several non-station
accounting rows appear. Some were filtered out by the original cleaning
pipeline; others made it through and are now flagged.

### 1. Joint traffic adjustments (Dr./Cr. rows) — filtered out

**14 rows** across the two decades. Entries like
"CR. ADJUSTMENT OF JOINT TRAFFIC (Queensboro Sub.)" and
"Dr. Adjustment of Joint Traffic, 6th Ave. 'El'" are accounting
transfers moving revenue between IRT and BMT on shared elevated lines
(2nd/3rd/6th Ave Els had joint-traffic arrangements). These were stripped
from master during original cleaning — they're not in your current data.

### 2. Conductor collections — flagged `is_aggregate_row = True`

**6 rows** in master (out of 2 source rows pivoted into years). Labels
like "Conductor Collections-Culver Line" and "Conductors' collections
and miscellaneous adjustments" represent fares collected on the train by
conductors (especially on the BMT Culver El remnant). They can't be
attributed to any specific station but are included in line totals.

**Impact:** For any line that had conductor collections, summing
station-level rows underestimates the line total. For example, the
CULVER LINE total on 1930s page 9 shows 13.17M for 1930, but the sum of
its 12 station rows is 11.57M — the 1.60M gap (~12%) is conductor
collections and miscellaneous.

### 3. Inter-company ticket credits — flagged `is_aggregate_row = True`

**1 row** in master. "N.Y. Rapid Transit Corp.'s Tickets - Cr." represents
BMT tickets sold at IRT stations (or vice versa) — a between-company
accounting credit, not a station-level count.

### 4. Partial-year stations — methodology note added

**51 rows** flagged. Many station labels contain opening dates like
"Overlook Terrace (from Sept. 10, 1932)" or "207th Street (from 9/10/32)."
The row for the year the station opened reflects only the months after
opening, not a full year — its ridership is not directly comparable to
the subsequent full-year rows.

**Impact:** If you chart year-over-year ridership and see a sharp jump
at year 2 of a new station, that's the partial-year artifact, not real
growth.

### 5. Miscellaneous ticket sales — filtered out

**19 rows** in source CSVs. Station-label entries like "Miscellaneous
ticket sales" on multiple pages are special or bulk sales not attributable
to turnstile traffic. Stripped by the original cleaning pipeline.

### 6. "All entrances" aggregates — filtered out

**2 rows** in source CSVs. 1930s page 2 has system-summary rows like
"Times Square (all entrances)" that combine what later pages break down
per-entrance. Stripped by the original cleaning pipeline.

### 7. The Queensboro Plaza 1930 anomaly — methodology note added

**10 rows** flagged. Queensboro Plaza jumps from ~$3.7M (1929) to ~$16.7M
(1930), a ~5x increase with no real-world cause. The 1930s PDF page 5
shows Queensboro Plaza listed alongside a "QUEENSBORO SUBWAY - GROSS
TOTAL" and a "CR. ADJUSTMENT OF JOINT TRAFFIC" row — structural elements
that weren't in the 1920s source document. The 1930 figure appears to
use a broader inclusion scope (likely including joint-traffic credits
previously excluded).

---

## How operator was assigned

### Post-1940 — via the `segment` lookup

33,132 rows. Operator comes from `segment_operator_lookup.csv` (52 rows,
all verified). The lookup tags by **lineage, not operator-at-time**:
Culver El stations stay BMT forever even after IND absorption in 1954;
Fulton El stations stay BMT forever even after IND absorption in 1956.

2,530 post-1940 rows have no segment in the source document; these are
tagged `unknown` rather than guessed.

### Pre-1940 — via page number in source PDF

9,560 rows. Operator derived from the page number in the source Transit
Commission PDF, verified by visual inspection:

**1920–1929:** p2 = summary; p3-7 = IRT (Subway + Elevated); p8-10 = BMT.

**1930–1939:** p1-2 = summary; p3-7 = IRT; p8-10 = BMT; p11-12 = IND.

### Line tagging (pre-1940 only)

- First try: forward-fill from ALL-CAPS header rows in the `label`
  column (pattern: uppercase text containing LINE/BRANCH/DIVISION/
  CONTRACT/ELEVATED/SUBWAY).
- Second try: 1930s `line` column (populated for summary rows only,
  used as anchor for forward-fill).
- Fallback: page-level contract name ("Contract 1 & 2 Stations" for
  page 3, etc.) when no explicit header exists.

This disambiguates cases like "103d Street" (different physical stations
on different IRT lines):

| _page | operator | line |
|---|---|---|
| 3 | IRT | Contract 1 & 2 Stations (now the 6 train) |
| 4 | IRT | MAIN LINE (under Lexington Ave Line, Contract 3) |

---

## Counts

### Operator counts by era

| era | IRT | BMT | IND | aggregate | unknown | SUMMARY |
|---|---|---|---|---|---|---|
| private_operators | 5,494 | 3,599 | 467 | 0 | 0 | 0 |
| board_of_transportation | 4,146 | 4,252 | 2,547 | 4,325 | 1,274 | 0 |
| mta | 4,198 | 4,171 | 2,582 | 4,351 | 1,256 | 0 |

### Unit of measurement

| unit | rows |
|---|---|
| fare_dollars_implied_fare_count | 9,560 |
| turnstile_registrations | 31,949 |
| turnstile_registrations_incl_metrocard | 1,153 |

### Flags

| flag | count |
|---|---|
| joint_operation = True | 567 |
| is_aggregate_row = True | 7 |
| methodology_note populated | 3,134 |

---

## What cannot be recovered from this dataset

1. **BMT's share of joint-operation station ridership (1923-1949):**
   on non-digitized source pages 149/151.
2. **Line-level precision for 1920s Contract 1/2 stations:** the
   page-level fallback groups what are now parts of the 2/3/4/5/6 trains
   under a single label ("Contract 1 & 2 Stations"). Per-station line
   mapping was out of scope.
3. **Per-operator split at post-1940 joint stations** (e.g., Queensboro
   Plaza 1940-1949): the Board of Transportation consolidated the books
   at source after unification. No per-operator split is available.
4. **Conductor collections at the station level:** structurally
   unknowable. They were collected on moving trains.
5. **Unique passenger counts, ever:** the transit system has never
   tracked unique humans. Every figure — pre-1940 or post — counts fare
   events, not riders.

---

## Practical implications for analysis

- **Comparing station A to station B in the same year, same era:** fine,
  data is consistent.
- **Comparing station A across years within an era:** mostly fine, watch
  for partial-year flags and joint-operation flags.
- **Comparing station A across the 1940 unification boundary:** accept
  a ~6-month fiscal-vs-calendar offset (documented in original
  ANNOTATIONS.md) and understand the unit name changes from "fares" to
  "registrations." Shapes of trends remain valid; exact ratios do not.
- **Comparing station A across the 1994 MetroCard boundary:** another
  unit shift. Years ending 1993 and earlier exclude bulk-purchase
  effects; 1994+ do not.
- **Summing all station rows for a line/year to get a line total:**
  undercount by conductor-collection amount where applicable. Use the
  line-total rows in the source CSVs (filtered out of master) for
  accurate line totals.
- **Treating joint-operation stations as "total activity":** don't.
  They're one party's share of a split. Multiply-by-2 is not a safe
  approximation because the contractual formula wasn't 50/50 — it
  depended on each company's actual train-miles and revenue.
