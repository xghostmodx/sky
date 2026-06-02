import numpy as np
import random
import matplotlib.pyplot as plt

# -----------------------
# PARAMETERS
# -----------------------
N = 14
beta = 2.0        # spin stiffness (temperature inverse)
c = 0.6           # wave speed
gamma = 0.02      # damping

# -----------------------
# FIELDS
# -----------------------
spin = np.random.uniform(-1, 1, (N, N, N))
phi_prev = np.zeros((N, N, N))
phi = np.zeros((N, N, N))

neighbors = [
    (dx, dy, dz)
    for dx in [-1, 0, 1]
    for dy in [-1, 0, 1]
    for dz in [-1, 0, 1]
    if not (dx == dy == dz == 0)
]

# -----------------------
# LAPLACIAN
# -----------------------
def laplacian(f, x, y, z):
    total = 0
    for dx, dy, dz in neighbors:
        total += f[(x+dx)%N, (y+dy)%N, (z+dz)%N]
    return total - len(neighbors) * f[x, y, z]

# -----------------------
# SIMULATION LOOP
# -----------------------
steps = 40000

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for step in range(steps):

    # -----------------------
    # SPIN FIELD EVOLUTION
    # -----------------------
    new_spin = np.copy(spin)

    for i in range(N):
        for j in range(N):
            for k in range(N):

                h = laplacian(spin, i, j, k)

                # smooth alignment (not flipping)
                new_spin[i, j, k] = np.tanh(beta * h)

    spin = new_spin

    # -----------------------
    # EM FIELD (WAVE EQUATION)
    # -----------------------
    new_phi = np.copy(phi)

    for i in range(N):
        for j in range(N):
            for k in range(N):

                wave_term = c**2 * laplacian(phi, i, j, k)
                inertia = 2 * phi[i, j, k] - phi_prev[i, j, k]

                new_phi[i, j, k] = inertia + wave_term - gamma * (phi[i, j, k] - phi_prev[i, j, k])

    phi_prev = phi
    phi = new_phi

    # -----------------------
    # COUPLING (spin → field)
    # -----------------------
    if step % 5 == 0:
        for i in range(N):
            for j in range(N):
                for k in range(N):

                    # spins inject energy into field
                    phi[i, j, k] += spin[i, j, k] * 0.02

    # -----------------------
    # VISUALIZATION
    # -----------------------
    if step % 2000 == 0:
        ax.clear()

        px, py, pz = [], [], []
        fx, fy, fz = [], [], []

        for i in range(N):
            for j in range(N):
                for k in range(N):

                    # “particles” = high curvature in spin field
                    if abs(laplacian(spin, i, j, k)) > 2.5:
                        px.append(i)
                        py.append(j)
                        pz.append(k)

                    # EM wave hotspots
                    if abs(phi[i, j, k]) > np.max(np.abs(phi)) * 0.6:
                        fx.append(i)
                        fy.append(j)
                        fz.append(k)

        ax.scatter(px, py, pz, c='cyan', s=20)
        ax.scatter(fx, fy, fz, c='yellow', s=10)

        ax.set_xlim(0, N)
        ax.set_ylim(0, N)
        ax.set_zlim(0, N)

        ax.set_title(f"Field Theory Model | step {step}")

        plt.pause(0.05)

plt.ioff()
plt.show()