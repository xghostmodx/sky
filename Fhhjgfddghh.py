particle_history = []

def detect_particle(grid):
    # find strongest curvature point (simple proxy)
    best = None
    best_val = 0

    for i in range(N):
        for j in range(N):
            for k in range(N):
                val = abs(laplacian(grid, i, j, k))
                if val > best_val:
                    best_val = val
                    best = (i, j, k)

    return best, best_val

def gradient(f, x, y, z):
    gx = f[(x+1)%N,y,z] - f[(x-1)%N,y,z]
    gy = f[x,(y+1)%N,z] - f[x,(y-1)%N,z]
    gz = f[x,y,(z+1)%N] - f[x,y,(z-1)%N]
    return np.array([gx, gy, gz])

for step in range(steps):

    # --- run your field update first ---
    # (spin + phi evolution here)

    # --- detect particle ---
    p, strength = detect_particle(spin)

    if p is not None:
        particle_history.append(p)

    # --- once we have enough history ---
    if len(particle_history) > 10:

        # velocity
        v1 = np.array(particle_history[-1])
        v0 = np.array(particle_history[-2])
        v = v1 - v0

        # acceleration
        if len(particle_history) > 20:
            v_prev = np.array(particle_history[-2]) - np.array(particle_history[-3])
            a = v - v_prev

            x, y, z = p

            Fs = gradient(spin, x, y, z)
            Fp = gradient(phi, x, y, z)

            # simple regression-style estimation
            A = np.dot(a, Fs) / (np.linalg.norm(Fs)+1e-6)
            B = np.dot(a, Fp) / (np.linalg.norm(Fp)+1e-6)

            print("Spin coupling A:", A, "Field coupling B:", B)