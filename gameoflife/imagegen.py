import math
import os

from PIL import Image

import game


class ImageGen:
    def __init__(self, cells, spritepath):
        # init game simulator
        self.cells = cells
        self.game = game.game_of_life(cells)
        
        # load and slice cell sprite
        sprite = Image.open(spritepath)
        width, height = sprite.size
        length = width / height
        self.animlength = length / 2
        self.frames = [sprite.crop((frame * height, 0, (frame + 1) * height, height))
                        for frame in range(length)]

        
    def draw(self, outpath, gencount, (width, height), (left, top)=(0, 0),
             cellsize=None, speed=1, outname='image'):
        """Draw (gencount) number of generations. Resize cells to (cellsize).
        Draw every (speed)th frame. speed must be a factor of self.animlength."""
        
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        
        # resize frames if necessary
        defaultsize = self.frames[0].size[0]
        if cellsize is None:
            cellsize = defaultsize
        elif cellsize != defaultsize:
            antialias = Image.ANTIALIAS if cellsize < defaultsize else Image.BILINEAR
            for i, sprite in enumerate(self.frames):
                self.frames[i] = sprite.resize((cellsize, cellsize), antialias)
            
        # set image attributes
        size = width * cellsize, height * cellsize
        total = gencount * self.animlength / speed
        pad = int(math.log10(total)) + 1
        update = 10
        percent = update

        # init image, draw first frame
        self.image = Image.new('RGBA', size, (0, 0, 0, 0))
        for x, y in self.cells:
            self.image.paste(self.frames[self.animlength - 1],
                             ((x + left) * cellsize, (y + top) * cellsize))

        for cycle in range(gencount):
            # get next generation
            newcells = next(self.game)
            birthing = newcells - self.cells
            dying = self.cells - newcells
            
            # animate generation
            for state in range(speed - 1, self.animlength, speed):
                # save frame
                frame = (cycle * self.animlength + state) / speed
                self.image.save(os.path.join(outpath, '{0}{1:0{2}}.png'.format(outname, frame, pad)))
                if float(frame + 1) / total * 100 >= percent:
                    print '{0}% done.'.format(percent)
                    percent += update
                
                # draw next frame
                for x, y in birthing:
                    self.image.paste(self.frames[state],
                                     ((x + left) * cellsize, (y + top) * cellsize))
                for x, y in dying:
                    self.image.paste(self.frames[state + self.animlength],
                                     ((x + left) * cellsize, (y + top) * cellsize))
                
            self.cells = newcells

                
                
if __name__ == '__main__':
    galaxy = ImageGen('spacefiller', 'circle8')
    galaxy.draw('d:\projects\gameoflife', 100, 5, 4)
    
            