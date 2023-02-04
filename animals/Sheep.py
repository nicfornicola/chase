import pygame

from animals.Body import Body


class Sheep(Body):
    def __init__(self, type, color, x, y, rad, speed, width, height):
        super().__init__(type, color, x, y, rad, speed, width, height)
        self.randMove = True
        self.img = pygame.transform.scale(pygame.image.load("img/sheep.png"), (25, 35))
