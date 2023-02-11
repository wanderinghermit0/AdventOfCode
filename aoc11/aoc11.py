import re

class Monkey:
    def __init__(self, lines):
        self.items = re.findall("[0-9]+", lines[1])
        self.items = [int(self.items[i]) for i in range(len(self.items))]
        self.operation = re.search("[*+]", lines[2]).group()

        if len(re.findall("old", lines[2])) == 2:
            self.oper_value = -1
        else:
            self.oper_value = int(re.search("[0-9]+", lines[2]).group())

        self.divisor = int(re.search("[0-9]+", lines[3]).group())

        self.neighbors = [0]*2
        self.neighbors[0] = int(re.search("[0-9]+", lines[4]).group())
        self.neighbors[1] = int(re.search("[0-9]+", lines[5]).group())
        self.inspections = 0

    def has_items(self):
        return len(self.items) > 0

    def play(self):
        if self.has_items():
            if self.oper_value == -1:
                term = self.items[0]
            else:
                term = self.oper_value
            if self.operation == "*":
                self.items[0] *= term
            else:
                self.items[0] += term

            self.inspections += 1

    def get_bored(self):
        self.items[0] //= 3

    def throw(self):
        if self.has_items():
            item = self.items.pop(0)
            if item % self.divisor == 0:
                new_monkey = self.neighbors[0]
            else:
                new_monkey = self.neighbors[1]

            return item, new_monkey
        else:
            return None, None

    def catch(self, item):
        self.items.append(item)


def aoc11a(lines):
    monkey_rows = 7
    monkeys = []
    for i in range(len(lines) // monkey_rows + 1):
        new_monkey = Monkey(lines[7 * i:7 * (i + 1) - 1])
        monkeys.append(new_monkey)

    rounds = 20
    for i in range(rounds):
        for j in range(len(monkeys)):

            while monkeys[j].has_items():
                monkeys[j].play()
                monkeys[j].get_bored()
                item, monkey_idx = monkeys[j].throw()
                monkeys[monkey_idx].catch(item)

    inspections = []
    for i in range(len(monkeys)):
        inspections.append(monkeys[i].inspections)
    inspections.sort(reverse=True)
    monkey_business = inspections[0] * inspections[1]
    print(monkey_business)


def get_relief(item, monkeys):
    factor = 1
    for i in range(len(monkeys)):
        factor *= monkeys[i].divisor

    return item % factor

def aoc11b(lines, verbose=0):
    monkey_rows = 7
    monkeys = []
    for i in range(len(lines) // monkey_rows + 1):
        new_monkey = Monkey(lines[7 * i:7 * (i + 1) - 1])
        monkeys.append(new_monkey)

    rounds = 10000
    for i in range(rounds):
        for j in range(len(monkeys)):

            while monkeys[j].has_items():
                monkeys[j].play()
                item, monkey_idx = monkeys[j].throw()
                item = get_relief(item, monkeys)
                monkeys[monkey_idx].catch(item)

        if (i + 1) % 1000 == 0 and verbose > 0:
            print("Round: {}".format(i + 1))
            for i in range(len(monkeys)):
                print("Monkey {0} inspected {1} times".format(i, monkeys[i].inspections))
            print("\n")

    inspections = []
    for i in range(len(monkeys)):
        inspections.append(monkeys[i].inspections)
    inspections.sort(reverse=True)
    monkey_business = inspections[0] * inspections[1]
    print(monkey_business)


f = open("input11_test.txt")
lines = f.readlines()
f.close()
aoc11a(lines)

f = open("input11.txt")
lines = f.readlines()
f.close()
aoc11a(lines)

f = open("input11_test.txt")
lines = f.readlines()
f.close()
aoc11b(lines)

f = open("input11.txt")
lines = f.readlines()
f.close()
aoc11b(lines)


