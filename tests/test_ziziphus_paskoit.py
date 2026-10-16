"""
Verification Test for ZIZIPHUS and PASKOIT primary records alignment.
Confirms the exact coincidence of 7724 8209 between PASKOIT and ZIZIPHUS in primary logs.
"""

import unittest
import sqlite3
import pathlib

DB_PATH = pathlib.Path("D:/Projects/ZIZIPHUS_JUJUBA/data/database/ziziphus_jujuba.db")

class TestZiziphusPaskoit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(str(DB_PATH))
        cls.conn.row_factory = sqlite3.Row

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_77248209_primary_coincidence(self):
        """Verifies that 7724 8209 is shared between PASKOIT and ZIZIPHUS."""
        rows = self.conn.execute("""
            SELECT m.date, m.time_as_logged, cb.code_word, cb.digit_combination,
                   m.source_file, m.source_line, m.full_word_sequence
            FROM CodeBlocks cb
            JOIN Messages m ON cb.message_id = m.id
            WHERE cb.digit_combination = '77248209'
            ORDER BY m.date ASC
        """).fetchall()

        self.assertEqual(len(rows), 2, "Expected exactly 2 primary radiograms for combination 7724 8209")
        
        # First appearance: PASKOIT
        r1 = rows[0]
        self.assertEqual(r1['date'], '2014-09-04')
        self.assertEqual(r1['code_word'], 'ПАСКОИТ')
        self.assertEqual(r1['digit_combination'], '77248209')
        self.assertEqual(r1['source_file'], '2014_logs.txt')
        self.assertEqual(r1['time_as_logged'], '13:24')

        # Second appearance: ZIZIPHUS
        r2 = rows[1]
        self.assertEqual(r2['date'], '2014-10-02')
        self.assertEqual(r2['code_word'], 'ЗИЗИФУС')
        self.assertEqual(r2['digit_combination'], '77248209')
        self.assertEqual(r2['source_file'], '2014_logs.txt')
        self.assertEqual(r2['time_as_logged'], '12:14')

    def test_gashenie_ziziphus_co_occurrence(self):
        """Verifies that GASHENIE and ZIZIPHUS co-occurred in the same radiogram."""
        rows = self.conn.execute("""
            SELECT m.date, m.full_word_sequence, m.source_file, m.source_line
            FROM Messages m
            WHERE m.full_word_sequence LIKE '%ГАШЕНИЕ%'
              AND m.full_word_sequence LIKE '%ЗИЗИФУС%'
        """).fetchall()

        self.assertGreaterEqual(len(rows), 1, "Expected at least 1 radiogram containing both GASHENIE and ZIZIPHUS")
        self.assertEqual(rows[0]['date'], '2014-04-09')

    def test_nizkij_ziziphus_co_occurrence(self):
        """Verifies that NIZKIJ and ZIZIPHUS co-occurred in the same radiogram in 2019."""
        rows = self.conn.execute("""
            SELECT m.date, m.full_word_sequence, m.source_file, m.source_line
            FROM Messages m
            WHERE m.full_word_sequence LIKE '%НИЗКИЙ%'
              AND m.full_word_sequence LIKE '%ЗИЗИФУС%'
        """).fetchall()

        self.assertGreaterEqual(len(rows), 1, "Expected at least 1 radiogram containing both NIZKIJ and ZIZIPHUS")
        self.assertEqual(rows[0]['date'], '2019-06-19')

if __name__ == '__main__':
    unittest.main()
