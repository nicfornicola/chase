import pygame

from animals.Body import Body


def flip(img):
    return pygame.transform.flip(img, True, False)


class Dog(Body):
    def __init__(self, type, color, x, y, rad, speed, width, height):
        super().__init__(type, color, x, y, rad, speed, width, height)
        self.sneak = False
        self.sneakRad = rad / 2
        self.sneakImg = pygame.transform.scale(
            pygame.image.load("img/dogSneak.png"), (85, 35))
        self.runImg = pygame.transform.scale(
            pygame.image.load("img/dogRun.png"), (85, 35))
        self.img = self.runImg

    def setSneak(self):
        self.sneak = not self.sneak

        if self.sneak:
            if self.isLeft:
                self.img = flip(self.sneakImg)
            else:
                self.img = self.sneakImg
        else:
            if self.isLeft:
                self.img = flip(self.runImg)
            else:
                self.img = self.runImg

    def setAisPressed(self, isPressed):
        self.AisPressed = isPressed

        if self.AisPressed and self.isRight:
            self.img = flip(self.img)
            self.isRight = False
            self.isLeft = True

    def setDisPressed(self, isPressed):
        self.DisPressed = isPressed

        if self.DisPressed and self.isLeft:
            self.img = flip(self.img)
            self.isLeft = False
            self.isRight = True

