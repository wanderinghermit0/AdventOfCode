#The letter score is as follows
#For a-z: 1-26
#For A-Z: 27-52
def letter_to_score(letter):
    score = 0
    if str.islower(letter):
        score = ord(letter) - ord('a') + 1
    elif str.isupper(letter):
        score = ord(letter) - ord('A') + 26 + 1

    return score

f = open("input3.txt")

#Part 1
total_score = 0
for line in f:
    #Getting letter for each half of the string
    first_half = line[:len(line)//2]
    second_half = line[len(line)//2:]

    #Trying to find if letters in the second half exist in the first half
    for letter in second_half:
        if letter in first_half:
            score = letter_to_score(letter)
            total_score += score
            break

print(total_score)

#Part 2
total_score = 0
f.seek(0)
line_count = 0
lines = [0]*3
for line in f:
    #Get three consecutive lines
    lines[line_count] = line
    line_count = (line_count + 1) % 3
    if line_count % 3 == 0:
        #Try to see if letter is present in all three lines
        for letter in lines[0]:
            if letter in lines[1] and letter in lines[2]:
                score = letter_to_score(letter)
                total_score += score
                break

print(total_score)
f.close()