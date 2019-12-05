import itertools as it
import sys
import unittest


def main():
    with open("input.txt", "r") as f:
        input_txt = f.read()
    codes = [int(i) for i in input_txt.split(",") if i]
    compy = Intcode(codes, 1)
    compy.execute_all()
    print(compy.output[-1])
    codes = [int(i) for i in input_txt.split(",") if i]
    compy = Intcode(codes, 5)
    compy.execute_all()
    print(compy.output[-1])


class DayFive(unittest.TestCase):

    def run_with(self, input_, expected, input_txt=None):
        input_txt = input_txt or self.input_txt
        codes = [int(i) for i in input_txt.split(",") if i]
        compy = Intcode(codes, input_, True)
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


class Intcode(object):

    def __init__(self, codes, input_, test=False):
        self.codes = codes[:]
        self.position = 0
        self.input_ = input_
        self.output = []
        self.test_buffer = [] if test else None

    def execute_all(self):
        while True:
            try:
                self.execute_next()
            except StopIteration:
                return self.output

    def execute_next(self):
        if self.test_buffer is not None:
            self.test_buffer.append((self.codes, self.position))
        operations = {
            1: self.add,
            2: self.mul,
            3: self.put_input,
            4: self.out,
            5: self.jtrue,
            6: self.jfalse,
            7: self.lt,
            8: self.eq,
            99: self.halt,
        }
        operation = operations.get(self.codes[self.position] % 100)
        immediate_modes = [x == "1" for x in reversed(str(self.codes[self.position])[:-2])]
        operation(*immediate_modes)

    def write_to_address(self, address, value):
        self.codes[self.codes[self.position + address]] = value

    def add(self, *immediate_modes):
        params = self.get_params(2, *immediate_modes)
        self.write_to_address(3, params[0] + params[1])
        self.position += 4

    def mul(self, *immediate_modes):
        params = self.get_params(2, *immediate_modes)
        self.write_to_address(3, params[0] * params[1])
        self.position += 4

    def put_input(self, *immediate_modes):
        self.write_to_address(1, self.input_)
        self.position += 2

    def out(self, *immediate_modes):
        params = self.get_params(1, *immediate_modes)
        self.output.append(params[0])
        self.position += 2

    def jtrue(self, *immediate_modes):
        params = self.get_params(2, *immediate_modes)
        if params[0]:
            self.position = params[1]
        else:
            self.position += 3

    def jfalse(self, *immediate_modes):
        params = self.get_params(2, *immediate_modes)
        if not params[0]:
            self.position = params[1]
        else:
            self.position += 3

    def lt(self, *immediate_modes):
        params = self.get_params(2, *immediate_modes)
        self.write_to_address(3, int(params[0] < params[1]))
        self.position += 4

    def eq(self, *immediate_modes):
        params = self.get_params(2, *immediate_modes)
        self.write_to_address(3, int(params[0] == params[1]))
        self.position += 4

    def halt(self, *args, **kwargs):
        raise StopIteration()

    def get_params(self, count, *immediate_modes):
        start = self.position + 1
        stop = self.position + count + 1
        params = [
            code if immediate else self.codes[code]
            for code, immediate in it.zip_longest(
                self.codes[start:stop],
                immediate_modes,
                fillvalue=False
            )
        ]
        return params


if __name__ == "__main__":
    main()
