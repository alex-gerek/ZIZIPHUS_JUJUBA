"""
ZIZIPHUS JUJUBA: Phase 2 Comprehensive Test Suite.
Verifies traffic dynamics, structural models, anomaly detection,
network evolution, advanced event study, and findings registry.
"""

import unittest
import sqlite3
import pathlib

from src.database.db_manager import DatabaseManager
from src.analysis.traffic_behavior import TrafficBehaviorEngine
from src.analysis.structural_analysis import StructuralDynamicsEngine
from src.analysis.anomaly_detector import AnomalyDetector
from src.models.network_evolution import NetworkEvolutionEngine
from src.models.event_study_advanced import AdvancedEventStudyEngine
from src.analysis.findings_registry import FindingsRegistryEngine

DB_PATH = pathlib.Path("D:/Projects/ZIZIPHUS_JUJUBA/data/database/ziziphus_jujuba.db")


class TestPhase2Suite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(DB_PATH)
        cls.conn.row_factory = sqlite3.Row

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_traffic_behavior(self):
        engine = TrafficBehaviorEngine(self.conn)
        vol = engine.get_volume_dynamics()
        self.assertGreater(vol['total_clean_messages'], 1000)
        self.assertIn(2014, vol['yearly_counts'])

        diu = engine.get_diurnal_distribution()
        self.assertGreater(diu['daytime_pct_utc'], 50.0)

        int_arr = engine.get_inter_arrival_analysis()
        self.assertGreater(int_arr['fano_factor'], 1.5)
        self.assertEqual(int_arr['poisson_hypothesis'], 'REJECTED')

        cyc = engine.get_periodicity_and_autocorrelation()
        self.assertIn('acf_series', cyc)

    def test_structural_changes(self):
        engine = StructuralDynamicsEngine(self.conn)
        cs = engine.get_callsign_evolution()
        self.assertGreater(len(cs['callsign_distribution']), 0)

        bl = engine.get_message_length_and_block_counts()
        self.assertGreater(bl['overall_metrics']['single_block_pct'], 80.0)

        voc = engine.get_vocabulary_turnover()
        self.assertLess(voc['heaps_law']['beta'], 1.0)
        self.assertGreater(voc['total_unique_vocabulary'], 500)

        cooc = engine.get_word_cooccurrence()
        self.assertIn('pairs', cooc)

    def test_anomaly_detector(self):
        detector = AnomalyDetector(self.conn)
        anom = detector.detect_daily_anomalies(threshold_mad=3.0)
        self.assertGreater(anom['anomalous_days_detected'], 0)

        feb = detector.audit_february_2022()
        self.assertGreater(feb['cross_file_duplicates_purged'], 0)
        self.assertIn('CONFIRMED', feb['scientific_verdict'])

        gaps = detector.audit_archive_coverage_and_gaps()
        self.assertGreater(gaps['major_gaps_count'], 0)

    def test_network_evolution(self):
        engine = NetworkEvolutionEngine(self.conn)
        epochs = engine.get_epoch_metrics()
        self.assertEqual(len(epochs), 4)
        self.assertGreater(epochs[1]['nodes'], 100)

        vis = engine.get_epoch_subgraph_vis('epoch_2')
        self.assertGreater(len(vis['nodes']), 0)
        self.assertGreater(len(vis['edges']), 0)

    def test_advanced_event_study(self):
        engine = AdvancedEventStudyEngine(self.conn)
        res = engine.run_rigorous_event_study(window_days=14)
        self.assertGreater(res['total_events'], 5)
        self.assertIn('fdr_threshold', res)
        self.assertIn('placebo_false_positive_rate', res)

    def test_findings_registry(self):
        engine = FindingsRegistryEngine()
        data = engine.get_findings_summary()
        self.assertGreaterEqual(len(data['confirmed_facts']), 5)
        self.assertGreaterEqual(len(data['refuted_or_unconfirmed_hypotheses']), 3)
        self.assertGreaterEqual(len(data['methodological_limitations']), 3)


if __name__ == "__main__":
    unittest.main()
