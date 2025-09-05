import pygame

# Início do módulo do Pygame
pygame.init()

# Definindo o tamanho da janela
WIDTH, HEIGHT = 1000, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Janela Simples")

# Definindo uma cor de fundo (azul escuro)
BG_COLOR = (20, 20, 100)

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Preencher a tela com a cor de fundo
    screen.fill(BG_COLOR)

    # Atualizar a tela        
    pygame.display.flip() 

# Finalizar o Pygame
pygame.quit()
