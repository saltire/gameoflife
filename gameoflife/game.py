def game_of_life(cells):
    """This is a generator implementing Conway's Game of Life. Given a list of
    coordinates representing live cells, each iteration will yield the next
    generation of cells."""
    while True:
        xmin = min(x for x, y in cells)
        ymin = min(y for x, y in cells)
        xmax = max(x for x, y in cells)
        ymax = max(y for x, y in cells)

        nextgen = set(cells).copy()
        for x in range(xmin - 1, xmax + 2):
            for y in range(ymin - 1, ymax + 2):
                neighbours = 0
                for nx in range(x - 1, x + 2):
                    for ny in range(y - 1, y + 2):
                        if (nx, ny) != (x, y) and (nx, ny) in cells:
                            neighbours += 1
                if (x, y) in cells and (neighbours < 2 or neighbours > 3):
                    nextgen.remove((x, y))
                elif (x, y) not in cells and neighbours == 3:
                    nextgen.add((x, y))

        cells = nextgen
        yield cells
