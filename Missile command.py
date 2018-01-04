import pygame
from pygame.locals import*
import os
import sys
import math
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ARCHIVOS = r"C:\Users\Usuario\AppData\Local\Programs\Python\Python35"
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (218, 112, 214)

def SetVector(origin, target, SquareModule):
    x = target[0] - origin[0]
    y = target[1] - origin[1]
    vector = pygame.math.Vector2(x,y)
    vector.scale_to_length(math.sqrt(SquareModule))
    return vector

def switch(array):
    #Add blank space value to the end of the list
    array.append(0)
    #Get last index
    i = len(array)-1
    #Loop from top to bottom copying the previous item to current index
    while True:
        array[i] = array[i-1]
        i-=1
        if i<=0:
            break

def VanishFromExistence(rect):
    rect = Rect(0,0,0,0)

class Gun(object):
    def __init__(self, posx, posy):
        Buildings.append(self)
        self.rect = Rect(posx, posy, 50, 50)
        self.ammo = 10
    def update(self):
        pygame.draw.rect(screen, BLUE, self.rect)

class PlayerBullet(object):
    def __init__(self, gun, vector, target):
        self.alive = True
        #Store the object in the bullet list
        bullets.append(self)
        #Set initial position to match the gun and consume ammo
        gun.ammo -=1
        self.posx = gun.rect.midtop[0]
        self.posy = gun.rect.midtop[1]
        self.rect = Rect(int(self.posx), int(self.posy), 3, 3)
        #Save the vector and create array to store the tail of rects
        self.vector = vector
        self.array = []
        #Save the target for collision detection and make a copy 
        self.targetRect = Rect(0,0,10,10)
        self.targetRect.center = target
        self.aux = target
        #Radius of the explosion which will increase
        self.radius = 0
        self.exploding = False
    def update(self):
        if self.alive: #Updating movement of bullet
            self.posx += self.vector[0]*deltaTime
            self.posy += self.vector[1]*deltaTime
            self.rect = Rect(int(self.posx), int(self.posy), 3, 3)
            switch(self.array)
            self.array[0]=(self.posx, self.posy)
            for position in self.array:
                pygame.draw.rect(screen, WHITE, Rect((position), (3, 3)))
            pygame.draw.rect(screen, RED, self.rect)
        if self.rect.colliderect(self.targetRect):
            #Target becomes 0 so collision is never detected again (deleting rect?)
            self.targetRect = Rect(0,0,0,0)
            self.array = []
            self.alive = False
            self.exploding = True
    def explosion(self):
        if self.alive == False and self.exploding:
            #Explosion animation
            self.circle = pygame.draw.circle(screen, PURPLE, self.aux, int(self.radius))
            self.radius += 0.4
            #Explosion collision detection
            for enemyBullet in enemyBullets:
                if self.circle.colliderect(enemyBullet.rect):
                    enemyBullet.array = []
                    enemyBullet.rect = Rect(0,-10,0,0) 
                    enemyBullet.alive = False
        if self.radius >= ExplosionSize:
            VanishFromExistence(self.circle)
            self.exploding = False

class EnemyBullet(object):
    def __init__(self, x, y, vector):
        self.alive = True
        enemyBullets.append(self)
        self.posx = x
        self.posy = y 
        self.rect = Rect(int(self.posx), int(self.posy), 3, 3)
        self.vector = vector
        self.array = []
    def update(self):
        global Hits
        if self.alive:
            self.posx += self.vector[0]*deltaTime
            self.posy += self.vector[1]*deltaTime
            self.rect = Rect(int(self.posx), int(self.posy), 3, 3)
            switch(self.array)
            self.array[0]=(self.posx, self.posy)
            for position in self.array:
                pygame.draw.rect(screen, GREEN, Rect((position), (3, 3)))
            pygame.draw.rect(screen, WHITE, self.rect)
        for building in Buildings:
            if building.rect.colliderect(self.rect):
                self.array = []
                self.rect = Rect(0,-10,0,0) 
                self.alive = False
                Hits += 1
                print(Hits)
                if hasattr(building, "ammo"):
                    building.ammo = 0      

class Building(object):
    def __init__(self, posx, posy):
        Buildings.append(self)
        self.rect = Rect(posx, posy, 100, 30)
    def update(self):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
          
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Missile command")
clock = pygame.time.Clock()
getTicksLastFrame = 0
text = pygame.font.Font(None, 40)

Floor = Rect(0, 530, 800, 70)
Leftsector = Rect(0, 0, 266, 600)
Centralsector = Rect(266, 0, 268, 600)
Rightsector = Rect(534, 0, 266, 600)

bullets = []
enemyBullets = []
Buildings = []
PlayerSpeed = 200000
EnemySpeed = 2000
ExplosionSize = 30
waves = 0
waveQuantity = 2
Hits = 0

LeftGun = Gun(100, 500)
MidGun = Gun(350, 500)
RightGun = Gun(650, 500)
Building1 = Building(200, 515)
Building2 = Building(500, 515)

pygame.time.set_timer(USEREVENT, 3000)

while True:
    screen.fill(BLACK)
    clock.tick(60)

    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    
    pygame.draw.rect(screen, BLUE, Floor)
    LeftGun.update()
    MidGun.update()
    RightGun.update()
    Building1.update()
    Building2.update()
    
    LeftAmmo = text.render(str(LeftGun.ammo), True, WHITE, BLUE)
    MidAmmo = text.render(str(MidGun.ammo), True, WHITE, BLUE)
    RightAmmo = text.render(str(RightGun.ammo), True, WHITE, BLUE)
    screen.blit(LeftAmmo, (110, 504))
    screen.blit(MidAmmo, (360, 504))
    screen.blit(RightAmmo, (660, 504))

    if LeftGun.ammo == 0:
        Centralsector = Rect(0, 0, 534, 600)
    if MidGun.ammo == 0:
        Leftsector = Rect(0, 0, 400, 600)
        Rightsector = Rect(400, 0, 400, 600)
    if RightGun.ammo == 0:
        Centralsector = Rect(266, 0, 534, 600)
    if LeftGun.ammo == 0 and MidGun.ammo == 0:
        Rightsector = Rect(0, 0, 800, 600)
    if LeftGun.ammo == 0 and RightGun.ammo == 0:
        Centralsector = Rect(0, 0, 800, 600)
    if MidGun.ammo == 0 and RightGun.ammo == 0:
        Leftsector = Rect(0, 0, 800, 600)

    for bullet in bullets:
        bullet.update()
        bullet.explosion()
        
    for enemyBullet in enemyBullets:
        enemyBullet.update()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            MousePos = pygame.mouse.get_pos()
            if Leftsector.collidepoint(MousePos) and LeftGun.ammo>0:
                PlayerBullet(LeftGun, SetVector(LeftGun.rect.midtop, MousePos, PlayerSpeed), MousePos)
            elif Centralsector.collidepoint(MousePos) and MidGun.ammo>0:
                PlayerBullet(MidGun, SetVector(MidGun.rect.midtop, MousePos, PlayerSpeed), MousePos)
            elif Rightsector.collidepoint(MousePos) and RightGun.ammo>0:
                PlayerBullet(RightGun, SetVector(RightGun.rect.midtop, MousePos, PlayerSpeed), MousePos)
        if event.type == USEREVENT and waves <= waveQuantity:
            waves += 1
            for i in range(6):
                x = random.randint(0, 800)
                y = random.randint(-400, 0)
                if i == 0:
                    EnemyBullet(x, y, SetVector([x,y], MidGun.rect.center, EnemySpeed))
                elif i==1:
                    EnemyBullet(x, y, SetVector([x,y], RightGun.rect.center, EnemySpeed))
                elif i==2 or i==3:
                    EnemyBullet(x, y, SetVector([x,y], LeftGun.rect.center, EnemySpeed))
                elif i==4:
                    EnemyBullet(x, y, SetVector([x,y], Building1.rect.center, EnemySpeed))
                elif i==5:
                    EnemyBullet(x, y, SetVector([x,y], Building2.rect.center, EnemySpeed))

    pygame.display.flip()
