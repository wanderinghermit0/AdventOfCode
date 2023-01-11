f = open("input9.txt")
commands = f.readlines()
f.close()

def head_move(head_pos, command, step):
    if command == "U":
        return (head_pos[0], head_pos[1] + step)
    elif command == "D":
        return (head_pos[0], head_pos[1] - step)
    elif command == "R":
        return (head_pos[0] + step, head_pos[1])
    elif command == "L":
        return (head_pos[0] - step, head_pos[1])
    else:
        return head_pos

def is_touching(tail_pos, head_pos):
    vert_dist = abs(tail_pos[0] - head_pos[0])
    hor_dist = abs(tail_pos[1] - head_pos[1])
    return not (vert_dist > 1 or hor_dist > 1)

def tail_move(tail_pos, head_pos):
    diff_pos = (tail_pos[0] - head_pos[0], tail_pos[1] - head_pos[1])

    if diff_pos[0] <= -2 and diff_pos[1] == 0:
        return (tail_pos[0] + 1, tail_pos[1])
    elif diff_pos[0] >= 2 and diff_pos[1] == 0:
        return (tail_pos[0] - 1, tail_pos[1])
    elif diff_pos[0] == 0 and diff_pos[1] <= -2:
        return (tail_pos[0], tail_pos[1] + 1)
    elif diff_pos[0] == 0 and diff_pos[1] >= 2:
        return (tail_pos[0], tail_pos[1] - 1)

    elif diff_pos[0] >= 1 and diff_pos[1] >= 2 or diff_pos[0] >= 2 and diff_pos[1] >= 1:
        return (tail_pos[0] - 1, tail_pos[1] - 1)
    elif diff_pos[0] <= -1 and diff_pos[1] >= 2 or diff_pos[0] <= -2 and diff_pos[1] >= 1:
        return (tail_pos[0] + 1, tail_pos[1] - 1)
    elif diff_pos[0] >= 1 and diff_pos[1] <= -2 or diff_pos[0] >= 2 and diff_pos[1] <= -1:
        return (tail_pos[0] - 1, tail_pos[1] + 1)
    elif diff_pos[0] <= -1 and diff_pos[1] <= -2 or diff_pos[0] <= -2 and diff_pos[1] <= -1:
        return (tail_pos[0] + 1, tail_pos[1] + 1)

    return tail_pos


def aoc9a(commands):
    head_pos = (0, 0)
    tail_pos = (0, 0)
    head_arr = [head_pos]
    tail_arr = [tail_pos]
    tail_all_pos = [tail_pos]
    for command in commands:
        command = command.split()
        head_pos = head_move(head_pos, command[0], int(command[1]))
        head_arr.append(head_pos)

        while not is_touching(tail_pos, head_pos):
            tail_pos = tail_move(tail_pos, head_pos)
            tail_all_pos.append(tail_pos)
        tail_arr.append([tail_pos])

    tail_arr[0] = [tail_arr[0]]
    return head_arr, tail_arr, tail_all_pos


def aoc9b(commands):
    rope_len = 9
    head_pos = (0, 0)
    knot_pos = (0, 0)
    head_arr = [head_pos]
    rope_arr = [[knot_pos]*rope_len]
    tail_all_pos = [knot_pos]
    for i, command in enumerate(commands):
        command = command.split()
        head_pos = head_move(head_pos, command[0], int(command[1]))
        head_arr.append(head_pos)
        old_knot_arr = rope_arr[-1]
        new_knot_arr = old_knot_arr.copy()
        knot_prev = head_pos
        for j in range(rope_len):
            while not is_touching(new_knot_arr[j], knot_prev):
                new_knot_arr[j] = tail_move(new_knot_arr[j], knot_prev)
                if j == rope_len - 1:
                    tail_all_pos.append(new_knot_arr[j])

            knot_prev = new_knot_arr[j]
        rope_arr.append(new_knot_arr)

    return head_arr, rope_arr, tail_all_pos


class Rope:
    def _get_positions(self):
        center = (self.dim[0] // 2, self.dim[1] // 2)
        for i in range(len(self.head_arr)):
            self.head_arr[i] = (-self.head_arr[i][1] + center[1], self.head_arr[i][0] + center[0])
            for j in range(self.rope_len):
                self.rope_arr[i][j] = (-self.rope_arr[i][j][1] + center[1], self.rope_arr[i][j][0] + center[0])

    def __init__(self, head_arr, rope_arr, dim, commands):
        self.head_arr = head_arr
        self.rope_arr = rope_arr
        self.dim = dim
        self.rope_len = len(self.rope_arr[0])
        self.commands = commands
        self._get_positions()

    def _print_map(self, head_pos, knot_arr):
        s = ""
        for i in range(dim[0]):
            for j in range(dim[1]):
                has_symbol = False
                if head_pos[0] == i and head_pos[1] == j:
                    s += "H"
                    has_symbol = True
                for k in range(len(knot_arr)):
                    if knot_arr[k][0] == i and knot_arr[k][1] == j and not has_symbol:
                        s += str(k + 1)
                        has_symbol = True
                        break
                if not has_symbol:
                    s += "."
            s += "\n"
        s += "\n"
        return s

    def print_hist(self, output_file):
        fw = open(output_file, "w")
        for i in range(len(self.head_arr)):
            fw.write(self._print_map(self.head_arr[i], self.rope_arr[i]))
            if i < len(self.head_arr) - 1:
                fw.write(self.commands[i])
            fw.write("")
        fw.close()


#Part 1
head_arr, tail_arr, tail_all_pos = aoc9a(commands)
tail_set = set(tail_all_pos)
print(len(tail_set))

fr = open("input9a_test.txt", "r")
commands_test = fr.readlines()
fr.close()

#Test 1
dim = (15, 15)
head_arr_test, tail_arr_test, tail_all_pos = aoc9a(commands_test)
rope_9a = Rope(head_arr_test, tail_arr_test, dim, commands_test)
rope_9a.print_hist("aoc9a-rope_map.txt")

#Part 2
_, _, tail_all_pos = aoc9b(commands)
tail_set = set(tail_all_pos)
print(len(tail_set))

#Test 1
head_arr_test, rope_arr_test, _ = aoc9b(commands_test)
rope_9b = Rope(head_arr_test, rope_arr_test, dim, commands_test)
rope_9b.print_hist("aoc9b-rope_map.txt")

#Test 2
fr = open("input9b_test.txt")
commands_test = fr.readlines()
fr.close()

head_arr_test, rope_arr_test, tail_all_pos = aoc9b(commands_test)
tail_set = set(tail_all_pos)
print(len(tail_set))

dim = (30, 30)
rope_9b2 = Rope(head_arr_test, rope_arr_test, dim, commands_test)
rope_9b2.print_hist("aoc9b2-rope_map.txt")