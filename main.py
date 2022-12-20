
import pygame
import sys
from pygame.locals import *
import random
from bodies import Body
from matplotlib import colors
import matplotlib.pyplot as plt
pygame.display.set_caption('Chase')

tick = True
sim_window = 800
currentSprite = 0
pygame.init()
window = pygame.display.set_mode((sim_window, sim_window))
screenColor = (255,255,255)
window.fill(0)
pygame.display.update(pygame.Rect(0,0,sim_window,sim_window))

# Font
font = pygame.font.Font('freesansbold.ttf', 24)
numberText = font.render(str(currentSprite), True, (255,255,255), (0,0,0))
typeText = font.render(str(currentSprite), True, (255,255,255), (0,0,0))
numberTextRect = numberText.get_rect()
typeTextRect = typeText.get_rect()
numberTextRect.center = (sim_window * .95, sim_window * .055)
typeTextRect.center = (sim_window * .90, sim_window * .025)

def getRand():
    return random.randint(0, sim_window)

# x and y are point to find if in circle 
def isInside(center, body):
    return ((body.x - center.x) * (body.x - center.x) +
            (body.y - center.y) * (body.y - center.y) <= center.rad * center.rad)

def drawCircle(body):
    pygame.draw.circle(window, body.color, [body.x, body.y], body.rad, 1) 

def draw(surface, body, size : float):   
    if(body.type == "DOG"):
        size = 6
 
    for i in range(0, size):
        pygame.draw.line(surface, body.color, (body.x, body.y - 1), (body.x,  body.y + 2), abs(size))
        drawCircle(body)

def inWindow(body):
    return 0 < body.x < sim_window and  0 < body.y < sim_window

def addBodies(count, type, color, x, y, rad, speed, randLoc):
    newBodies = []
    for i in range(count):
        if(randLoc):
            newBodies.append(Body(type, color, getRand(), getRand(), rad, speed))
        else:
            newBodies.append(Body(type, color, x, y, rad, speed))

    return newBodies

def moveAway(dog, bodies):
    for i in range(len(bodies)):
        if(bodies[i].type != "DOG" and isInside(dog, bodies[i])):
            if(bodies[i].x < dog.x):
                bodies[i].x = bodies[i].x - 1
            elif(dog.x < bodies[i].x):
                bodies[i].x = bodies[i].x + 1

            if(bodies[i].y < dog.y):
                bodies[i].y = bodies[i].y - 1
            elif(dog.y < bodies[i].y):
                bodies[i].y = bodies[i].y + 1

    return bodies

#  0 1 2
#  3 4 5
#  6 7 8
def randMove(body, rand):

    if(rand == 4):
        return body

    if(rand <= 2):
        body.y = body.y - body.speed
    elif(rand >= 6):
        body.y = body.y + body.speed

    if(rand % 3 == 0):
        body.x = body.x - body.speed
    elif((rand-2) % 3 == 0):
        body.x = body.x + body.speed

    return body

def setCurrentSprite(index):
    if(index < 0):
        return len(bodies) - 1
    elif(len(bodies) - 1 < index):
        return 0
    return index

def convertColor(color):
    #rgb is a 3tuple from 0-1, convert to 0-255 
    rgb = colors.to_rgb(color)
    return (rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)

bodies = (addBodies(4,   "DOG",   "TAN",   getRand(), getRand(), rad=150, speed=5, randLoc=True) +
          addBodies(100, "SHEEP", "WHITE", getRand(), getRand(), rad=20,  speed=1,  randLoc=True))

while 1:
    pygame.draw.rect(window,(0,0,0),(0,0,sim_window,sim_window))
    window.blit(numberText, numberTextRect)
    window.blit(typeText, typeTextRect)
    textColor = convertColor(bodies[currentSprite].color)
    typeText =   font.render(bodies[currentSprite].type, True, textColor, (0,0,0))
    numberText = font.render(str(currentSprite), True, textColor, (0,0,0))


    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_w or keys[pygame.K_w]:
            bodies[currentSprite].y = bodies[currentSprite].y - bodies[currentSprite].speed
        if event.type == KEYDOWN and event.key == K_a or keys[pygame.K_a]:
            bodies[currentSprite].x = bodies[currentSprite].x - bodies[currentSprite].speed
        if event.type == KEYDOWN and event.key == K_s or keys[pygame.K_s]:
            bodies[currentSprite].y = bodies[currentSprite].y + bodies[currentSprite].speed
        if event.type == KEYDOWN and event.key == K_d or keys[pygame.K_d]:
            bodies[currentSprite].x = bodies[currentSprite].x + bodies[currentSprite].speed
        if event.type == KEYDOWN and event.key == K_0:
            bodies[currentSprite].randMove = not bodies[currentSprite].randMove
        if event.type == KEYDOWN and event.key == K_LEFT:
            currentSprite = setCurrentSprite(currentSprite - 1)
        if event.type == KEYDOWN and event.key == K_RIGHT:
            currentSprite = setCurrentSprite(currentSprite + 1)


    #check if any bodies need to move away
    for i in range(len(bodies)):
        if(tick):
            if(bodies[i].type == "DOG"):
                bodies = moveAway(bodies[i], bodies)

            
            if(inWindow(bodies[i])):
                if(bodies[i].randMove):
                    bodies[i] = randMove(bodies[i], random.randint(0, 8))
            else:
                bodies[i].x = sim_window/2
                bodies[i].y = sim_window/2

        draw(window, bodies[i], size=3)

    tick = not tick


    pygame.display.update(pygame.Rect(0,0,sim_window,sim_window))
