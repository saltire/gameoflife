import math
import os

from PIL import Image

import game


class ImageGen:
    def __init__(self, cells, spritepath, (width, height), offset=(0, 0), cellsize=None):
        # init game generator
        self.cells = cells
        self.game = game.game_of_life(cells)
        
        # load cell sprite 
        sprite = Image.open(spritepath)
        swidth, sheight = sprite.size
        length = swidth / sheight
        self.animlength = length / 2
        
        # set cell size and resize sprite if necessary
        if cellsize is None:
            self.cellsize = sheight
        else:
            self.cellsize = cellsize
            antialias = Image.ANTIALIAS if cellsize < sheight else Image.BILINEAR
            sprite = sprite.resize((cellsize * length, cellsize), antialias)
        
        # slice sprite into frames
        self.frames = [sprite.crop((frame * self.cellsize, 0,
                                    (frame + 1) * self.cellsize, self.cellsize))
                       for frame in range(length)]
        
        # init size and offset
        self.size = (width * self.cellsize, height * self.cellsize)
        self.offset = offset

        
    def draw(self, outpath, gencount, speed=1, outname='image'):
        """Draw (gencount) number of generations. Resize cells to (cellsize).
        Draw every (speed)th frame. speed must be a factor of self.animlength."""
        
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        
        # set image attributes
        left, top = self.offset
        total = gencount * self.animlength / speed
        pad = int(math.log10(total)) + 1 # zero padding on each frame number
        update = 10
        percent = update

        # init image, draw first frame
        self.image = Image.new('RGBA', self.size, (0, 0, 0, 0))
        for x, y in self.cells:
            self.image.paste(self.frames[self.animlength - 1],
                             ((x + left) * self.cellsize, (y + top) * self.cellsize))

        for gen in range(gencount):
            # get next generation
            newcells = next(self.game)
            birthing = newcells - self.cells
            dying = self.cells - newcells
            
            # animate generation
            for state in range(speed - 1, self.animlength, speed):
                # save frame
                frame = (gen * self.animlength + state) / speed
                self.image.save(os.path.join(outpath, '{0}{1:0{2}}.png'.format(outname, frame, pad)))
                if float(frame + 1) / total * 100 >= percent:
                    print '{0}% done.'.format(percent)
                    percent += update
                
                # draw next frame
                for x, y in birthing:
                    self.image.paste(self.frames[state],
                                     ((x + left) * self.cellsize, (y + top) * self.cellsize))
                for x, y in dying:
                    self.image.paste(self.frames[state + self.animlength],
                                     ((x + left) * self.cellsize, (y + top) * self.cellsize))
                
            self.cells = newcells

                
                
if __name__ == '__main__':
    galaxy = ImageGen('spacefiller', 'circle8')
    galaxy.draw('d:\projects\gameoflife', 100, 5, 4)
    
            