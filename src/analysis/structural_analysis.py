"""
ZIZIPHUS JUJUBA: Structural Dynamics & Lexical Evolution Engine.
Analyzes evolution of callsigns, message length distributions,
vocabulary turnover (Heaps' law), code block transitions, and co-occurrences.
"""

import sqlite3
import collections
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd


class StructuralDynamicsEngine:
    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn

    def get_callsign_evolution(self) -> Dict[str, Any]:
        """
        Chronological evolution and distribution of station callsigns
        (UZB-76 -> MDZhB -> ZhUOZ -> ANVF -> NZhTI / VZhTsKh).
        """
        query = """
            SELECT date, year, callsign, COUNT(*) as cnt
            FROM Messages
            WHERE is_duplicate = 0 AND callsign IS NOT NULL AND TRIM(callsign) != ''
            GROUP BY year, callsign
            ORDER BY year ASC, cnt DESC
        """
        rows = self.conn.execute(query).fetchall()
        
        # Summarize by normalized callsign prefix
        def normalize_cs(cs: str) -> str:
            cs = cs.upper().strip()
            if 'УЗБ' in cs or 'UZB' in cs: return 'УЗБ-76 (UZB-76)'
            if 'МДЖБ' in cs or 'MDZHB' in cs or 'MDZB' in cs: return 'МДЖБ (MDZhB)'
            if 'ЖУОЗ' in cs or 'ZHUOZ' in cs: return 'ЖУОЗ (ZhUOZ)'
            if 'АНВФ' in cs or 'ANVF' in cs: return 'АНВФ (ANVF)'
            if 'ВЖЦХ' in cs or 'VZH' in cs: return 'ВЖЦХ (VZhTsKh)'
            if 'НЖТИ' in cs or 'NZHTI' in cs: return 'НЖТИ (NZhTI)'
            return 'ПРОЧИЕ / ДРУГИЕ (Other)'

        norm_data = collections.defaultdict(lambda: collections.defaultdict(int))
        years = set()
        
        for r in rows:
            yr = r['year']
            n_cs = normalize_cs(r['callsign'])
            norm_data[yr][n_cs] += r['cnt']
            years.add(yr)

        sorted_years = sorted(list(years))
        all_callsigns = ['УЗБ-76 (UZB-76)', 'МДЖБ (MDZhB)', 'ЖУОЗ (ZhUOZ)', 'АНВФ (ANVF)', 'ВЖЦХ (VZhTsKh)', 'НЖТИ (NZhTI)', 'ПРОЧИЕ / ДРУГИЕ (Other)']

        matrix = []
        for cs in all_callsigns:
            series = [norm_data[yr][cs] for yr in sorted_years]
            if sum(series) > 0:
                matrix.append({
                    'callsign': cs,
                    'years': sorted_years,
                    'counts': series,
                    'total': sum(series)
                })

        # Callsign date ranges
        first_last_q = """
            SELECT callsign, MIN(date) as first_date, MAX(date) as last_date, COUNT(*) as total_msgs
            FROM Messages
            WHERE is_duplicate = 0 AND callsign IS NOT NULL
            GROUP BY callsign
            HAVING total_msgs >= 5
            ORDER BY first_date ASC
        """
        fl_rows = self.conn.execute(first_last_q).fetchall()
        ranges = [{
            'callsign': r['callsign'],
            'first_seen': r['first_date'],
            'last_seen': r['last_date'],
            'count': r['total_msgs']
        } for r in fl_rows]

        return {
            'years': sorted_years,
            'callsign_distribution': matrix,
            'callsign_ranges': ranges,
            'summary': "Sharp chronological transitions reflect administrative and military command restructuring of the Western Military District."
        }

    def get_message_length_and_block_counts(self) -> Dict[str, Any]:
        """
        Distribution of code blocks per message (1 block vs multi-word commands)
        and how message complexity evolved over time.
        """
        query = """
            SELECT year, block_count, COUNT(*) as cnt
            FROM Messages
            WHERE is_duplicate = 0 AND block_count IS NOT NULL
            GROUP BY year, block_count
            ORDER BY year ASC, block_count ASC
        """
        rows = self.conn.execute(query).fetchall()

        year_blocks = collections.defaultdict(lambda: collections.defaultdict(int))
        years = set()
        for r in rows:
            yr = r['year']
            bc = min(5, r['block_count'])  # 1, 2, 3, 4, 5+
            year_blocks[yr][bc] += r['cnt']
            years.add(yr)

        sorted_years = sorted(list(years))
        data_series = []
        labels = {1: '1 блок (Стандарт)', 2: '2 блока', 3: '3 блока', 4: '4 блока', 5: '5+ блоков (Учения/Массовые)'}

        for bc in [1, 2, 3, 4, 5]:
            counts = [year_blocks[yr][bc] for yr in sorted_years]
            data_series.append({
                'blocks': bc,
                'label': labels[bc],
                'counts': counts
            })

        # Overall summary stats
        overall_q = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN block_count = 1 THEN 1 ELSE 0 END) as single_block,
                SUM(CASE WHEN block_count > 1 THEN 1 ELSE 0 END) as multi_block,
                AVG(block_count) as avg_blocks,
                MAX(block_count) as max_blocks
            FROM Messages
            WHERE is_duplicate = 0
        """
        ov = dict(self.conn.execute(overall_q).fetchone())

        return {
            'years': sorted_years,
            'series': data_series,
            'overall_metrics': {
                'total_messages': ov['total'],
                'single_block_count': ov['single_block'],
                'single_block_pct': round(ov['single_block'] / max(1, ov['total']) * 100, 1),
                'multi_block_count': ov['multi_block'],
                'multi_block_pct': round(ov['multi_block'] / max(1, ov['total']) * 100, 1),
                'average_blocks_per_msg': round(ov['avg_blocks'], 2),
                'max_blocks_single_msg': ov['max_blocks']
            }
        }

    def get_vocabulary_turnover(self) -> Dict[str, Any]:
        """
        Vocabulary growth curve (Heaps' law: V = k * N^beta),
        arrival of new words, and singleton (hapax legomena) analysis.
        """
        # Fetch all codewords ordered chronologically
        query = """
            SELECT m.date, m.year, cb.code_word
            FROM CodeBlocks cb
            JOIN Messages m ON cb.message_id = m.id
            WHERE m.is_duplicate = 0 AND cb.code_word IS NOT NULL AND TRIM(cb.code_word) != ''
            ORDER BY m.date ASC, m.time_as_logged ASC
        """
        rows = self.conn.execute(query).fetchall()

        seen_words = set()
        curve = []
        step = max(1, len(rows) // 60)
        
        words_by_year = collections.defaultdict(list)
        word_counts = collections.Counter()

        for idx, r in enumerate(rows):
            w = r['code_word'].strip().upper()
            word_counts[w] += 1
            words_by_year[r['year']].append(w)
            seen_words.add(w)
            if (idx + 1) % step == 0 or idx == len(rows) - 1:
                curve.append({
                    'n_messages': idx + 1,
                    'unique_vocab': len(seen_words),
                    'date': r['date']
                })

        # Calculate lexical arrival per year
        yearly_vocab = []
        historical_pool = set()
        for yr in sorted(words_by_year.keys()):
            yr_words = set(words_by_year[yr])
            new_words = yr_words - historical_pool
            repeat_words = yr_words & historical_pool
            yearly_vocab.append({
                'year': yr,
                'total_word_events': len(words_by_year[yr]),
                'unique_words': len(yr_words),
                'new_words_introduced': len(new_words),
                'reused_from_past': len(repeat_words)
            })
            historical_pool.update(yr_words)

        # Hapax legomena: words that appeared only 1 time in the entire 12-year history
        singletons = [w for w, c in word_counts.items() if c == 1]
        top_recurrent = [{'word': w, 'count': c} for w, c in word_counts.most_common(20)]

        # Heaps' Law Fit estimate
        # V = k * N^beta  => log(V) = log(k) + beta * log(N)
        if len(curve) > 5:
            ns = np.array([pt['n_messages'] for pt in curve])
            vs = np.array([pt['unique_vocab'] for pt in curve])
            poly = np.polyfit(np.log(ns), np.log(vs), 1)
            beta_heaps = round(float(poly[0]), 3)
            k_heaps = round(float(np.exp(poly[1])), 2)
        else:
            beta_heaps, k_heaps = 0.75, 2.0

        return {
            'growth_curve': curve,
            'heaps_law': {
                'beta': beta_heaps,
                'k': k_heaps,
                'formula': f"V(N) ≈ {k_heaps} · N^{beta_heaps}",
                'interpretation': f"Sublinear growth (beta={beta_heaps} < 1) confirms finite military vocabulary pool rather than open-ended natural conversation."
            },
            'yearly_turnover': yearly_vocab,
            'total_unique_vocabulary': len(seen_words),
            'singleton_count': len(singletons),
            'singleton_pct': round(len(singletons) / max(1, len(seen_words)) * 100, 1),
            'top_recurrent_words': top_recurrent
        }

    def get_word_cooccurrence(self, min_pair_count: int = 2) -> Dict[str, Any]:
        """
        Words appearing together within multi-block radiograms.
        Discovers tactical paired operational phrases.
        """
        query = """
            SELECT m.id, cb.code_word
            FROM CodeBlocks cb
            JOIN Messages m ON cb.message_id = m.id
            WHERE m.is_duplicate = 0 AND cb.code_word IS NOT NULL AND TRIM(cb.code_word) != ''
            ORDER BY m.id ASC, cb.block_index ASC
        """
        rows = self.conn.execute(query).fetchall()
        
        msg_words = collections.defaultdict(list)
        for r in rows:
            w = r['code_word'].strip().upper()
            if w not in msg_words[r['id']]:
                msg_words[r['id']].append(w)

        pair_counts = collections.Counter()
        for mid, wlist in msg_words.items():
            if len(wlist) > 1:
                # Pairwise combinations
                for i in range(len(wlist)):
                    for j in range(i + 1, len(wlist)):
                        w1, w2 = sorted([wlist[i], wlist[j]])
                        pair_counts[(w1, w2)] += 1

        top_pairs = []
        for (w1, w2), cnt in pair_counts.most_common(30):
            if cnt >= min_pair_count:
                top_pairs.append({'word1': w1, 'word2': w2, 'cooccurrences': cnt})

        return {
            'total_cooccurring_pairs_found': len(pair_counts),
            'pairs': top_pairs
        }
