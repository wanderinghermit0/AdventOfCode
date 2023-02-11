class Node:
    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.children = {}
        self.parent = None

class Tree:
    CurrentNode = Node("/")
    ParentNode = None
    def add(self, name, size):
        new_node = Node(name, size)
        new_node.parent = self.CurrentNode
        self.CurrentNode.children[name] = new_node

    def search_down(self, name):
        self.ParentNode = self.CurrentNode
        self.CurrentNode = self.CurrentNode.children[name]

    def search_up(self):
        self.CurrentNode = self.ParentNode
        self.ParentNode = self.ParentNode.parent

    def get_root(self):
        while self.ParentNode is not None:
            self.search_up()

    def get_sizes(self):
        total_size = self.CurrentNode.size
        if total_size > 100000 or len(self.CurrentNode.children) == 0:
            total_size = 0
        names = []
        if len(self.CurrentNode.children) > 0:
            names = self.CurrentNode.children.keys()
        for name in names:
            self.search_down(name)
            total_size += self.get_sizes()

        if self.ParentNode is not None:
            self.search_up()

        return total_size

    def get_smallest_directory(self, num, smallest_size, name):
        if self.CurrentNode.size > num and self.CurrentNode.size < smallest_size:
            smallest_size = self.CurrentNode.size
            name = self.CurrentNode.name
        names = []
        if len(self.CurrentNode.children) > 0:
            names = self.CurrentNode.children.keys()
        for name in names:
            self.search_down(name)
            name, smallest_size = self.get_smallest_directory(num, smallest_size, name)
        if self.ParentNode is not None:
            self.search_up()
        return name, smallest_size

    def set_directory_size(self):
        size = 0
        for name in self.CurrentNode.children.keys():
            size += self.CurrentNode.children[name].size
        self.CurrentNode.size += size



f = open("input7.txt")
dir_tree = Tree()
is_ls = False
for line in f:
    if line.startswith("$ cd"):
        command = line.split()
        if command[2] == "/":
            pass
        elif command[2] == "..":
            dir_tree.set_directory_size()
            dir_tree.search_up()
        else:
            dir_tree.search_down(command[2])
    elif line.startswith("$ ls"):
        pass
    else:
        file_data = line.split()
        size = 0
        if file_data[0] != "dir":
            size = int(file_data[0])
        dir_tree.add(file_data[1], size)

#Getting the sizes for the last node
while dir_tree.ParentNode is not None:
    dir_tree.set_directory_size()
    dir_tree.search_up()

#Setting the size for the root node
dir_tree.set_directory_size()

size = dir_tree.get_sizes()
print(size)

total_space = 70000000
update_space = 30000000
needed_space = update_space - (total_space - dir_tree.CurrentNode.size)
name, smallest_size = dir_tree.get_smallest_directory(needed_space, total_space, "/")
print("Name:{}, Size:{}".format(name, smallest_size))
print("Needed Space:{}".format(needed_space))
