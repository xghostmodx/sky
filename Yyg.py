for step in range(N):
    (N) = random_node()
    current = grid[x][y]
    sum_neighbors = sum_of_8_neighbors(x, y)

    # energy before
    E_before = sum_neighbors**2

    # try flip
    grid[x][y] *= -1
    new_sum = sum_of_8_neighbors(x, y)
    E_after = new_sum**2

    if E_after > E_before:
        grid[x][y] *= -1  # revert
