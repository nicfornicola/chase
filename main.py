
import pygame
import sys
from pygame.locals import *
import random
from bodies import Body
from matplotlib import colors
import matplotlib.pyplot as plt
pygame.display.set_caption('Chase')
from math import sin,cos,radians

tick = True
sim_window = 800
currentSprite = 0
pygame.init()
window = pygame.display.set_mode((sim_window, sim_window))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
window.fill(0)
pygame.display.update(pygame.Rect(0, 0, sim_window, sim_window))

def getRandGreen():
    x, y = random.randint(0, sim_window-50), random.randint(0, sim_window-50)
    maxWidth = sim_window - x
    maxHeight = sim_window - y
    width, height = random.randint(20, maxWidth), random.randint(20, maxHeight)
    
    return (x, y, width, height)

greenCords = getRandGreen()
SHEEP_IN = 0

# Font
font = pygame.font.Font('freesansbold.ttf', 24)
numberText = font.render(str(currentSprite), True, WHITE, BLACK)
numberTextRect = numberText.get_rect()
numberTextRect.center = (sim_window * .95, sim_window * .055)

typeText = font.render(str(currentSprite), True, WHITE, BLACK)
typeTextRect = typeText.get_rect()
typeTextRect.center = (sim_window * .90, sim_window * .025)

scoreText = font.render(str(SHEEP_IN), True, (255,0,0), (0,255,0))
scoreTextRect = scoreText.get_rect()
scoreTextRect.center = (greenCords[0]+greenCords[2]/2, greenCords[1]+greenCords[3]/2)


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

def inPen(body):
    if(greenCords[0] < body.x and greenCords[1] < body.y and body.x < greenCords[0]+greenCords[2] and body.y < greenCords[1]+greenCords[3]):
        body.inPen = True
    else:
        body.inPen = False
    return body
        
def inWindow(body):
    ltrb = [0,0,0,0]

    if(body.x <= 0):
        ltrb[0] = 1
    if(body.y <= 0):
        ltrb[1] = 1
    if(sim_window <= body.x):
        ltrb[2] = 1
    if(sim_window <= body.y):
        ltrb[3] = 1

    return ltrb

def addBodies(count, type, color, x, y, rad, speed, randLoc):
    newBodies = []
    for i in range(count):
        if(randLoc):
            newBodies.append(Body(type, color, getRand(), getRand(), rad, speed))
        else:
            newBodies.append(Body(type, color, x, y, rad, speed))

    return newBodies

def move(body, x, y):
   
    ltrb = inWindow(body)

    if(ltrb[0]):
        body.x = 0
    elif(ltrb[2]):
        body.x = sim_window

    if(ltrb[1]):
        body.y = 0
    elif(ltrb[3]):
        body.y = sim_window
    
    body.x += x
    body.y += y
    return body

def moveAway(body, bodies):
    for i in range(len(bodies)):
        if(isInside(body, bodies[i]) and bodies[i].type != "DOG"):
            if(bodies[i].x < body.x):
                bodies[i] = move(bodies[i], -1, 0)
            elif(body.x < bodies[i].x):
                bodies[i] = move(bodies[i], 1, 0)
            if(bodies[i].y < body.y):
                bodies[i] = move(bodies[i], 0, -1)
            elif(body.y < bodies[i].y):
                bodies[i] = move(bodies[i], 0, 1)

    return bodies

#  0 1 2
#  3 4 5
#  6 7 8
def randMove(body, rand):
    if(rand == 4):
        return body
    if(rand <= 2):
        body = move(bodies[i], 0, -body.speed)
    elif(rand >= 6):
        body = move(bodies[i], 0, body.speed)

    if(rand % 3 == 0):
        body = move(bodies[i], -body.speed, 0)
    elif((rand-2) % 3 == 0):
        body = move(bodies[i], body.speed, 0)
    
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

bodies = (addBodies(3,   "DOG",   "TAN",   getRand(), getRand(), rad=150, speed=5, randLoc=True) +
          addBodies(100, "SHEEP", "WHITE", getRand(), getRand(), rad=10,  speed=1,  randLoc=True))

while 1:
    pygame.draw.rect(window, BLACK, (0, 0, sim_window, sim_window))
    pygame.draw.rect(window, (0, 255, 0), greenCords)

    window.blit(numberText, numberTextRect)
    window.blit(typeText, typeTextRect)
    window.blit(scoreText, scoreTextRect)
    textColor = convertColor(bodies[currentSprite].color)
    typeText =   font.render(bodies[currentSprite].type, True, textColor, BLACK)
    numberText = font.render(str(currentSprite), True, textColor, BLACK)
    scoreText = font.render(str(SHEEP_IN), True, (255,0,0), (0,255,0))

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
    SHEEP_IN = 0

    #check if any bodies need to move away
    for i in range(len(bodies)):
        if(tick):
            bodies = moveAway(bodies[i], bodies)
            if(bodies[i].randMove):
                bodies[i] = randMove(bodies[i], random.randint(0, 8))
            
            bodies[i] = inPen(bodies[i])

        if(bodies[i].inPen):
            SHEEP_IN+=1
 
        draw(window, bodies[i], size=3)


    tick = not tick

    pygame.display.update(pygame.Rect(0,0,sim_window,sim_window))
