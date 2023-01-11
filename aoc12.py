class Direction:
    N = 0
    E = 1
    S = 2
    W = 3


class HeightMap:

    def hits_border(self, pos):
        map_dim = (len(self.map), len(self.map[0]))
        row_in_boundary = 0 <= pos[0] <= map_dim[0] - 1
        col_in_boundary = 0 <= pos[1] <= map_dim[1] - 1
        on_border = not row_in_boundary or not col_in_boundary
        return on_border


    def height_boundary(self, pos1, pos2=None):
        if pos2 is None:
            pos2 = self.cur_pos

        height_cond1 = self.map[pos2[0]][pos2[1]] + 2 <= self.map[pos1[0]][pos1[1]]
        return height_cond1

    def move(self, direction):
        if direction == Direction.N:
            new_pos = (self.cur_pos[0] - 1, self.cur_pos[1])
        elif direction == Direction.E:
            new_pos = (self.cur_pos[0], self.cur_pos[1] + 1)
        elif direction == Direction.S:
            new_pos = (self.cur_pos[0] + 1, self.cur_pos[1])
        elif direction == Direction.W:
            new_pos = (self.cur_pos[0], self.cur_pos[1] - 1)
        else:
            new_pos = self.cur_pos

        if not self.hits_border(new_pos) and not self.height_boundary(new_pos):
            self.prev_pos.append(self.cur_pos)
            self.cur_pos = new_pos

    def get_new_pos(self, pos):
        new_pos = []
        new_pos.append((pos[0] - 1, pos[1]))
        new_pos.append((pos[0], pos[1] + 1))
        new_pos.append((pos[0] + 1, pos[1]))
        new_pos.append((pos[0], pos[1] - 1))
        return new_pos


    def decide_direction(self):
        new_pos = self.get_new_pos(self.cur_pos)
        DIR_COUNT = 4
        max_score = -10000
        for i in range(len(new_pos)):
            if self.hits_border(new_pos[i]) or self.height_boundary(new_pos[i]):
                continue
            score = self.U[new_pos[i][0]][new_pos[i][1]]
            if max_score < score:
                max_score = score
                max_idx = i

        return max_idx


    def print_map(self):
        s = ""
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                pos = (i, j)
                if self.start == pos:
                    s += "S"
                elif self.goal == pos:
                    s += "G"
                elif pos in self.prev_pos:
                    s += "X"
                else:
                    s += "."
            s += "\n"

        print(s)

    def U_equality(self, U_prime):
        is_equals = True
        for i in range(len(self.U)):
            for j in range(len(self.U[0])):
                if self.U[i][j] != U_prime[i][j]:
                    is_equals = False

        return is_equals

    def update_U(self):
        U_prime = [[self.U[i][j] for j in range(len(self.U[0]))] for i in range(len(self.U))]
        n = 0
        while not self.U_equality(U_prime) or n == 0:
            self.U = [[U_prime[i][j] for j in range(len(U_prime[0]))] for i in range(len(U_prime))]
            for i in range(len(self.U)):
                for j in range(len(self.U[0])):
                    pos = (i, j)
                    if pos == self.goal:
                        continue

                    new_pos = self.get_new_pos(pos)
                    max_score = self.U[pos[0]][pos[1]]
                    for k in range(4):
                        if self.hits_border(new_pos[k]) or self.height_boundary(pos1=new_pos[k], pos2=pos):
                            continue

                        score = self.U[new_pos[k][0]][new_pos[k][1]]
                        if max_score < score:
                            max_score = score

                    if max_score > 0:
                        U_prime[pos[0]][pos[1]] = max_score - 1
                    else:
                        U_prime[pos[0]][pos[1]] = 0


            n += 1
            print(n)

    def get_low_elevations(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 0 and self.U[i][j] > 0:
                    self.low_elevations.append((i, j))

    def set_curr_low_elevation(self, idx):
        if idx > 0 and idx < len(self.low_elevations):
            self.cur_pos = self.low_elevations[idx]

    def __init__(self, lines):

        self.map = []
        self.start = (0, 0)
        self.goal = (0, 0)
        self.cur_pos = self.start
        self.low_elevations = []
        self.prev_pos = []

        for i in range(len(lines)):
            self.map.append([])
            row = lines[i]
            for j in range(len(row)):
                char = row[j]
                if char == "S":
                    self.map[-1].append(0)
                    self.start = (i, j)
                    self.cur_pos = self.start
                elif char == "E":
                    self.map[-1].append(26)
                    self.goal = (i, j)
                elif char == "\n":
                    pass
                else:
                    self.map[-1].append(ord(char) - ord('a'))

        self.U = [[0 for j in range(len(self.map[0]))] for i in range(len(self.map))]
        self.U[self.goal[0]][self.goal[1]] = 10000
        self.update_U()
        self.get_low_elevations()


def aoc12a(name):

    f = open(name)
    lines = f.readlines()
    height_map = HeightMap(lines)
    move_num = 0
    while height_map.cur_pos != height_map.goal:
        i = height_map.decide_direction()
        height_map.move(i)
        move_num += 1

    print(move_num)
    height_map.print_map()


def aoc12b(name):

    f = open(name)
    lines = f.readlines()
    height_map = HeightMap(lines)
    low_elevation_size = len(height_map.low_elevations)
    min_move_num = 10000
    for i in range(low_elevation_size):
        height_map.set_curr_low_elevation(i)
        move_num = 0
        while height_map.cur_pos != height_map.goal:
            i = height_map.decide_direction()
            height_map.move(i)
            move_num += 1

        if min_move_num > move_num:
            min_move_num = move_num

    print(min_move_num)


#aoc12a("input12_test.txt")
#aoc12a("input12.txt")

aoc12b("input12_test.txt")
aoc12b("input12.txt")