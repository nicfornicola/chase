
import pygame
import sys
from pygame.locals import *
import random
from bodies import Body

# x and y are point to find if in circle 
def isInside(center, body):

    return ((body.x - center.x) * (body.x - center.x) +
            (body.y - center.y) * (body.y - center.y) <= center.rad * center.rad)


def drawCircle(body):
    pygame.draw.circle(window, body.color, [body.x, body.y], body.rad, 1) 

def draw(surface, body, size: float):    
    for i in range(0, size):
        pygame.draw.line(surface, body.color, (body.x, body.y - 1), (body.x,  body.y + 2), abs(size))
        drawCircle(body)

def inWindow(body):
    return 0 < body.x < sim_window and  0 < body.y < sim_window

def moveAway(bodies):
    dog = bodies[0]
    sheeps = bodies[:0] + bodies[0+1:]
    for i in range(len(sheeps)):
        if(isInside(dog, sheeps[i])):
            if(sheeps[i].x < dog.x):
                sheeps[i].x = sheeps[i].x - 1
            elif(dog.x < sheeps[i].x):
                sheeps[i].x = sheeps[i].x + 1

            if(sheeps[i].y < dog.y):
                sheeps[i].y = sheeps[i].y - 1
            elif(dog.y < sheeps[i].y):
                sheeps[i].y = sheeps[i].y + 1

    return [dog] + sheeps

#  0 1 2
#  3 4 5
#  6 7 8
def randMove(body, rand):
    tiles = 1
    if(body.color == "TAN"):
        tiles = 4
    print(rand)
    if(rand == 4):
        print("still")
        return body

    if(rand <= 2):
        print("up")
        body.y = body.y - tiles
    elif(rand >= 6):
        print("down")
        body.y = body.y + tiles

    if(rand % 3 == 0):
        print("left")
        body.x = body.x - tiles
    elif((rand-2) % 3 == 0):
        print("right")
        body.x = body.x + tiles

    return body


bodies = [Body("TAN",100,100,200), 
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),
          Body("WHITE",105,105,20),]
sim_window = 800
pygame.init()
window = pygame.display.set_mode((sim_window, sim_window))
screenColor = (255,255,255)
window.fill(0)
pygame.display.update(pygame.Rect(0,0,sim_window,sim_window))

while 1:
    pygame.draw.rect(window,(0,0,0),(0,0,sim_window,sim_window))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_w:
            bodies[0].y = bodies[0].y - 4
        if event.type == KEYDOWN and event.key == K_a:
            bodies[0].x = bodies[0].x - 4
        if event.type == KEYDOWN and event.key == K_s:
            bodies[0].y = bodies[0].y + 4
        if event.type == KEYDOWN and event.key == K_d:
            bodies[0].x = bodies[0].x + 4


    #check if any bodies need to move away
    bodies = moveAway(bodies)
    for i in range(len(bodies)):
        if(inWindow(bodies[i])):
            bodies[i] = randMove(bodies[i], random.randint(0, 8))
        else:
            bodies[i].x = sim_window/2
            bodies[i].y = sim_window/2
        if(bodies[i].color == "TAN"):
            size = 6
        else: 
            size = 3
        draw(window, bodies[i], size=size)

    pygame.display.update(pygame.Rect(0,0,sim_window,sim_window))
