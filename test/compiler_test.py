import unittest
import sys
sys.path.append('.')
import compiler

class CompilerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_LD(self):
        self.assertEqual(
            0b0000101000000101,
            compiler.parse_line('LD 1 5(2)')
        )

    def test_ST(self):
        self.assertEqual(
            0b0100101000000101,
            compiler.parse_line('ST 1 5(2)')
        )

    def test_ADD(self):
        self.assertEqual(
            0b1101101000000000,
            compiler.parse_line('ADD 2 3')
        )

    def test_SUB(self):
        self.assertEqual(
            0b1101101000010000,
            compiler.parse_line('SUB 2 3')
        )

    def test_AND(self):
        self.assertEqual(
            0b1101101000100000,
            compiler.parse_line('AND 2 3')
        )

    def test_OR(self):
        self.assertEqual(
            0b1101101000110000,
            compiler.parse_line('OR 2 3')
        )

    def test_XOR(self):
        self.assertEqual(
            0b1101101001000000,
            compiler.parse_line('XOR 2 3')
        )

    def test_CMP(self):
        self.assertEqual(
            0b1101101001010000,
            compiler.parse_line('CMP 2 3')
        )

    def test_MOV(self):
        self.assertEqual(
            0b1101101001100000,
            compiler.parse_line('MOV 2 3')
        )

if __name__ == '__main__':
    unittest.main()
