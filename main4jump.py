import pygame
import os

# Inicializando o Pygame
pygame.init()

# Definindo o tamanho da janela padrão
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Janela redimensionável
pygame.display.set_caption("Movimento + Pulo com Gravidade e Chão")

# Definindo a cor de fundo
BG_COLOR = (193, 0, 40)  # cor de fundo (um tom escuro)

# Definindo a cor do chão
FLOOR_COLOR = (50, 200, 50)  # verde
FLOOR_HEIGHT = 50            # altura do chão

# Carregar a imagem
image_file = "game\\player.png"  # Coloque o nome correto da sua imagem aqui
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()  # Carregar a imagem
    img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centraliza a imagem
else:
    print("Imagem não encontrada!")

# Velocidade de movimento
SPEED = 3  # pixels por movimento

# Configuração do pulo e gravidade
JUMP_STRENGTH = 12   # Força do pulo (quanto maior, mais alto o pulo)
GRAVITY = 0.6        # Gravidade (quanto maior, mais rápido cai)
VELOCITY = 0         # Velocidade no eixo Y
isJumping = False    # Controle de pulo

# Função para centralizar a imagem conforme o tamanho da tela
def centralize_image():
    global img_rect, WIDTH, HEIGHT
    img_rect.center = (WIDTH // 2, HEIGHT // 2)

# Função para limitar o movimento dentro da tela
def limit_movement():
    global img_rect, WIDTH, HEIGHT
    if img_rect.left < 0:
        img_rect.left = 0
    if img_rect.right > WIDTH:
        img_rect.right = WIDTH

# Função para iniciar o pulo
def jump():
    global VELOCITY, isJumping
    if not isJumping:  # Só inicia o pulo se não estiver pulando
        VELOCITY = -JUMP_STRENGTH
        isJumping = True

# Função para atualizar a física do pulo
def update_jump():
    global VELOCITY, isJumping, img_rect
    if isJumping:
        VELOCITY += GRAVITY  # Aplica gravidade
        img_rect.y += VELOCITY  # Atualiza a posição no eixo Y

        # Chão está na posição HEIGHT - FLOOR_HEIGHT
        if img_rect.bottom >= HEIGHT - FLOOR_HEIGHT:
            img_rect.bottom = HEIGHT - FLOOR_HEIGHT
            isJumping = False
            VELOCITY = 0  # Reseta a velocidade

# Variáveis para controle de redimensionamento
last_width, last_height = WIDTH, HEIGHT

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verifica se o tamanho da janela foi alterado
    current_width, current_height = screen.get_size()

    if current_width != last_width or current_height != last_height:
        WIDTH, HEIGHT = current_width, current_height
        centralize_image()
        last_width, last_height = current_width, current_height

    # Pega as teclas pressionadas
    keys = pygame.key.get_pressed()

    # Movimento lateral (com diagonais se quiser)
    if keys[pygame.K_LEFT]:
        img_rect.x -= SPEED
    if keys[pygame.K_RIGHT]:
        img_rect.x += SPEED

    # Movimento vertical manual (opcional)
    if keys[pygame.K_UP]:
        img_rect.y -= SPEED
    if keys[pygame.K_DOWN]:
        img_rect.y += SPEED

    # Pulo (barra de espaço)
    if keys[pygame.K_SPACE]:
        jump()

    # Atualiza física do pulo
    update_jump()

    # Limita movimento nas laterais
    limit_movement()

    # Preencher o fundo
    screen.fill(BG_COLOR)

    # Desenhar o chão
    pygame.draw.rect(screen, FLOOR_COLOR, (0, HEIGHT - FLOOR_HEIGHT, WIDTH, FLOOR_HEIGHT))

    # Desenhar a imagem na tela
    screen.blit(img, img_rect.topleft)

    # Atualizar a tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()
