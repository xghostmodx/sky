import numpy as np
import random
import matplotlib.pyplot as plt

# Grid size
N = 60

# Spin field (+1 / -1)
grid = np.random.choice([-1, 1], size=(N, N))

# EMF-like continuous field
field = np.zeros((N, N))

# damping + diffusion controls wave behavior
decay = 0.98
diffusion = 0.15
temperature = 1.2

neighbors = [
    (-1,-1), (-1,0), (-1,1),
    (0,-1),         (0,1),
    (1,-1),  (1,0), (1,1)
]

def neighbor_sum(x, y):
    s = 0
    for dx, dy in neighbors:
        nx = (x + dx) % N
        ny = (y + dy) % N
        s += grid[nx, ny]
    return s

def laplacian(f, x, y):
    center = f[x, y]
    total = 0
    for dx, dy in neighbors:
        total += f[(x+dx)%N, (y+dy)%N]
    return total - 8 * center

steps = 50000

plt.ion()
fig, ax = plt.subplots()

for step in range(steps):

    # pick random site
    x = random.randint(0, N-1)
    y = random.randint(0, N-1)

    # compute local imbalance (particle strength)
    imbalance_before = abs(neighbor_sum(x, y))

    # propose flip
    old = grid[x, y]
    grid[x, y] *= -1

    imbalance_after = abs(neighbor_sum(x, y))

    # Metropolis-like acceptance
    dE = imbalance_after - imbalance_before

    if dE > 0 and random.random() > np.exp(-dE / temperature):
        grid[x, y] = old  # revert
        moved = False
    else:
        moved = True

    # EMF emission event
    if moved and imbalance_after >= 4:
        # inject wave burst
        field[x, y] += imbalance_after * 2.0

    # field evolution (wave diffusion + decay)
    new_field = np.copy(field)
    for i in range(N):
        for j in range(N):
            new_field[i, j] += diffusion * laplacian(field, i, j)

    field = new_field * decay

    # visualization
    if step % 2000 == 0:
        ax.clear()

        # show EMF field as heatmap
        ax.imshow(field, cmap='inferno', alpha=0.9)

        # overlay particles (defects)
        px, py = [], []
        for i in range(N):
            for j in range(N):
                if abs(neighbor_sum(i, j)) >= 4:
                    px.append(j)
                    py.append(i)

        ax.scatter(px, py, c='cyan', s=10)

        ax.set_title(f"Spin + Particle + EMF Field | step {step}")
        plt.pause(0.01)

plt.ioff()
plt.show()