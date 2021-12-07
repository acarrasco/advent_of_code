import sys
import scipy
import scipy.optimize

positions = scipy.array([int(x) for x in sys.stdin.read().strip().split(',')], dtype=int)


def cost(target):
    d = abs(positions - target)
    return (d * (d+1) / 2).sum()


best_position = scipy.optimize.minimize_scalar(cost, bounds=(0, positions.max()))

print(cost(int(best_position.x+0.5)))
