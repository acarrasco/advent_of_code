import sys
from collections import namedtuple
from typing import List

Draw = namedtuple('Draw', 'red green blue'.split())
Game = namedtuple('Game', 'id draws'.split())

def parse_color(color) -> (str, int):
    """
    >>> parse_color('8 green')
    ('green', 8)
    >>> parse_color('6 blue')
    ('blue', 6)
    >>> parse_color('20 red')
    ('red', 20)
    """
    tokens = color.strip().split()
    return tokens[1], int(tokens[0])

def parse_draws(line) -> List[Draw]:
    """
    >>> parse_draw('8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red')
    [Draw(red=20, green=8, blue=6), Draw(red=4, green=13, blue=5), Draw(red=1, green=5, blue=0)]
    """
    draws = []
    for draw in line.split(';'):
        colors = dict(map(parse_color, draw.split(',')))
        draws.append(Draw(red=colors.get('red', 0), green=colors.get('green', 0), blue=colors.get('blue', 0)))
    return draws

def parse_game(line) -> Game:
    """
    >>> parse_game('Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green')
    Game(id=1, draws=[Draw(red=4, green=0, blue=3), Draw(red=1, green=2, blue=6), Draw(red=0, green=2, blue=0)]
    """
    id_part, draws_part = line.split(':')
    game_id = int(id_part.split()[1])
    
    draws = parse_draws(draws_part)
    return Game(game_id, draws)

def find_minimal_valid_set(game: Game) -> Draw:
    """
    >>> find_minimal_set(Game(1, [Draw(red=4, green=0, blue=3), Draw(red=1, green=2, blue=6), Draw(red=0, green=2, blue=0)]))
    Draw(red=4, green=2, blue=6)
    """
    max_red = max(d.red for d in game.draws)
    max_green = max(d.green for d in game.draws)
    max_blue = max(d.blue for d in game.draws)
    return Draw(red=max_red, green=max_green, blue=max_blue)

def draw_power(draw: Draw) -> int:
    return draw.red * draw.green * draw.blue

def main():
    games = [parse_game(line) for line in sys.stdin]
    games_minimum_set = map(find_minimal_valid_set, games)
    set_powers = map(draw_power, games_minimum_set)
    sum_of_set_powers = sum(set_powers)
    print(sum_of_set_powers)

if __name__ == '__main__':
    main()