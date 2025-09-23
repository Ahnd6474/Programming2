""" mpPlane
    step 1 of mailPilot
    build plane sprite, 
    control it with mouse
"""
    
import pygame
pygame.init()

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("plane.gif")
        self.rect = self.image.get_rect()
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, 430)
        
def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Mail Pilot! mpPlane.py - creating the Plane sprite")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    plane = Plane()
    
    allSprites = pygame.sprite.Group(plane)
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
            