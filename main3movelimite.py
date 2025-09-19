
import pygame
import os

# Inicializando o Pygame
pygame.init()

# Definindo o tamanho da janela padrão
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Janela redimensionável
pygame.display.set_caption("Mover Imagem com Setas")

# Definindo a cor de fundo
BG_COLOR = (193, 0, 40)  # cor de fundo

# Carregar a imagem
image_file = "GAME/player.png"
if os.path.exists(image_file):
    img = pygame.image.load(image_file).convert_alpha()
    img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
else:
    print("Imagem não encontrada!")
    img = None
    img_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 0, 0)

# Velocidade de movimento
SPEED = 1  # pixels por movimento

# Centralizar imagem
def centralize_image():
    global img_rect, WIDTH, HEIGHT
    img_rect.center = (WIDTH // 2, HEIGHT // 2)

# Limite de movimento
def limit_movement():
    global img_rect, WIDTH, HEIGHT
    if img_rect.left < 0:
        img_rect.left = 0
    if img_rect.right > WIDTH:
        img_rect.right = WIDTH
    if img_rect.top < 0:
        img_rect.top = 0
    if img_rect.bottom > HEIGHT:
        img_rect.bottom = HEIGHT

# Controle de redimensionamento
last_width, last_height = WIDTH, HEIGHT

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verifica redimensionamento
    current_width, current_height = screen.get_size()
    if current_width != last_width or current_height != last_height:
        WIDTH, HEIGHT = current_width, current_height
        centralize_image()
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

    # Limitar movimento
    limit_movement()

    # Desenhar fundo e imagem
    screen.fill(BG_COLOR)
    if img:
        screen.blit(img, img_rect.topleft)

    pygame.display.flip()

pygame.quit()
