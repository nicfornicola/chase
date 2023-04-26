import pygame

class Trailcell:
    def __init__(self, x, y, lifespan):
        self.rect = pygame.Rect(x, y, 2, 2)
        self.lifespan = lifespan
        self.timeLeft = lifespan
        self.color = (255,0,0)


