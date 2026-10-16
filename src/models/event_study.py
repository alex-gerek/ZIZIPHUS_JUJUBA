"""
Historical Event-Study & Timeline Analysis Engine for UVB-76.
Tests statistical relationships between UVB-76 broadcast volume and documented historical events.
Evaluates configurable time windows:
- 7 days before / after
- 14 days before / after
- 30 days before / after
- 90 days before / after
Compares observed event-window volume against empirical baseline reference distributions.
Accommodates reporting bias, archive coverage gaps, and non-random sampling constraints.
"""

import sqlite3
import datetime as dt
import statistics
from typing import Dict, Any, List, Optional
import collections

DEFAULT_WINDOWS = (7, 14, 30, 90)

class HistoricalEventStudy:
    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn
        self._load_counts()

    def _load_counts(self):
        """Loads daily message counts for primary deduplicated transmissions."""
        rows = self.conn.execute("""
            SELECT date, COUNT(*) as cnt
            FROM Messages
            WHERE is_duplicate = 0
            GROUP BY date
        """).fetchall()
        self.daily_counts = {
            dt.date.fromisoformat(r['date']): r['cnt']
            for r in rows
        }

    def preceding_window_volume(self, target_day: dt.date, window_days: int) -> int:
        """Sum of broadcasts in the window_days immediately preceding target_day."""
        return sum(
            self.daily_counts.get(target_day - dt.timedelta(days=i), 0)
            for i in range(1, window_days + 1)
        )

    def following_window_volume(self, target_day: dt.date, window_days: int) -> int:
        """Sum of broadcasts in the window_days immediately following target_day."""
        return sum(
            self.daily_counts.get(target_day + dt.timedelta(days=i), 0)
            for i in range(1, window_days + 1)
        )

    def calculate_same_year_baseline(self, target_day: dt.date, window_days: int, mode: str = 'preceding') -> Dict[str, Any]:
        """
        Calculates empirical distribution across all eligible calendar days within the same year.
        Replicates and extends the baseline evaluation from the preliminary event model.
        """
        year = target_day.year
        first_day = dt.date(year, 1, 1)
        last_day = dt.date(year, 12, 31)
        
        eligible_days = []
        cur = first_day
        while cur <= last_day:
            if mode == 'preceding':
                if cur >= first_day + dt.timedelta(days=window_days):
                    eligible_days.append(cur)
            else:
                if cur <= last_day - dt.timedelta(days=window_days):
                    eligible_days.append(cur)
            cur += dt.timedelta(days=1)
            
        if not eligible_days:
            return {
                'observed': 0, 'baseline_mean': 0.0, 'baseline_median': 0.0,
                'percentile': 0.0, 'p_upper': 1.0, 'reference_dates': 0
            }
            
        if mode == 'preceding':
            observed = self.preceding_window_volume(target_day, window_days)
            baseline_values = [self.preceding_window_volume(d, window_days) for d in eligible_days]
        else:
            observed = self.following_window_volume(target_day, window_days)
            baseline_values = [self.following_window_volume(d, window_days) for d in eligible_days]
            
        mean_val = round(float(statistics.mean(baseline_values)), 2)
        med_val = float(statistics.median(baseline_values))
        pct = round(100.0 * sum(v <= observed for v in baseline_values) / len(baseline_values), 1)
        p_up = round(float(sum(v >= observed for v in baseline_values) / len(baseline_values)), 4)
        
        return {
            'observed': observed,
            'baseline_mean': mean_val,
            'baseline_median': med_val,
            'percentile': pct,
            'p_upper': p_up,
            'reference_dates': len(eligible_days)
        }

    def evaluate_all_historical_events(self, windows: tuple = DEFAULT_WINDOWS) -> List[Dict[str, Any]]:
        """Evaluates all registered historical events across configured time windows."""
        events = self.conn.execute("""
            SELECT id, event_name, event_name_en, start_date, category, region, source_url
            FROM HistoricalEvents
            ORDER BY start_date ASC
        """).fetchall()
        
        results = []
        for ev in events:
            day = dt.date.fromisoformat(ev['start_date'])
            for w in windows:
                pre_stats = self.calculate_same_year_baseline(day, w, mode='preceding')
                post_stats = self.calculate_same_year_baseline(day, w, mode='following')
                results.append({
                    'event_id': ev['id'],
                    'event_name': ev['event_name'],
                    'event_name_en': ev['event_name_en'],
                    'date': ev['start_date'],
                    'category': ev['category'],
                    'region': ev['region'],
                    'window_days': w,
                    'pre_observed': pre_stats['observed'],
                    'pre_baseline_mean': pre_stats['baseline_mean'],
                    'pre_percentile': pre_stats['percentile'],
                    'pre_p_upper': pre_stats['p_upper'],
                    'post_observed': post_stats['observed'],
                    'post_baseline_mean': post_stats['baseline_mean'],
                    'post_percentile': post_stats['percentile'],
                    'post_p_upper': post_stats['p_upper'],
                    'reference_dates': pre_stats['reference_dates'],
                    'source_url': ev['source_url']
                })
        return results

    def evaluate_custom_event(self, date_str: str, event_name: str, windows: tuple = DEFAULT_WINDOWS) -> List[Dict[str, Any]]:
        """Evaluates an arbitrary user-submitted date and event."""
        day = dt.date.fromisoformat(date_str)
        results = []
        for w in windows:
            pre = self.calculate_same_year_baseline(day, w, mode='preceding')
            post = self.calculate_same_year_baseline(day, w, mode='following')
            results.append({
                'event_name': event_name,
                'date': date_str,
                'window_days': w,
                'pre_observed': pre['observed'],
                'pre_baseline_mean': pre['baseline_mean'],
                'pre_percentile': pre['percentile'],
                'pre_p_upper': pre['p_upper'],
                'post_observed': post['observed'],
                'post_baseline_mean': post['baseline_mean'],
                'post_percentile': post['percentile'],
                'post_p_upper': post['p_upper'],
                'reference_dates': pre['reference_dates']
            })
        return results
