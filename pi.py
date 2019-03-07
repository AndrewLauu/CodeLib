#pi.py
from random import random
from math import sqrt
from time import clock
dart = 2**28
hits = 0
clock()
print("...")
for i in range(1,dart):
    x, y = random(), random()
    dist = sqrt(x**2 + y**2)
    if dist <= 1.0:
       hits = hits + 1
pi = 4 * (hits/dart)
print(pi)
print(clock())
