with open("input.txt", "r") as f:
    input_txt = f.read()
orbit_lines = [x for x in input_txt.split() if x]


class Orbit(object):

    orbits = {}

    def __init__(self, orbit_string):
        self.parent_name, self.name = orbit_string.split(")")
        self.orbits[self.name] = self

    @property
    def orbit_count(self):
        if self.parent_name == "COM":
            return 1
        else:
            return self.orbits[self.parent_name].orbit_count + 1

    @property
    def path_to_com(self):
        if self.parent_name == "COM":
            return []
        else:
            parent = self.orbits[self.parent_name]
            return [parent] + parent.path_to_com


for orbit_string in orbit_lines:
    Orbit(orbit_string)
print(sum(orbit.orbit_count for orbit in Orbit.orbits.values()))


you = Orbit.orbits["YOU"]
santa = Orbit.orbits["SAN"]
you_path = you.path_to_com
santa_path = santa.path_to_com
you_branch = set(you_path) - set(santa_path)
santa_branch = set(santa_path) - set(you_path)
print(len(you_branch) + len(santa_branch))
