import pygame

class Body:

    def __init__(self, type, color, x, y, rad, speed, width, height):
        self.type = type
        self.color = color
        self.rad = rad
        self.regRad = rad
        self.speed = speed
        self.inPen = False
        self.WisPressed = False
        self.AisPressed = False
        self.SisPressed = False
        self.DisPressed = False
        self.buttonPressed = None
        self.rect = pygame.Rect(x, y, 5, 5)
        self.randMove = False
        self.isLeft = False
        self.isRight = True
        self.runFrame = 0

