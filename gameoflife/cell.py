import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, images, size=10, frame=-1):
        pygame.sprite.Sprite.__init__(self)

        self.pos = x, y
        self.frames = images
        self.frame = frame

        self.rect = pygame.Rect((x * size, y * size, size, size))
        self.image = self.frames[self.frame]

    def update(self):
        self.frame += 1
        self.image = self.frames[self.frame]
