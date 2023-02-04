import pygame

from animals.Body import Body


def flip(img):
    return pygame.transform.flip(img, True, False)


class Dog(Body):
    def __init__(self, type, color, x, y, rad, speed, width, height):
        super().__init__(type, color, x, y, rad, speed, width, height)
        self.sneak = False
        self.sneakRad = rad / 2
        self.sneakImg = pygame.transform.scale(pygame.image.load("img/dogSneak.png"), (85, 35))
        self.runImgArray = [pygame.transform.scale(pygame.image.load("img/dogRun0.png"), (80, 45)),
                            pygame.transform.scale(pygame.image.load("img/dogRun1.png"), (105, 50)),
                            pygame.transform.scale(pygame.image.load("img/dogRun2.png"), (105, 50)),
                            pygame.transform.scale(pygame.image.load("img/dogRun3.png"), (85, 38))]
        self.img = self.runImgArray[0]

    def setSneak(self):
        self.sneak = not self.sneak

        if self.sneak:
            self.checkFlip(self.sneakImg)
        else:
            self.checkFlip(self.runImgArray[0])

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

    def checkFlip(self, img):
        self.img = flip(img) if self.isLeft else img

    def moving(self):
        return self.WisPressed or self.AisPressed or self.SisPressed or self.DisPressed

    def addFrame(self):
        if self.moving():
            if self.runFrame < 3:
                self.runFrame += 1
            else:
                self.runFrame = 1
        else:
            self.runFrame = 0

        if not self.sneak:
            self.checkFlip(self.runImgArray[self.runFrame])
