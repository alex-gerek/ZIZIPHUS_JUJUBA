"""
Frequency Analysis Module for UVB-76 Signal Intelligence.
Calculates frequencies, rank distributions, and proportions for:
- Code words (Zipf-like distribution, hapax legomena)
- 4-digit and 8-digit numerical groups
- Callsigns
- Radiogram block structures (single vs multi-block transmissions)
"""

import collections
import sqlite3
from typing import Dict, Any, List
import pandas as pd
import numpy as np

class FrequencyAnalyzer:
    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn

    def get_word_frequencies(self, top_n: int = 50, include_duplicates: bool = False) -> Dict[str, Any]:
        """Calculates codeword frequencies and statistical properties."""
        dup_filter = "" if include_duplicates else "AND m.is_duplicate = 0"
        query = f"""
            SELECT cb.code_word, COUNT(*) as frequency,
                   COUNT(DISTINCT m.date) as distinct_dates,
                   MIN(m.date) as first_seen,
                   MAX(m.date) as last_seen
            FROM CodeBlocks cb
            JOIN Messages m ON cb.message_id = m.id
            WHERE cb.code_word != '' {dup_filter}
            GROUP BY cb.code_word
            ORDER BY frequency DESC, cb.code_word ASC
        """
        df = pd.read_sql_query(query, self.conn)
        
        total_tokens = int(df['frequency'].sum()) if not df.empty else 0
        unique_words = len(df)
        hapax = int((df['frequency'] == 1).sum()) if not df.empty else 0
        hapax_ratio = round(hapax / unique_words, 4) if unique_words > 0 else 0
        
        top_words = df.head(top_n).to_dict(orient='records')
        
        return {
            'total_tokens': total_tokens,
            'unique_words': unique_words,
            'hapax_legomena_count': hapax,
            'hapax_ratio': hapax_ratio,
            'top_words': top_words
        }

    def get_digit_frequencies(self, top_n: int = 50, include_duplicates: bool = False) -> Dict[str, Any]:
        """Calculates 8-digit and 4-digit number group frequencies."""
        dup_filter = "" if include_duplicates else "AND m.is_duplicate = 0"
        
        # 8-digit combinations
        q8 = f"""
            SELECT cb.digit_combination, COUNT(*) as frequency,
                   COUNT(DISTINCT cb.code_word) as distinct_words,
                   GROUP_CONCAT(DISTINCT cb.code_word) as associated_words,
                   MIN(m.date) as first_seen, MAX(m.date) as last_seen
            FROM CodeBlocks cb
            JOIN Messages m ON cb.message_id = m.id
            WHERE cb.digit_combination != '' {dup_filter}
            GROUP BY cb.digit_combination
            ORDER BY frequency DESC, cb.digit_combination ASC
        """
        df8 = pd.read_sql_query(q8, self.conn)
        
        # 4-digit groups (both position 1 and 2)
        q4 = f"""
            SELECT digit_group, COUNT(*) as frequency,
                   COUNT(DISTINCT position) as in_positions
            FROM (
                SELECT digit_group_1 as digit_group, 1 as position FROM CodeBlocks cb
                JOIN Messages m ON cb.message_id = m.id WHERE cb.digit_group_1 != '' {dup_filter}
                UNION ALL
                SELECT digit_group_2 as digit_group, 2 as position FROM CodeBlocks cb
                JOIN Messages m ON cb.message_id = m.id WHERE cb.digit_group_2 != '' {dup_filter}
            )
            GROUP BY digit_group
            ORDER BY frequency DESC, digit_group ASC
        """
        df4 = pd.read_sql_query(q4, self.conn)
        
        return {
            'total_8digit_tokens': int(df8['frequency'].sum()) if not df8.empty else 0,
            'unique_8digit_combinations': len(df8),
            'top_8digit_combinations': df8.head(top_n).to_dict(orient='records'),
            'total_4digit_tokens': int(df4['frequency'].sum()) if not df4.empty else 0,
            'unique_4digit_groups': len(df4),
            'top_4digit_groups': df4.head(top_n).to_dict(orient='records')
        }

    def get_callsign_frequencies(self) -> Dict[str, Any]:
        """Calculates callsign distribution across years."""
        query = """
            SELECT 
                CASE 
                    WHEN callsign LIKE '%МДЖБ%' OR callsign LIKE '%MDZhB%' THEN 'МДЖБ / MDZhB'
                    WHEN callsign LIKE '%ЖУОЗ%' OR callsign LIKE '%ZhUOZ%' THEN 'ЖУОЗ / ZhUOZ'
                    WHEN callsign LIKE '%АНВФ%' OR callsign LIKE '%ANVF%' THEN 'АНВФ / ANVF'
                    WHEN callsign LIKE '%УЗБ%' OR callsign LIKE '%UZB%' THEN 'УЗБ-76 / UZB-76'
                    WHEN callsign LIKE '%ВЛХН%' OR callsign LIKE '%VLHN%' THEN 'ВЛХН / VLHN'
                    WHEN callsign LIKE '%701%' OR callsign LIKE '%Парамонов%' THEN '701-й Рожка Парамонов'
                    WHEN callsign LIKE '%ЛНР4%' OR callsign LIKE '%LNR4%' THEN 'ЛНР4 / LNR4'
                    WHEN callsign LIKE '%????%' THEN 'Неопознан (?????)'
                    WHEN callsign = '' OR callsign IS NULL THEN 'Без позывного'
                    ELSE 'Прочие позывные'
                END as normalized_callsign,
                COUNT(*) as count,
                MIN(year) as min_year,
                MAX(year) as max_year,
                ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM Messages WHERE is_duplicate = 0), 2) as percentage
            FROM Messages
            WHERE is_duplicate = 0
            GROUP BY normalized_callsign
            ORDER BY count DESC
        """
        df = pd.read_sql_query(query, self.conn)
        return {
            'callsigns': df.to_dict(orient='records')
        }

    def get_structure_frequencies(self) -> Dict[str, Any]:
        """Calculates distribution of radiogram lengths (number of code blocks per message)."""
        query = """
            SELECT block_count, COUNT(*) as count,
                   ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM Messages WHERE is_duplicate = 0), 2) as percentage
            FROM Messages
            WHERE is_duplicate = 0
            GROUP BY block_count
            ORDER BY block_count ASC
        """
        df = pd.read_sql_query(query, self.conn)
        return {
            'block_distribution': df.to_dict(orient='records')
        }
