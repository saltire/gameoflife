import sys

import pygame

import cell
import game

class GameOfLife:
    
    def __init__(self):
        pygame.init()
        
        # init map
        smap = [
                 '111111011',
                 '111111011',
                 '000000011',
                 '110000011',
                 '110000011',
                 '110000011',
                 '110000000',
                 '110111111',
                 '110111111'
                 ]
        start = set()
        for y in range(len(smap)):
            for x in range(len(smap[y])):
                if smap[y][x] == '1':
                    start.add((x, y))
        self.game = game.Game(start)
        
        # init window
        self.window = pygame.display.set_mode((400, 400))
        self.window.fill((0, 0, 0))
        self.offset = 110
        self.cellsize = 20
        
        # load and slice cell image
        image = pygame.image.load('cell.png')
        length = image.get_width() / image.get_height()
        image = pygame.transform.scale(image, (self.cellsize * length, self.cellsize))
        self.animlength = length / 2
        self.images = []
        for frame in range(length):
            self.images.append(image.subsurface((frame * self.cellsize, 0, self.cellsize, self.cellsize)))
                    
        # init starting cells
        self.cells = pygame.sprite.RenderUpdates()
        for x, y in start:
            self.cells.add(cell.Cell((x, y), self.images, self.cellsize, self.offset, self.animlength - 1))
        self.birthing = pygame.sprite.RenderUpdates()
        self.dying = pygame.sprite.RenderUpdates()
                    
        # draw starting cells
        updates = self.cells.draw(self.window)
        pygame.display.update(updates)

        # init clock, start loop
        self.clock = pygame.time.Clock()
        self.time = self.clock.tick()
        while 1:
            self.update()
        
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        oldcells = self.game.cells
        newcells = self.game.next_generation()
        
        for oldcell in self.cells:
            if oldcell.pos in oldcells - newcells:
                self.dying.add(oldcell)
            
        for x, y in newcells - oldcells:
            newcell = cell.Cell((x, y), self.images, self.cellsize, self.offset)
            self.cells.add(newcell)
            self.birthing.add(newcell)
            
        for i in range(self.animlength):
            self.birthing.update()
            self.dying.update()
            updates = self.birthing.draw(self.window) + self.dying.draw(self.window)
            pygame.display.update(updates)
            pygame.time.delay(20)
            
        pygame.time.delay(100)
            
        self.birthing.empty()
        self.cells.remove(self.dying)
        self.dying.empty()



class Cell(pygame.sprite.Sprite):
   
    def __init__(self, (x, y), images, size=10, offset=0, state=-1):
        pygame.sprite.Sprite.__init__(self)
        self.pos = x, y
        self.images = images
        self.state = state
        
        self.image = pygame.Surface((size, size))
        self.rect = pygame.Rect((x * size + offset, y * size + offset, size, size))
        self.draw()
        
        
    def update(self):
        self.state += 1
        self.draw()

        
    def draw(self):
        self.image.blit(self.images[self.state], (0, 0))
                
            
            
if __name__ == '__main__':
    GameOfLife()

        