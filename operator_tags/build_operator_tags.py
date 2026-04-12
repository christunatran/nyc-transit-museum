"""
build_operator_tags.py

Adds operator/line tagging and accounting-metadata columns to
master_ridership_long.csv.

Inputs:
  /mnt/project/master_ridership_long.csv
  /mnt/project/19201929_ridership_clean.csv
  /mnt/project/19301939_ridership_clean.csv
  /mnt/user-data/outputs/segment_operator_lookup.csv

Output:
  /mnt/user-data/outputs/master_ridership_with_operator.csv

New columns:
  original_operator    str    IRT | BMT | IND | aggregate | SUMMARY | unknown
  original_line        str    line/contract name (pre-1940 mainly)
  joint_operation      bool   True for IRT/BMT joint stations (Astoria/Flushing/Queensboro)
  is_aggregate_row     bool   True for non-station accounting rows (conductor colls, credits)
  methodology_note     str    free-text caveat where one applies (nullable)
  unit_of_measurement  str    explicit unit: fares vs turnstile registrations vs MetroCard
"""
import pandas as pd
import numpy as np
import re

# -------- INPUT PATHS (edit to match your environment) --------
MASTER  = '/mnt/project/master_ridership_long.csv'
LOOKUP  = '/mnt/user-data/outputs/segment_operator_lookup.csv'
CSV_20  = '/mnt/project/19201929_ridership_clean.csv'
CSV_30  = '/mnt/project/19301939_ridership_clean.csv'
OUT     = '/mnt/user-data/outputs/master_ridership_with_operator.csv'

master = pd.read_csv(MASTER)
lookup = pd.read_csv(LOOKUP)
df20   = pd.read_csv(CSV_20)
df30   = pd.read_csv(CSV_30)

# ============================================================
# STAGE 1: Tag pre-1940 source CSVs with operator + line
# ============================================================
# Page -> operator mapping verified by visual PDF inspection
PAGE_OP_20 = {2:'SUMMARY', 3:'IRT', 4:'IRT', 5:'IRT', 6:'IRT', 7:'IRT',
              8:'BMT', 9:'BMT', 10:'BMT'}
PAGE_OP_30 = {1:'SUMMARY', 2:'SUMMARY',
              3:'IRT', 4:'IRT', 5:'IRT', 6:'IRT', 7:'IRT',
              8:'BMT', 9:'BMT', 10:'BMT',
              11:'IND', 12:'IND'}

# Page-level line fallback when no explicit header appears (1920s Contract 1/2)
PAGE_CONTRACT_20 = {3:'Contract 1 & 2 Stations', 4:'Contract 3 Stations',
                    5:'Contract 3 Stations / Elevated Division', 6:'Elevated Division'}
PAGE_CONTRACT_30 = {3:'Contract 1 & 2 Stations', 4:'Contract 3 Stations',
                    5:'Contract 3 Stations / Elevated Division', 6:'Elevated Division'}

df20['_operator'] = df20['_page'].map(PAGE_OP_20)
df30['_operator'] = df30['_page'].map(PAGE_OP_30)

LINE_HDR = re.compile(r'\b(LINE|BRANCH|DIVISION|STATIONS|CONTRACT|ELEVATED|SUBWAY)\b', re.I)
TOTAL_RE = re.compile(r'^\s*(Total|Grand Total|Miscellaneous|Dr\.|DR\.|Cr\.|CR\.|Per Cent|Adjustment|.*ADJUSTMENT|.*TOTAL)', re.I)

def is_line_header(s):
    if not isinstance(s, str): return False
    letters = [c for c in s if c.isalpha()]
    if len(letters) < 4: return False
    return sum(1 for c in letters if c.isupper()) / len(letters) > 0.7 and bool(LINE_HDR.search(s))

def is_aggregate_label(s):
    if not isinstance(s, str): return False
    return is_line_header(s) or bool(TOTAL_RE.match(s.strip()))

def ff_line(df, use_col=False, page_fallback=None):
    df = df.sort_values('_page').reset_index(drop=True)
    current_line, current_page = None, None
    out = []
    for _, row in df.iterrows():
        if row['_page'] != current_page:
            current_line = None
            current_page = row['_page']
        if use_col and isinstance(row.get('line'), str) and row['line'].strip():
            current_line = row['line'].strip()
        else:
            lbl = row['label'] if isinstance(row['label'], str) else ''
            if is_line_header(lbl):
                current_line = lbl.strip()
        eff = current_line if current_line is not None else (page_fallback or {}).get(row['_page'])
        out.append(eff)
    df['_line'] = out
    return df

df20 = ff_line(df20, use_col=False, page_fallback=PAGE_CONTRACT_20)
df30 = ff_line(df30, use_col=True,  page_fallback=PAGE_CONTRACT_30)

JOINT_RE = re.compile(r'(ASTORIA|FLUSHING|QUEENSBORO)', re.I)
def is_joint_row(row):
    line = row.get('_line')
    if isinstance(line, str) and JOINT_RE.search(line): return True
    lbl = row.get('label')
    if isinstance(lbl, str) and re.search(r'Queensboro Plaza', lbl, re.I): return True
    return False

for d in (df20, df30):
    d['_joint'] = d.apply(is_joint_row, axis=1)
    d['_agg']   = d['label'].apply(is_aggregate_label)

# ============================================================
# STAGE 2: Pivot source CSVs to long form to match master keys
# ============================================================
def to_long(df, year_cols, src_label):
    id_cols = ['_page','label','_operator','_line','_joint','_agg']
    long = df.melt(id_vars=id_cols, value_vars=year_cols,
                   var_name='year', value_name='ridership')
    long['year'] = long['year'].astype(int)
    long['source'] = src_label
    return long

long_all = pd.concat([
    to_long(df20, [str(y) for y in range(1920,1930)], 'IRT/BMT (1920s)'),
    to_long(df30, [str(y) for y in range(1930,1940)], 'IRT/BMT/IND (1930s)'),
], ignore_index=True)

# ============================================================
# STAGE 3: Apply to master
# ============================================================
seg_map = dict(zip(lookup['segment'], lookup['operator']))
master['original_operator'] = master['segment'].map(seg_map)
master['original_line']     = pd.Series([np.nan]*len(master), dtype='object')
master['joint_operation']   = False
master['is_aggregate_row']  = False
master['methodology_note']  = pd.Series([np.nan]*len(master), dtype='object')

# Post-1940 rows without segment: unknown
post = master['era'].isin(['board_of_transportation','mta'])
unknown_post = post & master['segment'].isna()
master.loc[unknown_post, 'original_operator'] = 'unknown'
master.loc[unknown_post, 'methodology_note'] = (
    'Station has no segment tag in the 1940-1995 source document, so operator cannot '
    'be assigned from segment lookup. Manual disambiguation needed.'
)

# Pre-1940: merge
pre_idx = master[master['era']=='private_operators'].index
pre_key = master.loc[pre_idx, ['_page','label','source','year','ridership']].reset_index()
merged = pre_key.merge(
    long_all[['_page','label','source','year','ridership','_operator','_line','_joint','_agg']],
    on=['_page','label','source','year','ridership'], how='left'
)
merged.set_index('index', inplace=True)

master.loc[merged.index, 'original_operator'] = merged['_operator'].values
master.loc[merged.index, 'original_line']     = merged['_line'].values
master.loc[merged.index, 'joint_operation']   = merged['_joint'].fillna(False).astype(bool).values
master.loc[merged.index, 'is_aggregate_row']  = merged['_agg'].fillna(False).astype(bool).values

# ============================================================
# STAGE 4: Methodology notes
# ============================================================
def append_note(existing, addition):
    if pd.isna(existing) or existing == '':
        return addition
    return f'{existing} | {addition}'

# Joint-operation caveat (pre-1949)
joint_note = (
    'Joint IRT/BMT operation (1923-1949). Ridership shown is IRT net share after '
    'allocation to NYRTC/BMT per source footnote. BMT share of same station is on '
    'non-digitized source pages (149/151) and is not in this dataset.'
)
jmask = master['joint_operation'] & (master['year']<=1949)
master.loc[jmask, 'methodology_note'] = master.loc[jmask, 'methodology_note'].apply(
    lambda x: append_note(x, joint_note)
)

# Queensboro Plaza 1930 definition-change
qp_1930s = (master['label']=='Queensboro Plaza') & (master['year'].between(1930, 1939))
master.loc[qp_1930s, 'methodology_note'] = master.loc[qp_1930s, 'methodology_note'].apply(
    lambda x: append_note(x, '1930s Queensboro Plaza values are ~5x the 1920s values due to an apparent source-document definition change in 1930 (broader inclusion scope).')
)

# Conductor collections (on-train, not station-attributable)
conductor_mask = master['label'].str.contains('conductor', case=False, na=False)
master.loc[conductor_mask, 'is_aggregate_row'] = True
master.loc[conductor_mask, 'methodology_note'] = master.loc[conductor_mask, 'methodology_note'].apply(
    lambda x: append_note(x, 'Conductor collections — fares collected on the train, not at a turnstile. Included in line totals but not attributable to any specific station.')
)

# Inter-company ticket credits
ticket_cr_mask = master['label'].str.contains(r"Rapid Transit Corp.*Tickets", case=False, na=False, regex=True)
master.loc[ticket_cr_mask, 'is_aggregate_row'] = True
master.loc[ticket_cr_mask, 'methodology_note'] = master.loc[ticket_cr_mask, 'methodology_note'].apply(
    lambda x: append_note(x, 'Inter-company ticket credit — not a station count; represents tickets sold by one company credited to the other.')
)

# Partial-year stations (opened mid-year)
dated_re = re.compile(r'\(from\s+([A-Za-z]+\.?\s*\d+,?\s*\d{4}|\d+/\d+/\d+)', re.I)
def extract_start_year(label):
    if not isinstance(label, str): return None
    m = dated_re.search(label)
    if not m: return None
    text = m.group(1)
    ym = re.search(r'(19\d\d|20\d\d)', text)
    if ym: return int(ym.group(1))
    ym2 = re.search(r'/(\d\d)\b', text)
    if ym2:
        yy = int(ym2.group(1))
        return 1900 + yy if yy >= 20 else 2000 + yy
    return None

start_years = master['label'].apply(extract_start_year)
partial_mask = start_years.notna() & (master['year'] == start_years)
master.loc[partial_mask, 'methodology_note'] = master.loc[partial_mask, 'methodology_note'].apply(
    lambda x: append_note(x, 'Partial-year: station opened mid-year per label. Ridership reflects only months after opening, not a full year.')
)

# ============================================================
# STAGE 5: unit_of_measurement column (explicit about what "ridership" counts)
# ============================================================
def unit_for_row(row):
    era = row['era']
    if era == 'private_operators':
        return 'fare_dollars_implied_fare_count'  # source = fares collected in $; converts at fixed 5c
    if era == 'board_of_transportation':
        return 'turnstile_registrations'
    if era == 'mta':
        if row['year'] >= 1994:
            return 'turnstile_registrations_incl_metrocard'
        return 'turnstile_registrations'
    return 'unknown'

master['unit_of_measurement'] = master.apply(unit_for_row, axis=1)

# ============================================================
# STAGE 6: Diagnostics + save
# ============================================================
print('=== original_operator by era ===')
print(master.groupby(['era','original_operator'], dropna=False).size().unstack(fill_value=0))
print('\n=== unit_of_measurement ===')
print(master['unit_of_measurement'].value_counts())
print('\n=== joint_operation ===')
print(master['joint_operation'].value_counts())
print('\n=== is_aggregate_row ===')
print(master['is_aggregate_row'].value_counts())
print('\n=== rows with a methodology_note ===')
print(master['methodology_note'].notna().sum())

master.to_csv(OUT, index=False)
print(f'\nwrote {len(master)} rows, {len(master.columns)} columns to {OUT}')
