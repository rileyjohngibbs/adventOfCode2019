import sys


def main(test=False):
    if test:
        input_txt = "1,1,1,4,99,5,6,0,99"
    else:
        with open("input.txt", "r") as f:
            input_txt = f.read()
    codes = [int(i) for i in input_txt.split(",") if i]
    codes_one = codes[:]
    if not test:
        codes_one[1] = 12
        codes_one[2] = 2
    compy = Intcode(codes_one)
    compy.execute_all()
    if test:
        print(compy.codes)
    else:
        print(compy.codes[0])
    two_output = None
    for noun in range(0, 100):
        for verb in range(0, 100):
            two_output = measure_modified(codes, noun, verb)
            if two_output == 19690720:
                break
        if two_output == 19690720:
            break
    if two_output != 19690720:
        raise Exception("Not found")
    print(100 * noun + verb)


def measure_modified(codes, noun, verb):
    modded = codes[:]
    modded[1] = noun
    modded[2] = verb
    compy = Intcode(modded)
    compy.execute_all()
    return compy.codes[0]


class Halt:
    pass


class Intcode(object):

    INSTRUCTION_VALUES = 4
    _operations = {
        1: lambda x, y: x + y,
        2: lambda x, y: x * y,
        99: Halt,
    }

    def __init__(self, codes):
        self.codes = codes
        self.position = 0

    def execute_next(self):
        operation = self._operations.get(self.codes[self.position])
        if operation == Halt:
            raise StopIteration()
        first_operand = self.codes[self.codes[self.position + 1]]
        second_operand = self.codes[self.codes[self.position + 2]]
        destination = self.codes[self.position + 3]
        self.codes[destination] = operation(first_operand, second_operand)
        self.position += self.INSTRUCTION_VALUES

    def execute_all(self):
        while True:
            try:
                self.execute_next()
            except StopIteration:
                break


if __name__ == "__main__":
    main("test" in sys.argv)
