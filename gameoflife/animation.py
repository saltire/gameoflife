import sys

import pygame

import game


class Animation:
    def __init__(self, cells, spritepath, (width, height), cellsize=None):
        self.cellmap = cells
        self.game = game.game_of_life(cells)
        
        pygame.init()
        
        # load cell sprite
        sprite = pygame.image.load(spritepath)
        length = sprite.get_width() / sprite.get_height()
        self.animlength = length / 2
        
        # set cell size and resize sprite if necessary
        if cellsize is None:
            self.cellsize = sprite.get_height()
        else:
            self.cellsize = cellsize
            sprite = pygame.transform.scale(sprite, (cellsize * length, cellsize))
        
        # slice sprite into frames
        self.frames = [sprite.subsurface((frame * self.cellsize, 0,
                                          self.cellsize, self.cellsize))
                       for frame in range(length)]
                    
        # init window, background and offset
        self.window = pygame.display.set_mode((width * self.cellsize, height * self.cellsize))
        self.background = pygame.surface.Surface(self.window.get_size())
        self.background.fill((255, 255, 255))
        
        # init groups and starting cells
        self.cells = pygame.sprite.RenderUpdates()
        self.birthing = pygame.sprite.RenderUpdates()
        self.dying = pygame.sprite.RenderUpdates()
        for x, y in self.cellmap:
            self.cells.add(Cell((x, y), self.frames, self.cellsize, self.animlength - 1))
                    
        # draw starting cells
        self.window.blit(self.background, (0, 0))
        self.cells.draw(self.window)
        pygame.display.update()


    def run(self, framedelay=20, gendelay=100):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            # find the next generation of cells
            oldcellmap = self.cellmap
            self.cellmap = next(self.game)
            
            # add cells created this generation to birthing group
            for pos in self.cellmap - oldcellmap:
                newcell = Cell(pos, self.frames, self.cellsize)
                self.cells.add(newcell)
                self.birthing.add(newcell)
                
            # add cells removed this generation to dying group
            for oldcell in self.cells:
                if oldcell.pos in oldcellmap - self.cellmap:
                    self.dying.add(oldcell)
                
            # render animation for birthing and dying cells
            for _ in range(self.animlength):
                self.birthing.update()
                self.dying.update()
                
                self.window.blit(self.background, (0, 0))
                pygame.display.update(self.cells.draw(self.window))
                
                pygame.time.delay(framedelay)
                
            # remove dead cells, and reset groups
            self.cells.remove(self.dying)
            self.birthing.empty()
            self.dying.empty()

            pygame.time.delay(gendelay)
            


class Cell(pygame.sprite.Sprite):
    def __init__(self, (x, y), images, size=10, frame=-1):
        pygame.sprite.Sprite.__init__(self)
        
        self.pos = x, y
        self.frames = images
        self.frame = frame
        
        self.rect = pygame.Rect((x * size, y * size, size, size))
        self.image = self.frames[self.frame]
        
        
    def update(self):
        self.frame += 1
        self.image = self.frames[self.frame]
        
        
        