import sys

player_1_position = int(sys.stdin.readline().rsplit(':')[1]) -1
player_2_position = int(sys.stdin.readline().rsplit(':')[1]) -1

player_1_score = 0
player_2_score = 0

dice = 0
rolls_per_turn = 3
board_size = 10
dice_size = 100
max_score = 1000
rolls = 0

while player_1_score < max_score and player_2_score < max_score:
    for _ in range(rolls_per_turn):
        player_1_position = (player_1_position + dice + 1) % board_size
        dice = (dice + 1) % dice_size
        rolls += 1

    player_1_score += (1 + player_1_position)

    if player_1_score >= max_score:
        break

    for _ in range(rolls_per_turn):
        player_2_position = (player_2_position + dice + 1) % board_size
        dice = (dice + 1) % dice_size
        rolls += 1

    player_2_score += (1 + player_2_position)


print(rolls * min(player_1_score, player_2_score))
