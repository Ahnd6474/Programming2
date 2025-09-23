
# SnakeGame.py

import pygame, random
from pygame.locals import *
from pygame.font import *

from Snake import Snake
from Food import Food


# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
BLUE  = ( 0,   0,   255)



# -------------------------------------------



def drawGameOver(screen):
    im = font.render("Game Over", True, BLACK)
    x = (scrWidth - im.get_width())/2
    y = (scrHeight - im.get_height())/2
    screen.blit(im, (x,y))



# ---------- main -------------


pygame.init()
screen = pygame.display.set_mode((400,400))
screen.fill(WHITE)
pygame.display.set_caption("Snake Game")

scrWidth, scrHeight = screen.get_size()


# create sprites
snake = Snake(scrWidth, scrHeight)
food = Food(snake, scrWidth, scrHeight)


# game vars
dir = Snake.LEFT

font = pygame.font.SysFont('Comic Sans MS', 30)


clock = pygame.time.Clock()

running = True    
while running:
    clock.tick(30)
    currTime = pygame.time.get_ticks()

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT: 
            running = False
    
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_UP or event.key == K_w:
                dir = Snake.UP 
            elif event.key == K_DOWN or event.key == K_s:
                dir = Snake.DOWN 
            elif event.key == K_LEFT or event.key == K_a:
                dir = Snake.LEFT 
            elif event.key == K_RIGHT or event.key == K_d:
                dir = Snake.RIGHT 

            elif event.key == K_RETURN:
                if snake.isDead:   # to restart the game
                    snake.reset()
                    food.reset()


    # update game
    if not snake.isDead:
        snake.update(currTime, dir)
        food.update(currTime)
        

    # redraw game
    screen.fill(WHITE)
    food.draw(screen)
    snake.draw(screen)

    scoreStr = font.render(str(snake.score), True, BLACK)
    screen.blit(scoreStr,(10,0))

    if snake.isDead:
        drawGameOver(screen)

    pygame.display.update()


pygame.quit()


