import pygame

from collections import deque
from animals.Body import Body
from util.Trailcell import Trailcell


class Sheep(Body):
    def __init__(self, type, color, x, y, rad, speed, width, height):
        super().__init__(type, color, x, y, rad, speed, width, height)
        self.randMove = True
        self.img = pygame.transform.scale(pygame.image.load("img/sheep.png"), (25, 35))
        self.trail = deque()
        self.sheepSee = 100

    def setAisPressed(self, isPressed):
        self.AisPressed = isPressed

    def setDisPressed(self, isPressed):
        self.DisPressed = isPressed

    def addTrail(self, trailCell):
        if len(self.trail) > 200:
            self.trail.pop()
        self.trail.appendleft(trailCell)


