"""
Repetition Analysis Module for UVB-76 Signal Intelligence.
Investigates:
- Cross-word shared number groups
- Recurrence intervals (days between successive appearances of identical numbers)
- Sequential triplet patterns (e.g. Sep-Oct 2014 3-broadcast echo)
- Statistical probability of numerical collisions under random null hypothesis
"""

import sqlite3
import datetime as dt
from typing import Dict, Any, List
import pandas as pd
import numpy as np

class RepetitionAnalyzer:
    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn

    def get_repeated_numbers(self, min_occurrences: int = 2) -> Dict[str, Any]:
        """Extracts all 8-digit combinations that repeat across primary radiograms."""
        query = f"""
            SELECT cb.digit_combination,
                   COUNT(*) as occurrences,
                   COUNT(DISTINCT cb.code_word) as distinct_words,
                   GROUP_CONCAT(DISTINCT cb.code_word) as words,
                   GROUP_CONCAT(m.date, ' | ') as dates,
                   MIN(m.date) as first_date,
                   MAX(m.date) as last_date
            FROM CodeBlocks cb
            JOIN Messages m ON cb.message_id = m.id
            WHERE m.is_duplicate = 0 AND cb.digit_combination != ''
            GROUP BY cb.digit_combination
            HAVING occurrences >= {min_occurrences}
            ORDER BY distinct_words DESC, occurrences DESC, cb.digit_combination ASC
        """
        df = pd.read_sql_query(query, self.conn)
        
        # Calculate recurrence intervals in days
        records = df.to_dict(orient='records')
        intervals = []
        for r in records:
            dates = sorted(set(r['dates'].split(' | ')))
            d_objs = [dt.date.fromisoformat(d) for d in dates]
            diffs = [(d_objs[i] - d_objs[i-1]).days for i in range(1, len(d_objs))]
            r['min_interval_days'] = min(diffs) if diffs else 0
            r['max_interval_days'] = max(diffs) if diffs else 0
            r['mean_interval_days'] = round(float(np.mean(diffs)), 1) if diffs else 0
            intervals.extend(diffs)
            
        mean_interval = round(float(np.mean(intervals)), 1) if intervals else 0
        median_interval = float(np.median(intervals)) if intervals else 0
        
        # Partition into:
        # 1. Cross-word collisions (distinct words > 1)
        # 2. Same-word exact re-uses (distinct words == 1)
        cross_word = [r for r in records if r['distinct_words'] > 1]
        same_word = [r for r in records if r['distinct_words'] == 1]
        
        return {
            'total_repeating_combinations': len(records),
            'cross_word_count': len(cross_word),
            'same_word_reuse_count': len(same_word),
            'overall_mean_interval_days': mean_interval,
            'overall_median_interval_days': median_interval,
            'cross_word_links': cross_word,
            'same_word_repeats': same_word
        }

    def inspect_specific_targets(self) -> Dict[str, Any]:
        """Deep investigation into the ZIZIFUS, PASKOIT, GASHENIE, and NIZKIJ cluster."""
        targets = ['ЗИЗИФУС', 'ПАСКОИТ', 'ГАШЕНИЕ', 'НИЗКИЙ']
        q = f"""
            SELECT m.id as message_id, m.date, m.time_as_logged, m.callsign, m.header_number,
                   m.full_word_sequence, m.source_file, m.source_line,
                   cb.block_index, cb.code_word, cb.digit_combination, cb.digit_group_1, cb.digit_group_2
            FROM CodeBlocks cb
            JOIN Messages m ON cb.message_id = m.id
            WHERE cb.code_word IN ({','.join('?' for _ in targets)})
            ORDER BY m.date ASC, m.time_as_logged ASC
        """
        df = pd.read_sql_query(q, self.conn, params=targets)
        
        # Analyze 77248209 link
        q_7724 = """
            SELECT m.date, m.time_as_logged, cb.code_word, cb.digit_combination,
                   m.source_file, m.source_line, m.full_word_sequence
            FROM CodeBlocks cb
            JOIN Messages m ON cb.message_id = m.id
            WHERE cb.digit_combination = '77248209'
            ORDER BY m.date ASC
        """
        df_7724 = pd.read_sql_query(q_7724, self.conn)
        
        # Verify the 2014 September - October sequential triplet echo
        # Sep 4 2014 vs Oct 1-2 2014
        triplet_q = """
            SELECT m.date, m.time_as_logged, cb.code_word, cb.digit_combination,
                   m.header_number, m.source_file, m.source_line
            FROM CodeBlocks cb
            JOIN Messages m ON cb.message_id = m.id
            WHERE m.date IN ('2014-09-04', '2014-10-01', '2014-10-02')
              AND cb.digit_combination IN ('84232962', '77248209', '31809240')
            ORDER BY cb.digit_combination, m.date ASC
        """
        df_triplet = pd.read_sql_query(triplet_q, self.conn)
        
        return {
            'target_records': df.to_dict(orient='records'),
            'link_77248209': df_7724.to_dict(orient='records'),
            'triplet_echo': df_triplet.to_dict(orient='records'),
            'summary': {
                'ziziphus_paskoit_match_confirmed': len(df_7724) == 2,
                'paskoit_date': '2014-09-04',
                'ziziphus_date': '2014-10-02',
                'interval_days': 28,
                'shared_digit_combination': '77248209',
                'echo_triplet_size': len(df_triplet)
            }
        }
