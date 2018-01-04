import pygame
from pygame.locals import*
import os
import sys
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ARCHIVOS = r"C:\Users\Usuario\AppData\Local\Programs\Python\Python35"
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (252, 90, 184)
VERDE = (131, 245, 44)
AZUL = (13, 213, 252)
NARANJA = (255, 153, 51)
VVERT = pygame.math.Vector2(0,1)
VHORI = pygame.math.Vector2(1,0)

def load_image(nombre, dir_imagen, alpha=False):
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: "+ruta)
        sys.exit(1)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

def drawBricks(brickmap, bricks, powerups, brickNumber):
    global TILESIZEX
    global TILESIZEY
    bricks = []
    powerups = []
    brickNumber = 0
    x = y = 50
    for row in brickmap:
        for col in row:
            if col == "B":
                brick((x, y))
                brickNumber += 1
            elif col == "P":
                powerup((x, y))
                brickNumber += 1
            x += TILESIZEX+32
        y += TILESIZEY+20
        x = 50
    return brickNumber

class jugador():
    def __init__(self):
        self.posx = pygame.mouse.get_pos()[0]
        self.ancho = 100
        self.rect = Rect((self.posx, 550),(self.ancho, 10))
    def update(self):
        self.posx = pygame.mouse.get_pos()[0]
        self.rect = Rect((self.posx, 550),(self.ancho, 10))
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    def colision(self, pelota):
        if self.rect.colliderect(pelota.ball):
            if pelota.ball.midbottom[0] < self.rect.midtop[0] and pelota.speed[0] > 0:
                pelota.speed[0] = -pelota.speed[0]
            elif pelota.ball.midbottom[0] >= self.rect.midtop[0] and pelota.speed[0] < 0:
                pelota.speed[0] = -pelota.speed[0]
            pelota.speed[1] = -pelota.speed[1]

class pelota():
    def __init__(self):
        self.posx = 400
        self.posy = 500
        self.ball = pygame.draw.circle(screen, ROJO, (self.posx,self.posy), 10)
        self.speed = pygame.math.Vector2(3,3)
    def update(self):
        self.posx += int(self.speed[0])
        self.posy += int(self.speed[1])
        self.ball = pygame.draw.circle(screen, ROJO, (self.posx,self.posy), 10)
    def colisionBordes(self):
        if self.ball.left <= 0 and self.speed[0]<0:
            self.speed[0] = -self.speed[0]
        elif self.ball.right >= SCREEN_WIDTH and self.speed[0]>0:
            self.speed[0] = -self.speed[0]
        elif self.ball.top <= 0 and self.speed[1]<0:
            self.speed[1] = -self.speed[1]
        elif self.ball.bottom >= SCREEN_HEIGHT and self.speed[1]>0:
            self.speed[1] = -self.speed[1]

class brick():
    def __init__(self, pos):
        bricks.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], TILESIZEX, TILESIZEY)
    def __call__(self, pos):
        bricks.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], TILESIZEX, TILESIZEY)

class powerup():
    def __init__(self, pos):
        powerups.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], TILESIZEX, TILESIZEY)
        self.falling = False
        self.color = AZUL
        self.colisionenabled = True
    def __call__(self, pos):
        powerups.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], TILESIZEX, TILESIZEY)
        self.falling = False
        self.color = AZUL
        self.colisionenabled = True
    def alargar(self, barra):
            powerup.rect = pygame.Rect(0,0,0,0)
            pygame.time.set_timer(USEREVENT,4000)
            barra.ancho = 200
    def ralentizar(self, barra, esfera):
            powerup.rect = pygame.Rect(0,0,0,0)
            pygame.time.set_timer(USEREVENT+1,8000)
            esfera.speed.scale_to_length(math.sqrt(8))
        
#http://pygame.org/project-Rect+Collision+Response-1061-.html

powerupswitch = True

level1 = [
            "BBBBBBBB",
            "BBPBBBBB",
            "BBBBBPBB",
            "BBBBPBBB",
            "BBBBBPBB"
          ]

level2 = [
            "B B B B ",
            " B P B B",
            "B B B B ",
            " B B P B",
            "B B B B "
          ]

level3 = [
            " BBPBBB ",
            "B B  B B",
            "BBPBBPBB",
            "B      B",
            "BBPBBBBB"
          ]

bricks = []
powerups = []
levelcount = 1
brickNumber = 0
TILESIZEX = 60
TILESIZEY = 30

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("papu")

clock = pygame.time.Clock()
bola = pelota()
player = jugador()

while True:
    screen.fill(NEGRO)
    if levelcount == 1 and brickNumber == 0:
        brickNumber = drawBricks(level1, bricks, powerups, brickNumber)
    if levelcount == 2 and brickNumber == 0:
        brickNumber = drawBricks(level2, bricks, powerups, brickNumber)
    if levelcount == 3 and brickNumber == 0:
        brickNumber = drawBricks(level3, bricks, powerups, brickNumber)
    player.update()
    player.colision(bola)
    pygame.draw.rect(screen, NARANJA, player.rect)
    bola.update()
    bola.colisionBordes()
    clock.tick(60) 

    for brick in bricks:
        pygame.draw.rect(screen, AZUL, brick.rect)
        if bola.ball.colliderect(brick.rect):
            if bola.ball.left <= brick.rect.right and bola.speed[0]<0 and bola.ball.centerx >= brick.rect.centerx:
                bola.speed[0] = -bola.speed[0]
            elif bola.ball.right >= brick.rect.left and bola.speed[0]>0 and bola.ball.centerx <= brick.rect.centerx:
                bola.speed[0] = -bola.speed[0]
            if bola.ball.top <= brick.rect.bottom and bola.speed[1]<0 and bola.ball.centery >= brick.rect.centery:
                bola.speed[1] = -bola.speed[1]
            elif bola.ball.bottom >= brick.rect.top and bola.speed[1]>0 and bola.ball.centery <= brick.rect.centery:
                bola.speed[1] = -bola.speed[1]
            brick.rect = pygame.Rect(0,0,0,0)
            brickNumber -= 1

    for powerup in powerups:
        pygame.draw.rect(screen, powerup.color, powerup.rect)
        if bola.ball.colliderect(powerup.rect) and powerup.colisionenabled:
            if bola.ball.left <= powerup.rect.right and bola.speed[0]<0 and bola.ball.centerx >= powerup.rect.centerx:
                bola.speed[0] = -bola.speed[0]
            elif bola.ball.right >= powerup.rect.left and bola.speed[0]>0 and bola.ball.centerx <= powerup.rect.centerx:
                bola.speed[0] = -bola.speed[0]
            if bola.ball.top <= powerup.rect.bottom and bola.speed[1]<0 and bola.ball.centery >= powerup.rect.centery:
                bola.speed[1] = -bola.speed[1]
            elif bola.ball.bottom >= powerup.rect.top and bola.speed[1]>0 and bola.ball.centerx <= powerup.rect.centerx:
                bola.speed[1] = -bola.speed[1]
            powerup.colisionenabled = False
            powerup.falling = True
            powerup.rect.inflate_ip(-40,-10)
            powerup.color = VERDE
            brickNumber -= 1
        if powerup.falling:
            powerup.rect.move_ip(0,2)
        if powerup.rect.colliderect(player.rect):
            if powerupswitch:
                powerup.alargar(player)
                powerupswitch = False
            else:
                powerup.ralentizar(player, bola)
                powerupswitch = True
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == USEREVENT:
            player.ancho = 100
        if event.type == USEREVENT+1:
            bola.speed.scale_to_length(math.sqrt(18))
            bola.speed[0] = int(round(bola.speed[0]))
            bola.speed[1] = int(round(bola.speed[1]))
    if brickNumber == 0:
        levelcount +=1
    pygame.display.flip()
