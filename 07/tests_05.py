import unittest

from solution import Intcode


class DayFive(unittest.TestCase):

    def run_with(self, input_, expected, input_txt=None):
        input_txt = input_txt or self.input_txt
        codes = [int(i) for i in input_txt.split(",") if i]
        compy = Intcode(codes, input_, test=True)
        compy.execute_all()
        self.assertEqual(
            compy.output[-1],
            expected,
            "\n".join(f"{b[0]}\n{b[1]}" for b in compy.test_buffer)
        )


class ImmediateEqualsEight(DayFive):

    def setUp(self):
        self.input_txt = "3,3,1108,-1,8,3,4,3,99"

    def test_does(self):
        self.run_with(8, 1)

    def test_does_not(self):
        self.run_with(5, 0)


class Complicated(DayFive):

    def setUp(self):
        self.input_txt = (
            "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,"
            "98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,"
            "1101,1000,1,20,4,20,1105,1,46,98,99"
        )

    def test_less(self):
        self.run_with(7, 999)

    def test_equal(self):
        self.run_with(8, 1000)

    def test_grater(self):
        self.run_with(9, 1001)


class PositionNonZero(DayFive):

    def setUp(self):
        self.input_txt = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"

    def test_non_zero(self):
        self.run_with(8, 1)

    def test_zero(self):
        self.run_with(0, 0)


class ImmediateNonZero(DayFive):

    def setUp(self):
        self.input_txt = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"

    def test_non_zero(self):
        self.run_with(8, 1)

    def test_zero(self):
        self.run_with(0, 0)


