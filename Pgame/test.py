import pygame
from pygame.locals import *

pygame.init()

screenSize = (640, 480)
screen = pygame.display.set_mode(screenSize)
screen.fill((255,255,255))    # white background

pygame.display.set_caption("Hello, World!")  # set title bar

clock = pygame.time.Clock()
running = True
while running:  # game loop
    clock.tick(30)   # set loop speed to 30 FPS

    # handle events
    for event in pygame.event.get():
        print(event)
        if event.type == QUIT:
            running = False

    # update game state  (nothing yet)

    # redraw game
    pygame.display.update()

pygame.quit()
