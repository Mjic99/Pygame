import pygame
import random
from pygame.locals import*
import os
import sys

SCREEN_DIMS = (800,600)
BLACK = (0,0,0)
WHITE = (255,255,255)

walls=[]
for i in range(int(600/40)):
    walls.append([])
    for j in range(int(800/40)):
        walls[i].append(" ")

pygame.init()
screen = pygame.display.set_mode(SCREEN_DIMS)
pygame.display.set_caption("Crea tu mapa")

clock = pygame.time.Clock()
text = pygame.font.Font(None, 40)


while True:
    
    screen.fill(WHITE)
    
    pos = [0,0]
    for row in walls:
        pos[0]=0
        for i in row:
            if i == "A":
                pygame.draw.rect(screen, BLACK, (pos[0],pos[1],40,40))
            pos[0]+=40
        pos[1]+=40

    
    for i in range(0, SCREEN_DIMS[0], 40):
        pygame.draw.line(screen, (100,100,100), (i,0), (i,SCREEN_DIMS[1]))

    for i in range(0, SCREEN_DIMS[1], 40):
        pygame.draw.line(screen, (100,100,100), (0,i), (SCREEN_DIMS[0],i))
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            xd = pygame.mouse.get_pos()
            x = int((xd[0]-(xd[0]%40))/40)
            y = int((xd[1]-(xd[1]%40))/40)
            walls[y][x]="A"
        elif event.type == pygame.KEYDOWN:
            snake.direccionar(event.key)
            if event.key == K_SPACE:
                pass
                
    pygame.display.flip()
