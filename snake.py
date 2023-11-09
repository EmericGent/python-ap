import pygame
import random as rd

pygame.init()
clock = pygame.time.Clock()
(width,height) = (500,250)
side = 20
X = width//side
Y = height//side
screen = pygame.display.set_mode((width,height))
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
flag = True
snake = [(6,5),(5,5),(4,5)]
dir = 1
eaten = False
xf = rd.randint(0,X)
yf = rd.randint(0,Y)
framerate = 60
adv = 0
screen.fill(white)
for i in range(X) :
        for j in range(Y) :
            if (i+j+1)%2 :
                sq = pygame.Rect(side*i,side*j,side,side)
                pygame.draw.rect(screen,black,sq)
for p in snake :
    sq = pygame.Rect(side*p[0],side*p[1],side,side)
    pygame.draw.rect(screen,green,sq)
while flag :
    adv += 1
    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_q :
                flag = False
            if event.key == pygame.QUIT :
                flag = False
            if event.key == pygame.K_RIGHT :
                dir = 1
            if event.key == pygame.K_UP :
                dir = 2
            if event.key == pygame.K_LEFT :
                dir = 3
            if event.key == pygame.K_DOWN :
                dir = 4
    if (xf,yf) in snake :
        eaten = True
    if eaten :
        xf = rd.randint(0,X-1)
        yf = rd.randint(0,Y-1)
    fruit = pygame.Rect(side*xf,side*yf,side,side)
    pygame.draw.rect(screen,red,fruit)
    head = snake[0]
    if head[0] < 0 or head[0] > X-1 :
        flag = False
    if head[1] < 0 or head[1] > Y-1 :
        flag = False
    if snake.count(head) > 1 :
        flag = False
    if adv > 5 or eaten :
        adv = 0
        if dir == 1 :
            snake = [(head[0]+1,head[1])]+snake
        if dir == 2 :
            snake = [(head[0],head[1]-1)]+snake
        if dir == 3 :
            snake = [(head[0]-1,head[1])]+snake
        if dir == 4 :
            snake = [(head[0],head[1]+1)]+snake
        if not eaten :
            tail = snake.pop()
            checker = pygame.Rect(side*tail[0],side*tail[1],side,side)
            if (tail[0]+tail[1]+1)%2 :
                pygame.draw.rect(screen,black,check)
            else :
                pygame.draw.rect(screen,white,check)
#    for p in snake :
#        sq = pygame.Rect(side*p[0],side*p[1],side,side)
#        pygame.draw.rect(screen,green,sq)
    newsq = pygame.Rect(side*head[0],side*head[1],side,side)
    pygame.draw.rect(screen,green,newsq)
    eaten = False
    clock.tick(framerate)
    pygame.display.update()

pygame.quit()
quit(0)