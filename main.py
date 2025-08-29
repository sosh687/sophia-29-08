import pygame

# Isso inicio e  modulo do Pygame
pygame.init()

WIDTH, HEIGTH = 800,600

screen = pygame.displayset_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Menu Joguinho")

running = True

while running:
    for event in pygame.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip() 

pygame.quit