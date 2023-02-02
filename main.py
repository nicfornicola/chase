import math
import random
import sys

import pygame
from matplotlib import colors
from pygame.locals import *

from Walls import Wall
from animals.Dog import Dog
from animals.Sheep import Sheep

pygame.display.set_caption('Chase')
sim_window = 800
currentSprite = 0
pygame.init()
window = pygame.display.set_mode((sim_window, sim_window))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
window.fill(0)
pygame.display.update(pygame.Rect(0, 0, sim_window, sim_window))
clock = pygame.time.Clock()


def getRandGreen():
    x, y = random.randint(0, sim_window - 50), random.randint(0, sim_window - 50)
    maxWidth = sim_window - x
    maxHeight = sim_window - y
    width, height = random.randint(20, maxWidth), random.randint(20, maxHeight)

    return x, y, width, height


def getRand():
    return random.randint(0, sim_window)


def getWalls(greenCords):
    x, y, width, height = greenCords
    big = 4
    pen = [Wall(x, y, big, height),
           Wall(x, y, width, big),
           Wall(x + width, y, big, height),
           Wall(x, y + height, width + big, big)]

    # random gate side
    # TODO make it random sides
    gate = 1  # random.randint(0, 3)
    newWidth = (pen[gate].rect.width / 2.5)

    rect1 = pygame.Rect(pen[gate].rect.x, pen[gate].rect.y, pen[gate].rect.width, pen[gate].rect.height)
    rect1.width = newWidth
    pen.append(Wall(rect1.x, rect1.y, rect1.width, rect1.height))

    rect2 = pygame.Rect(pen[gate].rect.x, pen[gate].rect.y, pen[gate].rect.width, pen[gate].rect.height)
    rect2.width = newWidth
    rect2 = rect2.move(newWidth * 1.5 + 2, 0)
    pen.append(Wall(rect2.x, rect2.y, rect2.width, rect2.height))

    del pen[gate]

    return pen


greenCords = getRandGreen()
wallsArr = getWalls(greenCords)
SHEEP_IN = 0


def drawPenWalls():
    for i in range(0, len(wallsArr)):
        pygame.draw.rect(window, convertColor("BROWN"), wallsArr[i].rect)


# Font
font = pygame.font.Font('freesansbold.ttf', 24)
numberText = font.render(str(currentSprite), True, WHITE, BLACK)
numberTextRect = numberText.get_rect()
numberTextRect.center = (sim_window * .95, sim_window * .055)

typeText = font.render(str(currentSprite), True, WHITE, BLACK)
typeTextRect = typeText.get_rect()
typeTextRect.center = (sim_window * .90, sim_window * .025)

scoreText = font.render(str(SHEEP_IN), True, (255, 0, 0), (0, 255, 0))
scoreTextRect = scoreText.get_rect()
scoreTextRect.center = (greenCords[0] + greenCords[2] / 2, greenCords[1] + greenCords[3] / 2)


def convertColor(color):
    # rgb is a 3tuple from 0-1, convert to 0-255
    rgb = colors.to_rgb(color)
    return rgb[0] * 255, rgb[1] * 255, rgb[2] * 255


# x and y are point to find if in circle
def isInside(center, body):
    return pow(body.rect.x - center.rect.x, 2) + pow(body.rect.y - center.rect.y, 2) <= pow(center.rad, 2)


def drawCircle(body):
    pygame.draw.circle(window, body.color, [body.rect.x, body.rect.y], body.rad, 1)


def drawImg(body):
    # center the sprites
    x = body.rect.x - body.img.get_width() / 2
    y = body.rect.y - body.img.get_height() / 2

    window.blit(body.img, (x, y))


def draw(body):
    pygame.draw.rect(window, body.color, body.rect)
    drawCircle(body)
    drawPenWalls()
    drawImg(body)


def toggleInPen(body):
    if body.type != "DOG":
        body.inPen = (greenCords[0] < body.rect.x < greenCords[0] +
                      greenCords[2] and greenCords[1] < body.rect.y < greenCords[1] + greenCords[3])


def inWindow(body):
    if body.rect.x <= 0:
        body.rect.x = 0
    elif sim_window <= body.rect.x:
        body.rect.x = sim_window

    if body.rect.y <= 0:
        body.rect.y = 0
    elif sim_window <= body.rect.y:
        body.rect.y = sim_window


def isObstructed(body) -> bool:
    for i in range(0, len(wallsArr)):
        if wallsArr[i].rect.colliderect(body.rect):
            return True

    return False


def move(body, x, y):
    tempX = body.rect.x
    tempY = body.rect.y
    body.rect = body.rect.move(x, y)
    if isObstructed(body):
        body.rect.x = tempX
        body.rect.y = tempY

    inWindow(body)


def moveAway(body, bodies, index):
    for i in range(len(bodies)):
        if index != i:
            if bodies[i].type != "DOG" and isInside(body, bodies[i]):

                (dx, dy) = (bodies[i].rect.x - body.rect.x, bodies[i].rect.y - body.rect.y)
                angle = math.degrees(math.atan2(float(dx), float(dy)))

                speed = bodies[i].speed
                speedMod = speed * 1.5

                if -180 < angle < -135:
                    move(bodies[i], -speed, -speedMod)

                if -135 < angle < -90:
                    move(bodies[i], -speedMod, -speed)
                if -90 < angle < -45:
                    move(bodies[i], -speedMod, speed)

                if -45 < angle < 0:
                    move(bodies[i], -speed, speedMod)

                if 0 < angle < 45:
                    move(bodies[i], speed, speedMod)

                if 45 < angle < 90:
                    move(bodies[i], speedMod, speed)
                if 90 < angle < 135:
                    move(bodies[i], speedMod, -speed)

                if 135 < angle < 180:
                    move(bodies[i], speed, -speedMod)


#  0 1 2
#  3 4 5
#  6 7 8
def randMove(body, rand):
    if rand <= 2:
        move(bodies[i], 0, -body.speed)
    elif rand >= 6:
        move(bodies[i], 0, body.speed)

    if rand % 3 == 0:
        move(bodies[i], -body.speed, 0)
    elif (rand - 2) % 3 == 0:
        move(bodies[i], body.speed, 0)


def addBodies(count, type, color, x, y, rad, speed):
    newBodies = []
    for i in range(count):
        if type == "DOG":
            newBodies.append(Dog(type, color, getRand(), getRand(), rad, speed, 5, 5))
        elif type == "SHEEP":
            newBodies.append(Sheep(type, color, getRand(), getRand(), rad, speed, 2, 2))

    return newBodies


def setCurrentSprite(index):
    if index < 0:
        return len(bodies) - 1
    elif len(bodies) - 1 < index:
        return 0
    return index


def checkKeyEvents(body, keys, currentSprite):
    if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
        pygame.quit()
        sys.exit()

    if event.type == KEYDOWN and event.key == K_w or keys[pygame.K_w]:
        body.WisPressed = True
    elif event.type == KEYUP and event.key == K_w or keys[pygame.K_w]:
        body.WisPressed = False

    if event.type == KEYDOWN and event.key == K_a or keys[pygame.K_a]:
        body.setAisPressed(True)
    elif event.type == KEYUP and event.key == K_a or keys[pygame.K_a]:
        body.setAisPressed(False)

    if event.type == KEYDOWN and event.key == K_s or keys[pygame.K_s]:
        body.SisPressed = True
    elif event.type == KEYUP and event.key == K_s or keys[pygame.K_s]:
        body.SisPressed = False

    if event.type == KEYDOWN and event.key == K_d or keys[pygame.K_d]:
        body.setDisPressed(True)
    elif event.type == KEYUP and event.key == K_d or keys[pygame.K_d]:
        body.setDisPressed(False)

    if event.type == KEYDOWN and event.key == K_LSHIFT or keys[pygame.K_LSHIFT]:
        body.setSneak()

    if event.type == KEYDOWN and event.key == K_0:
        body.randMove = not body.randMove

    if event.type == KEYDOWN and event.key == K_LEFT:
        currentSprite = setCurrentSprite(currentSprite - 1)
    if event.type == KEYDOWN and event.key == K_RIGHT:
        currentSprite = setCurrentSprite(currentSprite + 1)

    return currentSprite


def checkMoveKeys(body):
    speed = body.speed / 2 if body.sneak else body.speed

    if body.WisPressed:
        move(body, 0, -speed)
    if body.AisPressed:
        move(body, -speed, 0)
    if body.SisPressed:
        move(body, 0, speed)
    if body.DisPressed:
        move(body, speed, 0)

    if body.sneak:
        body.rad = body.sneakRad
    else:
        body.rad = body.regRad


bodies = (addBodies(1, "DOG", "TAN", getRand(), getRand(), rad=100, speed=2) +
          addBodies(10, "SHEEP", "WHITE", getRand(), getRand(), rad=10, speed=1))

while 1:
    pygame.draw.rect(window, BLACK, (0, 0, sim_window, sim_window))
    pygame.draw.rect(window, (0, 255, 0), greenCords)

    window.blit(numberText, numberTextRect)
    window.blit(typeText, typeTextRect)
    window.blit(scoreText, scoreTextRect)
    textColor = convertColor(bodies[currentSprite].color)
    typeText = font.render(bodies[currentSprite].type, True, textColor, BLACK)
    numberText = font.render(str(currentSprite), True, textColor, BLACK)
    scoreText = font.render(str(SHEEP_IN), True, (255, 0, 0), (0, 255, 0))

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        currentSprite = checkKeyEvents(bodies[currentSprite], keys, currentSprite)

    checkMoveKeys(bodies[currentSprite])

    SHEEP_IN = 0

    # check if any bodies need to move away
    for i in range(len(bodies)):
        moveAway(bodies[i], bodies, i)
        if bodies[i].randMove:
            randMove(bodies[i], random.randint(0, 8))

        toggleInPen(bodies[i])
        if bodies[i].inPen:
            SHEEP_IN += 1

        draw(bodies[i])

    pygame.display.update(pygame.Rect(0, 0, sim_window, sim_window))
    clock.tick(144)
