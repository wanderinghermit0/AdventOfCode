import re


class Cave:

    def _convert_coord(self, wall_coord):
        map_coord = (wall_coord[0] - self.bounds[0], wall_coord[1] - self.bounds[2])
        return map_coord

    def print_map(self):
        dim = (self.bounds[3] - self.bounds[2] + 1, self.bounds[1] - self.bounds[0] + 1)
        map = [["." for j in range(dim[1])] for i in range(dim[0])]

        sand_source = self._convert_coord((500, 0))
        map[sand_source[1]][sand_source[0]] = "+"

        for sand in self.sandpile:
            sand = self._convert_coord(sand)
            map[sand[1]][sand[0]] = "o"

        for wall in self.wall_coord:
            wall = self._convert_coord(wall)
            map[wall[1]][wall[0]] = "#"

        s = ""
        for i in range(len(map)):
            for j in range(len(map[0])):
                s += map[i][j]
            s += "\n"

        print(s)

    def _outside_bounds(self, pos):
        inside_x = self.bounds[0] <= pos[0] <= self.bounds[1]
        inside_y = self.bounds[2] <= pos[1] <= self.bounds[3]
        return not inside_x or not inside_y

    def drop_sand(self):
        init_coord = (500, 0)
        stopped = False
        while not stopped:
            if self.finish:
                break

            next_pos = (init_coord[0], init_coord[1] + 1)
            if next_pos in self.wall_coord or next_pos in self.sandpile:
                next_pos = (init_coord[0] - 1, init_coord[1] + 1)
            if next_pos in self.wall_coord or next_pos in self.sandpile:
                next_pos = (init_coord[0] + 1, init_coord[1] + 1)
            if next_pos in self.wall_coord or next_pos in self.sandpile:
                stopped = True
                if init_coord not in self.sandpile:
                    self.sandpile.add(init_coord)
                else:
                    self.finish = True
            else:
                if self._outside_bounds(next_pos):
                    self.finish = True
                else:
                    init_coord = next_pos

    def _create_walls(self):
        for wall in self.walls:
            prev_wall_section = None
            for wall_section in wall:
                if prev_wall_section is not None:
                    if wall_section[0] != prev_wall_section[0]:
                        min_wall_x = min(wall_section[0], prev_wall_section[0])
                        max_wall_x = max(wall_section[0], prev_wall_section[0])
                        for i in range(min_wall_x, max_wall_x + 1):
                            self.wall_coord.add((i, wall_section[1]))
                    else:
                        min_wall_x = min(wall_section[1], prev_wall_section[1])
                        max_wall_x = max(wall_section[1], prev_wall_section[1])
                        for i in range(min_wall_x, max_wall_x + 1):
                            self.wall_coord.add((wall_section[0], i))
                prev_wall_section = wall_section

    def create_floor(self):
        self.bounds[3] = self.bounds[3] + 2
        center = 500
        deviation = self.bounds[3] - self.bounds[2] + 1
        self.bounds[0] = center - deviation
        self.bounds[1] = center + deviation
        for i in range(center - deviation, center + deviation):
            self.wall_coord.add((i, self.bounds[3]))

    def __init__(self, name):
        self.walls = []
        self.wall_coord = set()
        self.sandpile = set()
        self.finish = False
        min_x = 1000
        max_x = 0
        min_y = 0
        max_y = 0
        f = open(name)
        for line in f:
            wall_str = re.split("->", line)
            self.walls.append([])
            for i in range(len(wall_str)):
                wall_section_str = wall_str[i].strip().split(",")
                wall_tuple = (int(wall_section_str[0]), int(wall_section_str[1]))
                if wall_tuple[0] > max_x:
                    max_x = wall_tuple[0]
                if wall_tuple[0] < min_x:
                    min_x = wall_tuple[0]
                if wall_tuple[1] > max_y:
                    max_y = wall_tuple[1]
                self.walls[-1].append(wall_tuple)

        f.close()
        self.bounds = [min_x, max_x, min_y, max_y]
        self._create_walls()


def aoc14a(name):
    cave = Cave(name)
    sand_units = 0
    while not cave.finish:
        cave.drop_sand()
        #cave.print_map()
        sand_units += 1
        print(sand_units)

def aoc14b(name):
    cave = Cave(name)
    cave.create_floor()
    sand_units = 0
    cave.print_map()
    while not cave.finish:
        cave.drop_sand()
        sand_units += 1
        print(sand_units)

#aoc14a("input14_test.txt")
#aoc14a("input14.txt")
aoc14b("input14_test.txt")
aoc14b("input14.txt")