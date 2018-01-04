import pygame
from pygame.locals import*
import os
import sys

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
ARCHIVOS = r"C:\Users\Usuario\AppData\Local\Programs\Python\Python35\pong"

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

class Pelota(pygame.sprite.Sprite):
    def __init__(self, sonido_punto):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bola.png", ARCHIVOS, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH/2
        self.rect.centery = SCREEN_HEIGHT/2
        self.speed = [3,3]
        self.sonido_punto = sonido_punto
        self.sonido_punto.set_volume(0.6)

    def update(self):
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.sonido_punto.play()
            self.rect.centerx = SCREEN_WIDTH/2
            self.rect.centery = SCREEN_HEIGHT/2
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed[1] = -self.speed[1]
        self.rect.move_ip((self.speed[0],self.speed[1]))

    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            self.speed[0]=-self.speed[0]

class Paleta(pygame.sprite.Sprite):

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("paleta.png",ARCHIVOS,alpha=False)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = SCREEN_HEIGHT/2

    def humano(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0

    def cpu(self, objetivo):
        self.speed = [0, 2.5]
        if objetivo.speed[0] >= 0 and objetivo.rect.centerx >= SCREEN_WIDTH/2:
            if self.rect.centery > objetivo.rect.centery:
                self.rect.centery -= self.speed[1]
            if self.rect.centery < objetivo.rect.centery:
                self.rect.centery += self.speed[1]

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("papu")

    fondo = load_image("fondopong.jpg",ARCHIVOS,alpha=False)
    pygame.mixer.music.load("The Fall Of Troy - F C P R E M I X 8-Bit.mp3")
    pygame.mixer.music.play(-1, 9.9)
    pygame.mixer.music.set_volume(0.5)
    sonido_punto = load_sound("wilhelm_scream.ogg",ARCHIVOS)

    bola = Pelota(sonido_punto)
    jugador1 = Paleta(25)
    npc = Paleta(615)

    clock = pygame.time.Clock()
    pygame.key.set_repeat(1,25)
    pygame.mouse.set_visible(False)

    while True:
        screen.blit(fondo,(0,0))
        screen.blit(bola.image, bola.rect)
        screen.blit(jugador1.image, jugador1.rect)
        screen.blit(npc.image, npc.rect)
        pygame.display.flip()

        clock.tick(60)
        jugador1.humano()
        bola.update()
        bola.colision(jugador1)
        bola.colision(npc)
        npc.cpu(bola)
        
        pos_mouse = pygame.mouse.get_pos()
        mov_mouse = pygame.mouse.get_rel()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    jugador1.rect.centery -=5
                elif event.key == K_DOWN:
                    jugador1.rect.centery +=5
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    jugador1.rect.centery +=0
                elif event.key == K_DOWN:
                    jugador1.rect.centery +=0
            if mov_mouse[1] != 0:
                jugador1.rect.centery = pos_mouse[1]
                

if __name__ == "__main__":
    main()
