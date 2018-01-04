import pygame
import random
from pygame.locals import*
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARPETA = r"C:\Users\Usuario\AppData\Local\Programs\Python\Python35\snake"
COLOR_FONDO = (0, 0, 0)
COLOR_SNAKE = (255, 255, 255)
ROJO = (255, 0, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

cabeza_x = 400
cabeza_y = 300
objeto_x = 0
objeto_y = 0
agarrado = False

def ColocarItem():
    global objeto_x
    global objeto_y
    objeto_x = random.randint(0,SCREEN_WIDTH-10)
    objeto_y = random.randint(0,SCREEN_HEIGHT-10)

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.craneo = pygame.draw.rect(screen,COLOR_SNAKE,(cabeza_x, cabeza_y, 10, 10))
        self.velocidad = [3, 3]
        self.cola = []
        self.total = 0
        for i in range(self.total):
            pygame.draw.rect(screen,COLOR_SNAKE,(self.cola[i][0], self.cola[i][1], 10, 10))
    def update(self):
        for i in range(self.total-1):
            self.cola[i] = self.cola[i+1]
        self.cola[self.total-1] = [self.craneo.x,self.craneo.y]

class Cola(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.cuadrado = pygame.draw.rect(screen,COLOR_SNAKE,(x, y, 10, 10))

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.elemento = pygame.draw.rect(screen,ROJO,(x, y, 10, 10))
    def recolectado(self, cabeza):
        if self.elemento.colliderect(cabeza.craneo):
            ColocarItem()
            cabeza.total += 1
            agarrado = True
        
            
up = False
down = False
right = False
left = False
pygame.init()
    
pygame.display.set_caption("Esneik")
clock = pygame.time.Clock()
ColocarItem()

while True:  
    clock.tick(5)
    #instanciar la cabeza de la serpiente y llenar el background de negro
    serpiente = Snake()
    screen.fill(COLOR_FONDO)

    #colocar el recolectable y verificar si es recolectado
    objeto = Item(objeto_x, objeto_y)
    objeto.recolectado(serpiente)
    serpiente.update()

    #comprobar el input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                up = True
                down = False
                right = False
                left = False
            elif event.key == K_DOWN:
                down = True
                up = False
                right = False
                left = False
            elif event.key == K_RIGHT:
                right = True
                down = False
                up = False
                left = False
            elif event.key == K_LEFT:
                left = True
                down = False
                right = False
                up = False
    #mover la cabeza
    if up is True:
        cabeza_y -=10
    if down is True:
        cabeza_y +=10
    if right is True:
        cabeza_x +=10
    if left is True:
        cabeza_x -=10
    
    pygame.display.update()
