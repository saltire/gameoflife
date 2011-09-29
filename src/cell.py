import pygame

class Cell(pygame.sprite.Sprite):
    
    def __init__(self, pos, images, size=10, offset=0, state=-1):
        pygame.sprite.Sprite.__init__(self)
        self.pos = x, y = pos
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
