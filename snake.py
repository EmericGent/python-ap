import pygame
import random as rd

(WIDTH,HEIGHT) = (640,360)
SIDE = 20
X = WIDTH//SIDE
Y = HEIGHT//SIDE
FRAMERATE = 60
LIGHTG = (170,215,81)
DARKG = (162,209,73)
BLUE = (70,116,233)
RED = (231,71,29)
flag = True
lost = True
snake = []
highscore = 0
dif = 10

pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))

while flag :
    #ce bloc permet de reset le jeu quand le joueur perd
    if lost :
        SCREEN.fill(LIGHTG)
        for i in range(X) :
            for j in range(Y) :
                if (i+j+1)%2 :
                    sq = pygame.Rect(SIDE*i,SIDE*j,SIDE,SIDE)
                    pygame.draw.rect(SCREEN,DARKG,sq)
        if highscore < len(snake) :
            highscore = len(snake)
        snake = [(6,5),(5,5),(4,5)]
        dir = 'stop'
        eaten = True
        xf = 0
        yf = 0
        adv = 0
        lost = False
        for p in snake :
            sq = pygame.Rect(SIDE*p[0],SIDE*p[1],SIDE,SIDE)
            pygame.draw.rect(SCREEN,BLUE,sq)
    #ce bloc permet de réagir au inputs : dans l'ordre : quitter le jeu,
    #changer de direction, faire pause, changer la difficulté (plus dif est grand, plus le jeu est dur)
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
            if event.key == pygame.K_p :
                dir = 'stop'
            if event.key == pygame.K_r :
                lost = True
            if dir == 'stop' :
                if event.key == pygame.K_i :
                    dif = 7
                if event.key == pygame.K_j :
                    dif = 10
                if event.key == pygame.K_k :
                    dif = 20
    #on parcourt le serpent pour savoir si la tête ou le fruit est dans le serpent
    head = snake[0]
    headinsnake = 0
    for sqr in snake :
        if sqr == (xf,yf) :
            eaten = True
        if sqr == head :
            headinsnake += 1
    #on arrête le jeu si jamais une des conditions de mort est remplie
    if headinsnake > 1 :
        lost = True
    if head[0] < 0 or head[0] > X-1 :
        lost = True
    if head[1] < 0 or head[1] > Y-1 :
        lost = True
    #on allonge le serpent si jamais un fruit est mangé
    if eaten :
        xf = rd.randint(0,X-1)
        yf = rd.randint(0,Y-1)
        fruit = pygame.Rect(SIDE*xf,SIDE*yf,SIDE,SIDE)
        pygame.draw.rect(SCREEN,RED,fruit)
    #on ne fait avancer le serpent qu à certaines frames
    #pour avoir 60 tick/s pour capter les inputs mais 
    #avoir un serpent qui avance à une vitesse raisonnable
    #et on change la couleur des carrés qui évoluent
    adv += 1
    if adv >= FRAMERATE//dif or eaten :
        adv = 0
        if dir == 'right' :
            snake = [(head[0]+1,head[1])]+snake
        if dir == 'up' :
            snake = [(head[0],head[1]-1)]+snake
        if dir == 'left' :
            snake = [(head[0]-1,head[1])]+snake
        if dir == 'down' :
            snake = [(head[0],head[1]+1)]+snake
        if not eaten and dir != 'stop' :
            tail = snake.pop()
            checker = pygame.Rect(SIDE*tail[0],SIDE*tail[1],SIDE,SIDE)
            if (tail[0]+tail[1]+1)%2 :
                pygame.draw.rect(SCREEN,DARKG,checker)
            else :
                pygame.draw.rect(SCREEN,LIGHTG,checker)
    newsq = pygame.Rect(SIDE*head[0],SIDE*head[1],SIDE,SIDE)
    pygame.draw.rect(SCREEN,BLUE,newsq)
    eaten = False
    CLOCK.tick(FRAMERATE)
    pygame.display.set_caption('Score '+str(len(snake))+' Highscore '+str(highscore))
    pygame.display.update()

pygame.quit()
quit(0)