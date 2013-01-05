from gameoflife import imagegen
from gameoflife import animation


class GameOfLife:
    def __init__(self, patternpath, dims=None, offset=None):
        # load starting pattern
        self.cells = set()
        with open(patternpath, 'rb') as pfile:
            width, height, left, top = (int(num) for num in pfile.readline().strip().split(','))
            for y, line in enumerate(pfile.readlines()):
                for x, char in enumerate(line):
                    if char == '.':
                        self.cells.add((x, y))
                        
        self.dims = dims if dims is not None else (width, height)
        self.offset = offset if offset is not None else (left, top)


    def render_images(self, spritepath, gencount, outpath='.', cellsize=None):
        imagegen.ImageGen(self.cells, spritepath).draw(outpath, gencount, self.dims, 
                                                       self.offset, cellsize)
        
        
    def show_animation(self, spritepath, cellsize=None):
        animation.Animation(self.cells, spritepath, self.dims,
                            self.offset, cellsize).run()
        
        

if __name__ == '__main__':
    patternpath = 'patterns/galaxy.txt'
    spritepath = 'sprites/circle8.png'
    
    #GameOfLife(patternpath).show_animation(spritepath, 50)
    GameOfLife(patternpath).render_images(spritepath, 4, './images', 25)