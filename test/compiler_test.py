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

    def test_LD_sign_ext(self):
        self.assertEqual(
            0b0000101011111011,
            compiler.parse_line('LD 1 -5(2)')
        )

    def test_ST(self):
        self.assertEqual(
            0b0100101000000101,
            compiler.parse_line('ST 1 5(2)')
        )

    def test_ST_sign_ext(self):
        self.assertEqual(
            0b0100101011111011,
            compiler.parse_line('ST 1 -5(2)')
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

    def test_LI(self):
        self.assertEqual(
            0b1000000100001111,
            compiler.parse_line('LI 1 15')
        )

    def test_LI_sign_ext(self):
        self.assertEqual(
            0b1000000111110001,
            compiler.parse_line('LI 1 -15')
        )

    def test_B(self):
        self.assertEqual(
            0b1010000100001111,
            compiler.parse_line('B 1 15')
        )

    def test_B_sign_ext(self):
        self.assertEqual(
            0b1010000111110001,
            compiler.parse_line('B 1 -15')
        )

    def test_BE(self):
        self.assertEqual(
            0b1011100000001111,
            compiler.parse_line('BE 15')
        )

    def test_BE_sign_ext(self):
        self.assertEqual(
            0b1011100011110001,
            compiler.parse_line('BE -15')
        )

    def test_BLT(self):
        self.assertEqual(
            0b1011100100001111,
            compiler.parse_line('BLT 15')
        )

    def test_BLT_sign_ext(self):
        self.assertEqual(
            0b1011100111110001,
            compiler.parse_line('BLT -15')
        )

    def test_BLE(self):
        self.assertEqual(
            0b1011101000001111,
            compiler.parse_line('BLE 15')
        )

    def test_BLE_sign_ext(self):
        self.assertEqual(
            0b1011101011110001,
            compiler.parse_line('BLE -15')
        )

    def test_BNE(self):
        self.assertEqual(
            0b1011101100001111,
            compiler.parse_line('BNE 15')
        )

    def test_BNE_sign_ext(self):
        self.assertEqual(
            0b1011101111110001,
            compiler.parse_line('BNE -15')
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

    def test_ADI(self):
        self.assertEqual(
            0b1100001001110011,
            compiler.parse_line('ADI 2 3')
        )

    def test_ADI_sign_ext(self):
        self.assertEqual(
            0b1100001001111101,
            compiler.parse_line('ADI 2 -3')
        )

    def test_SLL(self):
        self.assertEqual(
            0b1100001010000011,
            compiler.parse_line('SLL 2 3')
        )

    def test_SLR(self):
        self.assertEqual(
            0b1100001010010011,
            compiler.parse_line('SLR 2 3')
        )

    def test_SRL(self):
        self.assertEqual(
            0b1100001010100011,
            compiler.parse_line('SRL 2 3')
        )

    def test_SRA(self):
        self.assertEqual(
            0b1100001010110011,
            compiler.parse_line('SRA 2 3')
        )

    def test_IN(self):
        self.assertEqual(
            0b1100001111000000,
            compiler.parse_line('IN 3')
        )

    def test_OUT(self):
        self.assertEqual(
            0b1101100011010000,
            compiler.parse_line('OUT 3')
        )

    def test_HLT(self):
        self.assertEqual(
            0b1100000011110000,
            compiler.parse_line('HLT')
        )

    def test_parse_error(self):
        self.assertRaises(
            ValueError,
            compiler.parse_line,
            'HOGE 1 2'
        )

if __name__ == '__main__':
    unittest.main()
