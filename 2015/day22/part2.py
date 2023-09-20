
from collections import namedtuple, defaultdict

# problem input, hardcoded
BOSS_DAMAGE = 10
BOSS_HP = 71

MIN_MANA_PER_HP_DAMAGE = 9 # this is for the best case scenario heuristic, with poison spell

inf = float('inf')

Effect = namedtuple('Effect', ['name', 'duration', 'execute', 'end'])

State = namedtuple('State', ['player_hp', 'boss_hp', 'player_armor', 'player_mana', 'spent_mana', 'active_effects'])

Turn = namedtuple('Turn', ['turn', 'state'])

Spell = namedtuple('Spell', ['cast'])



def noop(state):
    return state

def cast_magic_missile(state):
    player_hp, boss_hp, player_armor, player_mana, spent_mana, active_effects = state
    return State(player_hp, boss_hp-4, player_armor, player_mana-53, spent_mana+53, active_effects)

def cast_drain(state):
    player_hp, boss_hp, player_armor, player_mana, spent_mana, active_effects = state
    return State(player_hp+2, boss_hp-2, player_armor, player_mana-73, spent_mana+73, active_effects)

def shield_end(state):
    player_hp, boss_hp, player_armor, player_mana, spent_mana, active_effects = state
    return State(player_hp, boss_hp, player_armor-7, player_mana, spent_mana, active_effects)

def cast_shield(state):
    player_hp, boss_hp, player_armor, player_mana, spent_mana, active_effects = state
    for effect in active_effects:
        if effect.name == 'shield':
            return None
    new_effects = active_effects + (Effect('shield', 6, noop, shield_end),)
    return State(player_hp, boss_hp, player_armor+7, player_mana-113, spent_mana+113, new_effects)

def poison_effect(state):
    player_hp, boss_hp, player_armor, player_mana, spent_mana, active_effects = state
    return State(player_hp, boss_hp-3, player_armor, player_mana, spent_mana, active_effects)

def cast_poison(state):
    player_hp, boss_hp, player_armor, player_mana, spent_mana, active_effects = state
    for effect in active_effects:
        if effect.name == 'poison':
            return None
    new_effects = active_effects + (Effect('poison', 6, poison_effect, noop),)
    return State(player_hp, boss_hp, player_armor, player_mana-173, spent_mana+173, new_effects)

def recharge_effect(state):
    player_hp, boss_hp, player_armor, player_mana, spent_mana, active_effects = state
    return State(player_hp, boss_hp, player_armor, player_mana+101, spent_mana, active_effects)

def cast_recharge(state):
    player_hp, boss_hp, player_armor, player_mana, spent_mana, active_effects = state
    for effect in active_effects:
        if effect.name == 'recharge':
            return None
    new_effects = active_effects + (Effect('recharge', 5, recharge_effect, noop),)
    return State(player_hp, boss_hp, player_armor, player_mana-229, spent_mana+229, new_effects)


player_spells = (
    Spell(cast_magic_missile),
    Spell(cast_drain),
    Spell(cast_shield),
    Spell(cast_poison),
    Spell(cast_recharge),
)

def activate_effects(state):
    next_state = state
    new_effects = []
    for name, duration, execute, end in state.active_effects:
        next_state = execute(next_state)
        if duration == 1:
            next_state = end(next_state)
        else:
            new_effects.append(Effect(name, duration-1, execute, end))
    player_hp, boss_hp, player_armor, player_mana, spent_mana, _ = next_state
    return State(player_hp, boss_hp, player_armor, player_mana, spent_mana, tuple(new_effects))


def next_turn_options(turn):
    n, state = turn
    simulate_turn_function = n % 2 and simulate_player_turn or simulate_boss_turn
    next_valid_states = (s for s in simulate_turn_function(state) if s and s.player_hp > 0 and s.player_mana >= 0)
    for next_state in next_valid_states:
        yield Turn(n+1, next_state)

def simulate_player_turn(state):
    player_hp, boss_hp, player_armor, player_mana, spent_mana, active_effects = state
    if player_hp <= 1:
        return ()
    next_state = activate_effects(State(player_hp-1, boss_hp, player_armor, player_mana, spent_mana, active_effects))
    for spell in player_spells:
        yield spell.cast(next_state)

def simulate_boss_turn(state):
    next_state = activate_effects(state)
    player_hp, boss_hp, player_armor, player_mana, spent_mana, active_effects = next_state
    if boss_hp <= 0:
        return next_state,
    damage = max(BOSS_DAMAGE - player_armor, 1)
    return State(player_hp-damage, boss_hp, player_armor, player_mana, spent_mana, active_effects),

def a_star(start, is_goal, neighbors, d, h):
    open_set = {start}

    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: inf)
    f_score[start] = h(start)

    while open_set:
        current = min(open_set, key=f_score.__getitem__)
        if  is_goal(current):
            return g_score[current]

        open_set.remove(current)
        for neighbor in neighbors(current):
            tentative_g_score = g_score[current] + d(current, neighbor)
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                fs = tentative_g_score + h(neighbor)
                if fs != inf:
                    f_score[neighbor] = fs
                open_set.add(neighbor)
    return None


def d(current_turn, next_turn):
    return next_turn.state.spent_mana - current_turn.state.spent_mana

def h(turn):
    return turn.state.boss_hp // MIN_MANA_PER_HP_DAMAGE

def is_goal(turn):
    return turn.state.boss_hp <= 0

START = Turn(1, State(50, BOSS_HP, 0, 500, 0, ()))


print(a_star(START, is_goal, next_turn_options, d, h))