
class shape:
    ROW = 0
    CROSS = 1
    L = 2
    COL = 3
    SQUARE = 4

class Pit:

    def __init__(self, max_rocks):
        self.height_added = []
        self.tower_height = 0
        self.tower_pos = set([(0, i) for i in range(-3, 3 + 1)])
        self.rock_count = 0
        self.max_rocks = max_rocks

    def create_last_cycle(self, set):
        cycle_rocks = self.rock_count
        cycle_height = self.tower_height
        num_cycles = self.max_rocks // self.rock_count
        self.rock_count = num_cycles * cycle_rocks
        self.tower_height = num_cycles * cycle_height
        for element in set:
            pos = (element[0] + (num_cycles - 1)*cycle_height, element[1])
            self.tower_pos.add(pos)

        return self.rock_count

    def detect_repeats(self, seq_len=5):
        for i in range(len(self.height_added) - seq_len):
            seq1 = self.height_added[i:i+seq_len]
            for j in range(i + seq_len, len(self.height_added) - seq_len):
                seq2 = self.height_added[j:j+seq_len]
                if seq1 == seq2:

                    return (i, j - i)

        return (0, 0)

    def detect_rocks(self, pos):
        detection = False
        for fragment in self.rock.shape:
            new_pos = (fragment[0] + pos[0], fragment[1] + pos[1])
            if new_pos in self.tower_pos:
                detection = True

        return detection

    def detect_walls(self, pos):
        detected = False
        if pos[1] < -3:
            detected = True
        if pos[1] + self.rock.width() - 1 > 3:
            detected = True

        return detected

    def initialize_rock(self, rock):
        self.rock = rock
        self.rock_count += 1
        self.rock.position = [self.tower_height + 3 + 1, -1]

    def pile_rock(self):
        max_height = 0
        for fragment in self.rock.shape:
            new_pos = (fragment[0] + self.rock.position[0], fragment[1] + self.rock.position[1])

            if new_pos[0] > max_height:
                max_height = new_pos[0]

            self.tower_pos.add(new_pos)

        if max_height > self.tower_height:
            self.height_added.append(max_height - self.tower_height)
            self.tower_height = max_height
        else:
            self.height_added.append(0)

    def move_left(self):
        new_pos = (self.rock.position[0], self.rock.position[1] - 1)
        if not self.detect_walls(new_pos) and not self.detect_rocks(new_pos):
            self.rock.move_left()

    def move_right(self):
        new_pos = (self.rock.position[0], self.rock.position[1] + 1)
        if not self.detect_walls(new_pos) and not self.detect_rocks(new_pos):
            self.rock.move_right()

    def move_down(self):
        new_pos = (self.rock.position[0] - 1, self.rock.position[1])
        if not self.detect_walls(new_pos) and not self.detect_rocks(new_pos):
            self.rock.move_down()
        elif self.detect_rocks(new_pos):
            self.rock.has_fallen = True
            self.pile_rock()

    def print_coord(self, pos, height, min_x):
        new_pos = ((height - 1) - pos[0], pos[1] - min_x)
        return new_pos

    def print_pit(self):
        max_y = self.tower_height + 3 + 1 + self.rock.height()
        min_y = 0
        max_x = 3
        min_x = -3

        arr = [["." for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y)]

        for fragment in self.rock.shape:
            pos = (fragment[0] + self.rock.position[0], fragment[1] + self.rock.position[1])
            pos = self.print_coord(pos, len(arr), min_x)
            arr[pos[0]][pos[1]] = "@"

        for fragment in self.tower_pos:
            pos = self.print_coord(fragment, len(arr), min_x)
            arr[pos[0]][pos[1]] = "#"

        s = ""
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                s += arr[i][j]
            s += "\n"

        s += "\n\n"
        print(s)

class Rock:

    def __init__(self, shape_type):
        self.has_fallen = False
        self.position = [-1, 0]

        if shape_type == shape.ROW:
            self.create_row()
        elif shape_type == shape.CROSS:
            self.create_cross()
        elif shape_type == shape.L:
            self.create_l()
        elif shape_type == shape.COL:
            self.create_col()
        elif shape_type == shape.SQUARE:
            self.create_square()
        else:
            print("No shape exists.")

    def create_row(self):
        self.shape = {(0, 0), (0, 1), (0, 2), (0, 3)}

    def create_cross(self):
        self.shape = {(0, 1), (1, 1), (2, 1), (1, 0), (1, 2)}

    def create_l(self):
        self.shape = {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)}

    def create_col(self):
        self.shape = {(0, 0), (1, 0), (2, 0), (3, 0)}

    def create_square(self):
        self.shape = {(0, 0), (0, 1), (1, 0), (1, 1)}

    def move_left(self):
        self.position[1] -= 1

    def move_right(self):
        self.position[1] += 1

    def move_down(self):
        self.position[0] -= 1

    def width(self):
        width = 0
        for fragment in self.shape:
            if fragment[1] + 1 > width:
                width = fragment[1] + 1

        return width

    def height(self):
        height = 0
        for fragment in self.shape:
            if fragment[0] + 1 > height:
                height = fragment[0] + 1

        return height


def aoc17a(name):
    f = open(name)
    input = f.read()
    f.close()

    input_idx = 0
    rocks_num = 10
    pit = Pit(rocks_num)
    for i in range(rocks_num):

        rock = Rock(i % 5)
        pit.initialize_rock(rock)
        while not rock.has_fallen:
            pit.print_pit()
            direction = input[input_idx % len(input)]
            if direction == "<":
                pit.move_left()
            else:
                pit.move_right()
            pit.print_pit()
            pit.move_down()
            input_idx += 1

    print(pit.tower_height)


def aoc17b(name):
    f = open(name)
    input = f.read()
    f.close()

    input_idx = 0
    rocks_num = 1000000000000
    pit = Pit(rocks_num)
    i = 0
    offset = 0
    cycle_len = 0
    while i < rocks_num and cycle_len == 0:

        rock = Rock(i % 5)
        pit.initialize_rock(rock)
        while not rock.has_fallen and cycle_len == 0:
            direction = input[input_idx % len(input)]
            if direction == "<":
                pit.move_left()
            else:
                pit.move_right()
            #pit.print_pit()
            pit.move_down()
            (offset, cycle_len) = pit.detect_repeats(seq_len=10)

            input_idx += 1

            #pit.print_pit()

        i += 1
        #print(i)

    num_cycles = rocks_num // cycle_len
    cycles_height = num_cycles*sum(pit.height_added[offset:offset+cycle_len])
    remainder_start = rocks_num - num_cycles*cycle_len
    remainder = pit.height_added[]
    total_height = pit.height_added[0:offset] + cycles_height
    print(pit.tower_height)

#aoc17a("input17_test.txt")
aoc17b("input17_test.txt")

'''
pit = Pit(1000)
set1 = {(0, 0), (0, 1), (0, 2), (1, 1), (2, 1), (3, 1), (2, 0), (3, 2), (4, 1)}
set2 = set1.copy()
for element in set1:
    if element[0] > 0:
        pos = (element[0] + 4, element[1])
        set2.add(pos)

        if pos[0] > pit.tower_height:
            pit.tower_height = pos[0]

pit.tower_pos = set2
repeats = pit.detect_repeats()
print(repeats)
'''