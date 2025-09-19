import pygame
import os

# Inicializando o Pygame
pygame.init()

# Definindo tamanho da janela
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo com Imagens")

# Carregar o fundo
bg_file = "background.png"
if os.path.exists(bg_file):
    background = pygame.image.load(bg_file).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # ajusta ao tamanho da tela
else:
    print("Background não encontrado!")
    background = None

# Carregar o player
player_file = "player.png"
if os.path.exists(player_file):
    player = pygame.image.load(player_file).convert_alpha()
    player_rect = player.get_rect(center=(WIDTH // 2, HEIGHT // 2))
else:
    print("Player não encontrado!")
    player = None
    player_rect = None

# Carregar o passarinho
bird_file = "passarinho.png"
if os.path.exists(bird_file):
    bird = pygame.image.load(bird_file).convert_alpha()
    bird_rect = bird.get_rect(topleft=(50, 50))  # posição inicial
else:
    print("Passarinho não encontrado!")
    bird = None
    bird_rect = None

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenhar fundo
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((30, 30, 40))  # fallback

    # Desenhar player
    if player:
        screen.blit(player, player_rect.topleft)

    # Desenhar passarinho
    if bird:
        screen.blit(bird, bird_rect.topleft)

    # Atualizar a tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()
