import sys
import numpy

positions = [int(x) for x in sys.stdin.read().strip().split(',')]

target = numpy.median(positions)

print(sum(abs(x - target) for x in positions))