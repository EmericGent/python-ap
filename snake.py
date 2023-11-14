import argparse
import pygame
import random as rd

parser = argparse.ArgumentParser(description='')
parser.add_argument('--bg_color_1', type = str, default = (170,215,81), help="The first color of the background")
parser.add_argument('--bg_color_2', type = str, default = (162,209,73), help="The second color of the background")
parser.add_argument('--height', type = int, default = 360, help="Height of the game screen")
parser.add_argument('--width', type = int, default = 640, help="Width of the game screen")
parser.add_argument('--fps', type = int, default = 60, help="Framerate of the Game")
parser.add_argument('--fruit_color', type = str, default = (231,71,29), help="Color of the fruit")
parser.add_argument('--snake_color', type = str, default = (70,116,233),  help="Color of the snake")
parser.add_argument('--snake_length', type = int, default = 3, help="Initial lenght of the snake")
parser.add_argument('--tile_size', type = int, default = 20, help="Size of the tile")
args = parser.parse_args()

if args.height%args.tile_size :
    raise ValueError("Height must be a multiple of tile_size")
if args.width%args.tile_size :
    raise ValueError("Width must be a multiple of tile_size")
if args.height//args.tile_size < 12 :
    raise ValueError("The game needs at least 12 rows")
if args.width//args.tile_size < 20 :
    raise ValueError("The game needs at least 20 columns")
if args.snake_color == args.bg_color_1 or args.snake_color == args.bg_color_2 or args.snake_color == args.fruit_color :
    raise ValueError("All the colors must be different from each other")
if args.fruit_color == args.bg_color_1 or args.fruit_color == args.bg_color_2 :
    raise ValueError("All the colors must be different from each other")
if args.bg_color_2 == args.bg_color_1 :
    raise ValueError("All the colors must be different from each other")
if args.snake_length < 2 :
    raise ValueError("The snake is too short")
if args.snake_length > args.width//args.tile_size-8 :
    raise ValueError("The snake is too long")

X = args.width//args.tile_size
Y = args.height//args.tile_size
flag = True
lost = True
snake = []
highscore = 0
dif = 10

pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((args.width,args.height))

while flag :
    #ce bloc permet de reset le jeu quand le joueur perd
    if lost :
        SCREEN.fill(args.bg_color_1)
        for i in range(X) :
            for j in range(Y) :
                if (i+j+1)%2 :
                    sq = pygame.Rect(args.tile_size*i,args.tile_size*j,args.tile_size,args.tile_size)
                    pygame.draw.rect(SCREEN,args.bg_color_2,sq)
        if highscore < len(snake) :
            highscore = len(snake)
        snake = [(3+args.snake_length-i,5)for i in range(args.snake_length)]
        dir = 'stop'
        eaten = True
        xf = 0
        yf = 0
        adv = 0
        lost = False
        for p in snake :
            sq = pygame.Rect(args.tile_size*p[0],args.tile_size*p[1],args.tile_size,args.tile_size)
            pygame.draw.rect(SCREEN,args.snake_color,sq)
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
        fruit = pygame.Rect(args.tile_size*xf,args.tile_size*yf,args.tile_size,args.tile_size)
        pygame.draw.rect(SCREEN,args.fruit_color,fruit)
    #on ne fait avancer le serpent qu à certaines frames
    #pour avoir 60 tick/s pour capter les inputs mais 
    #avoir un serpent qui avance à une vitesse raisonnable
    #et on change la couleur des carrés qui évoluent
    adv += 1
    if adv >= args.fps//dif or eaten :
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
            checker = pygame.Rect(args.tile_size*tail[0],args.tile_size*tail[1],args.tile_size,args.tile_size)
            if (tail[0]+tail[1]+1)%2 :
                pygame.draw.rect(SCREEN,args.bg_color_2,checker)
            else :
                pygame.draw.rect(SCREEN,args.bg_color_1,checker)
    newsq = pygame.Rect(args.tile_size*head[0],args.tile_size*head[1],args.tile_size,args.tile_size)
    pygame.draw.rect(SCREEN,args.snake_color,newsq)
    eaten = False
    CLOCK.tick(args.fps)
    pygame.display.set_caption('Score '+str(len(snake))+' Highscore '+str(highscore))
    pygame.display.update()

pygame.quit()
quit(0)