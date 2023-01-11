f = open("input5.txt")

second_half_start = -1
lines = f.readlines()
i = 0
boxes = []
while lines[i][1] != "1":
    j = 0
    letter_pos = 1
    while letter_pos < len(lines[i]):
        if len(boxes) < j + 1:
            boxes.append([])
        if len(lines[i][letter_pos].strip()) > 0:
            boxes[j].append(lines[i][letter_pos])
        letter_pos += 4
        j += 1
    i += 1

second_half_start = i + 1

amount_arr = []
prev_arr = []
next_arr = []
for i in range(second_half_start + 1, len(lines)):
    action = lines[i].split()
    amount_arr.append(int(action[1]))
    prev_arr.append(int(action[3]) - 1)
    next_arr.append(int(action[5]) - 1)
f.close()

def print_message(boxes):
    message = ""
    for box in boxes:
        if len(box) > 0:
            message += box[0]
    print(message)

def copy_boxes(boxes):
    boxes_copy = []
    for i in range(len(boxes)):
        boxes_copy.append([])
        for j in range(len(boxes[i])):
            boxes_copy[i].append(boxes[i][j])

    return boxes_copy


#Part 1
boxes_first = copy_boxes(boxes)
for i in range(len(amount_arr)):
    for _ in range(amount_arr[i]):
        #Boxes can be treated as stacks
        letter = boxes_first[prev_arr[i]].pop(0)
        boxes_first[next_arr[i]].insert(0, letter)

print_message(boxes_first)


#Part 2
boxes_second = copy_boxes(boxes)
for i in range(len(amount_arr)):
    #Index needs to be constant as elements are being popped
    for j in range(amount_arr[i] - 1, -1, -1):
        letter = boxes_second[prev_arr[i]].pop(j)
        boxes_second[next_arr[i]].insert(0, letter)

print_message(boxes_second)