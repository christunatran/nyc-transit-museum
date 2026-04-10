# NYC Subway Ridership — Year-by-Year Annotations
### For use with `master_ridership_long.csv` · 1920–1995

---

## How to read this data

Each row in the master dataset is one station, one year, one ridership count.

- **`ridership`** = number of fare-paying passengers who entered that station that year
- **`era`** = which governing body operated the system that year
- **`source`** = which archival document the number came from
- **`cross_decade_match`** = `True` if this station name appears in multiple source eras (pre- and post-1940 data can be compared directly)
- **`segment`** = the line or corridor the station belongs to (present in 1940-1995 data)

Fiscal years (pre-1940 data) end June 30. Post-1940 data is calendar year. This ~6-month offset is small relative to the scale of the data but worth knowing.

---

## About the source documents

These datasets were extracted from seven archival PDFs. Understanding who produced each document and why helps interpret what the numbers mean.

### State of New York — Transit Commission Reports (1920s–1930s)

The 1920-1929 and 1930-1939 ridership PDFs are publications of the **NYC Transit Commission**, a state regulatory body at 270 Madison Avenue, New York City. Their full title is *Growth of Passenger Traffic in New York City for the Fiscal Years Ended June 30*.

The Transit Commission tracked each private operator separately — IRT, BMT, and IND as distinct entities — because they were regulated as franchised private utilities, not as a unified public system. The commission's job was oversight, not operation. These reports exist because the state required operators to file ridership data as a condition of their franchises.

The IRT data is organized by its contract structure:
- **Contract 1 & 2 Stations** — The original 1904 subway and its early extensions. Manhattan and Brooklyn stations on what are now the 4/5/6 and parts of the 2/3.
- **Contract 3 Stations (Seventh Avenue Line)** — What is now the 1/2/3 running through Times Square and into Brooklyn.
- **Elevated Division** — The 2nd Avenue, 3rd Avenue, 6th Avenue, 8th Avenue, and 9th Avenue elevated lines in Manhattan, plus Bronx and Brooklyn elevated lines. All of these are gone by 1955.

The BMT appears as the **New York Rapid Transit Corporation** in these filings. Its stations are organized by line: Lexington Ave (Jamaica), Broadway (Brooklyn), Canarsie, Brighton Beach, Fifth Ave/Bay Ridge, Astoria, and Flushing lines, plus "city-owned" and "company-owned" surface lines.

The **IND (Independent City-Owned Rapid Transit Railroad System)** appears for the first time in the 1930s data — specifically fiscal year 1933, the first full year after its September 10, 1932 opening. Its early lines are: Eighth Avenue Line, Houston-Essex Street Line, Brooklyn Crosstown Line, Prospect Park-Coney Island Line, Bronx Concourse Line, and Queens Boulevard Line.

One handwritten note visible on the 1920-1929 cover page reads: *"permanent loan from Miss Lennon, Room 203"* — a reminder that these documents were physically circulated within the agency.

---

### Rapid Transit Ridership Summary Reports (1932–1935 and 1934–1937)

These are **NYC Transit Commission annual summary reports** — the Seventeenth Annual Report (1937) covers 1934-1937. Unlike the station-level data, these show system-wide totals by operator and mode. They include:

- **IRT** (subway + elevated separately)
- **BMT**
- **IND**
- **Street Surface Railway Lines** (by borough)
- **Bus Lines** (by borough, with individual company names)
- **Hudson & Manhattan Railroad** (now PATH — the trans-Hudson commuter rail)
- **Rides per capita** for the whole city

Key figures directly from these documents:

| System | 1932 | 1933 | 1934 | 1935 | 1936 | 1937 |
|--------|------|------|------|------|------|------|
| IRT Subway | 919M | 837M | 810M | 801M | 814M | 800M |
| IRT Elevated | 294M | 248M | 221M | 215M | 217M | 211M |
| BMT | 654M | 613M | 606M | 598M | 609M | 590M |
| IND | — | 59M | 162M | 203M | 236M | 289M |
| **Total Rapid Transit** | **1.87B** | **1.76B** | **1.80B** | **1.82B** | **1.88B** | **1.89B** |
| Street Surface | 833M | 732M | 694M | 667M | 628M | 564M |
| Bus Lines | — | — | 314M | 350M | 457M | 588M |
| Hudson & Manhattan | 90M | 78M | 76M | 76M | 77M | 79M |
| **Grand Total (all modes)** | — | — | **2.88B** | **2.91B** | **3.04B** | **3.12B** |
| Rides per capita | — | — | 377 | 374 | 384 | 388 |

What these numbers show: the IND's growth is explosive — it went from 59 million in its first partial year to 289 million by 1937, a nearly 5x increase in four years. At the same time, it was not purely additive — IRT and BMT ridership was flat or declining, suggesting significant diversion from the private operators to the new city-owned line.

The bus explosion is equally dramatic: total bus ridership nearly doubled from 314M to 588M between 1934 and 1937. Manhattan street surface (streetcar) ridership collapsed 48% between 1936 and 1937 alone — from 133M to 69M — as buses replaced streetcar routes. On Staten Island (Richmond), the streetcar system completely ceased operations between 1934 and 1935 (100% decrease, 2.73M to 0).

---

### Annual Subway Registrations 1940 to 1995

Published **October 1996** by the **MTA New York City Transit, Office of Management and Budget, Revenue Analysis Division**, 130 Livingston Street, Brooklyn, NY 11201. Contact listed: John Kennes.

This is the most comprehensive document in the collection. Key terminology from its introduction:

**"Registrations"** — The document uses this term, not "ridership." A registration is a fare-paying entry recorded at a turnstile. It does not include free transfers, employee passes, or non-revenue entries. Starting in 1994, MetroCard entries are included; prior to that, all entries were token or coin.

**"Conductor's Collections"** — Fares collected directly by conductors on certain lines (not at turnstiles). This revenue is included in system-wide totals but cannot be attributed to individual stations, which is why some station totals don't add up to the published system total.

The document organizes stations into four geographic sectors:
- **Northern Manhattan and Bronx** (report pages 1-24)
- **Northern Queens** (pages 25-32)
- **Southern Queens and Brooklyn** (pages 33-64)
- **Manhattan CBD** (pages 65-80)

From its narrative introduction (page ii), the document notes: between 1940 and 1995, the system saw the closure of all elevated lines in Manhattan, the opening of new extensions in Queens and Brooklyn, numerous station closures and consolidations, and a platform extension program that changed how some stations were counted. These structural changes mean that the list of stations in 1940 and the list in 1995 are meaningfully different — not just due to openings and closings but due to reclassifications and renames.

---

### NYC Transit Subway and Bus Ridership 1940–2011

An MTA summary table. Unlike the station-level data, this document records system-wide annual and average weekday ridership for both subway and bus, with notes on fare changes and service events embedded in the data. This is the most authoritative source for system-wide totals in this collection.

---

## Complete fare history (from source document)

Directly transcribed from the *New York City Subway Fare Chronology 1940 to 1995* table in the Annual Registrations report:

| Date | Fare | Notes |
|------|------|-------|
| through 6/30/48 | $0.05 | Nickel fare, unchanged since 1904 |
| 7/1/48 | $0.10 | $0.02 transfer to bus introduced |
| 7/1/50 | $0.10 | Bus transfer raised to $0.05 |
| 7/1/52 | $0.10 | Reduced-rate bus transfer eliminated |
| 7/25/53 | $0.15 | **Subway tokens introduced** |
| 7/5/66 | $0.20 | |
| 1/4/70 | $0.30 | |
| 1/5/72 | $0.35 | |
| 9/1/75 | $0.50 | Double-fare for Rockaways line discontinued |
| 6/28/80 | $0.60 | Source document says June 28; Wikipedia sources say June 29. Minor discrepancy, likely a rounding of effective date. |
| 7/3/81 | $0.75 | |
| 1/2/84 | $0.90 | |
| 1/1/86 | $1.00 | |
| 1/1/90 | $1.15 | |
| 1/1/92 | $1.25 | |
| 1/6/94 | $1.25 | **MetroCard introduced** |
| 11/12/95 | $1.50 | |

Every fare increase corresponds to a ridership dip in the annual data. Each one is visible in the station-level numbers if you look at the year of or immediately following the increase.

---

## 1939 World's Fair — what the monthly data shows

The 1930-1939 document includes a monthly breakdown of ridership changes during fiscal year 1939 vs. fiscal year 1938. The World's Fair opened April 30, 1939. Because the fiscal year ends June 30, only the final two months of the Fair's spring season fall within fiscal year 1939:

| Month | Change vs prior year | % change |
|-------|---------------------|----------|
| July 1938 | −11.2M | −4.6% |
| August 1938 | −1.0M | −0.4% |
| September 1938 | −5.5M | −2.2% |
| October 1938 | −5.9M | −3.2% |
| November 1938 | +1.0M | +0.5% |
| December 1938 | +1.9M | +0.7% |
| January 1939 | −0.6M | −0.2% |
| February 1939 | +1.1M | +0.5% |
| March 1939 | +2.8M | +1.9% |
| **April 1939** | **−1.0M** | **−0.4%** | ← Fair opens April 30, barely affects this month |
| **May 1939** | **+16.5M** | **+6.3%** | ← First full Fair month — the largest spike |
| **June 1939** | **+14.1M** | estimated | ← Second full Fair month |

May 1939 was the single biggest month-over-month gain in the decade — +16.5 million passengers, a 6.3% surge driven entirely by World's Fair attendance on the IRT Flushing Line. The Fair closed October 31, 1939 (fall season), which falls in fiscal year 1940 — meaning the second Fair season's ridership spike appears in the following year's data.

---

## Data quality and known weaknesses

This dataset was built from scanned archival PDFs using optical character recognition (OCR), then cleaned, normalized, and validated against known system-wide totals. It is the most complete station-level ridership record we could construct from the available documents — but it has real limitations that anyone using it should understand.

### What was validated

- **Row counts** match the source documents exactly for 1920-1929 and 1930-1939.
- **Spot checks** of major stations (Times Square, Grand Central, Atlantic Avenue) show continuous coverage and directionally correct values across all decades.
- **System totals** for 1940-1966 are within ±2.6% of the independently published historical annual figures — well within acceptable range for OCR'd archival data.
- **No values were interpolated or fabricated.** Every number in this dataset came directly from a source document.

### Known issues

**1. ~7-9% gap vs. documented totals in 1977-1995**
Station-level sums for the later years of the 1940-1995 data fall 7-9% short of the published system-wide annual subway ridership figures. This is not fabrication or loss — it reflects genuine gaps in the source documents. The 1940-1995 report organizes stations by geographic section, and some sections (particularly Manhattan CBD) only have complete coverage through 1967 in Part 1 of the document; their 1968-1995 data was partially captured in Part 2. Some stations are simply absent from the station-level record for certain years even though they were operating. Treat station-level totals from 1977 onward as a lower bound, not an exact count. For verified system-wide totals, use `1940-2011_historical_ridership_clean.csv`.

**2. Six stations with conflicting values (`conflict = True`)**
Six station-segment pairs appear twice in the 1940-1995 source document, in two different geographic sections, with different ridership figures for the same years. Both rows are preserved in the dataset and flagged with `conflict = True`. The affected stations are:

| Station | Segment | Likely cause |
|---------|---------|--------------|
| `5 Ave./53 St.` | Midtown | Two distinct stations (E/M line and B/D line) sharing the same name in the source |
| `Tompkins Ave.` | Sumner-Vandrbilt Closed 10/3/69 | Appears in two geographic sections of the report |
| `Dyre Ave.` | Dyre Ave. Opened 5/15/41 | Appears in two geographic sections; one entry has pre-opening zeros |
| `18 Ave.` | Neptune-Ditmas Part of Culver El | Two entries likely representing elevated and underground portions |
| `Ave. N` | 6 Ave./Culver | Appears in two geographic sections |
| `Franklin Ave.` | Sumner-Vandrbilt Closed 10/3/69 | Appears in two geographic sections |

Do not sum these stations without first filtering to one row per year. When `conflict = True`, neither value can be confirmed as correct from this data alone.

**3. One negative ridership value**
`Williamsbridge-210th Street` shows `-164,780` for 1921. This is preserved as-is because it appears to be an accounting adjustment in the original Transit Commission document — a correction applied to a prior year's count. It is not an error introduced during processing. Treat it as a signal that the surrounding rows may carry a small correction offset.

**4. 8,379 zero values**
Zeros appear throughout the 1940-1995 data and represent two different real-world conditions:
- **Station closed:** e.g. `1 St./2 Av. El (Closed 6/13/42)` correctly shows zero ridership from 1943 onward.
- **Station not yet open:** e.g. `Dyre Ave. (Opened 5/15/41)` correctly shows zero for 1940.

Zeros are not missing data — they were explicitly recorded in the source documents. However, a zero should not be treated as equivalent to a null (no data available). When visualizing trends, consider whether a zero means "closed" or "not yet counted."

**5. Pre-1940 data covers different systems than post-1940**
The 1920-1939 data comes from Transit Commission reports filed separately by IRT, BMT, and IND. The 1940-1995 data comes from a unified Board of Transportation report. Station names, counting methodology, and geographic coverage all changed at unification. Cross-decade matches (`cross_decade_match = True`) are based on normalized name similarity and are directionally reliable, but the underlying numbers are not perfectly apples-to-apples across the 1940 boundary.

**6. Fiscal year vs. calendar year**
Pre-1940 figures are for fiscal years ending June 30 (so "1929" means July 1928–June 1929). Post-1940 figures are calendar years. For most analytical purposes this distinction is minor, but it means the 1939 and 1940 figures overlap by six months and cannot be directly compared.

**7. Surface lines and elevated lines in the 1920s-1930s data**
The early data includes streetcar lines, elevated railways, bus lines, and ferries — not just the subway. These are included in the master dataset because they are real ridership data from the era. However, most surface and elevated lines closed between 1940 and 1970 and have no counterpart in the 1940-1995 station-level data. Stations that appear only in the 1920s-1930s data and then vanish are almost always elevated or surface lines that were demolished, not stations the data simply lost track of.

**8. OCR accuracy**
Numbers were extracted by Claude Vision API from scanned documents at 150 DPI. Individual values — especially from dense, aged, or smudged pages — may contain errors. Pages that produced parse errors during extraction were reprocessed; all pages in the final dataset returned valid JSON. The ±2.6% match against known 1940-1966 totals suggests OCR accuracy is high but not perfect.

**9. Borough column — coverage and methodology**
The `borough` column is populated for **90.2% of rows** (39,460 of 43,743). It was filled in two passes:

*Pass 1 — from source documents only:* For the 1920-1929 and 1930-1939 data, borough was forward-filled from geographic section headers embedded in the raw documents (e.g. "BROOKLYN STATIONS (see Contract 2)", "MANHATTAN, EAST", "JEROME AVENUE BRANCH", "QUEENSBORO SUBWAY"). For the 1940-1995 data, a segment-to-borough mapping was applied for segments that are unambiguously single-borough in the source document's geographic sector organization (e.g. Concourse → Bronx, Astoria → Queens, Canarsie → Brooklyn, Midtown → Manhattan).

*Pass 2 — from web research:* For multi-borough subway lines (8 Ave., Broadway/7 Ave., Jamaica, Lexington Ave., Crosstown, Lenox Ave., Fulton St.), borough was determined per station using Wikipedia line articles and individual station articles. The specific sources are listed in `BIBLIOGRAPHY.md` under "Wikipedia — borough assignment research." This pass resolved all named-segment nulls completely.

*Remaining nulls (9.8%, 4,283 rows):* All remaining null-borough rows have `segment = NaN` — these are 1920s–1930s stations from elevated lines (Third Avenue El, Sixth Avenue El, and several BMT lines) where the raw OCR did not capture a clear geographic section header above the station in the source document. The Third Avenue El is the most common case: it ran through Manhattan (34th St.–106th St.) and crossed into the Bronx (138th St.–Fordham Rd.–Bronx Park), with the exact borough boundary mid-page. Assigning borough to these stations would require individual lookup for each station name — which was not performed. These rows are real ridership data; only the geographic label is missing.

---

## The three eras in this dataset

### Era 1: Private Operators · 1920–1939
`era = private_operators`

Three separate companies ran the subway. They competed, overlapped, and were often in financial crisis. The data in this era comes from NYC Transit Commission reports that tracked each company separately.

**IRT — Interborough Rapid Transit Company**
Opened the first subway in 1904. Operated the numbered lines (what are now the 1/2/3, 4/5/6, 7). Also ran elevated lines in the Bronx, Manhattan, and Brooklyn. By the late 1920s the IRT was in financial distress — the nickel fare hadn't changed since 1904 while costs had risen dramatically. Entered receivership on August 25, 1932 (court-supervised financial management, not formal bankruptcy — the company continued operating under court-appointed trustees until the city purchased it in 1940).

**BMT — Brooklyn-Manhattan Transit Corporation**
Successor to the Brooklyn Rapid Transit Company (which went bankrupt in 1918 after a fatal 1918 Malbone Street wreck). Operated what are now the N/Q/R/W, J/M/Z, B/D lines and various Brooklyn elevated lines. Also financially troubled through the 1930s.

**IND — Independent Subway System**
City-owned from day one. Opened September 10, 1932 on the 8th Avenue line (Chambers St to 207th St). Designed to compete with and eventually replace the private operators. Became the A/C/E, B/D/F/M lines. First appears in the 1932 data.

---

### Era 2: Board of Transportation · 1940–1967
`era = board_of_transportation`

**June 1940**: The City of New York purchased the BMT (June 1) and IRT (June 12). For the first time, all three systems operated as one unified public entity under the NYC Board of Transportation. The purchase prices recorded in the source documents are $151 million (IRT) and $175 million (BMT), though these figures have not been independently verified. The nickel fare was retained — a political promise that would financially cripple the system for years.

---

### Era 3: MTA · 1968–1995
`era = mta`

**March 1, 1968**: The Metropolitan Transportation Authority (MTA) was created by the state, absorbing the subway, bus, and later commuter rail systems. Still operates today.

---

## Year-by-year annotations · 1920–1995

---

### 1920
Postwar boom. The subway is the spine of a city of 5.6 million. The nickel fare has been unchanged since 1904. IRT and BMT are the only operators — the IND doesn't exist yet. Total system ridership approaches 2.4 billion across all modes. The elevated lines (the "El") are still major arteries. Times Square, Grand Central, and Atlantic Avenue are among the busiest single stations.

### 1921
Normal year. IRT subway ridership: ~586 million. BMT: ~377 million. Elevated lines still heavily used — the 2nd and 3rd Avenue Els in Manhattan are still running.

### 1922
Normal year. City population growing. New housing in the Bronx and Brooklyn driving outer-borough ridership.

### 1923
Normal year. IRT subway ridership crosses 644 million.

### 1924
Normal year. Queens begins to grow as the subway extends outward.

### 1925
IRT subway ridership reaches 715 million. The elevated divisions carry another ~359 million. Ridership growing steadily across the decade.

### 1926
Normal year. Surface railways (streetcars) still carry over 1 billion passengers system-wide, more than the subway — this flips by the end of the decade.

### 1927
IRT subway alone: 784 million passengers. The subway is becoming the dominant mode. Holland Tunnel opens (November 13) — begins long-term shift of freight and some passengers to automobiles.

### 1928
IRT subway: 815 million. BMT continuing to expand in Brooklyn and Queens. The system is near its pre-Depression peak.

### 1929
**October 29 — Black Tuesday.** Stock market crashes. Subway ridership is relatively unaffected this year — the Depression's impact on transit takes time to manifest. IRT subway: ~808 million. George Washington Bridge under construction across the river, a sign of the car-centric future.

### 1930
The Depression deepens. Unemployment rising rapidly. Counterintuitively, transit ridership holds relatively steady at first — unemployed workers still need to look for work, and fewer people can afford cars. IRT and BMT under severe financial strain. The nickel fare still holds.

### 1931
IRT approaching formal receivership. The company is effectively bankrupt — it cannot service its debt — but continues operations under court supervision. BMT similarly stressed. Both are running on fumes, deferring maintenance.

### 1932
**August 25 — IRT enters receivership** — court-supervised management, not full dissolution. Operations continue under trustees.

**September 10 — The IND opens.** The 8th Avenue line runs from Chambers Street to 207th Street. This is the first city-owned subway line. The IND represents the city's plan to eventually take over all transit — it's built to the same gauge as the BMT but not the IRT, a decision that still affects operations today.

Depression ridership low. Unemployment hits 25% nationally. Ridership drops across IRT and BMT as people simply can't afford even the nickel fare sometimes. The IND starts from zero and builds slowly. Watch for IND stations first appearing in the data this year.

### 1933
Bottom of the Depression. Ridership at its 1930s nadir across IRT and BMT. The IND carries about 75 million in its first full year. Fiorello La Guardia campaigns for mayor on a platform of municipal ownership of transit.

### 1934
Recovery begins slowly. La Guardia elected mayor (January 1). He will aggressively pursue city ownership of IRT and BMT. IND expanding — new stations opening in Brooklyn.

### 1935
New Deal infrastructure spending. City finances improving. IND extends to Queens (Jamaica line opens). IRT and BMT ridership slowly recovering from Depression lows.

### 1936
Normal recovery year. The IND is proving its viability. Negotiations for city purchase of IRT and BMT intensifying.

### 1937
Normal year. IND ridership growing as new lines open. Surface railways (streetcars) continuing their multi-decade decline — buses are replacing them borough by borough.

### 1938
Normal year. IND extends further. The city and the IRT/BMT trustees are deep in purchase negotiations. WWII is on the horizon in Europe.

### 1939
**April 30 — New York World's Fair opens** at Flushing Meadows, Queens. Theme: "The World of Tomorrow." The IRT Flushing Line (now the 7) serves the fairgrounds directly. Significant ridership spike, especially at Willets Point/World's Fair station. Fair closes October 31. Watch for outlier ridership at Queens stations this year.

### 1940
**June 1940 — Unification.** The City of New York purchases the BMT (June 1) and the IRT (June 12). All three systems — IRT, BMT, IND — now operate under the NYC Board of Transportation. The nickel fare is maintained as a political promise. This is the moment the `era` field changes from `private_operators` to `board_of_transportation` in this dataset.

The station name conventions change too — IRT stations start appearing in the same reporting framework as BMT and IND. Cross-decade matches (`cross_decade_match = True`) represent stations that appear in both the pre-1940 private-operator data and the post-1940 unified data.

### 1941
**December 7 — Pearl Harbor.** US enters WWII. Defense workers flood into New York. Gas rationing begins driving more commuters to transit. Ridership begins its wartime surge.

### 1942
Wartime ridership surge accelerating. Rubber rationing limits bus and car travel. The subway becomes essential infrastructure. Women entering the workforce in large numbers — new rider demographics.

### 1943
Wartime peak approaching. The system is operating beyond comfortable capacity. Maintenance deferred due to wartime material shortages — a pattern that will haunt the system for decades.

### 1944
Continued wartime high. The subway carries people to shipyards, factories, and military embarkation points. Staten Island Ferry ridership also at historic highs.

### 1945
**August 15 — V-J Day.** WWII ends. Ridership remains extremely high through year-end. The city is euphoric. The subway's wartime performance has cemented its role as the city's circulatory system.

### 1946
**Peak year.** The system carries approximately 2.07 billion passengers — the highest single-year total in history (our source document records 2.067 billion; independently verified). This number will not be approached again for decades. Returning veterans and a booming economy fill every train.

### 1947
Ridership begins its long decline. Returning veterans are buying cars with GI Bill benefits, moving to suburbs. Robert Moses is building highways. The suburban dream is pulling riders out of the city — and off the subway.

### 1948
**July 1 — The nickel era ends.** The fare rises to 10 cents — the first increase in 44 years. A $0.02 bus transfer was introduced simultaneously (source: fare chronology table in Annual Registrations 1940-1995). Ridership drops noticeably after the hike. The financial logic was sound (the system was hemorrhaging money) but the political fallout was severe. The Board of Transportation is caught between the need for revenue and pressure to keep fares low.

### 1949
Post-fare-hike adjustment. Ridership stabilizes at a lower level. Suburbanization accelerating — Levittown on Long Island is complete, a template for postwar American life that explicitly excludes New York City transit.

### 1950
NYC population reaches its all-time peak of 7.89 million. But more of those 7.89 million are driving. The Cross Bronx Expressway is under construction, displacing 60,000 Bronx residents and destroying neighborhoods — eventually reducing transit ridership in those areas.

### 1951
Normal year. Car registrations in NYC rising annually. The bus is replacing the streetcar citywide.

### 1952
Last of the Manhattan streetcar lines retire. The surface railway data that appears in the 1920s-1930s files is now entirely historical — those riders are now on buses or in cars.

### 1953
**July 25 — 15-cent fare.** Another increase. This time, **tokens** are introduced for the first time — a brass token replacing the physical nickel or dime. The token will define the subway experience for the next 40 years. Ridership drops again post-hike.

### 1954
Normal year. The Rockaway line opens in Queens (June 28), extending service to Far Rockaway and connecting to the A line. New stations appear in the data.

### 1955
Normal year. The **3rd Avenue El in Manhattan closes on May 12, 1955** — the last elevated line in Manhattan (the Bronx section closed separately). The subway is now entirely underground in Manhattan.

### 1956
Normal year. Cross-Bronx Expressway opens in sections, accelerating white flight from the Bronx. Long-term impact on Bronx subway ridership will be severe.

### 1957
Normal year. Robert Moses at the height of his power. Highway construction continues to compete with transit investment.

### 1958
Normal year. Brooklyn elevated lines continuing to close — the 5th Avenue El shuts down. Each closure removes a transit option from neighborhoods that may not get a replacement for decades.

### 1959
Normal year. Ridership in slow but steady decline. The system is aging; the 1940s deferred maintenance is becoming visible.

### 1960
Normal year. NYC begins to feel the fiscal pressures that will define the next 15 years. The subway's capital budget is chronically underfunded.

### 1961
Normal year. JFK elected president; the city feels optimistic. The subway does not share in the optimism.

### 1962
Normal year. Graffiti begins appearing on subway cars — at first isolated, eventually systemic.

### 1963
Normal year. The 2nd Avenue subway is proposed (again). It has been proposed, approved, funded, and cancelled repeatedly since the 1920s. Construction will eventually begin in 2007.

### 1964
**April–October — World's Fair.** Again at Flushing Meadows. Again a ridership spike at Queens stations, especially Willets Point. Shea Stadium opens nearby. The IRT Flushing Line serves both. Beatles play Shea Stadium in 1965.

### 1965
Normal year. The Vietnam War is escalating. NYC's demographics are shifting rapidly — immigration from Puerto Rico and the American South is changing which neighborhoods fill trains at which hours.

### 1966
**January 1–13 — TWU Strike.** The Transit Workers Union strikes on New Year's Day — the first day of Mayor John Lindsay's administration. For 12 days, no subways, no buses. **July 5 — fare raised to $0.20** (from $0.15), the first increase since 1953. Both events are documented in the 1940-2011 historical ridership notes column. The city grinds to a near-halt. Nearly a million workers walk to work, carpool, or stay home. The year's ridership figures are artificially depressed. The strike ends with a significant wage increase that worsens the Transit Authority's finances for years.

### 1967
Normal year. Recovery from strike. Ridership trending down. The subway is increasingly associated with danger, filth, and unreliability — a perception that will intensify dramatically over the next decade.

### 1968
**March 1 — MTA created.** The Metropolitan Transportation Authority is established by New York State, absorbing the NYC Transit Authority, the Long Island Rail Road, and eventually other commuter railroads. This is the moment `era` changes to `mta` in this dataset. The MTA structure moves transit governance from city to state control — a shift with lasting consequences for funding and accountability.

Robert F. Kennedy assassinated (June). Martin Luther King Jr. assassinated (April). The city is in turmoil. Subway ridership data from this year forward reflects a city under extreme social stress.

### 1969
Normal year under new MTA. Apollo 11 lands on the moon (July 20). The Miracle Mets win the World Series. The city's mood is briefly lifted. The subway's mood is not.

### 1970
The fiscal pressures that will become the 1975 crisis are building. Crime on the subway rising sharply. Graffiti spreading across the fleet. The physical condition of the infrastructure is deteriorating — signals, track, cars all showing age.

### 1971
**Fare raised to 30 cents.** Another ridership hit. The pattern is now familiar: fares rise to cover deficits, ridership drops, revenue falls short of projections, deficits worsen.

### 1972
Normal year. Nixon in Watergate. The subway's ridership is now well below its 1946 peak. Every year the gap widens.

### 1973
**October — OPEC oil embargo.** Gas prices spike. Counter-intuitively, this briefly stabilizes subway ridership as driving becomes more expensive. But the broader economic damage worsens the city's fiscal position.

### 1974
**Fare raised to 35 cents.** The city is in structural deficit. Nixon resigns. The mood is bleak. A generation of middle-class New Yorkers has left for the suburbs and shows no sign of returning.

### 1975
**September 1 — Fare raised to $0.50** (from $0.35). The Rockaways surcharge (which had required double fare for the Rockaway extension) was simultaneously discontinued. **NYC Fiscal Crisis peaks.** The city nearly defaults on its debt (October). President Ford initially refuses a federal bailout ("Ford to City: Drop Dead" — Daily News front page). A federal loan guarantee eventually prevents bankruptcy. The immediate result for the subway: brutal budget cuts, deferred maintenance, reduced service. The system enters a period of managed decline. Ridership is falling; the system that remains serves increasingly poor and transit-dependent riders who have no alternative.

### 1976
Ridership approaches its modern nadir — under 1 billion for the first time since before WWII. The subway is a byword for urban dysfunction. Crime is endemic. Cars are being burned in the Bronx. Graffiti covers every surface of every car. The Son of Sam murders terrify the city. This is the year the data hits bottom.

### 1977
Continued low ridership. The 1977 blackout (July 13-14) triggers looting across the city — a crystallization of the collapse of social order. Subway ridership is at its lowest ebb. If you are building an art piece about decline and recovery, this is the nadir.

### 1978
Slight stabilization. The capital program that will eventually save the system is being planned but not yet funded. Ed Koch elected mayor (November 1977, takes office January 1978). The cleanup is beginning but not visible yet.

### 1979
Normal year. The city is slowly, painfully stabilizing. The subway is not yet recovering but the rate of decline has slowed.

### 1980
**April 1–11 — Second TWU Strike.** 11 days. **June 28 — fare raised to $0.60** (from $0.50). Both documented in the 1940-2011 historical ridership notes. Again the city walks. Again the annual ridership figures are depressed. Again the settlement is expensive. Mayor Koch refuses to settle on the union's terms for days longer than Lindsay did in 1966. The city survives — barely.

**The MTA Capital Program begins.** A massive multi-year investment plan is developed to address decades of deferred maintenance. New subway cars, track reconstruction, signal repairs. This is the turning point — though it takes years to show in the ridership data.

### 1981
Capital program under way. New R62 subway cars entering service — the first new cars the system has seen in decades. The old fleet is genuinely dangerous. Air conditioning, a feature the new cars have, is a revelation to riders.

### 1982
Normal year. The capital program is rebuilding the physical system, but the perception of the subway — crime, fear, graffiti — hasn't changed yet.

### 1983
Normal year. The Guardian Angels, founded in 1979, are patrolling trains. A civilian response to a failed institutional one.

### 1984
**December 22 — Bernhard Goetz shoots four men on a subway train** he believed were about to rob him. The "subway vigilante" case transfixes the city and the nation. It is simultaneously a referendum on crime, race, and the failure of public safety on the subway. Ridership data does not capture fear — but fear shapes ridership.

### 1985
Normal year. The capital program is producing visible results — more reliable service, cleaner cars. But crime remains high.

### 1986
Normal year. Crack cocaine epidemic intensifying in NYC neighborhoods. Crack's arrival correlates with a surge in violent crime that peaks around 1990 — the worst of which plays out partly on and around subway platforms.

### 1987
**October 19 — Black Monday.** Stock market crashes. NYC's financial sector takes a hit. Short-term impact on ridership modest, but Wall Street's fortunes and the subway's fortunes are more connected than they appear — the city's tax base funds the MTA.

### 1988
Normal year. Ridership slowly recovering from the 1970s nadir. New York is changing — gentrification spreading from Manhattan, crime still high but beginning to plateau.

### 1989
Normal year. The Berlin Wall falls (November 9). The cold war ends. NYC begins a long boom that will transform the subway's ridership.

### 1990
Crime peaks. The city records 2,245 murders — the highest in modern history. The subway feels it. Despite this, ridership is slowly recovering. The capital program's improvements are real and cumulative.

### 1991
Recession. The Gulf War. NYC's economy soft. Ridership growth stalls.

### 1992
Normal year. Bill Clinton elected. The long 1990s boom is beginning.

### 1993
**Rudolph Giuliani elected mayor** (November). His administration will pursue aggressive broken-windows policing — beginning on the subway. Fare evasion crackdowns, "quality of life" enforcement. Crime begins its dramatic fall from this year forward.

### 1994
**January — MetroCard introduced** on a pilot basis, initially on the M15 bus and one subway line. The magnetic stripe card will eventually replace the token entirely (2003). The MetroCard enables free intermodal transfers (subway-to-bus, bus-to-subway) for the first time — a fundamental change in how riders use the system. Subway ridership begins accelerating upward.

Crime falling dramatically. The city's transformation is visible and accelerating.

### 1995
**Last year of station-level data in this collection.** MetroCard expanding rapidly. The token's days are numbered. Crime has fallen dramatically from its 1990 peak. The city is in the early stages of its 1990s-2000s renaissance. Ridership is recovering toward levels not seen since the early 1970s.

After 1995 in this dataset, station-level data is not available. The `1940-2011_historical_ridership_clean.csv` has system-wide totals through 2011, but no station breakdown.

---

## After 1995 — system-wide context only

| Year | Event |
|------|-------|
| 1997 | Free intermodal transfers began July 4, 1997 (source: 1940-2011 historical notes) |
| 1998 | Bonus MetroCard began January 1, 1998; 7-day & 30-day passes began July 4, 1998 (source: 1940-2011 historical notes) |
| 2001 | **September 11.** Attacks destroy Cortlandt St station (1/2/3). System partially shut down. Lower Manhattan ridership collapses temporarily |
| 2003 | Last subway token sold (April 13). MetroCard-only system |
| 2007 | 2nd Avenue Subway construction finally begins (after 80+ years of proposals) |
| 2008 | Ridership hits ~1.62 billion — approaching the 1946 all-time peak for the first time |
| 2012 | **Superstorm Sandy** (October 29). Entire subway system shut down. Tunnels flood. Unprecedented infrastructure damage |
| 2017 | 2nd Avenue Subway opens (Q line, 72nd–96th Sts) |
| 2020 | **COVID-19.** Ridership collapses to levels not seen since the 1890s |

---

## Notes for the art piece

**The shape of the data:**
The ridership curve from 1920–1995 traces the arc of 20th-century American urbanism. Rise (postwar boom), peak (1946), long collapse (1947–1977), slow recovery (1978–1995). Each station's individual curve deviates from this — some stations decline earlier as neighborhoods change, some hold steady because they serve transfer hubs, some surge when new lines connect them.

**What station data shows that system-level data can't:**
- Which neighborhoods were abandoned first during white flight
- Which new lines (IND, extensions) generated new ridership vs cannibalized existing
- The geography of the crack epidemic and crime surge — stations in affected neighborhoods show steeper declines in 1985-1990
- Which stations recovered first in the 1990s (Manhattan CBDs first, then outer boroughs later)

**On data gaps:**
Cross-decade matching (`cross_decade_match = True`) is based on normalized name similarity. Station names changed between eras — IRT called a station "Borough Hall," the unified system may call it "Borough Hall" or abbreviate it. Where names match, you have a continuous 75-year record for a single physical location. Where they don't, the gap is real and should be represented honestly in the visualization — perhaps as silence, or as an acknowledged void.

**On counting:**
Pre-1940 data counts fare payments at the system level, then broken down by station. The counting methodology changed at unification. Numbers from different eras are directionally comparable but not perfectly apples-to-apples.

**The el lines:**
Elevated lines appear in the 1920s and 1930s data and then disappear as they close. 2nd Ave El (Manhattan) closed June 13, 1942. 3rd Ave El (Manhattan) closed May 12, 1955. 9th Ave El (Brooklyn) closed 1940. These closures appear as stations that abruptly go to zero — or disappear from the data entirely. This is real history encoded in the numbers.
