"""
Dataset Build Pipeline for ZIZIPHUS JUJUBA.
Integrates raw log parsing, multi-category auditing, SQLite storage,
repeated number analysis, and export generation.
"""

import pathlib
import json
import csv
import collections
import hashlib
from typing import List, Dict, Any

from src.database.db_manager import DatabaseManager
from src.parsing.log_parser import UVBLogParser
from src.cleaning.audit_deduplication import DataAuditor

BASE_DIR = pathlib.Path("D:/Projects/ZIZIPHUS_JUJUBA")
RAW_LOGS_DIR = BASE_DIR / "data/raw/github_repo/UVB-76-Structured-Signal-Analysis-main/data/raw"
CLEANED_DIR = BASE_DIR / "data/cleaned"
EXPORTS_DIR = BASE_DIR / "exports"
DOWNLOADS_DIR = pathlib.Path("C:/Users/User/Downloads")
EVENTS_FILE = BASE_DIR / "data/historical_events/events_2013_2014.json"

def run_pipeline():
    print("=" * 60)
    print("ZIZIPHUS JUJUBA: INITIATING DATA PIPELINE")
    print("=" * 60)
    
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Initialize Database
    db = DatabaseManager()
    db.reset_db()
    print("SQLite database reset and schema initialized.")
    
    # 2. Parse Raw Logs
    parser = UVBLogParser()
    all_raw_messages = []
    source_stats = {}
    
    log_files = sorted(RAW_LOGS_DIR.glob("*_logs.txt"))
    for lf in log_files:
        if lf.name == "2010_logs.txt":
            # 2010_logs.txt contains spike dates rather than raw radiogram text
            continue
        content = lf.read_bytes()
        sha256 = hashlib.sha256(content).hexdigest()
        lines = lf.read_text(encoding="utf-8", errors="replace").splitlines()
        
        src_id = db.insert_source(
            file_name=lf.name,
            source_url="https://priyom.org",
            total_lines=len(lines),
            retrieval_date="2026-10-16",
            checksum_sha256=sha256,
            notes=f"Archival log file for year {lf.stem.split('_')[0]}"
        )
        
        recs = parser.parse_file(lf)
        for r in recs:
            r['source_id'] = src_id
        all_raw_messages.extend(recs)
        source_stats[lf.name] = len(recs)
        print(f"  Parsed {lf.name}: {len(recs)} entries (SHA256: {sha256[:12]}...)")
        
    print(f"Total raw message entries parsed: {len(all_raw_messages)}")
    
    # 3. Audit & Deduplication
    auditor = DataAuditor()
    audited_all, primary_records, stats = auditor.audit_and_deduplicate(all_raw_messages)
    
    print("\n--- AUDIT & DEDUPLICATION RESULTS ---")
    print(f"Total raw parsed: {stats['total_raw_records']}")
    print(f"Total deduplicated primary broadcasts: {stats['total_deduplicated_primary']}")
    print(f"Total flagged duplicates/anomalies: {stats['total_flagged_duplicates']}")
    print("Duplicates by category:", stats['duplicates_by_category'])
    print("Year counts (before):", stats['year_counts_before'])
    print("Year counts (after deduplication):", stats['year_counts_after'])
    
    # 4. Load Historical Events
    events_data = []
    if EVENTS_FILE.exists():
        events_data = json.loads(EVENTS_FILE.read_text(encoding='utf-8'))
        print(f"Loaded {len(events_data)} historical events.")
        
    # 5. High performance batch insertion into SQLite
    print("\nPopulating SQLite database (batch transaction)...")
    db.batch_insert_all(audited_all, auditor.audit_log, events_data)
    print("Database population completed successfully.")
        
    # 6. Build Repeated Numbers and Crossword Links
    print("\nAnalyzing repeated numbers and crossword links...")
    # Repeated numbers across ALL records (before deduplication)
    all_pairs = []
    for r in audited_all:
        for b in r.get('blocks', []):
            all_pairs.append({
                'date': r['date'],
                'time': r['time_as_logged'],
                'callsign': r['callsign'],
                'word': b['code_word'],
                'digits': b['digit_combination'],
                'digit_group_1': b['digit_group_1'],
                'digit_group_2': b['digit_group_2'],
                'source_file': r['source_file'],
                'source_line': r['source_line'],
                'is_duplicate': r.get('is_duplicate', 0)
            })
            
    # Deduplicated pairs (primary only)
    dedup_pairs = [p for p in all_pairs if not p['is_duplicate']]
    
    def extract_shared_numbers(pairs_list):
        by_digits = collections.defaultdict(list)
        for p in pairs_list:
            by_digits[p['digits']].append(p)
        shared = []
        for digits, entries in by_digits.items():
            if len(entries) > 1:
                words = sorted(set(x['word'] for x in entries))
                dates = sorted(set(x['date'] for x in entries))
                shared.append({
                    'digits': digits,
                    'distinct_words': len(words),
                    'occurrences': len(entries),
                    'words': ' | '.join(words),
                    'dates': ' | '.join(dates),
                    'sources': ' | '.join(sorted(set(f"{x['source_file']}:{x['source_line']}" for x in entries)))
                })
        shared.sort(key=lambda x: (-x['distinct_words'], -x['occurrences'], x['digits']))
        return shared

    repeated_all = extract_shared_numbers(all_pairs)
    repeated_deduped = extract_shared_numbers(dedup_pairs)
    
    # Crossword number links specifically where distinct_words > 1
    crossword_links = [x for x in repeated_deduped if x['distinct_words'] > 1]
    
    print(f"Repeated number combinations (all records): {len(repeated_all)}")
    print(f"Repeated number combinations (deduplicated): {len(repeated_deduped)}")
    print(f"Crossword number links (distinct words > 1): {len(crossword_links)}")
    
    # 7. Generate CSV and JSON Exports
    def write_csv(filepath, rows, fieldnames):
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
            
    msg_fields = [
        'source_file', 'source_line', 'date', 'year', 'month', 'day',
        'time_as_logged', 'timezone', 'callsign', 'header_number',
        'full_word_sequence', 'block_count', 'quality_flag',
        'is_duplicate', 'duplicate_type', 'duplicate_reason', 'full_text'
    ]
    
    # Full messages (all raw messages)
    write_csv(EXPORTS_DIR / 'UVB76_full_messages.csv', audited_all, msg_fields)
    write_csv(CLEANED_DIR / 'UVB76_full_messages.csv', audited_all, msg_fields)
    
    # Full messages deduplicated (primary records)
    write_csv(EXPORTS_DIR / 'UVB76_full_messages_deduplicated.csv', primary_records, msg_fields)
    write_csv(CLEANED_DIR / 'UVB76_full_messages_deduplicated.csv', primary_records, msg_fields)
    
    # Duplicates audit
    audit_fields = ['source_file', 'source_line', 'date', 'time', 'audit_type', 'action_taken', 'rationale', 'raw_snippet']
    write_csv(EXPORTS_DIR / 'UVB76_duplicates_audit.csv', auditor.audit_log, audit_fields)
    write_csv(CLEANED_DIR / 'UVB76_duplicates_audit.csv', auditor.audit_log, audit_fields)
    
    # Repeated numbers
    rep_fields = ['digits', 'distinct_words', 'occurrences', 'words', 'dates', 'sources']
    write_csv(EXPORTS_DIR / 'UVB76_repeated_numbers.csv', repeated_all, rep_fields)
    write_csv(CLEANED_DIR / 'UVB76_repeated_numbers.csv', repeated_all, rep_fields)
    
    write_csv(EXPORTS_DIR / 'UVB76_repeated_numbers_deduplicated.csv', repeated_deduped, rep_fields)
    write_csv(CLEANED_DIR / 'UVB76_repeated_numbers_deduplicated.csv', repeated_deduped, rep_fields)
    
    # Crossword number links
    cw_fields = ['digits', 'distinct_words', 'occurrences', 'words', 'dates']
    write_csv(EXPORTS_DIR / 'UVB76_crossword_number_links.csv', crossword_links, cw_fields)
    write_csv(CLEANED_DIR / 'UVB76_crossword_number_links.csv', crossword_links, cw_fields)
    
    # Copy to Downloads as well so user's expectation is satisfied
    for fname in [
        'UVB76_full_messages.csv',
        'UVB76_full_messages_deduplicated.csv',
        'UVB76_duplicates_audit.csv',
        'UVB76_repeated_numbers.csv',
        'UVB76_repeated_numbers_deduplicated.csv',
        'UVB76_crossword_number_links.csv'
    ]:
        write_csv(DOWNLOADS_DIR / fname, 
                  audited_all if 'full_messages.csv' in fname else 
                  primary_records if 'deduplicated.csv' in fname and 'full' in fname else
                  auditor.audit_log if 'audit' in fname else
                  repeated_all if 'repeated_numbers.csv' in fname else
                  repeated_deduped if 'repeated_numbers_deduplicated.csv' in fname else
                  crossword_links,
                  msg_fields if 'full_messages' in fname else
                  audit_fields if 'audit' in fname else
                  cw_fields if 'crossword' in fname else rep_fields)
        
    print("CSV files exported to D:/Projects/ZIZIPHUS_JUJUBA/exports, data/cleaned, and C:/Users/User/Downloads.")
    
    # 8. Check specific target words: ЗИЗИФУС, ПАСКОИТ, ГАШЕНИЕ, НИЗКИЙ
    print("\n--- SIGNAL INTELLIGENCE TARGET VERIFICATION ---")
    targets = ['ЗИЗИФУС', 'ПАСКОИТ', 'ГАШЕНИЕ', 'НИЗКИЙ']
    for t in targets:
        matches = [p for p in all_pairs if t in p['word']]
        print(f"Target [{t}]: {len(matches)} occurrences")
        for m in matches:
            print(f"  {m['date']} {m['time']} -> {m['word']} {m['digit_group_1']} {m['digit_group_2']} ({m['source_file']}:{m['source_line']})")
            
    # Check 77248209 match
    pair_7724 = [p for p in all_pairs if p['digits'] == '77248209']
    print(f"\nVerification of combination 7724 8209 ({len(pair_7724)} primary logs):")
    for p in pair_7724:
        print(f"  Date: {p['date']} | Time: {p['time']} | Word: {p['word']} | Digits: {p['digits']} | Source: {p['source_file']}:{p['source_line']}")
        
    return stats

if __name__ == "__main__":
    run_pipeline()
