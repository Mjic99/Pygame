import pygame
import random
from pygame.locals import*
import sys
import os
SCREEN_WIDTH = 898
SCREEN_HEIGHT = 639
CARPETA = r"C:\Users\Usuario\AppData\Local\Programs\Python\Python35\shooter"
COLOR_FONDO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

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

def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    try:
        sonido = pygame.mixer.Sound(ruta)
    except (pygame.error) as message:
        print("No se pudo cargar el sonido: ",ruta)
        sonido = None
    return sonido

class trump():
    def __init__(self):
        self.faces = [load_image("trump.png", CARPETA, alpha=True),load_image("trump2.png", CARPETA, alpha=True)]
        self.image = self.faces[0]
        self.rect = self.image.get_rect()

class player():
    def __init__(self):
        self.mano = load_image("hand.png", CARPETA, alpha=True)
        self.rect_mano = self.mano.get_rect()
        self.crosshair = load_image("crosshair.png", CARPETA, alpha=True)
        self.cross_rect = self.crosshair.get_rect()

pygame.init()
pygame.font.init()
    
pygame.display.set_caption("repoio")
clock = pygame.time.Clock()

fondo = load_image("fondo.jpg", CARPETA, alpha=False)

pygame.mouse.set_visible(False)

trump_alive = True

pygame.time.set_timer(USEREVENT+1, 3000)

president = trump()
jugador = player()

i=0 #para ir por el array de 2 imagenes

puntaje=0

texto = pygame.font.Font(None, 40)

while True:
    SCREEN.blit(fondo,(0,0))
    clock.tick(30) 

    if trump_alive:
        SCREEN.blit(president.image, president.rect)
    SCREEN.blit(jugador.mano, jugador.rect_mano)
    SCREEN.blit(jugador.crosshair, jugador.cross_rect)

    jugador.rect_mano.midtop = pygame.mouse.get_pos()
    jugador.cross_rect.centerx = pygame.mouse.get_pos()[0]
    jugador.cross_rect.centery = pygame.mouse.get_pos()[1]

    mensaje = texto.render("Puntaje: "+str(puntaje), True,(0,0,0))
    SCREEN.blit(mensaje, (0,0))

    for event in pygame.event.get():
        if event.type == USEREVENT+1:
            trump_alive = True
            president.rect = president.image.get_rect()
            president.rect.x = random.randint(0,898-president.rect.width)
            president.rect.y = random.randint(0,639-president.rect.height)
            president.image = president.faces[i]
            if i==0:
                i = 1
            elif i==1:
                i = 0
            pygame.time.set_timer(USEREVENT+2, 750)
        if event.type == USEREVENT+2:
            trump_alive = False
            president.rect = pygame.Rect(0,0,0,0)
        if event.type == pygame.MOUSEBUTTONDOWN and president.rect.collidepoint(pygame.mouse.get_pos()):
            trump_alive = False
            president.rect = pygame.Rect(0,0,0,0)
            puntaje +=1
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
