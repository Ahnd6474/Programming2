
# Snake.py

import pygame, math


class Snake():

    # some colors
    GREEN = ( 0, 255, 0)
    BLUE  = ( 0, 0, 255)
    

    # directions
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


    GROW_TIME = 100


    def __init__(self, scrWidth, scrHeight):
        self.score = 0
        self.maxLength = 10
        self.scrWidth = scrWidth
        self.scrHeight = scrHeight
        self.reset()


    def reset(self):
        self.head = [self.scrWidth/2, self.scrHeight/2]
        self.isDead = False
        self.tail = []
        self.growTime = 0
        self.xDir = -1  # -1 (left), 0, 1 (right)
        self.yDir = 0   # -1 (up), 0, 1 (down)



    def update(self, currTime, dir):
        self.move(currTime, dir)
        self.isDead = self.checkDeath()



    def move(self, currTime, dir):

        # change direction but do not allow reversing
        if dir == Snake.UP and self.yDir != +1:
            self.xDir = 0 
            self.yDir = -1
        elif dir == Snake.DOWN and self.yDir != -1:
            self.xDir = 0
            self.yDir = +1
        elif dir == Snake.LEFT and self.xDir != +1:
            self.xDir = -1
            self.yDir = 0
        elif dir == Snake.RIGHT and self.xDir != -1:
            self.xDir = +1
            self.yDir = 0

        # move head and grow if enough time has passed
        if (currTime - self.growTime) >= Snake.GROW_TIME :
            self.tail.insert(0, [self.head[0], self.head[1]] )
            self.head[0] += (self.xDir*10)
            self.head[1] += (self.yDir*10)
            if len(self.tail) > self.maxLength :
                self.tail.pop( len(self.tail)-1 )
            self.growTime = currTime


    def checkDeath(self):
        for p in self.tail :    # head has touched part of tail?
            if p[0] == self.head[0] and p[1] == self.head[1] :
                return True

        # head has left the window?
        if self.head[0] < 0 or self.head[0] > self.scrWidth-1 or \
           self.head[1] < 0 or self.head[1] > self.scrHeight-1 :
            return True

        return False


    def containsPt(self, pt):
        # is pt near the snake's head or tail?
        if self.distApart(self.head,pt) < 10 :  # near enough
            return true
        for p in self.tail :
            if self.distApart(p,pt) < 10 :  # near enough
                return True
        return False


    def distApart(self, pt1, pt2):
        return math.sqrt( (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2 )


    def grow(self):
        self.maxLength += 1
        self.score += 5




    def draw(self, screen):
        pygame.draw.rect(screen, Snake.BLUE, 
                                         (self.head[0], self.head[1], 10, 10))
        for pt in self.tail :
            pygame.draw.rect(screen, Snake.GREEN, (pt[0], pt[1], 10, 10))


