import os

from PIL import Image

import game

class GamePIL:

    def __init__(self, pattern):
        self.pattern = pattern

        # load starting pattern
        start = set()
        with open('{0}.txt'.format(pattern), 'r') as smap:
            self.width, self.height, self.offset = [int(num) for num in smap.readline().strip().split(',')]
            for y, line in enumerate(smap.readlines()):
                for x, value in enumerate(line):
                    if value == '.':
                        start.add((x, y))
        
        # init game simulator
        self.game = game.Game(start)
        self.cells = self.game.cells

        # load and slice cell sprite
        sprite = Image.open('cell.png')
        width, height = sprite.size
        length = width / height
        self.animlength = length / 2
        self.sprites = []
        for state in range(length):
            self.sprites.append(sprite.crop((state * height, 0, (state + 1) * height, height)))

        
    def draw(self, cycles, path, cellsize=None):
        self.path = path
        
        # resize sprites if necessary
        defaultsize = self.sprites[0].size[0]
        if cellsize is None:
            cellsize = defaultsize
            
        if cellsize != defaultsize:
            for i, sprite in enumerate(self.sprites):
                self.sprites[i] = sprite.resize((cellsize, cellsize), Image.ANTIALIAS if cellsize < defaultsize else Image.BILINEAR)
            
        # set image attributes
        size = (self.width * cellsize, self.height * cellsize)
        offset = self.offset * cellsize

        # animate a single generation
        for cycle in range(cycles):
            newcells = self.game.next_generation()
            birthing = newcells - self.cells
            dying = self.cells - newcells
            
            self.image = Image.new('RGBA', size, (0, 0, 0, 0))
            for state in range(self.animlength):
                if state == 0:
                    for x, y in self.cells:
                        self.image.paste(self.sprites[self.animlength], (x * cellsize + offset, y * cellsize + offset))
                else:
                    for x, y in birthing:
                        self.image.paste(self.sprites[state], (x * cellsize + offset, y * cellsize + offset))
                    for x, y in dying:
                        self.image.paste(self.sprites[state + self.animlength], (x * cellsize + offset, y * cellsize + offset))
    
                self.image.save(os.path.join(self.path, '{0}{1:03}.png'.format(self.pattern, cycle * self.animlength + state)))
                
            self.cells = newcells
            
        print 'done.'

                
                
if __name__ == '__main__':
    galaxy = GamePIL('galaxy')
    galaxy.draw(8, 'd:\projects\gameoflife', 50)
    
            