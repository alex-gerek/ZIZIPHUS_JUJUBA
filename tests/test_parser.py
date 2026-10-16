"""
Tests for UVB-76 Log Parser.
"""

import unittest
from src.parsing.log_parser import extract_code_blocks, clean_word, UVBLogParser

class TestUVBParser(unittest.TestCase):
    def test_single_block_8digit(self):
        text = "ПЕХОТИНЕЦ 33278882"
        blocks = extract_code_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]['code_word'], "ПЕХОТИНЕЦ")
        self.assertEqual(blocks[0]['digit_group_1'], "3327")
        self.assertEqual(blocks[0]['digit_group_2'], "8882")
        self.assertEqual(blocks[0]['digit_combination'], "33278882")

    def test_multi_block_radiogram(self):
        text = "ГАШЕНИЕ 4895 4813 ЗИЗИФУС 9836 1935"
        blocks = extract_code_blocks(text)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0]['code_word'], "ГАШЕНИЕ")
        self.assertEqual(blocks[0]['digit_combination'], "48954813")
        self.assertEqual(blocks[1]['code_word'], "ЗИЗИФУС")
        self.assertEqual(blocks[1]['digit_combination'], "98361935")

    def test_ziziphus_paskoit_strings(self):
        paskoit_text = "PASKOIT 77248209"
        ziziphus_text = "ZIZIFUS 77248209"
        b1 = extract_code_blocks(paskoit_text)
        b2 = extract_code_blocks(ziziphus_text)
        self.assertEqual(b1[0]['digit_combination'], "77248209")
        self.assertEqual(b2[0]['digit_combination'], "77248209")
        self.assertEqual(b1[0]['digit_combination'], b2[0]['digit_combination'])

if __name__ == '__main__':
    unittest.main()
