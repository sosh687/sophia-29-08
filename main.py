import pygame

# Isso inicio e  modulo do Pygame
pygame.init()

# Definindo o tamanho da janela
WIDTH, HEIGTH = 800,600
screen = pygame.displayset_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Janela Simples")

# Loop principal do jogo
running = True
while running:
    for event in pygame.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar a tela        
    pygame.display.flip() 

 # Finalizar o Pygame
pygame.ouit()