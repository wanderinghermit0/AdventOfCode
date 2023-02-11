f = open("input2a.txt")
actions_num = []

for line in f:
    action_letter = str.split(line, " ")
    action_letter[1] = str.strip(action_letter[1])
    action_num = [0]*2

    #Transforming letters to numbers
    #First number is the opponent's action, second number is the player's action
    action_num[0] = ord(action_letter[0]) - ord('A')
    action_num[1] = ord(action_letter[1]) - ord('X')
    actions_num.append(action_num)

f.close()

score1 = 0
score2 = 0
for action_num in actions_num:
    # Part 1
    #First part of the score is the action being taken (1 - rock, 2 - paper, 3 - scissors
    round_score = action_num[1] + 1
    #Second part of the score is the outcome (0 - loss, 3 - tie, 6 - win)
    #A win is alway 1 ahead modulo 3, need to convert it to 2 ahead
    round_score += 3 * ((action_num[1] - action_num[0] + 1) % 3)
    score1 += round_score

    # Part 2
    #The offset of the play is given by the outcome of the event, subtracted by one
    outcome_offset = (action_num[1] - 1) % 3
    response = (action_num[0] + outcome_offset) % 3
    round_score = (response + 1) + action_num[1]*3
    score2 += round_score

print(score1)
print(score2)