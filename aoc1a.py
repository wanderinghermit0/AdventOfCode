fh = open("input1a.txt")
calories = [0]

for x in fh:
    try:
        term = int(x)
        calories[-1] += term
    except:
        calories.append(0)

fh.close()
print(max(calories))

max_calories = []
for i in range(3):
    max_calories.append(max(calories))
    calories.remove(max(calories))

print(sum(max_calories))

