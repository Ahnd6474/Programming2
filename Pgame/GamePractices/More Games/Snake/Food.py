
# Food.py


import pygame, random, math




class Food():

    GROW_TIME = 3000


    def __init__(self, snake, scrWidth, scrHeight):
        self.snake = snake
        self.scrWidth = scrWidth
        self.scrHeight = scrHeight
        self.reset()
        self.eatSnd = pygame.mixer.Sound('eat.wav')
        self.eatSnd.set_volume(1)


    def reset(self):
        self.food = []
        self.growTime = 0


    def update(self, currTime):
        # add food if enough time has passed
        if (currTime - self.growTime >= Food.GROW_TIME) or \
           len(self.food) == 0:
            x,y = self.randomPos()
            self.food.append([x,y])
            self.growTime = currTime 
        
        # has snake eaten some food?
        for pt in self.food :
             if self.distApart(self.snake.head, pt) < 8 :  # very near
                self.snake.grow()
                self.food.remove(pt)
                self.eatSnd.play()



    def randomPos(self):
        # generate a position not near existing food or the snake
        isUnique = False
        while not isUnique:
            x = random.randint(0, self.scrWidth-1)
            y = random.randint(0, self.scrHeight-1)
            isUnique = True
            if self.snake.containsPt([x,y]) or self.inFood([x,y]):
                isUnique = False
        return x,y


    def inFood(self, pt):
        # is pt near existing food?
        for p in self.food :
            if self.distApart(p,pt) < 10 :  # near enough
                return True
        return False


    def distApart(self, pt1, pt2):
        return math.sqrt( (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2 )


    def draw(self, screen):
        for pt in self.food :   # red squares
            pygame.draw.rect(screen, (255,0,0), (pt[0], pt[1], 10, 10))



