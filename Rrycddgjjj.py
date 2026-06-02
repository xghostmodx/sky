import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -----------------------
# SYSTEM PARAMETERS
# -----------------------
N = 14  # smaller for performance

temperature = 1.2
decay = 0.97
diffusion = 0.12

grid = np.random.choice([-1, 1], size=(N, N, N))
field = np.zeros((N, N, N))

neighbors = [
    (dx, dy, dz)
    for dx in [-1, 1]
    for dy in [-1, 1]
    for dz in [-1, 1]
]

# -----------------------
# CORE FUNCTIONS
# -----------------------

def neighbor_sum(x, y, z):
    s = 0
    for dx, dy, dz in neighbors:
        nx = (x + dx) % N
        ny = (y + dy) % N
        nz = (z + dz) % N
        s += grid[nx, ny, nz]
    return s

def laplacian(f, x, y, z):
    center = f[x, y, z]
    total = 0
    for dx, dy, dz in neighbors:
        total += f[(x+dx)%N, (y+dy)%N, (z+dz)%N]
    return total - 8 * center

def particle_strength(x, y, z):
    return abs(neighbor_sum(x, y, z))

# -----------------------
# SIMULATION LOOP
# -----------------------
steps = 60000

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for step in range(steps):

    x = random.randint(0, N-1)
    y = random.randint(0, N-1)
    z = random.randint(0, N-1)

    # imbalance before
    before = particle_strength(x, y, z)

    old = grid[x, y, z]
    grid[x, y, z] *= -1

    after = particle_strength(x, y, z)

    dE = after - before

    # Metropolis rule
    if dE > 0 and random.random() > np.exp(-dE / temperature):
        grid[x, y, z] = old
        moved = False
    else:
        moved = True

    # -----------------------
    # EMF EMISSION
    # -----------------------
    if moved and after >= 5:
        field[x, y, z] += after * 2.5

    # -----------------------
    # FIELD EVOLUTION
    # -----------------------
    new_field = np.copy(field)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                new_field[i, j, k] += diffusion * laplacian(field, i, j, k)

    field = new_field * decay

    # -----------------------
    # VISUALIZATION
    # -----------------------
    if step % 2500 == 0:
        ax.clear()

        px, py, pz = [], [], []
        fx, fy, fz = [], [], []

        for i in range(N):
            for j in range(N):
                for k in range(N):

                    # particles
                    if particle_strength(i, j, k) >= 5:
                        px.append(i)
                        py.append(j)
                        pz.append(k)

                    # EMF field hotspots
                    if field[i, j, k] > field.max() * 0.6:
                        fx.append(i)
                        fy.append(j)
                        fz.append(k)

        # particles (cyan)
        ax.scatter(px, py, pz, c='cyan', s=20)

        # EMF bursts (yellow)
        ax.scatter(fx, fy, fz, c='yellow', s=10)

        ax.set_xlim(0, N)
        ax.set_ylim(0, N)
        ax.set_zlim(0, N)

        ax.set_title(f"3D Spin + Particles + EMF Waves | step {step}")

        plt.pause(0.05)

plt.ioff()
plt.show()