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
v = 1
eaten = False
xf = rd.randint(0,X)
yf = rd.randint(0,Y)
c = 0

while flag :
    c += 1
    screen.fill(white)
    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_l :
                flag = False
            if event.key == pygame.K_RIGHT :
                if v == 3 :
                    flag = False
                v = 1
            if event.key == pygame.K_UP :
                if v == 4 :
                    flag = False
                v = 2
            if event.key == pygame.K_LEFT :
                if v == 1 :
                    flag = False
                v = 3
            if event.key == pygame.K_DOWN :
                if v == 2 :
                    flag = False
                v = 4
    for i in range(X) :
        for j in range(Y) :
            if (i+j+1)%2 :
                sq = pygame.Rect(side*i,side*j,side,side)
                pygame.draw.rect(screen,black,sq)
    for p in snake :
        sq = pygame.Rect(side*p[0],side*p[1],side,side)
        pygame.draw.rect(screen,green,sq)
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
    if c > 5 or eaten :
        c = 0
        if v == 1 :
            snake = [(head[0]+1,head[1])]+snake
        if v == 2 :
            snake = [(head[0],head[1]-1)]+snake
        if v == 3 :
            snake = [(head[0]-1,head[1])]+snake
        if v == 4 :
            snake = [(head[0],head[1]+1)]+snake
        if not eaten :
            snake.pop()
    eaten = False
    clock.tick(60)
    pygame.display.update()

pygame.quit()