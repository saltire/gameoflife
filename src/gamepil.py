import os

from PIL import Image

import game

class GamePIL:

    def __init__(self, pattern, cellsize, path):
        self.path = path

        # load starting pattern
        start = set()
        with open('{0}.txt'.format(pattern), 'r') as smap:
            mwidth, mheight, offset = smap.readline().strip().split(',')
            for y, line in enumerate(smap.readlines()):
                for x, value in enumerate(line):
                    if value == '.':
                        start.add((x, y))
        
        # init image attributes
        self.cellsize = cellsize
        self.size = (int(mwidth) * self.cellsize, int(mheight) * self.cellsize)
        self.origin = int(offset) * self.cellsize

        # init game simulator
        self.game = game.Game(start)
        self.cells = self.game.cells

        # load cell sprite
        sprite = Image.open('cell.png')
        swidth, sheight = sprite.size
        length = swidth / sheight
        self.animlength = length / 2

        # resize and slice cell sprite
        self.sprites = []
        if sheight != self.cellsize:
            sprite = sprite.resize((self.cellsize * length, self.cellsize), Image.ANTIALIAS)
        for state in range(length):
            self.sprites.append(sprite.crop((state * self.cellsize, 0, state * self.cellsize + self.cellsize, self.cellsize)))

        # start loop
        for cycle in range(8):
            self.draw_cycle(cycle)

        print 'done.'
            
        
    def draw_cycle(self, cycle):
        newcells = self.game.next_generation()
        birthing = newcells - self.cells
        dying = self.cells - newcells
        
        self.image = Image.new('RGBA', self.size, (0, 0, 0, 0))
        for state in range(self.animlength):
            if state == 0:
                for x, y in self.cells:
                    self.image.paste(self.sprites[self.animlength], (x * self.cellsize + self.origin, y * self.cellsize + self.origin))
            else:    
                for x, y in birthing:
                    self.image.paste(self.sprites[state], (x * self.cellsize + self.origin, y * self.cellsize + self.origin))
                for x, y in dying:
                    self.image.paste(self.sprites[state + self.animlength], (x * self.cellsize + self.origin, y * self.cellsize + self.origin))

            self.image.save(os.path.join(self.path, 'frame{0:03}.png'.format(cycle * self.animlength + state)))
            
        self.cells = newcells

                
                
if __name__ == '__main__':
    GamePIL('galaxy', 50, 'd:\projects\gameoflife')
            