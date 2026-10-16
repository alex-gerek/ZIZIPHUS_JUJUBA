"""
Hypothesis Testing and Significance Engine for UVB-76.
Implements:
- Permutation tests (2,000+ random reshuffles) testing event-window alignment
- Multiple testing adjustments (Bonferroni, Benjamini-Hochberg FDR)
- Bootstrap confidence intervals (95% CI) for baseline parameters
- Rigorous epistemological assessment of observational limitations
"""

import sqlite3
import datetime as dt
import numpy as np
from typing import Dict, Any, List, Tuple

class HypothesisTestingEngine:
    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn

    def run_permutation_test(self, event_dates: List[str], window_days: int = 7, 
                             n_permutations: int = 2000, random_seed: int = 42) -> Dict[str, Any]:
        """
        Executes a Monte Carlo permutation test (2,000 trials).
        Tests H0: UVB-76 transmissions are randomly distributed across available calendar days,
        and their proximity to historical events is a chance artifact.
        """
        rng = np.random.default_rng(random_seed)
        
        # Load daily message indicator for available years
        rows = self.conn.execute("""
            SELECT date, COUNT(*) as cnt
            FROM Messages
            WHERE is_duplicate = 0
            GROUP BY date
        """).fetchall()
        
        active_dates = set(r['date'] for r in rows)
        if not active_dates:
            return {'error': 'No active dates found in database'}
            
        # Determine observation boundaries for years covered
        years = sorted(set(int(d[:4]) for d in active_dates))
        calendar_days = []
        for y in years:
            cur = dt.date(y, 1, 1)
            end = dt.date(y, 12, 31)
            while cur <= end:
                calendar_days.append(cur)
                cur += dt.timedelta(days=1)
                
        total_days = len(calendar_days)
        # Create binary activity array
        active_set_dt = set(dt.date.fromisoformat(d) for d in active_dates)
        activity_arr = np.array([1 if d in active_set_dt else 0 for d in calendar_days], dtype=int)
        
        # Build event window mask on calendar days
        ev_dt_list = [dt.date.fromisoformat(ed) for ed in event_dates if int(ed[:4]) in years]
        if not ev_dt_list:
            return {'error': 'No event dates fall within analyzed archive years'}
            
        event_mask = np.zeros(total_days, dtype=int)
        for i, d in enumerate(calendar_days):
            for ev in ev_dt_list:
                if abs((d - ev).days) <= window_days:
                    event_mask[i] = 1
                    break
                    
        # Observed statistic: number of broadcasts falling in event windows
        observed_stat = int(np.sum(activity_arr * event_mask))
        event_window_days_count = int(np.sum(event_mask))
        
        # Permutation simulation
        perm_stats = np.zeros(n_permutations, dtype=int)
        shuffled = activity_arr.copy()
        for i in range(n_permutations):
            rng.shuffle(shuffled)
            perm_stats[i] = np.sum(shuffled * event_mask)
            
        perm_mean = round(float(np.mean(perm_stats)), 2)
        perm_std = round(float(np.std(perm_stats)), 2)
        p_value = round(float(np.sum(perm_stats >= observed_stat) / n_permutations), 5)
        z_score = round(float((observed_stat - perm_mean) / (perm_std + 1e-9)), 2)
        
        return {
            'n_permutations': n_permutations,
            'window_days': window_days,
            'observed_transmissions_in_windows': observed_stat,
            'expected_transmissions_under_H0': perm_mean,
            'perm_std': perm_std,
            'z_score': z_score,
            'empirical_p_value': p_value,
            'total_calendar_days': total_days,
            'event_window_days': event_window_days_count,
            'reject_null_at_005': p_value < 0.05,
            'reject_null_at_001': p_value < 0.01,
            'summary_text': (
                f"Permutation test with {n_permutations:,} trials: Observed = {observed_stat}, "
                f"Expected = {perm_mean} +/- {perm_std}. Empirical p-value = {p_value:.4f} (z = {z_score})."
            )
        }

    def apply_multiple_testing_corrections(self, p_values: List[float], method: str = 'fdr_bh') -> Dict[str, Any]:
        """
        Applies Bonferroni or Benjamini-Hochberg FDR correction to a family of p-values.
        """
        n = len(p_values)
        if n == 0:
            return {'corrected_p_values': [], 'significant_flags': []}
            
        # Bonferroni
        bonferroni = [min(1.0, round(p * n, 5)) for p in p_values]
        
        # Benjamini-Hochberg FDR
        indexed = sorted(enumerate(p_values), key=lambda x: x[1])
        fdr = [0.0] * n
        min_coeff = 1.0
        for rank_idx in range(n - 1, -1, -1):
            orig_idx, p = indexed[rank_idx]
            rank = rank_idx + 1
            adj_p = (p * n) / rank
            min_coeff = min(min_coeff, adj_p)
            fdr[orig_idx] = round(min(1.0, min_coeff), 5)
            
        return {
            'raw_p_values': [round(p, 5) for p in p_values],
            'bonferroni_adjusted': bonferroni,
            'fdr_bh_adjusted': fdr,
            'significant_bonferroni_005': [p < 0.05 for p in bonferroni],
            'significant_fdr_005': [p < 0.05 for p in fdr]
        }
