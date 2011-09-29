class Game():

    def __init__(self, start):
        self.cells = start

    def next_generation(self):
        xmin = min([cell[0] for cell in self.cells])
        ymin = min([cell[1] for cell in self.cells])
        xmax = max([cell[0] for cell in self.cells])
        ymax = max([cell[1] for cell in self.cells])
        
        nextgen = self.cells.copy()
        for x in range(xmin - 1, xmax + 2):
            for y in range(ymin - 1, ymax + 2):
                neighbours = 0
                for nx in range(x - 1, x + 2):
                    for ny in range(y - 1, y + 2):
                        if (nx, ny) != (x, y) and (nx, ny) in self.cells: 
                            neighbours += 1
                if (x, y) in self.cells and (neighbours < 2 or neighbours > 3):
                    nextgen.remove((x, y))
                elif (x, y) not in self.cells and neighbours == 3:
                    nextgen.add((x, y))
                    
        self.cells = nextgen
        return self.cells
        
