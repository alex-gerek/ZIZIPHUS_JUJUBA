import sqlite3
import unittest
from src.radio.live_receiver import LiveRadioManager

class TestLiveRadio(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("""
            CREATE TABLE Messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER,
                source_file TEXT,
                source_line INTEGER,
                date TEXT,
                year INTEGER,
                month INTEGER,
                day INTEGER,
                time_as_logged TEXT,
                timezone TEXT,
                callsign TEXT,
                header_number TEXT,
                full_text TEXT,
                full_word_sequence TEXT,
                block_count INTEGER,
                quality_flag TEXT,
                is_duplicate INTEGER DEFAULT 0
            )
        """)
        self.conn.execute("""
            CREATE TABLE CodeBlocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER,
                block_index INTEGER,
                code_word TEXT,
                digit_group_1 TEXT,
                digit_group_2 TEXT,
                digit_combination TEXT,
                uncertainty_flag INTEGER DEFAULT 0,
                notes TEXT
            )
        """)
        self.conn.execute("""
            CREATE TABLE AuditLog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file TEXT,
                source_line INTEGER,
                date TEXT,
                time TEXT,
                audit_type TEXT,
                action_taken TEXT,
                rationale TEXT,
                raw_snippet TEXT
            )
        """)
        self.mgr = LiveRadioManager(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_receivers_and_specs(self):
        receivers = self.mgr.get_receivers()
        self.assertGreaterEqual(len(receivers), 4)
        specs = self.mgr.get_station_specs()
        self.assertIn("4625.0 kHz", specs["transmitter"]["primary_frequency"])

    def test_log_and_retrieve_interception(self):
        res = self.mgr.log_interception(
            callsign="МДЖБ",
            codeword="ЗИЗИФУС",
            digit_combination="7724 8209",
            header_number="12 345",
            signal_quality="5/5",
            notes="Test interception"
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertGreater(res["message_id"], 0)
        self.assertIn("ЗИЗИФУС", res["full_text"])

        recent = self.mgr.get_recent_interceptions()
        self.assertEqual(len(recent), 1)
        self.assertEqual(recent[0]["codeword"], "ЗИЗИФУС")
        self.assertEqual(recent[0]["digit_combination"], "7724 8209")

if __name__ == "__main__":
    unittest.main()
