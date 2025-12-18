import pygame, random

# Initialize pygame
pygame.init()


def make_text(font_object, text, color, background_color):
    return font.render(text, True, color, background_color)


def blit(surface, item, rect):
    surface.blit(item, rect)


def fill(surface, color):
    surface.fill(color)


def update_display():
    pygame.display.update()


# Set display surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Dragon")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# Set colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set fonts
font = pygame.font.Font("assets/AttackGraffiti.ttf", 32)

# Set text
score_text = make_text(font, "Score: " + str(score), GREEN, DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = make_text(font, "Feed the Dragon", GREEN, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = (WINDOW_WIDTH // 2)
title_rect.y = 10

lives_text = make_text(font, "Lives: " + str(player_lives), GREEN, DARKGREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("GAMEOVER", True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render("Press any key to play again", True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 32)

# Set sounds and music
coin_sound = pygame.mixer.Sound("assets/coin_sound.wav")
miss_coin = pygame.mixer.Sound("assets/miss_sound.wav")
miss_coin.set_volume(0.1)
pygame.mixer.music.load("assets/ftd_background_music.wav")

# Set images
player_image = pygame.image.load("assets/dragon_right.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT // 2

coin_image = pygame.image.load("assets/coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

# The main game loop
pygame.mixer.music.play(-1, 0)
running = True


def tick():
    clock.tick(FPS)


def is_still_running():
    global running
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False


def move_player():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY


def handle_coin():
    global player_lives
    if coin_rect.x < 0:
        player_lives -= 1
        miss_coin.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    else:
        coin_rect.x -= coin_velocity


def handle_collisions():
    global score, coin_velocity
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)


def update_hud():
    global score_text, lives_text
    score_text = make_text(font, "Score: " + str(score), GREEN, DARKGREEN)
    lives_text = make_text(font, "Lives: " + str(player_lives), GREEN, DARKGREEN)


def game_over_check():
    global player_lives, coin_velocity, running, score
    if player_lives == 0:
        blit(display_surface, game_over_text, game_over_rect)
        blit(display_surface, continue_text, continue_rect)
        update_display()

        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGHT // 2
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                if event.type == pygame.QUIT:
                    running = False
                    is_paused = False


def update_screen():
    fill(display_surface, BLACK)
    blit(display_surface, score_text, score_rect)
    blit(display_surface, title_text, title_rect)
    blit(display_surface, lives_text, lives_rect)

    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    blit(display_surface, player_image, player_rect)
    blit(display_surface, coin_image, coin_rect)
    update_display()


while running:
    is_still_running()
    move_player()
    handle_coin()
    handle_collisions()
    update_hud()
    game_over_check()
    update_screen()
    tick()

# End the game
pygame.quit()
