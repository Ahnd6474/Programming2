""" mpCollision
    step 4 of mailPilot
    add audio and collision 
    detection
"""
    
import pygame, random
pygame.init()

screen = pygame.display.set_mode((640, 480))

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("plane.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        if not pygame.mixer:
            print "problem with sound"
        else:
            pygame.mixer.init()
            self.sndYay = pygame.mixer.Sound("yay.ogg")
            self.sndThunder = pygame.mixer.Sound("thunder.ogg")
            self.sndEngine = pygame.mixer.Sound("engine.ogg")
            self.sndEngine.play(-1)

        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex, 430)
        
        
        
class Island(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("island.gif")
        self.image = self.image.convert()
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
      
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Cloud.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()
    
    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(5, 10)
        self.dx = random.randrange(-2, 2)
        
def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Mail Pilot! mpCollision.py - collisions and sounds")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    plane = Plane()
    island = Island()
    cloud = Cloud()
    
    allSprites = pygame.sprite.Group(island, plane, cloud)
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        #check collisions
        if plane.rect.colliderect(island.rect):
            plane.sndYay.play()
            island.reset()
        if plane.rect.colliderect(cloud.rect):
            plane.sndThunder.play()
            cloud.reset()
            
        
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
        
    plane.sndEngine.stop()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
if __name__ == "__main__":
    main()
            