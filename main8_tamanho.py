import pygame
import os

# Inicializando o Pygame
pygame.init()

# Definindo o tamanho da janela padrão
WIDTH, HEIGHT = 720, 420
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Janela redimensionável
pygame.display.set_caption("Mover Imagem com Setas")

# Definindo a cor de fundo (usada se não houver imagem de fundo)
BG_COLOR = (0, 0, 95)  # tom escuro

# Tamanho dos personagens (um pouco menores)
PLAYER_WIDTH, PLAYER_HEIGHT = 80, 80
TARGET_WIDTH, TARGET_HEIGHT = 50, 50

# Carregar a imagem do personagem principal (jogador)
image_file = "player.png"
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()
    img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
    img_rect = img.get_rect(midbottom=(WIDTH // 2, HEIGHT))  # Inicia no chão
else:
    print("Imagem do personagem não encontrada!")
    img = None
    img_rect = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

# Carregar a imagem do personagem alvo (para ser chutado)
target_file = "passarinho.png"
if os.path.exists(target_file):
    target_img = pygame.image.load(target_file).convert_alpha()
    target_img = pygame.transform.scale(target_img, (TARGET_WIDTH, TARGET_HEIGHT))
    target_rect = target_img.get_rect(midbottom=(WIDTH // 2 + 200, HEIGHT))
else:
    print("Imagem do personagem alvo não encontrada!")
    target_img = None
    target_rect = pygame.Rect(WIDTH // 2 + 200, HEIGHT - TARGET_HEIGHT, TARGET_WIDTH, TARGET_HEIGHT)

# Carregar a imagem de fundo
background_file = "background.png"
if os.path.exists(background_file):
    background_orig = pygame.image.load(background_file).convert()
    background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
else:
    print("Imagem de fundo não encontrada!")
    background_orig = None
    background = None

# Velocidade e física
SPEED = 3
JUMP_STRENGTH = 18
GRAVITY = 0.8
VELOCITY_Y = 0
JUMPING = False

# Variáveis para o alvo chutado
target_velocity_x = 0
target_velocity_y = 0
target_jumping = False
target_gravity = GRAVITY

# Controle redimensionamento
last_width, last_height = WIDTH, HEIGHT

# Limitar movimento para não sair da tela
def limit_movement(rect):
    if rect.left < 0:
        rect.left = 0
    if rect.right > WIDTH:
        rect.right = WIDTH
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > HEIGHT:
        rect.bottom = HEIGHT

# Função para pular do jogador
def jump():
    global VELOCITY_Y, JUMPING
    if not JUMPING:
        VELOCITY_Y = -JUMP_STRENGTH
        JUMPING = True

# Atualiza o pulo do jogador
def update_jump():
    global VELOCITY_Y, JUMPING, img_rect, GRAVITY
    if JUMPING:
        VELOCITY_Y += GRAVITY
        img_rect.y += VELOCITY_Y
        if img_rect.bottom >= HEIGHT:
            img_rect.bottom = HEIGHT
            VELOCITY_Y = 0
            JUMPING = False

# Atualiza o pulo / queda do alvo chutado
def update_target_physics():
    global target_velocity_x, target_velocity_y, target_jumping, target_rect, target_gravity

    if target_jumping:
        target_velocity_y += target_gravity
        target_rect.y += target_velocity_y
        target_rect.x += target_velocity_x

        if target_rect.bottom >= HEIGHT:
            target_rect.bottom = HEIGHT
            target_jumping = False
            target_velocity_y = 0
    else:
        target_velocity_x *= 0.95  # atrito no chão

# Função para "chutar" o alvo
def kick():
    global target_velocity_x, target_velocity_y, target_jumping, target_rect, img_rect
    dist_x = target_rect.centerx - img_rect.centerx
    dist_y = target_rect.centery - img_rect.centery
    distancia = (dist_x ** 2 + dist_y ** 2) ** 0.5

    if distancia < 150:
        target_velocity_x = 20 if dist_x > 0 else -20
        target_velocity_y = -20
        target_jumping = True

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detectar redimensionamento
        current_width, current_height = screen.get_size()
        if current_width != last_width or current_height != last_height:
            WIDTH, HEIGHT = current_width, current_height
            if background_orig:
                background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
            last_width, last_height = current_width, current_height

    # Teclas pressionadas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        img_rect.x -= SPEED
    if keys[pygame.K_RIGHT]:
        img_rect.x += SPEED
    if keys[pygame.K_UP]:
        img_rect.y -= SPEED
    if keys[pygame.K_DOWN]:
        img_rect.y += SPEED

    if keys[pygame.K_SPACE]:
        jump()
    if keys[pygame.K_f]:
        kick()

    limit_movement(img_rect)
    limit_movement(target_rect)
    update_jump()
    update_target_physics()

    # --- Desenhar fundo ---
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # --- Desenhar jogador ---
    if img:
        screen.blit(img, img_rect.topleft)
    else:
        pygame.draw.rect(screen, (255, 0, 0), img_rect)

    # --- Desenhar alvo ---
    if target_img:
        screen.blit(target_img, target_rect.topleft)
    else:
        pygame.draw.rect(screen, (0, 255, 0), target_rect)

    pygame.display.flip()

pygame.quit()
