def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()
    first_wire_moves, second_wire_moves = [line.split(",") for line in lines]
    first_current_point = (0, 0)
    first_wire_points = []
    second_current_point = (0, 0)
    second_wire_points = []
    for move in first_wire_moves:
        new_points = make_move(move, first_current_point)
        first_current_point = new_points[-1] if new_points else first_current_point
        first_wire_points.extend(new_points)
    for move in second_wire_moves:
        new_points = make_move(move, second_current_point)
        second_current_point = new_points[-1] if new_points else second_current_point
        second_wire_points.extend(new_points)
    crossings = set(first_wire_points).intersection(set(second_wire_points))
    print(min(abs(x[0]) + abs(x[1]) for x in crossings))
    print(min(first_wire_points.index(c) + second_wire_points.index(c) + 2 for c in crossings))


def make_move(move, start_point):
    distance = int(move[1:])
    direction = move[0]
    index = 0 if direction in ("U", "D") else 1
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
