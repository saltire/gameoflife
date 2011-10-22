import math
import os

from PIL import Image

import game

class GamePIL:

    def __init__(self, pattern):
        self.pattern = pattern

        # load starting pattern
        start = set()
        with open('{0}.txt'.format(pattern), 'r') as smap:
            self.width, self.height, self.offsetx, self.offsety = [int(num) for num in smap.readline().strip().split(',')]
            for y, line in enumerate(smap.readlines()):
                for x, value in enumerate(line):
                    if value == '.':
                        start.add((x, y))
        
        # init game simulator
        self.game = game.Game(start)
        self.cells = self.game.cells

        # load and slice cell sprite
        sprite = Image.open('cell8.png')
        width, height = sprite.size
        length = width / height
        self.animlength = length / 2
        self.sprites = []
        for state in range(length):
            self.sprites.append(sprite.crop((state * height, 0, (state + 1) * height, height)))

        
    def draw(self, path, cycles, cellsize=None, speed=1):
        """Draw (cycles) number of generations. Resize cells to (cellsize).
        Draw every (speed)th frame. speed must be a factor of self.animlength."""
        
        self.path = os.path.join(path, self.pattern)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        
        # resize sprites if necessary
        defaultsize = self.sprites[0].size[0]
        if cellsize is None:
            cellsize = defaultsize
        elif cellsize != defaultsize:
            for i, sprite in enumerate(self.sprites):
                self.sprites[i] = sprite.resize((cellsize, cellsize), Image.ANTIALIAS if cellsize < defaultsize else Image.BILINEAR)
            
        # set image attributes
        size = self.width * cellsize, self.height * cellsize
        offsetx, offsety = self.offsetx * cellsize, self.offsety * cellsize
        total = cycles * self.animlength / speed
        pad = int(math.log10(total)) + 1
        update = 10
        percent = update

        print 'rendering {0} ({1} frames)'.format(self.pattern, total)
        
        # init image, draw first frame
        self.image = Image.new('RGBA', size, (0, 0, 0, 0))
        for x, y in self.cells:
            self.image.paste(self.sprites[self.animlength - 1], (x * cellsize + offsetx, y * cellsize + offsety))

        for cycle in range(cycles):
            # get next generation
            newcells = self.game.next_generation()
            birthing = newcells - self.cells
            dying = self.cells - newcells
            
            # animate generation
            for state in range(speed - 1, self.animlength, speed):
                # save frame
                frame = (cycle * self.animlength + state) / speed
                self.image.save(os.path.join(self.path, '{0}{1:0{2}}.png'.format(self.pattern, frame, pad)))
                if float(frame + 1) / total * 100 >= percent:
                    print '{0}% done.'.format(percent)
                    percent += update
                
                # draw next frame
                for x, y in birthing:
                    self.image.paste(self.sprites[state], (x * cellsize + offsetx, y * cellsize + offsety))
                for x, y in dying:
                    self.image.paste(self.sprites[state + self.animlength], (x * cellsize + offsetx, y * cellsize + offsety))
                
            self.cells = newcells

                
                
if __name__ == '__main__':
    galaxy = GamePIL('galaxy')
    galaxy.draw('d:\projects\gameoflife', 8)
    
            