from ast import match_case
from collections import Counter
import sys

def card_value(card):
    match card:
        case 'T': return 10
        case 'J': return 1
        case 'Q': return 12
        case 'K': return 13
        case 'A': return 14
        case _: return int(card)

def apply_jokers(hand):
    if 'J' not in hand:
        return hand
    
    counts = Counter(card for card in hand if card != 'J')
    if len(counts) == 0:
        return 'AAAAA'
    [(most_common_card, _)] = counts.most_common(1)
    return hand.replace('J', most_common_card)


def hand_sorting_key(hand_bet):
    hand, _ = hand_bet
    hand_with_jokers_applied = apply_jokers(hand)
    counts = sorted(Counter(hand_with_jokers_applied).values())
    match counts:
        case [5]: return 7, tuple(card_value(card) for card in hand)
        case [1, 4]: return 6, tuple(card_value(card) for card in hand)
        case [2, 3]: return 5, tuple(card_value(card) for card in hand)
        case [1, 1, 3]: return 4, tuple(card_value(card) for card in hand)
        case [1, 2, 2]: return 3, tuple(card_value(card) for card in hand)
        case [1, 1, 1, 2]: return 2, tuple(card_value(card) for card in hand)
        case [1, 1, 1, 1, 1]: return 1, tuple(card_value(card) for card in hand)
    raise ValueError(f'Invalid hand: {hand} {counts}')
    
def parse_line(line):
    hand, bet = line.split()
    bet = int(bet)
    return hand, bet

def solve(hands_and_bets):
    sorted_hands = sorted(hands_and_bets, key=hand_sorting_key)
    winnings = 0
    for rank, (hand, bet) in enumerate(sorted_hands):
        winnings += (rank + 1) * bet
    return winnings

problem = list(map(parse_line, sys.stdin))
print(solve(problem))