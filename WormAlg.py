import pygame
from pygame.locals import*
import os
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ARCHIVOS = r"C:\Users\Usuario\AppData\Local\Programs\Python\Python35"

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

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("papu")

clock = pygame.time.Clock()

x = 200
y = 200

head = Rect(x, y, 30, 30)

array = []

radius = 5

while True:
    clock.tick(30)

    screen.fill((0,0,0))

    pygame.draw.circle(screen, (218, 112, 214), (100,100), radius)

    radius += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            switch(array)
            array[0]=[x, y]

    pygame.display.flip()
