import itertools as it


def main():
    with open("input.txt", "r") as f:
        input_txt = f.read()
    codes = [int(i) for i in input_txt.split(",") if i]
    max_output = float("-inf")
    max_sequence = None
    for sequence in it.permutations([0, 1, 2, 3, 4]):
        output = run_phase_sequence(codes, sequence)
        if output > max_output:
            max_output = output
            max_sequence = sequence
    print(max_output)
    max_output = float("-inf")
    max_sequence = None
    for sequence in it.permutations([5, 6, 7, 8, 9]):
        output = run_feedback_loop(codes, sequence)
        if output > max_output:
            max_output = output
            max_sequence = sequence
    print(max_output)


def run_phase_sequence(codes, sequence):
    input_ = 0
    for phase in sequence:
        compy = Intcode(codes, phase, input_)
        compy.execute_all()
        input_ = compy.output[-1]
    return input_


def run_feedback_loop(codes, sequence):
    input_ = 0
    index = 4
    first_run = True
    compies = (
        [Intcode(codes, sequence[0], 0)]
        + [Intcode(codes, phase, None) for phase in sequence[1:]]
    )
    for i, compy in enumerate(compies):
        compy.input_source = compies[(i + 4) % 5]
    output = compies[-1].execute_all()
    return output


def infinite_gen(output):
    while True:
        yield output


class Intcode(object):

    def __init__(self, codes, phase, input_=None, test=False):
        self.codes = codes[:]
        self.position = 0
        self.phase = phase
        self.static_input = input_
        self.input_source = None
        self.input_gen = (x for x in [phase, input_] if x is not None)
        self.output = []
        self.test_buffer = [] if test else None

    @property
    def input_(self):
        try:
            return next(self.input_gen)
        except StopIteration:
            if self.input_source is not None:
                if not self.input_source.output:
                    self.input_source.generate_output()
                return self.input_source.output.pop(0)
            else:
                return self.static_input

    @property
    def is_complete(self):
        return self.codes[self.position] == 99

    def execute_all(self, with_input=None):
        while True:
            try:
                self.execute_next(with_input)
            except StopIteration:
                return self.output[-1]

    def generate_output(self):
        output_count = len(self.output)
        while output_count == len(self.output):
            self.execute_next()

    def execute_next(self, with_input=None):
        if with_input is not None:
            original_input = self.input_
            self.input_ = with_input
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
        if with_input is not None:
            self.input_ = original_input

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
