"""
Tests for Mathematical Models and Analytics in ZIZIPHUS JUJUBA.
"""

import unittest
import sqlite3
import pathlib

from src.analysis.frequency_analysis import FrequencyAnalyzer
from src.analysis.repetition_analysis import RepetitionAnalyzer
from src.analysis.time_series import TimeSeriesAnalyzer
from src.models.clustering_modes import OperationalModesClustering
from src.models.graph_intelligence import GraphIntelligenceEngine
from src.models.event_study import HistoricalEventStudy
from src.models.hypothesis_tests import HypothesisTestingEngine

DB_PATH = pathlib.Path("D:/Projects/ZIZIPHUS_JUJUBA/data/database/ziziphus_jujuba.db")

class TestAnalyticsModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(str(DB_PATH))
        cls.conn.row_factory = sqlite3.Row

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_frequency_analysis(self):
        fa = FrequencyAnalyzer(self.conn)
        words = fa.get_word_frequencies(top_n=10)
        self.assertGreater(words['total_tokens'], 1000)
        self.assertGreater(words['unique_words'], 500)
        
        callsigns = fa.get_callsign_frequencies()
        self.assertGreater(len(callsigns['callsigns']), 3)

    def test_repetition_analysis(self):
        ra = RepetitionAnalyzer(self.conn)
        reps = ra.get_repeated_numbers(min_occurrences=2)
        self.assertGreater(reps['total_repeating_combinations'], 50)
        self.assertGreater(reps['cross_word_count'], 20)
        self.assertGreater(reps['overall_mean_interval_days'], 0)

    def test_time_series_matrix(self):
        ts = TimeSeriesAnalyzer(self.conn)
        mat = ts.get_normalized_monthly_matrix()
        self.assertGreaterEqual(len(mat['years']), 8)
        self.assertEqual(len(mat['matrix']), len(mat['years']))

    def test_clustering_modes(self):
        cl = OperationalModesClustering(self.conn)
        res = cl.fit_clustering(n_clusters=3)
        self.assertEqual(res['n_clusters'], 3)
        self.assertIn('silhouette_score', res)
        self.assertEqual(len(res['clustered_years']), 8)

    def test_graph_intelligence(self):
        ge = GraphIntelligenceEngine(self.conn)
        sub = ge.get_target_subgraph(target_words=['ЗИЗИФУС', 'ПАСКОИТ'])
        self.assertGreater(sub['node_count'], 2)
        self.assertGreater(sub['edge_count'], 1)

    def test_event_study(self):
        es = HistoricalEventStudy(self.conn)
        results = es.evaluate_all_historical_events()
        self.assertGreater(len(results), 10)
        for r in results:
            self.assertIn('pre_observed', r)
            self.assertIn('pre_baseline_mean', r)
            self.assertIn('pre_p_upper', r)

    def test_permutation_test(self):
        ht = HypothesisTestingEngine(self.conn)
        res = ht.run_permutation_test(['2014-02-22', '2014-03-16'], window_days=7, n_permutations=200)
        self.assertEqual(res['n_permutations'], 200)
        self.assertIn('empirical_p_value', res)
        self.assertIn('z_score', res)

if __name__ == '__main__':
    unittest.main()
