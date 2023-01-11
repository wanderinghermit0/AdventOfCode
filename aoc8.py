import numpy as np
import enum

def build_tree(f):
    tree_map = []
    for i, line in enumerate(f):
        tree_map.append([])
        for num in line:
            if num.isnumeric():
                tree_map[i].append(int(num))
    tree_map = np.array(tree_map)

    return tree_map


def aoc8a(tree_map):
    visible_count = 0
    for i in range(tree_map.shape[0]):
        for j in range(tree_map.shape[1]):
            is_visible = False
            if j > 0 and np.max(tree_map[i, :j]) < tree_map[i, j]:
                is_visible = True
            if j < tree_map.shape[1] - 1 and np.max(tree_map[i, j + 1:]) < tree_map[i, j]:
                is_visible = True
            if i > 0 and np.max(tree_map[:i, j]) < tree_map[i, j]:
                is_visible = True
            if i < tree_map.shape[0] - 1 and np.max(tree_map[i + 1:, j]) < tree_map[i, j]:
                is_visible = True
            if j == 0 or i == 0 or j == tree_map.shape[1] - 1 or i == tree_map.shape[0] - 1:
                is_visible = True
            if is_visible:
                visible_count += 1

    print(visible_count)

Directions = enum.Enum("Directions", ["N", "E", "S", "W"])


def hits_border(tree_dim, pos):

    in_border = not(0 <= pos[0] <= tree_dim[0] - 1) or not(0 <= pos[1] <= tree_dim[1] - 1)
    return in_border


def viewable_trees(tree_map, start_pos, direction):
    score = 0
    max_height = tree_map[start_pos[0], start_pos[1]]
    curr_height = -1
    tree_dim = (len(tree_map), len(tree_map[0]))
    pos = (start_pos[0], start_pos[1])
    while curr_height < max_height and not hits_border(tree_dim, pos):
        if direction.value == Directions.N.value:
            pos = (pos[0] - 1, pos[1])
        elif direction.value == Directions.E.value:
            pos = (pos[0], pos[1] + 1)
        elif direction.value == Directions.S.value:
            pos = (pos[0] + 1, pos[1])
        elif direction.value == Directions.W.value:
            pos = (pos[0], pos[1] - 1)
        else:
            return score

        if not hits_border(tree_dim, pos):
            curr_height = tree_map[pos[0], pos[1]]
            score += 1

    return score

def aoc8b(tree_map):
    max_scenic_score = -1
    for i in range(tree_map.shape[0]):
        for j in range(tree_map.shape[1]):
            scenic_score = 1
            scenic_score *= viewable_trees(tree_map, (i, j), Directions.N)
            scenic_score *= viewable_trees(tree_map, (i, j), Directions.E)
            scenic_score *= viewable_trees(tree_map, (i, j), Directions.S)
            scenic_score *= viewable_trees(tree_map, (i, j), Directions.W)
            max_scenic_score = max(max_scenic_score, scenic_score)
    print(max_scenic_score)


f = open("input8.txt")
tree_map = build_tree(f)
f.close()
aoc8a(tree_map)

f = open("input8_test.txt")
tree_map = build_tree(f)
f.close()
aoc8b(tree_map)

f = open("input8.txt")
tree_map = build_tree(f)
f.close()
aoc8b(tree_map)