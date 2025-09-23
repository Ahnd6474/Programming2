""" mpIsland
    step 2 of mailPilot
    add island, move it,
    don't worry about collisions yet
"""
    
import pygame, random
pygame.init()

screen = pygame.display.set_mode((640, 480))

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("plane.gif")
        self.rect = self.image.get_rect()
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, 430)
        
        
class Island(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("island.gif")
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dy = 5
    
    def update(self):
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()
            
    def reset(self):
        self.rect.top = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
    
    
def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Mail Pilot! mpIsland - adding the Island")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    plane = Plane()
    island = Island()
    
    allSprites = pygame.sprite.Group(island, plane)
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
            