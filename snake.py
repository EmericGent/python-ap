import pygame
import random as rd

pygame.init()
clock = pygame.time.Clock()
(width,height) = (640,360)
side = 20
X = width//side
Y = height//side
screen = pygame.display.set_mode((width,height))
lightg = (170,215,81)
darkg = (162,209,73)
blue = (70,116,233)
red = (231,71,29)
flag = True
snake = [(6,5),(5,5),(4,5)]
dir = 'right'
eaten = True
xf = 0
yf = 0
framerate = 60
adv = 0
screen.fill(lightg)
for i in range(X) :
        for j in range(Y) :
            if (i+j+1)%2 :
                sq = pygame.Rect(side*i,side*j,side,side)
                pygame.draw.rect(screen,darkg,sq)
for p in snake :
    sq = pygame.Rect(side*p[0],side*p[1],side,side)
    pygame.draw.rect(screen,blue,sq)

while flag :
    adv += 1
    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_q :
                flag = False
            if event.key == pygame.QUIT :
                flag = False
            if event.key == pygame.K_RIGHT :
                dir = 'right'
            if event.key == pygame.K_UP :
                dir = 'up'
            if event.key == pygame.K_LEFT :
                dir = 'left'
            if event.key == pygame.K_DOWN :
                dir = 'down'
    head = snake[0]
    headinsnake = 0
    for sqr in snake :
        if sqr == (xf,yf) :
            eaten = True
        if sqr == head :
            headinsnake += 1
    if headinsnake > 1 :
        flag = False
    if head[0] < 0 or head[0] > X-1 :
        flag = False
    if head[1] < 0 or head[1] > Y-1 :
        flag = False
    if eaten :
        xf = rd.randint(0,X-1)
        yf = rd.randint(0,Y-1)
        fruit = pygame.Rect(side*xf,side*yf,side,side)
        pygame.draw.rect(screen,red,fruit)
    if adv > 5 or eaten :
        adv = 0
        if dir == 'right' :
            snake = [(head[0]+1,head[1])]+snake
        if dir == 'up' :
            snake = [(head[0],head[1]-1)]+snake
        if dir == 'left' :
            snake = [(head[0]-1,head[1])]+snake
        if dir == 'down' :
            snake = [(head[0],head[1]+1)]+snake
        if not eaten :
            tail = snake.pop()
            checker = pygame.Rect(side*tail[0],side*tail[1],side,side)
            if (tail[0]+tail[1]+1)%2 :
                pygame.draw.rect(screen,darkg,checker)
            else :
                pygame.draw.rect(screen,lightg,checker)
    newsq = pygame.Rect(side*head[0],side*head[1],side,side)
    pygame.draw.rect(screen,blue,newsq)
    eaten = False
    clock.tick(framerate)
    pygame.display.update()

pygame.quit()
quit(0)