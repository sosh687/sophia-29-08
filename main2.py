import pygame
import os

# Inicializando o Pygame
pygame.init()

# Definindo tamanho da janela
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Janela com Imagem")

# Definindo cor de fundo (um tom escuro)
BG_COLOR = (30, 30, 40)

# Carregar a imagem
image_file = "player.png"  # Coloque o nome da sua imagem aqui
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()
    img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # centraliza a imagem
else:
    print("Imagem não encontrada!")
    img = None
    img_rect = None

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Preencher fundo
    screen.fill(BG_COLOR)

    # Desenhar a imagem na tela
    if img:
        screen.blit(img, img_rect.topleft)

    # Atualizar a tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()
