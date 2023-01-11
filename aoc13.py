import timeit
import time
import copy

def create_packet(line, packet):
    num_str = ""
    i = 0
    while i < len(line):
        char = line[i]
        if char == "[":
            term, incr, num_str = create_packet(line[i+1:], [])
            i += incr
            packet.append(term)
        elif char.isnumeric():
            num_str += char
        elif char == ",":
            if line[i - 1].isnumeric():
                num = int(num_str)
                packet.append(num)
            num_str = ""
        elif char == "]":
            if line[i - 1].isnumeric():
                num = int(num_str)
                packet.append(num)
            num_str = ""

            return packet, i + 1, num_str
        else:
            return packet[0], i + 1, num_str

        i += 1

class Log:
    def __init__(self):
        self.f = open("aoc13_log.txt", "w")
        self.indent = ""
        self.item = 0

    def close_log(self):
        self.f.close()

    def compare_intro(self, left_value, right_value):
        self.f.write(self.indent)
        self.f.write("Compare {} vs {}\n".format(left_value, right_value))

    def left_greater(self):
        self.f.write(self.indent)
        self.f.write("Right side is smaller, so inputs are not in the right order\n")

    def right_greater(self):
        self.f.write(self.indent)
        self.f.write("Left side is smaller, so inputs are in the right order\n")

    def left_no_items(self):
        self.f.write(self.indent)
        self.f.write("Left side ran out of items, so inputs are in the right order\n")

    def right_no_items(self):
        self.f.write(self.indent)
        self.f.write("Right side ran out of items, so inputs are not in the right order\n")

    def level_up(self):
        self.indent += "    "

    def level_down(self):
        if len(self.indent) > 0:
            self.indent = self.indent[4:]

    def next_item(self):
        self.indent = ""
        self.f.write("\n\nItem {}\n".format(self.item))
        self.item += 1

def compare_packet(compare_term):
    i = 0
    right_order = -1

    while i < len(compare_term[0]) and right_order:
        if i > len(compare_term[1]) - 1:
            return 0

        left_value = compare_term[0][i]
        right_value = compare_term[1][i]

        if isinstance(left_value, list) and isinstance(right_value, list):
            right_order = compare_packet([left_value, right_value])
        elif isinstance(left_value, int) and isinstance(right_value, int):
            if right_value - left_value < 0:
                return 0
            elif right_value - left_value > 0:
                return 1
        elif isinstance(left_value, list) and isinstance(right_value, int):
            right_value = [right_value]
            right_order = compare_packet([left_value, right_value])
        elif isinstance(left_value, int) and isinstance(right_value, list):
            left_value = [left_value]
            right_order = compare_packet([left_value, right_value])

        if right_order != -1:
            return right_order

        i += 1

    if len(compare_term[0]) < len(compare_term[1]):
        return 1

    return right_order

def create_packets(name):
    f = open(name)
    compare_arr = []
    for i, line in enumerate(f):
        if i % 3 == 0:
            compare_term = [[], []]
            compare_arr.append(compare_term)
            create_packet(line, compare_arr[-1][0])
            compare_arr[-1][0] = compare_arr[-1][0][0]
        elif i % 3 == 1:
            create_packet(line, compare_arr[-1][-1])
            compare_arr[-1][-1] = compare_arr[-1][-1][0]
    f.close()
    return compare_arr

def aoc13a(compare_arr):
    sum = 0
    log = Log()
    for i in range(len(compare_arr)):
        log.next_item()
        log.compare_intro(compare_arr[i][0], compare_arr[i][1])
        if compare_packet(compare_arr[i]) == 1:
            sum += (i + 1)
    print(sum)
    log.close_log()

def bubble_sort(packets):
    is_sorted = False
    j = 1
    while not is_sorted:
        is_sorted = True
        for i in range(len(packets) - j):
            if compare_packet([packets[i], packets[i + 1]]) == 0:
                temp = packets[i]
                packets[i] = packets[i + 1]
                packets[i + 1] = temp
                is_sorted = False
        j += 1


def insertion_sort(packets):
    for i in range(1, len(packets)):
        j = i
        while compare_packet([packets[j - 1], packets[j]]) == 0 and j > 0:
            temp = packets[j]
            packets[j] = packets[j - 1]
            packets[j - 1] = temp
            j -= 1


def merge(packets, left, middle, end):
    left_arr = packets[left:middle + 1]
    right_arr = packets[middle + 1:end + 1]
    left_idx = 0
    right_idx = 0
    packet_idx = 0
    while left_idx < len(left_arr) and right_idx < len(right_arr):
        if compare_packet([left_arr[left_idx], right_arr[right_idx]]) == 1:
            packets[left + packet_idx] = left_arr[left_idx]
            left_idx += 1
        else:
            packets[left + packet_idx] = right_arr[right_idx]
            right_idx += 1

        packet_idx += 1
    while left_idx < len(left_arr):
        packets[left + packet_idx] = left_arr[left_idx]
        left_idx += 1
        packet_idx += 1
    while right_idx < len(right_arr):
        packets[left + packet_idx] = right_arr[right_idx]
        right_idx += 1
        packet_idx += 1

def merge_sort(packets, start, end):
    middle = start + (end - start) // 2

    if end <= start:
        return

    merge_sort(packets, start, middle)
    merge_sort(packets, middle + 1, end)

    merge(packets, start, middle, end)


def aoc13b(compare_arr):
    packets = []
    for i in range(len(compare_arr)):
        packets.append(compare_arr[i][0])
        packets.append(compare_arr[i][1])
    packets.append([[2]])
    packets.append([[6]])

    packets_sorted = copy.deepcopy(packets)
    before = time.time()
    merge_sort(packets_sorted, 0, len(packets))
    after = time.time()
    
    print("Time {:0.5f}".format(after - before))

    divider = []
    divider.append(packets.index([[2]]) + 1)
    divider.append(packets.index([[6]]) + 1)

    print(divider[0]*divider[1])


compare_arr_test = create_packets("input13_test.txt")
#aoc13a(compare_arr_test)
#aoc13b(compare_arr_test)

compare_arr = create_packets("input13.txt")
#aoc13a(compare_arr)
#aoc13b(compare_arr)


packets = []
for i in range(len(compare_arr)):
    packets.append(compare_arr[i][0])
    packets.append(compare_arr[i][1])
packets.append([[2]])
packets.append([[6]])

print(timeit.timeit("bubble_sort(packets)", globals=globals(), number=10000))

print(timeit.timeit("insertion_sort(packets)", globals=globals(), number=10000))

packets_sorted = copy.deepcopy(packets)
print(timeit.timeit("merge_sort(packets, 0, len(packets))", globals=globals(), number=10000))


divider = []
divider.append(packets.index([[2]]) + 1)
divider.append(packets.index([[6]]) + 1)

print(divider[0] * divider[1])