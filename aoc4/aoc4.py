f = open("input4.txt")

pairs = []
#Retrieving the data from the file
#Each line is formatted like this 1-3,4-4, providing a pair of ranges
for line in f:
    assignments = line.split(",")
    assignment_num = [[]]*2
    #Each range are inclusive
    for i in range(2):
        assignment_num[i] = assignments[i].split("-")
        assignment_num[i] = list(range(int(assignment_num[i][0]), int(assignment_num[i][1]) + 1))

    pairs.append(assignment_num)
f.close()

#Part 1
contained_sum = 0
for pair in pairs:
    #Need to see if each range in the pair is overlapping each other
    for i in range(2):
        contain_list = []
        #Gather which assignments are contained
        for assignment in pair[i]:
            if assignment in pair[(i + 1) % 2]:
                contain_list.append(assignment)
        #If the list that is contained consists of the entirity of the range
        if len(contain_list) == len(pair[i]):
            contained_sum += 1
            break
print(contained_sum)

#Part 2
overlap_sum = 0
for pair in pairs:
    contain_list = []
    #Need to find only find one assignment to demonstrate overlap
    for assignment in pair[0]:
        if assignment in pair[1]:
            overlap_sum += 1
            break
print(overlap_sum)