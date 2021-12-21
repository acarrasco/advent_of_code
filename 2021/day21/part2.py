import sys
from collections import Counter, defaultdict
import itertools
from pprint import pprint

rolls_per_turn = 3
board_size = 10
dice_size = 3
max_score = 21

roll_histogram = Counter(sum(rolls) for rolls in itertools.product(*[range(1, dice_size+1)]*rolls_per_turn))

def simulate_one_turn(turn, states_frequencies):
    next_turn = turn + 1
    for (position, score) in itertools.product(range(board_size), range(max_score)):
        prev_freq = states_frequencies.get((turn, position, score))
        if prev_freq:
            for roll_value, roll_freq in roll_histogram.items():
                next_position = (position+roll_value) % board_size
                next_score = score + 1 + next_position
                next_state = next_turn, next_position, next_score
                states_frequencies[next_state] += roll_freq * prev_freq


def simulate(starting_pos):
    states_frequencies = defaultdict(int)
    states_frequencies[0, starting_pos, 0] = 1
    for turn in range(max_score):
        simulate_one_turn(turn, states_frequencies)
    return states_frequencies


player_1_starting_pos = int(sys.stdin.readline().rsplit(':')[1]) -1
player_2_starting_pos = int(sys.stdin.readline().rsplit(':')[1]) -1

player_1_state_frequencies = simulate((player_1_starting_pos - 1) % board_size)
player_2_state_frequencies = simulate((player_2_starting_pos - 1) % board_size)

p1_wins = 0
p2_wins = 0

for (p1_turn, _, p1_score), p1_freq in player_1_state_frequencies.items():
    for (p2_turn, _, p2_score), p2_freq in player_2_state_frequencies.items():
        if p1_turn == p2_turn + 1:
            if p1_score >= max_score and p2_score < max_score:
                p1_wins += p1_freq * p2_freq
        elif p2_turn == p1_turn:
            if p2_score >= max_score and p1_score < max_score:
                p2_wins += p1_freq * p2_freq

print(max(p1_wins, p2_wins))