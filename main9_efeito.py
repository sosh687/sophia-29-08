import pygame
import os
import time

# --- Inicialização ---
pygame.init()

# Janela
WIDTH, HEIGHT = 720, 420
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("main9_efeito - completo")

# Fallback de cor de fundo
BG_COLOR = (50, 50, 60)

# Tamanhos (ajuste conforme as suas imagens)
PLAYER_WIDTH, PLAYER_HEIGHT = 90, 225
TARGET_WIDTH, TARGET_HEIGHT = 90, 225

# Caminhos das imagens (coloque os arquivos na mesma pasta do .py)
PLAYER_FILE = "player.png"
TARGET_FILE = "passarinho.png"
BACKGROUND_FILE = "background.png"

# Carregar jogador
if os.path.exists(PLAYER_FILE):
    img = pygame.image.load(PLAYER_FILE).convert_alpha()
    img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
    img_rect = img.get_rect(midbottom=(WIDTH // 2, HEIGHT))
else:
    print("Aviso: player não encontrado:", PLAYER_FILE)
    img = None
    img_rect = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

# Carregar alvo
if os.path.exists(TARGET_FILE):
    target_img = pygame.image.load(TARGET_FILE).convert_alpha()
    target_img = pygame.transform.scale(target_img, (TARGET_WIDTH, TARGET_HEIGHT))
    target_rect = target_img.get_rect(midbottom=(WIDTH // 2 + 200, HEIGHT))
else:
    print("Aviso: alvo não encontrado:", TARGET_FILE)
    target_img = None
    target_rect = pygame.Rect(WIDTH // 2 + 200, HEIGHT - TARGET_HEIGHT, TARGET_WIDTH, TARGET_HEIGHT)

# Carregar fundo
if os.path.exists(BACKGROUND_FILE):
    background_orig = pygame.image.load(BACKGROUND_FILE).convert()
    background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
else:
    background_orig = None
    background = None
    print("Aviso: fundo não encontrado:", BACKGROUND_FILE)

# --- Física / constantes ---
SPEED = 3
JUMP_STRENGTH = 18
GRAVITY = 0.8

VELOCITY_Y = 0.0
JUMPING = False

target_velocity_x = 0.0
target_velocity_y = 0.0
target_jumping = False
target_gravity = GRAVITY

# Efeito de dano
damage_time = 0.0
damage_duration = 0.22  # segundos do tint vermelho

# Vida do alvo
TARGET_MAX_HP = 100
target_hp = TARGET_MAX_HP
DAMAGE_PER_KICK = 12

# Controle redimensionamento
last_width, last_height = WIDTH, HEIGHT

# Clock (FPS)
clock = pygame.time.Clock()
FPS = 60

# --- Funções utilitárias ---
def limit_movement(rect):
    """Evita que o rect saia da tela atual (usa WIDTH, HEIGHT atuais)."""
    if rect.left < 0:
        rect.left = 0
    if rect.right > WIDTH:
        rect.right = WIDTH
    if rect.top < 0:
        rect.top = 0
    if rect.bottom > HEIGHT:
        rect.bottom = HEIGHT

def jump():
    """Inicia pulo do jogador se não estiver pulando."""
    global VELOCITY_Y, JUMPING
    if not JUMPING:
        VELOCITY_Y = -JUMP_STRENGTH
        JUMPING = True

def update_jump():
    """Atualiza física do pulo do jogador."""
    global VELOCITY_Y, JUMPING, img_rect
    if JUMPING:
        VELOCITY_Y += GRAVITY
        img_rect.y += VELOCITY_Y
        if img_rect.bottom >= HEIGHT:
            img_rect.bottom = HEIGHT
            VELOCITY_Y = 0
            JUMPING = False

def update_target_physics():
    """Aplica gravidade e arrasto ao alvo chutado."""
    global target_velocity_x, target_velocity_y, target_jumping, target_rect
    # Aplica velocidades
    target_rect.x += int(target_velocity_x)
    target_rect.y += int(target_velocity_y)
    # Aplica gravidade
    target_velocity_y += target_gravity

    # Colisão com chão
    if target_rect.bottom >= HEIGHT:
        target_rect.bottom = HEIGHT
        target_velocity_y = 0
        target_jumping = False
        # atrito quando no chão
        target_velocity_x *= 0.90
        if abs(target_velocity_x) < 0.05:
            target_velocity_x = 0.0
    else:
        # no ar reduz levemente a velocidade horizontal
        target_velocity_x *= 0.995

def kick():
    """Chuta o alvo se estiver perto. Aplica velocidade e causa dano."""
    global target_velocity_x, target_velocity_y, target_jumping, damage_time, target_hp
    dx = target_rect.centerx - img_rect.centerx
    dy = target_rect.centery - img_rect.centery
    distancia = (dx ** 2 + dy ** 2) ** 0.5
    if distancia < 150:
        # aplica impulso no alvo
        target_velocity_x = 20.0 if dx > 0 else -20.0
        target_velocity_y = -20.0
        target_jumping = True
        damage_time = time.time()
        # aplica dano
        target_hp -= DAMAGE_PER_KICK
        if target_hp < 0:
            target_hp = 0

def draw_health_bar(surface, rect, current_hp, max_hp, bar_width=80, bar_height=10, offset_y=10):
    """Desenha uma barra de vida acima do rect."""
    x = rect.centerx - bar_width // 2
    y = rect.top - offset_y - bar_height
    # borda
    pygame.draw.rect(surface, (30, 30, 30), (x - 1, y - 1, bar_width + 2, bar_height + 2))
    # fundo da barra
    pygame.draw.rect(surface, (60, 60, 60), (x, y, bar_width, bar_height))
    # preenchimento proporcional
    if max_hp > 0:
        fill = int(bar_width * (current_hp / max_hp))
    else:
        fill = 0
    # cor (verde -> amarelo -> vermelho)
    pct = current_hp / max_hp if max_hp else 0
    if pct > 0.6:
        color = (80, 200, 80)
    elif pct > 0.3:
        color = (230, 200, 80)
    else:
        color = (230, 80, 80)
    pygame.draw.rect(surface, color, (x, y, fill, bar_height))

# --- Loop principal ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            # Atualiza tamanho da janela
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            # redimensiona fundo se existia
            if background_orig:
                background = pygame.transform.scale(background_orig, (WIDTH, HEIGHT))
            # garante personagens no chão após redim.
            img_rect.bottom = HEIGHT
            target_rect.bottom = HEIGHT
            last_width, last_height = WIDTH, HEIGHT

    # Controles
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

    # Limites e atualizações físicas
    limit_movement(img_rect)
    limit_movement(target_rect)
    update_jump()
    update_target_physics()

    # Desenho do fundo
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BG_COLOR)

    # Desenha jogador
    if img:
        screen.blit(img, img_rect.topleft)
    else:
        pygame.draw.rect(screen, (255, 0, 0), img_rect)

    # Desenha alvo com efeito de dano
    if target_img:
        if time.time() - damage_time < damage_duration:
            # aplica tint vermelho temporário sem alterar a original
            tinted = target_img.copy()
            tinted.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(tinted, target_rect.topleft)
        else:
            screen.blit(target_img, target_rect.topleft)
    else:
        pygame.draw.rect(screen, (0, 255, 0), target_rect)

    # Barra de vida do alvo (desenha mesmo se imagem ausente)
    draw_health_bar(screen, target_rect, target_hp, TARGET_MAX_HP, bar_width=TARGET_WIDTH + 20)

    # Indicador simples se alvo morto
    if target_hp <= 0:
        font = pygame.font.SysFont(None, 28)
        txt = font.render("ALVO DESTRUIDO", True, (255, 200, 80))
        screen.blit(txt, (target_rect.centerx - txt.get_width() // 2, target_rect.bottom + 6))

    # Atualiza tela e FPS
    pygame.display.flip()
    clock.tick(FPS)

# Finaliza
pygame.quit()
