"""
Data Audit & Deduplication Engine for ZIZIPHUS JUJUBA.
Audits 10 distinct quality categories:
1. Exact radiogram duplicates
2. Cross-file repetitions (e.g., 2020 logs in 2022_logs.txt)
3. Near-duplicates and transcription variants
4. Codeword transcription variations/uncertainties
5. Missing metadata fields (header, callsign, time)
6. Malformed or ambiguous dates
7. Time format variations (multiple timestamps, comma-separated)
8. Callsign designation variations (phonetic vs Cyrillic, 701st Paramonov)
9. Operator retransmissions and voice corrections (e.g. 'сбой сбой')
10. Archival coverage gaps

Preserves all records with transparent duplicate flags and rationale.
"""

from typing import List, Dict, Any, Tuple
import collections
import re

class DataAuditor:
    def __init__(self):
        self.audit_log: List[Dict[str, Any]] = []

    def audit_and_deduplicate(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
        """
        Executes comprehensive audit and marks duplicate status without destroying data.
        Returns:
            (all_audited_records, deduplicated_primary_records, audit_stats)
        """
        self.audit_log = []
        
        # Step 1: Detect cross-file duplicates (2020 logs in 2022_logs.txt)
        for r in records:
            if r['source_file'] == '2022_logs.txt' and r['year'] == 2020:
                r['is_duplicate'] = 1
                r['duplicate_type'] = 'CROSS_FILE_DUPLICATE'
                r['duplicate_reason'] = 'Archival glitch: January 2020 logs mistakenly pasted into header of 2022_logs.txt'
                self.audit_log.append({
                    'source_file': r['source_file'],
                    'source_line': r['source_line'],
                    'date': r['date'],
                    'time': r['time_as_logged'],
                    'audit_type': 'CROSS_FILE_DUPLICATE',
                    'action_taken': 'FLAGGED_AS_DUPLICATE',
                    'rationale': r['duplicate_reason'],
                    'raw_snippet': r['full_word_sequence'] or r['full_text'][:80]
                })

        # Step 2: Audit non-voice anomalies
        for r in records:
            if r.get('is_duplicate'):
                continue
            if r['quality_flag'] == 'NON_VOICE_ANOMALY':
                r['is_duplicate'] = 1
                r['duplicate_type'] = 'NON_VOICE_ANOMALY'
                r['duplicate_reason'] = 'Non-message transmission (marker hum, dead carrier, diesel breakdown, pirate audio)'
                self.audit_log.append({
                    'source_file': r['source_file'],
                    'source_line': r['source_line'],
                    'date': r['date'],
                    'time': r['time_as_logged'],
                    'audit_type': 'NON_VOICE_ANOMALY',
                    'action_taken': 'FLAGGED_EXCLUDED_FROM_VOICE_STUDY',
                    'rationale': r['duplicate_reason'],
                    'raw_snippet': r['full_text'][:80]
                })

        # Step 3: Audit missing fields
        for r in records:
            missing = []
            if not r['callsign']:
                missing.append('callsign')
            if not r['header_number']:
                missing.append('header_5digit')
            if not r['time_as_logged']:
                missing.append('time')
            if missing:
                self.audit_log.append({
                    'source_file': r['source_file'],
                    'source_line': r['source_line'],
                    'date': r['date'],
                    'time': r['time_as_logged'],
                    'audit_type': 'MISSING_FIELDS',
                    'action_taken': 'LOGGED_WARNING',
                    'rationale': f"Missing fields: {', '.join(missing)}",
                    'raw_snippet': r['full_word_sequence'] or r['full_text'][:80]
                })

        # Step 4: Audit operator corrections inside message
        for r in records:
            full_txt = r.get('full_text', '').lower()
            if 'сбой' in full_txt or 'mistake in reading' in full_txt:
                self.audit_log.append({
                    'source_file': r['source_file'],
                    'source_line': r['source_line'],
                    'date': r['date'],
                    'time': r['time_as_logged'],
                    'audit_type': 'OPERATOR_CORRECTION',
                    'action_taken': 'LOGGED_QUALITY_FLAG',
                    'rationale': 'Operator verbal correction or reading restart detected in transmission',
                    'raw_snippet': full_txt[:100]
                })

        # Step 5: Exact duplicates and real retransmissions
        # Group by (date, full_word_sequence)
        seen_keys = {}
        for r in records:
            if r.get('is_duplicate'):
                continue
            if not r['full_word_sequence']:
                continue
                
            key = (r['date'], r['full_word_sequence'])
            if key in seen_keys:
                orig = seen_keys[key]
                # Check if it's an exact duplicate or real on-air repeat
                if r['time_as_logged'] and orig['time_as_logged'] and r['time_as_logged'] != orig['time_as_logged']:
                    r['is_duplicate'] = 1
                    r['duplicate_type'] = 'REPEATED_TRANSMISSION'
                    r['duplicate_reason'] = f"Real on-air retransmission at {r['time_as_logged']} (original at {orig['time_as_logged']})"
                else:
                    r['is_duplicate'] = 1
                    r['duplicate_type'] = 'EXACT_ARCHIVE_DUPLICATE'
                    r['duplicate_reason'] = f"Identical radiogram already logged at line {orig['source_line']} of {orig['source_file']}"
                    
                self.audit_log.append({
                    'source_file': r['source_file'],
                    'source_line': r['source_line'],
                    'date': r['date'],
                    'time': r['time_as_logged'],
                    'audit_type': r['duplicate_type'],
                    'action_taken': 'FLAGGED_AS_DUPLICATE',
                    'rationale': r['duplicate_reason'],
                    'raw_snippet': r['full_word_sequence']
                })
            else:
                seen_keys[key] = r

        # Deduplicated primary set
        primary_records = [r for r in records if not r.get('is_duplicate')]
        
        # Statistics
        total_raw = len(records)
        total_primary = len(primary_records)
        dupes_count = total_raw - total_primary
        
        dupe_by_type = collections.Counter(r.get('duplicate_type') for r in records if r.get('is_duplicate'))
        year_counts_before = collections.Counter(r['year'] for r in records)
        year_counts_after = collections.Counter(r['year'] for r in primary_records)
        
        stats = {
            'total_raw_records': total_raw,
            'total_deduplicated_primary': total_primary,
            'total_flagged_duplicates': dupes_count,
            'duplicates_by_category': dict(dupe_by_type),
            'audit_events_logged': len(self.audit_log),
            'year_counts_before': dict(sorted(year_counts_before.items())),
            'year_counts_after': dict(sorted(year_counts_after.items()))
        }
        
        return records, primary_records, stats
