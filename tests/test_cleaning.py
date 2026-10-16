"""
Tests for Data Auditor and Deduplication Engine.
"""

import unittest
from src.cleaning.audit_deduplication import DataAuditor

class TestDataAuditor(unittest.TestCase):
    def setUp(self):
        self.auditor = DataAuditor()

    def test_cross_file_detection(self):
        sample_records = [
            {
                'source_file': '2020_logs.txt',
                'source_line': 10,
                'date': '2020-01-02',
                'year': 2020,
                'time_as_logged': '09:21',
                'callsign': 'АНВФ',
                'header_number': '06948',
                'full_word_sequence': 'ДОЛОХУК 5528 6989',
                'quality_flag': 'NORMAL'
            },
            {
                'source_file': '2022_logs.txt',
                'source_line': 4,
                'date': '2020-01-02',
                'year': 2020,
                'time_as_logged': '09:21',
                'callsign': 'АНВФ',
                'header_number': '06948',
                'full_word_sequence': 'ДОЛОХУК 5528 6989',
                'quality_flag': 'NORMAL'
            }
        ]
        all_audited, primary, stats = self.auditor.audit_and_deduplicate(sample_records)
        self.assertEqual(len(all_audited), 2)
        self.assertEqual(len(primary), 1)
        self.assertEqual(all_audited[1]['duplicate_type'], 'CROSS_FILE_DUPLICATE')
        self.assertEqual(all_audited[1]['is_duplicate'], 1)

    def test_exact_duplicate_detection(self):
        sample_records = [
            {
                'source_file': '2014_logs.txt',
                'source_line': 100,
                'date': '2014-04-09',
                'year': 2014,
                'time_as_logged': '11:48',
                'callsign': 'МДЖБ',
                'header_number': '34568',
                'full_word_sequence': 'ГАШЕНИЕ 4895 4813',
                'quality_flag': 'NORMAL'
            },
            {
                'source_file': '2014_logs.txt',
                'source_line': 120,
                'date': '2014-04-09',
                'year': 2014,
                'time_as_logged': '11:48',
                'callsign': 'МДЖБ',
                'header_number': '34568',
                'full_word_sequence': 'ГАШЕНИЕ 4895 4813',
                'quality_flag': 'NORMAL'
            }
        ]
        all_audited, primary, stats = self.auditor.audit_and_deduplicate(sample_records)
        self.assertEqual(len(primary), 1)
        self.assertEqual(all_audited[1]['duplicate_type'], 'EXACT_ARCHIVE_DUPLICATE')

if __name__ == '__main__':
    unittest.main()
