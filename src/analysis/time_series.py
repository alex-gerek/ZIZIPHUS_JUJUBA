"""
Time Series and Temporal Dynamics Module for UVB-76.
Analyzes:
- Spike-day frequency and longitudinal trends
- Normalized monthly activity matrix (% of yearly maximum)
- Diurnal distribution (hourly broadcast patterns)
- Archival coverage gaps and observational limitations
"""

import sqlite3
import collections
import datetime as dt
from typing import Dict, Any, List
import pandas as pd
import numpy as np

class TimeSeriesAnalyzer:
    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn

    def get_daily_activity(self) -> Dict[str, Any]:
        """Calculates daily message counts and spike-days."""
        query = """
            SELECT date, year, month, day, COUNT(*) as message_count,
                   COUNT(DISTINCT callsign) as distinct_callsigns,
                   SUM(block_count) as total_blocks
            FROM Messages
            WHERE is_duplicate = 0
            GROUP BY date
            ORDER BY date ASC
        """
        df = pd.read_sql_query(query, self.conn)
        
        # Spike-days: binary indicator (1 if messages >= 1)
        # Intense spike-days: messages >= 3
        df['is_spike_day'] = 1
        df['is_high_volume_day'] = (df['message_count'] >= 3).astype(int)
        
        total_days_with_broadcasts = len(df)
        busiest_days = df.sort_values(by='message_count', ascending=False).head(10).to_dict(orient='records')
        
        return {
            'total_active_days': total_days_with_broadcasts,
            'busiest_days': busiest_days,
            'daily_series': df.to_dict(orient='records')
        }

    def get_normalized_monthly_matrix(self) -> Dict[str, Any]:
        """
        Builds the 12-month activity matrix scaled to % of yearly maximum spike-days,
        strictly replicating the methodology from the Leerrooy95 longitudinal paper.
        """
        query = """
            SELECT year, month, COUNT(DISTINCT date) as spike_days,
                   COUNT(*) as total_messages
            FROM Messages
            WHERE is_duplicate = 0
            GROUP BY year, month
            ORDER BY year ASC, month ASC
        """
        df = pd.read_sql_query(query, self.conn)
        
        # Build complete grid of years and months 1..12
        years = sorted(df['year'].unique())
        matrix_rows = []
        
        for y in years:
            row = {'year': int(y)}
            y_df = df[df['year'] == y]
            month_counts = {int(r['month']): int(r['spike_days']) for _, r in y_df.iterrows()}
            
            # Find max spike-days in this year
            max_val = max(month_counts.values()) if month_counts else 0
            
            for m in range(1, 13):
                cnt = month_counts.get(m, 0)
                norm_val = round((cnt / max_val * 100.0), 1) if max_val > 0 else 0.0
                row[f'm{m}'] = norm_val
                row[f'cnt_{m}'] = cnt
            row['yearly_max_spike_days'] = max_val
            row['total_spike_days'] = sum(month_counts.values())
            matrix_rows.append(row)
            
        return {
            'years': [int(y) for y in years],
            'matrix': matrix_rows
        }

    def get_diurnal_distribution(self) -> Dict[str, Any]:
        """Analyzes broadcast timing by hour of the day."""
        query = """
            SELECT time_as_logged, source_file
            FROM Messages
            WHERE is_duplicate = 0 AND time_as_logged != ''
        """
        df = pd.read_sql_query(query, self.conn)
        
        hour_counts = collections.Counter()
        for _, r in df.iterrows():
            t_str = r['time_as_logged']
            # Could be comma-separated
            for part in t_str.split(','):
                part = part.strip()
                if ':' in part:
                    try:
                        hr = int(part.split(':')[0])
                        if 0 <= hr < 24:
                            hour_counts[hr] += 1
                    except ValueError:
                        pass
                        
        hourly_data = [
            {'hour': h, 'count': hour_counts.get(h, 0),
             'hour_label': f"{h:02d}:00"}
            for h in range(24)
        ]
        
        return {
            'hourly_distribution': hourly_data,
            'peak_hour': max(hourly_data, key=lambda x: x['count']) if hourly_data else None
        }

    def get_archive_coverage_audit(self) -> Dict[str, Any]:
        """Summarizes known gaps in monitoring coverage across years."""
        known_gaps = {
            2010: "Priyom logs restricted mostly to Sep-Dec; baseline monitoring initiation.",
            2011: "Strong coverage Feb-Nov; missing Jan & Dec.",
            2014: "Logs present Jan, Feb, Mar, Apr, Sep, Oct; gaps in summer.",
            2015: "Logs present Jan-Dec with high coverage.",
            2017: "Missing July, August, October, November, December in source logs.",
            2018: "Missing March, April, May, June, July, August, December.",
            2019: "Missing January, August, November.",
            2020: "Partial coverage (mostly Jan, Feb, Nov, Dec).",
            2022: "Coverage concentrated around January, February, and December."
        }
        
        query = """
            SELECT year, COUNT(DISTINCT month) as active_months,
                   GROUP_CONCAT(DISTINCT month) as recorded_months,
                   COUNT(*) as message_count
            FROM Messages
            WHERE is_duplicate = 0
            GROUP BY year
            ORDER BY year ASC
        """
        df = pd.read_sql_query(query, self.conn)
        coverage_rows = []
        for _, r in df.iterrows():
            y = int(r['year'])
            rec_m = [int(m) for m in r['recorded_months'].split(',')]
            miss_m = sorted(set(range(1, 13)) - set(rec_m))
            coverage_rows.append({
                'year': y,
                'active_months_count': int(r['active_months']),
                'missing_months': miss_m,
                'message_count': int(r['message_count']),
                'known_archive_note': known_gaps.get(y, "Standard archival log.")
            })
            
        return {
            'coverage_summary': coverage_rows
        }
