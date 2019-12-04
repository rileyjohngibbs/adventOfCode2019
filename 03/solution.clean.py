from functools import reduce
import re

MOVE_RE = re.compile("(U|D|L|R)(\d+)")


def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()
    moves_lists = [line.split(",") for line in lines]
    paths = []
    for moves_list in moves_lists:
        new_path = []
        paths.append(new_path)
        location = (0, 0)
        for move in moves_list:
            new_points = make_move(move, location)
            location = new_points[-1] if new_points else location
            new_path.extend(new_points)
    crossings = reduce(lambda x, y: x.intersection(y), paths[1:], set(paths[0]))
    minimum_manhattan = min(abs(x[0]) + abs(x[1]) for x in crossings)
    print(minimum_manhattan)
    minimum_steps = min(
        sum(path.index(c) + 1 for path in paths)
        for c in crossings
    )
    print(minimum_steps)


def make_move(move, start_point):
    direction, distance= re.match(MOVE_RE, move).groups()
    distance = int(distance)
    vertical = direction in ("U", "D")
    sign = -1 if direction in ("U", "L") else 1
    return [
        (
            start_point[0] + sign * (i + 1) * vertical,
            start_point[1] + sign * (i + 1) * (not vertical)
        )
        for i in range(distance)
    ]


if __name__ == "__main__":
    main()
