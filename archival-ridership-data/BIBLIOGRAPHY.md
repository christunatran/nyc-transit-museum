# Annotated Bibliography & Works Cited
### NYC Archival Ridership Dataset · 1920–1995

---

## How this bibliography is organized

Sources are divided into three categories:

1. **Primary sources** — the archival documents from which all ridership data in this repository was directly extracted
2. **Secondary sources** — historical works, journalism, and reference materials used to contextualize and fact-check the data and annotations
3. **Data infrastructure** — tools and APIs used in the extraction and cleaning pipeline

All historical claims in `ANNOTATIONS.md` were cross-checked against at least one secondary source. Where discrepancies between sources exist, they are noted.

---

## I. Primary Sources

### 1. *Growth of Passenger Traffic in New York City for the Fiscal Years Ended June 30, 1920–1929*

**Publisher:** New York City Transit Commission, 270 Madison Avenue, New York City  
**Format:** Scanned archival PDF  
**Files in this repo:** `pdf/1920-1929 Ridership.pdf` → `csv/1920-1929_ridership.csv` → `cleaned_data/1920-1929_ridership_clean.csv`

**Annotation:**  
Compiled by the state regulatory body responsible for overseeing franchised private transit operators. Organized by operator (IRT, BMT) and then by line and station within each operator. The IRT section is structured by contract (Contract 1 & 2; Contract 3 / Seventh Avenue Line; Elevated Division). The BMT appears under the corporate name *New York Rapid Transit Corporation*. Counts are labeled "registrations" — fare-paying turnstile entries, not boardings or unlinked trips.

Data covers fiscal years ending June 30 (so "1920" = July 1919–June 1920). A handwritten note on the cover page reads *"permanent loan from Miss Lennon, Room 203"*, indicating the document was physically circulated within the agency. The physical state of the scan varies by page — some columns are partially obscured.

Pages 1–2 contain system-level summaries. Pages 3–10 are station-level. This dataset uses only pages 3–10 (663 rows after cleaning).

---

### 2. *Growth of Passenger Traffic in New York City for the Fiscal Years Ended June 30, 1930–1939*

**Publisher:** New York City Transit Commission, 270 Madison Avenue, New York City  
**Format:** Scanned archival PDF  
**Files in this repo:** `pdf/1930-1939 Ridership.pdf` → `csv/1930-1939 Ridership.csv` → `cleaned_data/1930-1939_ridership_clean.csv`

**Annotation:**  
Same format and publisher as the 1920-1929 report, now covering the Depression decade and the introduction of the IND. The IND (Independent City-Owned Rapid Transit Railroad System) appears for the first time in fiscal year 1933 — the first full year after the Eighth Avenue Line's September 10, 1932 opening. The IND's early lines listed in this document are: Eighth Avenue, Houston-Essex Street, Brooklyn Crosstown, Prospect Park–Coney Island, Bronx Concourse, and Queens Boulevard lines.

This report includes a monthly breakdown of fiscal year 1939 ridership changes compared to 1938 — the only month-by-month data in the collection. The source explicitly flags the 1939 World's Fair (opened April 30, Flushing Meadows, Queens) as the cause of the May and June 1939 ridership spikes. May 1939 shows a +16.5 million passenger increase (+6.3%) over the same month the prior year.

Pages 1–2 are system-level monthly tables. Pages 3–12 are station-level. This dataset uses only pages 3–12.

---

### 3. *Rapid Transit Ridership 1932–1935*

**Publisher:** New York City Transit Commission  
**Format:** Scanned archival PDF  
**Files in this repo:** `pdf/Rapid Transit Ridership 1932-1935.pdf` → `csv/Rapid Transit Ridership 1932-1935.csv` → `cleaned_data/rapid_transit_1932-1935_clean.csv`

**Annotation:**  
A system-level annual summary, not a station-level document. Covers all major transit operators as distinct line items: IRT subway, IRT elevated, BMT, IND, street surface railways (by borough), bus lines, and the Hudson & Manhattan Railroad (now PATH). The document tracks the IND's rapid growth from its first partial year (59M riders in 1933) through its early expansion.

The Hudson & Manhattan Railroad figures (roughly 75–76M annually through this period) provide context for trans-Hudson commuter traffic. The document predates the unified system by nearly a decade — the Transit Commission's role was regulatory, not operational.

---

### 4. *Seventeenth Annual Report — Rapid Transit Ridership 1934–1937*

**Publisher:** New York City Transit Commission  
**Format:** Scanned archival PDF  
**Files in this repo:** `pdf/Rapid Transit Ridership 1934-1937.pdf` → `csv/Rapid Transit Ridership 1934-1937.csv` → `cleaned_data/rapid_transit_1934-1937_clean.csv`

**Annotation:**  
The seventeenth annual report of the Transit Commission. Covers the same operator categories as the 1932-1935 report but adds per-capita ridership figures for the entire city. Also breaks out bus ridership by borough in greater detail than any other document in this collection.

Key finding visible in this data: bus ridership nearly doubled between 1934 (314M) and 1937 (588M) while street surface railway ridership collapsed. Manhattan's streetcar ridership fell 48% between 1936 and 1937 alone. Staten Island (Richmond) shows 2.73M surface railway trips in 1934 and zero in 1935 — complete cessation in one year. This document is the clearest evidence of the transit mode shift from rail to rubber that defined the mid-20th century.

Rides-per-capita data: ~377 in 1934, ~388 in 1937.

---

### 5. *Annual Subway Registrations 1940 to 1995*

**Publisher:** MTA New York City Transit, Office of Management and Budget, Revenue Analysis Division  
**Published:** October 1996  
**Address:** 130 Livingston Street, Brooklyn, NY 11201  
**Contact listed in document:** John Kennes  
**Format:** Scanned archival PDF (two parts)  
**Files in this repo:** `pdf/1940-1995-Ridership-Part1.pdf` + `pdf/1940-1995-Ridership-Part2.pdf` → `cleaned_data/1940-1995_ridership_clean.csv`

**Annotation:**  
The most comprehensive document in the collection. Provides station-level annual registration counts for every subway station for 55 consecutive years, organized into four geographic sectors:
- Northern Manhattan and Bronx (report pages 1–24)
- Northern Queens (pages 25–32)
- Southern Queens and Brooklyn (pages 33–64)
- Manhattan CBD (pages 65–80)

Years are split across pages in 14-year chunks (e.g., 1940–1953 on one page, 1954–1967 on the next). The document spans two physical parts due to its size.

Contains the *New York City Subway Fare Chronology 1940 to 1995* (page 6 of Part 1) — the complete fare history from the nickel era through MetroCard. This table is transcribed in full in `ANNOTATIONS.md`.

The introductory narrative (page ii) explains that the list of stations in 1940 and 1995 are meaningfully different due to closures, openings, reclassifications, and platform extensions — not merely ridership changes. The document uses the term "registrations" explicitly to distinguish turnstile counts from total boardings, and notes that "Conductor's Collections" (fares collected directly, not at turnstiles) are excluded from station-level totals, explaining why station sums don't always equal system totals.

Six station-segment pairs appear in two geographic sections with conflicting values; both are preserved in the cleaned dataset with `conflict = True`.

---

### 6. *NYC Transit Subway and Bus Ridership 1940–2011*

**Publisher:** MTA New York City Transit  
**Format:** Scanned archival PDF  
**Files in this repo:** `pdf/1940-2011 Historical Ridership.pdf` → `csv/1940-2011 Historical Ridership.csv` → `cleaned_data/1940-2011_historical_ridership_clean.csv`

**Annotation:**  
A system-wide summary document, not station-level. Provides annual and average-weekday ridership for both subway and bus, 1940–2011. Unlike the other PDFs in this collection, this document's underlying text is machine-readable (not a scanned image), allowing direct text extraction.

This is the most authoritative source in the collection for system-wide verification of the station-level data. Notes are embedded directly in the data rows, flagging: fare increases, TWU strikes (1966, 1980, 2005), 9/11 (2001), MetroCard launch (1994), free intermodal transfers (1997), and bonus MetroCard (1998).

Key verified benchmarks from this document: ridership peaked at 2.067 billion in 1946; bottomed near 976 million in 1976–1977; reached approximately 1.62 billion by 2008. These figures were used to cross-validate the station-level data in `build_master_dataset.py`. The station-level sums for 1940–1966 are within ±2.6% of these totals; the gap widens to 7–9% for later years (see `ANNOTATIONS.md` § Data quality).

---

### 7. *Report of the Public Service Commission for the First District of the State of New York* (1907)

**Author:** New York (State). Public Service Commission for the First District  
**Publisher:** Albany: J.B. Lyon Company, printers, 1908 (annual series continues through 1921)  
**Coverage:** Six months ending December 31, 1907; transmitted to the Legislature January 20, 1908  
**Original held by:** Cornell University Library  
**Digitized by:** Google (public domain)  
**HathiTrust:** https://hdl.handle.net/2027/coo.31924012950345  
**HathiTrust catalog:** https://catalog.hathitrust.org/Record/010425199  
**File in this repo:** `Report of the Public Service Commission for the First District of the State of New York 1907.txt` (full text, 51,122 lines)

**Annotation:**  
This is the founding report of the Public Service Commission for the First District, the regulatory body that succeeded the Board of Rapid Transit Railroad Commissioners (and the earlier Rapid Transit Commission) as of July 1, 1907. The PSC First District is the direct institutional predecessor of the NYC Transit Commission that published the 1920-1929 and 1930-1939 ridership documents forming the first two primary sources in this bibliography. It was itself preceded by the Rapid Transit Commission and followed by a succession of bodies: Transit Commission (1921) → Board of Transportation (1940) → NYCTA (1953) → MTA (1968). The ridership data in this repository was filed under the Transit Commission era of that chain.

The report covers all franchised surface railways, elevated railroads, and the nascent IRT subway under the PSC's jurisdiction (New York, Kings, Queens, and Richmond counties). In six months of operation, the Commission held 179 hearings and issued 186 orders; it was meeting at least weekly. The commissioners were: William R. Willcox (Chair), William McCarroll, Edward M. Bassett, Milo R. Maltbie, and John E. Eustis.

**Ridership context (thirteen years before this dataset begins):**

Total passengers transported under PSC First District jurisdiction in fiscal year ending June 30, 1907: **1,323,273,368 — a daily average of more than 3,560,000 persons.** This was a 5.9% increase (73 million passengers) over the prior year. The report notes that during peak hours, companies were "carrying passengers to the number of 500,000 an hour — more than 10% of the entire population of the city during some portions of the day."

A single-day count at Brooklyn Bridge on October 17, 1907: **426,364 persons crossed** (exceeding the entire population of Buffalo), requiring 15,263 cars across 1,302 elevated trains and 600 bridge trains. During the heaviest hour, 54,736 persons crossed in one direction alone. The report called this "an average bridge day's traffic."

These numbers establish the scale of demand in 1907 — thirteen years before the 1920 start of this dataset. By 1920, system-wide ridership across all modes had grown to approximately 2.4 billion. The base was already enormous.

**Overcrowding as a policy problem in 1907:**

The overcrowding that defines the 1940s peak and the 1970s crisis was already documented and extreme in 1907. The report includes direct measurements: surface cars with seating capacity of 22 carrying 45 passengers; capacity-36 cars carrying 80; capacity-65 cars carrying 105. One large open car had "all the seats taken, aisles crowded between seats, passengers on the front and rear bumpers and on the running board." At Cypress Hills station, passengers waited fifteen minutes for a car, standing in the street without shelter.

On the express subway: *"The express service is already overcrowded and the main problem is to find how a still greater carrying capacity can be obtained pending the completion of other north and south lines in Manhattan."*

On Brooklyn Bridge: *"The congestion in the hours of heaviest traffic is extreme and almost unendurable. This regrettable condition is the growth of many years."*

The Commission estimated that its orders in the first six months alone added over **15,000,000 additional seats per annum** to the system through required schedule increases.

**Peak-hour concentration:**

The report documents that 60% of daily traffic — approximately 2,000,000 passengers — moved within four daily hours: 7:30–9:30 a.m. and 5:00–7:00 p.m. This peak-hour concentration is the structural fact underlying every ridership number in the 1920-1995 dataset. Annual totals aggregate billions of individual rush-hour trips; the system was not designed for even distribution across the day.

**The five-cent fare and its politics:**

The nickel fare is treated in this report as fixed and unquestionable — the PSC does not discuss raising it. It does note the financial logic that made it politically permanent: "the financial success of the subway now in operation has removed the doubts that existed fifteen years ago." The fifty million dollars in subway bonds were not a taxpayer burden because "the operating company has agreed to pay the city the interest and sinking fund charges upon the entire amount issued." This financial arrangement — operators subsidizing city debt in exchange for franchise rights — is exactly the structure that later collapsed, leading to the 1940 city purchase and the removal of the nickel fare in 1948.

One fare equity finding from 1907: the Interborough charged 10 cents from Westchester to 110th Street but only 8 cents in the reverse direction on the same route. The Commission ordered an 8-cent maximum in both directions. Price discrimination on identical routes was documented and formally prohibited by Commission Order No. 146.

**Infrastructure decisions with consequences visible in the dataset:**

*Ninety-sixth Street bottleneck:* The main IRT line divides at 96th Street into the Lenox Avenue and Broadway branches. A $850,000 modification (approved by the Board of Estimate) would allow "one-third more local trains during the rush hours." The IRT testified this was their highest-priority capacity fix. The capacity increase at 96th Street set the throughput ceiling for the IRT for the next several decades; every station south of that point on the 1/2/3/4/5/6 in the 1920-1929 data reflects traffic constrained by this bottleneck.

*Fourth Avenue Subway (Brooklyn):* The PSC modified the tunnel headroom from 13.5 to 14.5 feet to allow suburban Long Island railroad cars to potentially operate through. The stated goal was to "bring the suburbanite from Long Island right into the heart of Manhattan." This suburban through-running vision was never realized, but the physical infrastructure it created became the BMT's Fourth Avenue corridor — now the N/R/D trains through Brooklyn, whose stations first appear in the 1920s ridership data.

*Center Street Loop (Brooklyn Bridge connections):* Same headroom revision (13'6" → 14'6"), same suburban integration rationale, same unrealized vision.

*Canal Street Extension ($7,000,000):* A planned crosstown connection from Manhattan Bridge through Canal Street to West Street, enabling "cars run through from the Bronx to Fort Hamilton or Coney Island via Manhattan Bridge and the Fourth Avenue subway." The inter-line connectivity the PSC was designing in 1907 is the same connectivity that defined IRT/BMT service patterns in the 1920s data.

*Ventilation:* $500,000 invested in ventilation for the subway to address rush-hour discomfort. The 1907 subway was hot, airless, and crowded — physical conditions that shaped rider behavior and ridership patterns.

**The corporate financial scandal:**

The New York City Railway Company — the dominant surface carrier transporting 344,770,368 passengers in fiscal year 1907 — reported a $3.3 million deficit despite $7.1 million in net operating earnings. The PSC's investigation found systematic misappropriation charged to construction accounts:

- $916,438 in legal fees to one firm + $238,227 to a sister company over 4.5 years (with no corresponding legal work documented)
- $180,000 paid to one official with no vouchers on file
- $250,000 per year in executive compensation for work "not yet been performed"
- $75,000 for drafting one lease; $25,000 for preparing one argument
- $965,607 for purchasing a railroad corporation "toward which not a shovelful of dirt had ever been turned, nor a pound of rails purchased"
- Books of one subsidiary "had been sold and destroyed"

This financial structure — private operators extracting value through legal and executive fees while nominally insolvent — is the same dynamic that drove IRT into receivership in 1932 and forced the 1940 city purchase. The PSC's 1907 investigation documented the pattern twenty-five years before the receivership; it was not a surprise.

**The monopoly investigation:**

The PSC initiated formal hearings to determine whether the Interborough-Metropolitan Company and Brooklyn Rapid Transit Company "illegally and as monopolies control and operate the several properties now under their control." The investigation spanned 38 hearings and produced 2,538 printed pages of testimony. This is the same monopoly structure that characterized the private-operator era (1920-1939) in this dataset, and the same operators that the city eventually purchased in 1940.

**Accident data:**

In just six months of operation, transportation companies under PSC jurisdiction reported **24,209 accidents and 288 deaths**. The Commission called this "appalling." For context: the transit system's 1907 safety record meant that riding transit was a statistically meaningful physical risk. This background helps interpret why regulatory compliance and equipment safety orders dominate so much of the report — the PSC's safety enforcement role was not bureaucratic, it was responding to mass-casualty conditions.

**On the regulatory lineage (for interpreting subsequent documents):**

The PSC replaced three prior bodies: the Board of Rapid Transit Railroad Commissioners (subway planning), the Commission of Gas and Electricity, and the State Inspector of Gas Meters. It held both planning authority (for new subway construction) and enforcement authority (over existing operators). The Transit Commission that published the 1920-1939 ridership reports in this dataset was established in 1921 and inherited this dual mandate. The data formats, terminology, and organizational logic of the Transit Commission reports — fiscal year reporting, operator-by-operator breakdowns, station-level granularity — all derive from the PSC reporting framework established in 1907.

One constitutional constraint the PSC documented explicitly shapes the entire subsequent history: a **1894 referendum** determined that new rapid transit roads must be constructed and owned by the city of New York. *"No city or State board can to-day grant a franchise to a private company for the construction and operation of an independent rapid transit road within Greater New York."* Private capital could only build extensions of existing lines; all new independent lines required city ownership. This is why the IND — the city-owned system that opened in 1932 and first appears in the 1930-1939 ridership data — was built at all. It was not a policy choice made in the 1920s; it was a constitutional mandate from 1894.

**First-person voices from 1907:**

These are the oldest direct voices in the record:

- Brooklyn merchants on Fulton Street/Flatbush Avenue construction: criticism of torn-up streets, compelled the Commission to assign an engineer to minimize business interference.
- Federal Court receivers of the NYC Railway Company, in a letter to PSC, October 7, 1907: *"Although we shall not be represented, it is our desire as receivers to facilitate the efforts of the Commission in every way possible."*
- General Manager Oren Root of NYC Railway, on staffing constraints: The Commission's investigator countered that if "conditions were to be made less attractive," fewer men would work — and if conditions improved, the company would secure the staff it needed. The company's claim of labor unavailability was documented as a policy choice, not a fact.
- A fatal accident on Staten Island, August 23, 1907: *"A passenger on a car running from South Beach to St. George, Staten Island, while pulling down the curtain, lost her balance and fell to the street, the rear trucks passing over her body."* The PSC refused the corporation's request to delay the investigation pending civil litigation: *"If we should establish the precedent of postponing investigations...until trials of damage suits should take place, we should be remiss in our duties."*

**Note on completeness:**  
The full text (51,122 lines) of the 1907 report was read in preparation of this bibliography. This is the first year of the PSC annual report series; subsequent years (1908–1921) are available through HathiTrust and likely contain additional ridership data, service order histories, and testimony. The 1921 report would be particularly relevant as the immediate predecessor to the Transit Commission's 1920-1929 ridership document (Primary Source #1 in this bibliography).

---

### 8. *Report of the Public Service Commission for the First District of the State of New York* (1920) — Fourteenth Annual Report

**Author:** New York (State). Public Service Commission for the First District  
**Publisher:** Albany: J.B. Lyon Company, printers  
**Coverage:** Calendar year 1920; transmitted to the Legislature January 10, 1921  
**Original held by:** University of Michigan  
**Digitized by:** Google (public domain)  
**HathiTrust:** https://hdl.handle.net/2027/mdp.35112103617132  
**File in this repo:** `Report of the Public Service Commission for the First District of the State of New York 1920.txt` (full text, 146,819 lines)

**Annotation:**  
This is the fourteenth and final annual report of the PSC First District — the last document in the regulatory series before the NYC Transit Commission assumed oversight and began publishing the ridership data that forms Primary Sources 1–4 in this bibliography. A footnote in the document references records "on file with the Transit Commission," confirming the institutional transition was underway. This report is the immediate predecessor to the 1920-1929 ridership series: the fiscal year ending June 30, 1920 documented here is the same starting year as that dataset.

**Ridership in the year your dataset begins:**

Total passengers transported in the fiscal year ending June 30, 1920: **2,364,775,067** — an increase of 284,830,770 (13.69%) over fiscal year 1919. Per capita: 421 transit rides per New York City resident (up from 376 in 1919). Broken down by operator:

| Mode | Passengers (FY 1920) | Change vs. 1919 |
|------|----------------------|-----------------|
| IRT Subway | 586,098,633 | +27.1% |
| IRT Elevated | 369,034,477 | +6.0% |
| BRT Elevated/Subway | 376,782,635 | +22.0% |
| Hudson-Manhattan Tubes | 92,250,836 | +7.2% |
| **Total Rapid Transit** | **1,424,166,581** | **+18.3%** |
| Surface Lines | 940,608,486 | +7.4% |
| **Grand Total** | **2,364,775,067** | **+13.7%** |

These are the exact baseline figures for IRT and BRT that your station-level data begins tracking. The 586 million IRT subway passengers in fiscal year 1920 distribute across the individual station counts in `1920-1929_ridership_clean.csv`.

**The congestion paradox:**

The report states that "notwithstanding the operation of ten-car trains every two minutes or less on the Interborough subways during rush hours, the congestion is almost as bad as it was three years ago before the new lines were opened." The Dual System expansion (Contracts 3 and 4, 1913), which added dozens of new stations visible in the 1920-1929 data, had been entirely absorbed by demand growth. Infrastructure could not outrun the city's growth. The Commission warned: *"Unless New York City takes prompt steps to plan and build new rapid transit lines and have them ready for operation within four or five years, the traffic situation in the city will have become little less than terrible."* This is the crowding that opens your dataset. The 1946 wartime peak was not an anomaly — the system was already under extreme pressure in 1920.

**The nickel fare crisis:**

The Dual System Contracts (1913) explicitly locked fares at five cents by contract language — not Commission authority. When the IRT and BRT applied for fare increases in May and June 1920, the Commission denied both applications on the grounds it lacked jurisdiction to override the contract terms. Both companies obtained court writs and the cases were pending at year-end. This legal standoff is why the nickel fare survived through 1948: it was embedded in contracts, not just in politics. Every ridership number in your 1920-1929 dataset was produced at a five-cent fare that the operators considered financially ruinous.

**Financial collapse despite record ridership:**

Total system operating revenue for fiscal year 1920: $127,880,161. Total operating expenses: $96,059,605. Despite record passenger volumes, the combined corporate income was a **deficit of $10,735,399** — worse than the prior year's $8.6 million deficit. The PSC called this "surprising." Nine major properties were in receivership by year-end. The Commission documented a deferred maintenance backlog of $10.9 million, growing. The financial structure that would force the 1940 city purchase was already visibly collapsing in 1920 — twenty years before it happened.

Lines abandoned in 1920 due to insolvency include: Metropolitan Avenue Line, Pelham Park–City Island Line, Queensboro Bridge Line, and all Staten Island Midland Railway operations (ceased January 19, 1920). Each abandonment removed transit access from neighborhoods; those riders either walked, drove, or shifted to surviving lines — which intensified congestion on the lines that remained.

**Three strikes in a single year:**

1920 was the most strike-disrupted year in the early dataset period:

*BRT Strike (August–September 1920):* All BRT subway, elevated, and surface lines stopped. "A large portion of the population of Brooklyn was forced to walk." What prevented complete paralysis was the continued operation of IRT lines — a reminder that the three-system structure, while financially inefficient, provided redundancy. The strike ended with workers returning on the receiver's terms; court control of wages made arbitration legally impossible. The Commission's statement in the hearing record: *"The necessity of the people in a matter of this kind is paramount...but the Commission has no power to order either side to do anything."*

*April 1920 freight strike:* Marine workers, trainmen, and freight handlers struck simultaneously, nearly paralyzing the port of New York. Fear of food shortages prompted PSC Commissioner Barrett to personally assist freight diversion. The freight system and transit system shared infrastructure, labor pools, and political attention — a disruption to one cascaded into the other.

*Manhattan and Queens Traction Strike (August 1920):* Workers demanded 25% wage increases. The company had been in receivership since 1916 and could not match wage scales of other transit systems. Resolved only by an authorized fare increase (two-zone system) that passed the cost to riders.

**Infrastructure opened in 1920 — stations that first appear in your data this year:**

- **Eastern Parkway Line** (November 22, 1920): Main stem opened from tunnel under Eastern Parkway to Buffalo Avenue; Nostrand Avenue branch opened same day to Flatbush Avenue. These are IRT stations that appear for the first time in the fiscal year 1920 column of the 1920-1929 ridership data.
- **Webster Avenue Extension** (October 4, 1920): Third Avenue elevated line extension opened, connecting Pelham Bay Park and White Plains Road branches.
- **Pelham Bay Park Branch elevated portion** (December 1920): Lexington Avenue subway elevated extension to Pelham Bay Park completed. New stations at the end of what is now the 6 line.
- **Culver Line reconstruction** completed; through service to Coney Island restored at 5 cents per the Dual Contract terms.

Any station in your 1920-1929 dataset that shows ridership beginning in the year 1920 column but zeros before it likely opened during this fiscal year.

**First-person voices, 1920:**

PSC Commissioner Alfred M. Barrett, at the BRT strike hearing:
> *"The Commission finds that the public is being seriously inconvenienced; that the people are not being carried on the cars in Brooklyn; that disorder exists in connection with the transportation system there. The Commission has no power to order either side to do anything... The necessity of the people in a matter of this kind is paramount."*

U.S. District Judge Julius M. Mayer, in a letter read into the hearing record, on the BRT strikers:
> *"There would be no negotiations, directly or indirectly, by the Receiver or the Court, with those leaders who 'either instituted the strike or were powerless to prevent it.'"*

A company president, on wage demands:
> *"We will all quit together."*

**The Manhattan surface decline:**

While the overall system grew 13.69%, Manhattan surface (streetcar) lines declined 5.71%. New York Railways Company was still in receivership; unprofitable lines were abandoned. This is the beginning of the surface railway collapse visible across the 1920-1939 data — Manhattan streetcars are dying in 1920, killed by a combination of financial insolvency, new subway competition, and early automobile pressure. By 1952, Manhattan's last streetcar line will be gone.

**On the PSC as predecessor:**

This report's cover identifies it as the "Fourteenth Annual Report" — which counts back to 1907. The Transit Commission that succeeds it was established in 1921. The PSC's data collection methods, reporting frameworks, and station-level accounting conventions were directly inherited by the Transit Commission, which is why the 1920-1929 ridership report (Primary Source #1) uses the same fiscal year structure, the same operator categories, and the same "registrations" terminology. The data you are working with was produced by the same bureaucratic machinery; only the name on the door changed.

---

## II. Secondary Sources

The following sources were consulted for historical fact-checking and contextual annotation. All facts in `ANNOTATIONS.md` attributed to a specific date, event, or named statistic were cross-checked against at least one of these sources.

---

### Wikipedia — Individual articles consulted

Wikipedia was used as an initial reference for dates and basic facts, then cross-checked against more authoritative sources where available. Specific articles used:

- **"Interborough Rapid Transit"** — for the 1932 receivership date (August 25, 1932), IRT history, contract structure
- **"Brooklyn–Manhattan Transit Corporation"** — for the 1918 Malbone Street wreck, BMT corporate lineage, purchase date (June 1, 1940)
- **"Independent Subway System"** — for IND opening date (September 10, 1932), early line structure
- **"History of the New York City Subway"** — general timeline, purchase dates, unification
- **"New York City Transit Authority"** — Board of Transportation / NYCTA / MTA succession
- **"Metropolitan Transportation Authority"** — MTA founding (March 1, 1968)
- **"New York City subway fares"** — fare history, token introduction dates
- **"New York subway token"** — token introduction (July 25, 1953), last token (April 13, 2003)
- **"Second Avenue Subway"** — construction history (proposals since 1920s, construction began 2007, Q line opened 2017)
- **"Third Avenue El"** — closure of Manhattan portion (May 12, 1955)
- **"Second Avenue Elevated"** — closure (June 13, 1942)
- **"1966 New York City transit strike"** — January 1–13, 1966; first day of Lindsay administration
- **"1980 New York City transit strike"** — April 1–11, 1980
- **"New York City fiscal crisis"** — 1975 crisis, near-default (October), Ford loan guarantee
- **"MetroCard"** — pilot launch (January 1994 on M15 bus and one subway line), system-wide rollout, free transfers
- **"Bernhard Goetz"** — shooting (December 22, 1984)
- **"Cross Bronx Expressway"** — construction, displacement of 60,000 Bronx residents, Robert Moses
- **"Robert Moses"** — general highway construction, relationship to transit decline
- **"Holland Tunnel"** — opening (November 13, 1927)
- **"1939 New York World's Fair"** — Flushing Meadows, April 30 opening, IRT Flushing Line, Willets Point station
- **"1964 New York World's Fair"** — April–October, Shea Stadium
- **"1977 New York City blackout"** — July 13–14, looting
- **"1973 oil crisis"** — OPEC embargo, October 1973
- **"Malbone Street wreck"** — November 1, 1918; led to BMT reorganization
- **"Guardian Angels"** — founded 1979, subway patrols
- **"New York City crisis of the 1970s"** — general background on fiscal crisis and urban decline
- **"COVID-19 pandemic in New York City"** — ridership collapse in 2020
- **"Superstorm Sandy"** — October 29, 2012; subway tunnel flooding
- **"Hudson–Bergen Light Rail"** / **"PATH train"** — Hudson & Manhattan Railroad lineage

**Note on Wikipedia reliability:** All dates used from Wikipedia were cross-checked against at least one additional source (newspaper archives, official MTA documentation, or the primary source documents in this collection). Where Wikipedia and another source disagreed, the discrepancy is noted in `ANNOTATIONS.md` (see: fare increase of June 28/29, 1980).

---

### Wikipedia — Borough assignment research (Pass 2 borough fill)

The following Wikipedia articles were consulted specifically to determine which borough each station belongs to for the multi-borough subway lines in the 1940–1995 dataset. This research populated the `borough` column for stations on lines that physically cross borough boundaries. All lookups were performed in April 2026. The methodology and coverage gaps are documented in `ANNOTATIONS.md` § Data quality, issue 9.

**Line articles (for overall routing and borough sequence):**
- **"IND Eighth Avenue Line"** — confirmed all 18 stations in the 8 Ave. segment listing are in Manhattan (72 St.–207 St., upper West Side / Washington Heights / Inwood)
- **"IRT Broadway–Seventh Avenue Line"** — confirmed all stations in the Broadway/7 Ave. segment listing are in Manhattan, with one exception: 242 St. (Van Cortlandt Park terminal) is in the Bronx
- **"IND Crosstown Line"** — confirmed all 8 stations in the Crosstown segment listing are in Brooklyn; the G train's Queens stations (Court Square, 21 St.) do not appear in the dataset
- **"IND Fulton Street Line"** — established Brooklyn/Queens boundary: Grant Ave. is the last Brooklyn station; 111 St., 104 St., Lefferts Blvd. are in Queens
- **"BMT Jamaica Line"** — established Brooklyn/Queens boundary: Cypress Hills is the last Brooklyn station; Elderts Lane onward is Queens
- **"IRT Lenox Avenue Line"** — confirmed all 6 stations are in Manhattan (Harlem, 110 St.–148 St.)
- **"IRT Lexington Avenue Line"** — confirmed all 8 stations in the Lexington Ave. segment listing are in Manhattan (68 St.–125 St., Upper East Side / East Harlem); Bronx stations on this line appear under separate segments (Pelham, White Plains Rd., etc.)

**Per-station articles (for stations where line article was ambiguous):**
- **"Marble Hill–225th Street station"** — 225 St. on Broadway/7 Ave.: geographically north of the Harlem River ship canal (Bronx landmass) but administered as part of Manhattan County; MTA officially lists as Manhattan
- **"Grant Avenue station (IND Fulton Street Line)"** — confirmed Grant Ave. is Brooklyn's last station on the Fulton Street line
- **"104th Street station (IND Fulton Street Line)"** — confirmed Queens
- **"Liberty Avenue station"** — disambiguated Liberty Ave. on the Fulton St. segment (Brooklyn, East New York) from other Liberty Ave. references
- **"Shepherd Avenue station"** — confirmed Brooklyn (East New York); also resolved OCR spelling variant "Shephard Ave."
- **"Van Siclen Avenue station (IND Fulton Street Line)"** — confirmed Brooklyn
- **"Cypress Hills station"** — confirmed Brooklyn (last Brooklyn station on BMT Jamaica Line)
- **"104th Street station (BMT Jamaica Line)"** — confirmed Queens (Richmond Hill)
- **"Myrtle Avenue station (BMT Jamaica Line)"** — confirmed Brooklyn (Bedford-Stuyvesant/Bushwick border)
- **"91st Street station (IRT Broadway–Seventh Avenue Line)"** — confirmed Manhattan (closed February 2, 1959)

**What was not resolved:** The Third Avenue El and Sixth Avenue El stations in the 1920s–1930s data (`segment = NaN`) cross the Manhattan–Bronx boundary mid-page in the source document. Individual station lookups for these historical elevated lines were not performed; those 4,283 rows remain with null borough. Wikipedia articles for "Third Avenue El" and "Third Avenue Elevated (Bronx)" exist and could be used for a future pass.

---

### New York Daily News

- **"Ford to City: Drop Dead"** — front page, *New York Daily News*, October 30, 1975. Referenced in the 1975 annotation. This headline became a defining cultural artifact of the NYC fiscal crisis, though President Ford never used those words — they were the Daily News editorial desk's characterization of his policy position. The headline is public record and widely reproduced.

---

### MTA Open Data Portal

**URL:** https://data.ny.gov  
Referenced in `README.md` as the source for post-2011 ridership data not present in this collection. The portal provides annual subway ridership, turnstile-level counts, and other open datasets published by the MTA. Not used directly in this dataset, but recommended for extending coverage beyond 1995 (station-level) or 2011 (system-wide).

---

### NYC Transit Commission — Seventeenth Annual Report (internal cross-reference)

As noted above under Primary Source #4. The annual report number ("Seventeenth") was extracted directly from the document and used to anchor the Commission's reporting timeline. The Transit Commission was established in 1921; the seventeenth annual report (covering 1934–1937) was therefore published circa 1938.

---

## III. Data Infrastructure

The following tools and APIs were used in extracting, processing, and cleaning the data in this repository. They are listed here for reproducibility.

---

### Anthropic Claude API (Vision)

**Model used:** `claude-sonnet-4-6`  
**API:** Anthropic Messages API  
**Role:** OCR extraction of tabular data from scanned PDF images  
**Key parameters:** `max_tokens=16384`, DPI 150 for image rendering  

Each PDF page was rendered to a grayscale PNG image and submitted to the Claude Vision API with a structured prompt requesting JSON output of the table's headers and rows. Output was parsed and flattened to CSV. Pages that returned malformed JSON were reprocessed with `--start-page` to avoid re-billing clean pages.

---

### PyMuPDF (`fitz`)

**Version:** installed via `pip install pymupdf`  
**Role:** Rendering PDF pages to PNG images at 150 DPI for submission to Claude Vision API  
**Constraint:** 300 DPI images from dense pages exceeded Claude API's 5MB per-image limit; 150 DPI remained within limit for all pages in this collection.

---

### pandas

**Role:** Data cleaning, normalization, wide-to-long melting, cross-decade station name matching, conflict flagging  
**Key operations:** `melt()`, `combine_first()`, `groupby()`, regex-based normalization via `re` module

---

### poppler / pdftotext

**Role:** Attempted direct text extraction from PDFs to supplement OCR  
**Result:** Five of the seven PDFs are scanned images with no embedded text layer. Only `1940-2011 Historical Ridership.pdf` yielded clean machine-readable text. The station-level data documents (all six others) required Claude Vision OCR.

---

## IV. Notes on source evaluation

**What these sources do well:**  
The primary sources are government-filed regulatory documents with no obvious incentive to misrepresent ridership counts — operators were required by franchise agreements to report accurately. The documents are internally consistent (station sums within each document reconcile to system totals within expected variance). Where two documents cover overlapping years (1932–1939 in both the Commission summary reports and the station-level detail reports), the totals agree within rounding.

**What these sources don't capture:**  
- Fare evasion (not counted in turnstile registrations)
- Employee passes and non-revenue entry
- Transfer passengers (a rider who transfers from the A to the C is counted once, not twice — but a rider who exits and re-enters is counted twice)
- The subjective experience of transit — crowding, delays, fear, accessibility — is entirely absent from quantitative ridership data

**On Wikipedia as a verification tool:**  
Wikipedia articles on NYC transit history are generally well-sourced and cite primary materials (MTA reports, contemporary newspaper accounts, academic histories). For this project, Wikipedia served as a fast initial check; discrepancies triggered deeper search. No annotation was left relying solely on Wikipedia where a more authoritative source was available.

**On the HathiTrust document:**  
The URL https://catalog.hathitrust.org/Record/010425199 was provided as a potential source for transit policy testimony and rider experience documentation. Due to access restrictions, its content could not be reviewed. If that document is a Transit Commission annual report, Board of Transportation memo, or rider testimony collection from the mid-20th century, it would substantially enrich the policy and human-experience context that the quantitative ridership data alone cannot provide. Future researchers should attempt institutional access.
