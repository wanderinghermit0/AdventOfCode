def aoc10a(commands):
    clock_time = 0
    register = 1
    cycles = [20, 60, 100, 140, 180, 220]
    cycle_idx = 0
    signal_strength = 0
    for command in commands:
        command = command.split()
        if command[0] == "addx":
            clock_time += 2
        else:
            clock_time += 1
        if clock_time >= cycles[cycle_idx]:
            signal_strength += cycles[cycle_idx] * register
            cycle_idx += 1
        if command[0] == "addx":
            register += int(command[1])
        if cycle_idx >= len(cycles):
            break

    print(signal_strength)


def place_pixel(message_arr, clock_time, sprite_pos):
    cycle_len = len(message_arr[0])
    col = clock_time % cycle_len
    row = clock_time // cycle_len

    for i in range(cycle_len):
        diff = abs(sprite_pos - col)
        if diff <= 1:
            message_arr[row][col] = "*"
            break
        else:
            message_arr[row][col] = " "
            break

def print_message(message_arr):
    s = ""
    for i in range(len(message_arr)):
        for j in range(len(message_arr[i])):
            s += message_arr[i][j]
        s += "\n"
    s += "\n"

    print(s)

def aoc10b(commands):
    cycles = [40, 80, 120, 160, 200, 240]
    clock_time = 0
    is_adding = False
    sprite_pos = 1
    command_idx = 0
    message_arr = [[" " for _ in range(cycles[0])] for _ in range(len(cycles))]
    value = 0
    for i in range(cycles[-1]):
        place_pixel(message_arr, clock_time, sprite_pos)
        if not is_adding:
            command = commands[command_idx].split()
            command_idx += 1
            if command[0] == "addx":
                is_adding = True
                value = int(command[1])
        else:
            is_adding = False
            sprite_pos += value
        clock_time += 1

    print_message(message_arr)


#Part 1
f = open("input10_test.txt")
commands = f.readlines()
f.close()
aoc10a(commands)

f = open("input10.txt")
commands = f.readlines()
f.close()
aoc10a(commands)

#Part 2
f = open("input10_test.txt")
commands = f.readlines()
f.close()
aoc10b(commands)

f = open("input10.txt")
commands = f.readlines()
f.close()
aoc10b(commands)