from collections import namedtuple
import itertools
import pprint

Stats = namedtuple('Stats', ['attack', 'defence', 'hitpoints'])

class Item(namedtuple('Item', ['name', 'cost', 'damage', 'armor'])):
    def __add__(self, x):
        if x in (0, dummy):
            return self
        elif self == dummy:
            return x
        return Item(
            self.name + '+' + x.name,
            self.cost + x.cost,
            self.damage + x.damage,
            self.armor + x.armor
        )

dummy = Item('Dummy', 0, 0, 0)

weapons = [
    Item('Dagger',        8,     4,       0),
    Item('Shortsword',   10,     5,       0),
    Item('Warhammer',    25,     6,       0),
    Item('Longsword',    40,     7,       0),
    Item('Greataxe',     74,     8,       0),
]
armor = [
    Item('Leather',      13,     0,       1),
    Item('Chainmail',    31,     0,       2),
    Item('Splintmail',   53,     0,       3),
    Item('Bandedmail',   75,     0,       4),
    Item('Platemail',   102,     0,       5),
]
rings = [
    Item('Damage +1',    25,     1,       0),
    Item('Damage +2',    50,     2,       0),
    Item('Damage +3',   100,     3,       0),
    Item('defence +1',   20,     0,       1),
    Item('defence +2',   40,     0,       2),
    Item('defence +3',   80,     0,       3),
]

def generate_loadouts():
    for weapon in weapons:
        yield (weapon,)
        for armor_piece in armor + [dummy]:
            for ring_combination in itertools.combinations(rings, 2):
                yield (weapon, armor_piece) + ring_combination
            for ring in rings + [dummy]:
                yield (weapon, armor_piece, ring)

def aggregate_loadout(loadout):
    return sum(loadout, start=dummy)

# returns true if the player wins
def simulate_fight(player_stats, enemy_stats):
    fighters = (
        player_stats._asdict(),
        enemy_stats._asdict()
    )    
    turn = 0
    while fighters[turn % 2]['hitpoints'] > 0:
        attacker = fighters[turn % 2]
        turn += 1
        defender = fighters[turn % 2]
        damage = max(1, attacker['attack'] - defender['defence'])
        defender['hitpoints'] -= damage

    return turn % 2 == 1

def loses_cost():
    for loadout in generate_loadouts():
        aggregated = aggregate_loadout(loadout)
        player_stats = Stats(aggregated.damage, aggregated.armor, 100)
        enemy_stats = Stats(9, 2, 103)
        if not simulate_fight(player_stats, enemy_stats):
            yield aggregated.cost

print(max(loses_cost()))

