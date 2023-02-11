class CircleList:

    def __init__(self, arr: list):
        self.arr = arr.copy()
        self.size = len(arr)

    def get_item(self, idx):
        return self.arr[(idx % self.size)]

    def move(self, num):
        idx = self.arr.index(num)
        self.arr.remove(num)
        new_idx = (idx + num) % self.size

        self.arr.insert(new_idx, num)

    def find_zero(self):
        return self.arr.index(0)

def aoc20(name):
    f = open(name)
    encrypted_file = []
    for line in f:
        encrypted_file.append(int(line))
    f.close()

    circle_list = CircleList(encrypted_file)
    for num in encrypted_file:
        circle_list.move(num)

    zero_idx = circle_list.find_zero()
    grove_coordinates = [0]*3
    grove_coordinates[0] = circle_list.get_item(zero_idx + 1000)
    grove_coordinates[1] = circle_list.get_item(zero_idx + 2000)
    grove_coordinates[2] = circle_list.get_item(zero_idx + 3000)

    print(sum(grove_coordinates))


aoc20("input20_test.txt")
aoc20("input20.txt")