import pygame
from random import randint
import json

pygame.init()

screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)

background_foto = pygame.image.load("sprites/sem título.jpg")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_foto, (50, 0))
    pygame.display.update()