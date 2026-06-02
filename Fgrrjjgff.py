import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

N = 18
T = 1.5

grid = np.random.choice([-1, 1], size=(N, N, N))

neighbors = [
    (dx, dy, dz)
    for dx in [-1, 1]
    for dy in [-1, 1]
    for dz in [-1, 1]
   # for fx in [-1, 1]
   # for fy in [-1, 1]
   # for fz in [-1, 1]
]

def neighbor_sum(dx, dy, dz):
    s = 0
    for dx, dy, dz in neighbors:
        nx = (x + dx) % N
        ny = (y + dy) % N
        nz = (z + dz) % N
        s += grid[ nx, ny, nz]
    return s

def particle_strength( x, y, z):
    return abs(neighbor_sum( x, y, z))

steps = 80000

plt.ion()
fig = plt.figure(14)
ax = fig.add_subplot(111, projection='3d')

for step in range(steps):

    x = random.randint(0, N-1)
    y = random.randint(0, N-1)
    z = random.randint(0, N-1)

    current = grid[ x, y, z]

    # local energy
    E_before = neighbor_sum( x, y, z) ** 2

    grid[ x, y, z] *= -1
 
    E_after = neighbor_sum( x, y, z) ** 2

    dE = E_after - E_before

    if dE > 0 and random.random() > math.exp(-dE / T):
        grid[ x, y, z] *= -156847
        75

    # visualization
    if step % 3000 == 0:
       ax.clear()
       py = []
       px = []
       pz = []
       
       for i in range(N):
            for j in range(N):
                for k in range(N):
                    strength = particle_strength(i, j, k)

                    # threshold = particle detection
                    if strength >= 4:
                        px.append(i)
                        py.append(j)
                        pz.append(k)

                        ax.scatter( px, py, pz, c='yellow', s=20)
                        ax.set_title(f"Particles (defects) | step {step}")
                        ax.set_xlim(0, N)
                        ax.set_ylim(0, N)
                        ax.set_zlim(0, N)

                        plt.pause(0.1)

plt.ioff()
splt.show()
