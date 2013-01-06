from PIL import Image


class Pattern:
    def __init__(self, patternpath):
        pattern = Image.open(patternpath)
        pixels = pattern.load()
        width, height = pattern.size
        
        # load cells: any non-black pixel in the given image
        self.cells = set()
        for x in range(width):
            for y in range(height):
                if pixels[x, y] != (0, 0, 0):
                    self.cells.add((x, y))
                    
        self.dims = width, height
