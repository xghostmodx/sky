import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

# Grid size
N = 18

# Temperature (try 0.1 → 5.0)
T = 1.5

grid = np.random.choice([-1, 1], size=(N, N, N))

neighbors = [
    (dx, dy, dz)
    for dx in [-1, 1]
    for dy in [-1, 1]
    for dz in [-1, 1]
]

def neighbor_sum(x, y, z):
    s = 0
    for dx, dy, dz in neighbors:
        nx = (x + dx) % N
        ny = (y + dy) % N
        nz = (z + dz) % N
        s += grid[nx, ny, nz]
    return s

def energy(x, y, z, val):
    # local imbalance energy
    return (neighbor_sum(x, y, z) * val) ** 2

steps = 80000

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for step in range(steps):

    x = random.randint(0, N - 1)
    y = random.randint(0, N - 1)
    z = random.randint(0, N - 1)

    current_val = grid[x, y, z]

    E_before = energy(x, y, z, current_val)

    # propose flip
    grid[x, y, z] *= -1
    new_val = grid[x, y, z]

    E_after = energy(x, y, z, new_val)

    dE = E_after - E_before

    # Metropolis rule
    if dE <= 0:
        accept = True
    else:
        accept = random.random() < math.exp(-dE / T)

    if not accept:
        grid[x, y, z] *= -1

    # visualize
    if step % 3000 == 0:
        ax.clear()

        xs_p, ys_p, zs_p = [], [], []
        xs_n, ys_n, zs_n = [], [], []

        for i in range(N):
            for j in range(N):
                for k in range(N):
                    if grid[i, j, k] == 1:
                        xs_p.append(i); ys_p.append(j); zs_p.append(k)
                    else:
                        xs_n.append(i); ys_n.append(j); zs_n.append(k)

        ax.scatter(xs_p, ys_p, zs_p, c='red', s=10)
        ax.scatter(xs_n, ys_n, zs_n, c='blue', s=10)

        ax.set_title(f"3D Entanglement + Temperature T={T} | step {step}")
        ax.set_xlim(0, N)
        ax.set_ylim(0, N)
        ax.set_zlim(0, N)

        plt.pause(0.1)

plt.ioff()
plt.show()