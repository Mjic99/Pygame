import pygame
import random
from pygame.locals import*
import os
import sys

SCREEN_DIMS = (800,600)
BLACK = (0,0,0)
WHITE = (255,255,255)

dirs = {
    K_UP:(0,-1),
    K_DOWN:(0,1),
    K_RIGHT:(1,0),
    K_LEFT:(-1,0)
}

walls = [
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "                    ",
    "               A    ",
    "                    ",
    "             A      ",
    "             A      ",
    "       A     A      ",
    "                    "]

class culebra:

    def __init__(self):
        self.thicc = 40
        self.px = 80
        self.py = 80
        self.speedx = 0
        self.speedy = self.thicc
        self.rect = Rect(self.px,self.py,self.thicc,self.thicc)
        self.body = []
        self.time = pygame.time.get_ticks()

    def step(self):
        self.rect.topleft = (self.px,self.py)
        pygame.draw.rect(screen, BLACK, self.rect)

        n_time = pygame.time.get_ticks()

        if (n_time - self.time) >= 400: 
            self.px += self.speedx
            self.py += self.speedy
            self.time = n_time
            switch(self.body)
            if len(self.body)>0:
                self.body[0]=self.rect.topleft

            for i in range(1, len(self.body)):
                if self.body[i] == self.rect.topleft:
                    pygame.event.post(pygame.event.Event(USEREVENT, code="kill"))
            
        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_DIMS[0] or self.rect.centery < 0 or self.rect.centery > SCREEN_DIMS[1]:
            pygame.event.post(pygame.event.Event(USEREVENT, code="kill"))


    def direccionar(self, key):
        try:
            self.speedx = self.thicc*dirs[key][0]
            self.speedy = self.thicc*dirs[key][1]
        except:
            pass

    def eat(self):
        self.body.append(0)
        switch(self.body)
        if len(self.body)>0:
            self.body[0]=self.rect.topleft
        self.px += self.speedx
        self.py += self.speedy
        self.rect.topleft = (self.px,self.py)

    def serpenteo(self):
        for i in range(len(self.body)):
            pygame.draw.rect(screen, BLACK, (self.body[i][0],self.body[i][1],self.thicc,self.thicc))
        


class comidita:
    
    def __init__(self):
        self.px = None
        self.py = None
        self.spawn()
        self.rect = Rect(self.px,self.py,40,40)

    def update(self, player):
        if self.rect.colliderect(player.rect):
            player.eat()
            self.spawn()
            self.rect.topleft = (self.px,self.py)
        pygame.draw.rect(screen, (255,0,0), self.rect)

    def spawn(self):
        self.px = random.randint(0,(SCREEN_DIMS[0]-40)/40)*40
        self.py = random.randint(0,(SCREEN_DIMS[1]-40)/40)*40

        

def switch(array):
    for i in range(len(array)-1, 0, -1):
        array[i] = array[i-1]

pygame.init()
screen = pygame.display.set_mode(SCREEN_DIMS)
pygame.display.set_caption("papu")

clock = pygame.time.Clock()

snake = culebra()
food = comidita()


while True:
    screen.fill(WHITE)

    pos = [0,0]
    for row in walls:
        for i in row:
            if i == "A":
                pygame.draw.rect(screen,(100,100,100), (pos[0],pos[1],40,40))
            pos[0]+=40
        pos[1]+=40

    snake.step()
    snake.serpenteo()
    food.update(snake)

    for i in range(0, SCREEN_DIMS[0], 40):
        pygame.draw.line(screen, (100,100,100), (i,0), (i,SCREEN_DIMS[1]))

    for i in range(0, SCREEN_DIMS[1], 40):
        pygame.draw.line(screen, (100,100,100), (0,i), (SCREEN_DIMS[0],i))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            snake.direccionar(event.key)
            if event.key == K_SPACE:
                snake.eat()
        if event.type == USEREVENT:
            if event.code == "kill":
                pygame.draw.rect(screen, (0,0,255), (100,100,SCREEN_DIMS[0]-100,SCREEN_DIMS[1]-100))
                font = pygame.font.Font(None, 60)
                screen.blit(font.render("Super Coin Get", True, WHITE), (100,100,SCREEN_DIMS[0]-100,SCREEN_DIMS[1]-100))
                pygame.time.delay(3000)
                pygame.quit()
                sys.exit()

    pygame.display.flip()
