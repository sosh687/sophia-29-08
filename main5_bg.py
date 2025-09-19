import pygame
import os

# Inicializando o Pygame
pygame.init()

# Tamanho da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # janela redimensionável
pygame.display.set_caption("Jogo com fundo e pulo")

# Cor de fundo padrão (usada caso a imagem não carregue)
BG_COLOR = (30, 30, 40)

# Carregar imagem do personagem
image_file = "player.png"  # Coloque o nome correto da sua imagem aqui
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()
    img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # centraliza a imagem
else:
    print("Imagem do personagem não encontrada!")
    img = None
    img_rect = None

# Carregar imagem de fundo
background_file = "background.png"
if os.path.exists(background_file):
    background = pygame.image.load(background_file).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
else:
    print("Imagem de fundo não encontrada!")
    background = None

# Configurações do movimento
SPEED = 5
JUMP_STRENGTH = 15
GRAVITY = 1
VELOCITY_Y = 0
JUMPING = False

# Últimas dimensões (para redimensionamento do fundo)
last_width, last_height = WIDTH, HEIGHT

# Função para centralizar imagem ao redimensionar
def centralizar_imagem(rect, width, height):
    rect.center = (width // 2, height // 2)

# Função de pulo
def jump():
    global VELOCITY_Y, JUMPING
    if not JUMPING:
        VELOCITY_Y = -JUMP_STRENGTH  # inicia o pulo para cima
        JUMPING = True

# Função que atualiza gravidade
def update_gravity():
    global VELOCITY_Y, JUMPING
    img_rect.y += VELOCITY_Y
    VELOCITY_Y += GRAVITY  # adiciona gravidade
    if img_rect.bottom >= HEIGHT:  # não deixa cair além do chão
        img_rect.bottom = HEIGHT
        VELOCITY_Y = 0
        JUMPING = False

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Redimensionar a janela
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            if background:
                background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            centralizar_imagem(img_rect, WIDTH, HEIGHT)
            last_width, last_height = WIDTH, HEIGHT

    # Controles de movimento
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        img_rect.x -= SPEED
    if keys[pygame.K_RIGHT]:
        img_rect.x += SPEED
    if keys[pygame.K_UP]:
        img_rect.y -= SPEED
    if keys[pygame.K_DOWN]:
        img_rect.y += SPEED
    if keys[pygame.K_SPACE]:  # Pulo
        jump()

    # Atualizar gravidade
    update_gravity()

    # Preencher tela
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # Desenhar personagem
    if img:
        screen.blit(img, img_rect.topleft)

    # Atualizar tela
    pygame.display.flip()

pygame.quit()
