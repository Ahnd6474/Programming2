
# CardGame.py
''' Basic classes for Card, Deck and Hand along with a
    game loop that allows card movement, card flipping,
    card position resetting, and deck rotation
'''

import pygame, random
from pygame.locals import *
from pygame.font import *



# some colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
DARKGRAY = ( 47, 79, 79)

RED   = ( 255,   0,   0)
GREEN = (   0, 255,   0)
DARKGREEN = ( 0, 155, 0)
BLUE  = ( 0,   0,   255)

CARD_OFFSET = 16

# ----------------------------------------------------------


class Card(pygame.sprite.Sprite):
    # represents a playing card

    suitNames = ["Clubs", "Diamonds", "Hearts", "Spades"]

    rankNames = [None, "Ace", "2", "3", "4", "5", "6", "7", 
                 "8", "9", "10", "Jack", "Queen", "King"]


    def __init__(self, suit, rank, cardIm, backIm):
        super().__init__()
        self.suit = suit
        self.rank = rank
        self.image = cardIm
        self.rect = self.image.get_rect()
        self.backIm = backIm
        self.isFacing = True


    def __str__(self):
        # Return a human-readable string representation
        return '%s of %s' % (Card.rankNames[self.rank],
                             Card.suitNames[self.suit])

    def flip(self):
        self.isFacing =  not self.isFacing


    def draw(self, screen):
        if self.isFacing:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.backIm, self.rect)
    

    def isBelow(self, mousePos):
        return self.rect.collidepoint(mousePos)


    # compare this card to other, first by suit, then rank

    def __lt__(self, other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2

    def __gt__(self, other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 > t2

    def __eq__(self, other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 == t2


# ----------------------------------------------------------


class Deck(pygame.sprite.Sprite):
    # represents a deck of cards
    
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('deck.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.name = "deck"
        self.none = pygame.image.load('none.png').convert()

        cardsSheet = pygame.image.load('cards.png').convert()
        cardWidth = cardsSheet.get_width()/13
        cardHeight = cardsSheet.get_height()/4
        backIm = pygame.image.load('back.png').convert()
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                x = (rank-1)*cardWidth
                y = suit*cardHeight
                cardIm = cardsSheet.subsurface(x, y, cardWidth, cardHeight).convert()
                card = Card(suit, rank, cardIm, backIm)
                self.cards.append(card)


    def __str__(self):
        if self.isEmpty():
            return "deck is empty\n"
        else:
            res = []
            for card in self.cards:
                res.append(str(card))
            return '\n'.join(res)


    def printRange(self):
        if self.isEmpty():
            print("deck is empty")
        else:
            print("Bottom --> Top of Deck:")
            for card in self.cards[:3]:
                print(" ", str(card))
            print("...")
            for card in self.cards[-3:]:
                print(" ", str(card))
        print("")


    def draw(self, screen):
        if self.isEmpty():
            screen.blit(self.none, self.rect)
        else:
            screen.blit(self.image, self.rect)
            topCard = self.cards[-1]
            topCard.rect.topleft = self.rect.topleft
            topCard.draw(screen)


    def isBelow(self, mousePos):
        return self.rect.collidepoint(mousePos)


    def addCard(self, card):
        # add a card to the deck
        self.cards.append(card)


    def removeCard(self, card):
        # remove a card from the deck
        self.cards.remove(card)


    def insertCard(self, idx, card):
        # insert a card into the deck
        self.cards.insert(idx, card)


    def popCard(self, i=-1):
        # remove and return a card from the deck.
        # by default, pops the last card
        return self.cards.pop(i)


    def shuffle(self):
        # shuffle the cards in this deck
        random.shuffle(self.cards)


    def sort(self):
        # sort the cards in ascending order
        self.cards.sort()


    def isEmpty(self):
        return (len(self.cards) == 0)


    def deal(self, hand, num):
        # Move num cards to the hand in sorted order
        cards = []   # make a new list for sorting
        for i in range(num):
            if self.isEmpty(): # if out of cards
                break
            cards.append( self.popCard() )
        cards.sort()

        # copy sorted list into hand
        for c in cards:
            hand.addCard(c)
        hand.reset()


# ----------------------------------------------------------


class Hand(Deck):
    # represents a hand of playing cards
    
    def __init__(self, label, pos):
        super().__init__(pos)
        self.cards = []
        self.label = label
        self.name = "hand"


    def __str__(self):
        str = self.label + "'s hand"
        if self.isEmpty():
            str = str + " is empty\n"
        else:
            str = str + ":\n"
        return str + Deck.__str__(self) + "\n"


    def draw(self, screen):
        str = self.label + "'s hand"
        if self.isEmpty():
            str = str + " is empty"
            screen.blit(font.render(str, True, WHITE), self.topleft)
        else:
            for card in self.cards:
                card.draw(screen)

            y = self.rect.y + self.cards[0].rect.height + 12
            screen.blit(font.render(str, True, WHITE), (self.rect.x, y))


    def isBelow(self, mousePos):
        # look in reverse order of cards since last card is the 'top' one
        for card in reversed(self.cards):  
            if card.isBelow(mousePos):
                return card
        return None


    def reset(self):
        # reset position of cards
        x = self.rect.x
        for c in self.cards:
            c.rect.topleft = (x, self.rect.y)
            x += CARD_OFFSET   # hand is spread horizontally


# -----------------------------------------------


def selectCard(hands, pos):
    for h in hands:
        card = h.isBelow(pos)
        if not card is None:
            return card
    return None


# ------------ main --------------

pygame.init()
screen = pygame.display.set_mode([640,480])
screen.fill(DARKGREEN)
pygame.display.set_caption("Card Game")

scrWidth, scrHeight = screen.get_size()

font = pygame.font.Font(None, 30)


# create the deck
deck = Deck((300,20))
deck.shuffle()

# create two hands of 5 cards each

hand1 = Hand("Andrew", (20,20))
deck.deal(hand1, 5)

hand2 = Hand("John", (20,200))
deck.deal(hand2, 5)

hands = [hand1, hand2]

# print start state of game
print(hand1)
print(hand2)
deck.printRange()


# game vars
mousePos = (scrWidth/2, scrHeight/2)
selectedCard = None

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)


    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == MOUSEMOTION:  # move selected card with mouse
            if selectedCard is not None:
                mPos = pygame.mouse.get_pos()
                selectedCard.rect.x += (mPos[0] - mousePos[0])
                selectedCard.rect.y += (mPos[1] - mousePos[1])
                mousePos = mPos

        # left button is pressed to select a card or the deck
        if event.type == MOUSEBUTTONDOWN and \
                 pygame.mouse.get_pressed()[0] and \
                 selectedCard is None: 
            mousePos = pygame.mouse.get_pos()
            selectedCard = selectCard(hands, mousePos)
            if selectedCard is None:    # try the deck
                if deck.isBelow(mousePos):
                    deck.insertCard(0, deck.popCard())  # move top to bottom
                    # deck.printRange()

        # middle button is pressed to reset the cards to their starting pos
        if event.type == MOUSEBUTTONDOWN and \
                 pygame.mouse.get_pressed()[1]:
            for h in hands:
                h.reset()

        # right button is pressed to flip the card under the mouse
        if event.type == MOUSEBUTTONDOWN and \
                 pygame.mouse.get_pressed()[2]:
            mPos = pygame.mouse.get_pos()
            card = selectCard(hands, mPos)
            if card is not None:
                card.flip()
            else:    # try the deck
                if deck.isBelow(mPos):
                    deck.cards[-1].flip()
    


        # mouse-up cancels selected card (if there is one)
        if event.type == MOUSEBUTTONUP:
            selectedCard = None

            
    # update game


    # redraw game
    screen.fill(DARKGREEN)

    for h in hands:
        h.draw(screen)
    deck.draw(screen)

    pygame.display.update()


pygame.quit()
