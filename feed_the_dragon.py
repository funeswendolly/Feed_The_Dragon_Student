import pygame, random

# Initialize pygame
pygame.init()

def make_text(font_object, text, color, background_color):
    return font.render(text, True, color,background_color)

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
# TODO:
#   - Create constants for:
#       * PLAYER_STARTING_LIVES (e.g., 5)
#       * PLAYER_VELOCITY (how fast the dragon moves up/down) (e.g., 10)
#       * COIN_STARTING_VELOCITY (how fast the coin moves at the start) (e.g, 10)
#       * COIN_ACCELERATION (how much faster the coin gets after each catch) (e.g., 0.5)
#       * BUFFER_DISTANCE (how far off-screen to respawn the coin on the right) (e.g, 100)
#   - Create variables for:
#       * score (starting at 0)
#       * player_lives (start at PLAYER_STARTING_LIVES)
#       * coin_velocity (start at COIN_STARTING_VELOCITY)
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100
score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# Set colors
# TODO:
#   - Define color constants using RGB tuples, such as:
#       * GREEN
#       * DARKGREEN:  RGB value of 10, 50, 10
#       * WHITE
#       * BLACK
GREEN = (0, 255, 0)
DARKGREEN = (10,50,10)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Set fonts
# TODO:
#   - Create a font object using pygame.font.Font(...)
#   - Use the provided font file from the assets folder (e.g., "assets/AttackGraffiti.ttf")
#   - Choose a font size (e.g., 32)
font = pygame.font.Font("assets/AttackGraffiti.ttf",32 )

# Set text
score_text = make_text(font, "Score: " + str(score), GREEN, DARKGREEN)
title_text = make_text(font, "Feed the Dragon",GREEN,WHITE)
lives_text = make_text(font, "Lives: " + str(player_lives), GREEN,DARKGREEN)

score_rect = score_text.get_rect()
title_rect = title_text.get_rect()
lives_rect = lives_text.get_rect()

score_rect.topleft = (10,10)
title_rect.centerx = (WINDOW_WIDTH//2)
title_rect.y = 10
lives_rect.topright = (WINDOW_WIDTH -10,10)

# Set sounds and music
# TODO:
#   - Load sound effects for:
#       * missing a coin (e.g., "assets/miss_sound.wav")
#   - Optionally adjust the miss sound volume using set_volume(...)
#   - Load background music (e.g., "assets/ftd_background_music.wav") using pygame.mixer.music.load(...)
catching_a_coin = pygame.mixer.Sound("assets/coin_sound.wav")
missing_a_coin = pygame.mixer.Sound("assets/miss_sound.wav")
missing_a_coin.set_volume(0.1)
pygame.mixer.music.load("assets/ftd_background_music.wav")
# Set images
# TODO:
#   - Load the player image (dragon) from "assets/dragon_right.png" using pygame.image.load(...)
#   - Get its rect with .get_rect() and:
#       * place it near the left side of the screen
#       * center it vertically in the window
#   - Load the coin image from "assets/coin.png"
#   - Get its rect and:
#       * start it off to the right of the window by BUFFER_DISTANCE
#       * give it a random y-position somewhere between a top margin (like 64) and near the bottom
player_image = pygame.image.load("assets/dragon_right.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT//2

coin_image = pygame.image.load("assets/coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(65,WINDOW_HEIGHT)

# The main game loop
# TODO:
#   - Play the background music in a loop using pygame.mixer.music.play(...)
#   - Create a variable named running and set it to True; this will control the main while loop.
pygame.mixer.music.play(-1,0,0)
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
    for key in keys:
        if key == pygame.K_UP and player_rect.y > 64:
             player_rect.y -= PLAYER_VELOCITY
        if key == pygame.K_DOWN and player_rect.y < WINDOW_HEIGHT - 32:
             player_rect.x += PLAYER_VELOCITY


def handle_coin():
    # * Subtract 1 from player_lives.
    global player_lives
    if coin_rect.x < 0:
        player_lives -= 1
        missing_a_coin.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64,WINDOW_HEIGHT)
    else:
        coin_rect.x -= coin_velocity

def handle_collisions():
    global score, coin_velocity
    if player_rect.colliderect(coin_rect):
        score += 1
        catching_a_coin.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64,WINDOW_HEIGHT)

def update_hud():
    global score_text
    score_text = make_text(font, "Score: " + str(score), GREEN, DARKGREEN)
    make_text(lives_text, "Lives: " + str(player_lives), GREEN, DARKGREEN)

def game_over_check():
    global player_lives
    if player_lives == 0:
        blit(display_surface, game_over_text, game_over_rect)

    continue_text = font.render("press any key to play again", True, GREEN, DARKGREEN)
    continue_rect = continue_text.get_rect()

    display_surface.blit(game_over_text, game_over_rect)
    display_surface.blit(continue_text, continue_rect)
    pygame.display.update()

    is_paused = True
    while is_paused:
        for event in pygame.event.get():
         if event.type == pygame.KEYDOWN:
            score = 0
            player_lives = PLAYER_STARTING_LIVES
            centered_vertically = player_position
            coin_velocity = COIN_STARTING_VELOCITY
            background_music = pygame.mixer.Sound("assets/coin_sound.wav")
            runing = False
            is_paused = False

def update_screen():
    # TODO:
    #   - Fill the display_surface with a background color (e.g., BLACK) using your fill(...) helper.
    #   - Draw the HUD elements on the screen:
    #       * score_text, title_text, lives_text at their rect positions using your blit(...) helper.
    #   - Draw a horizontal line across the screen near the top to separate the HUD from the play area.
    #   - Draw the player image and the coin image at their rect positions using your blit(...) helper.
    #   - Finally, call update_display() so that everything appears on the screen.
    pass

    display_surface.fill(BLACK)
    score_text.blit(title_rect)
    title_text.blit(title_rect)
    lives_text.blit(lives_rect)

    player_image.blit(player_rect)
    coin_image.blit(coin_rect)
    update_display()

while running:
    # Main game loop steps:
    #   1. Handle quit events.
    #   2. Move the player based on keyboard input.
    #   3. Move the coin and handle misses.
    #   4. Check for collisions between player and coin.
    #   5. Update the HUD text to match the current score and lives.
    #   6. Check if the game is over and either reset or quit.
    #   7. Draw everything on the screen.
    #   8. Tick the clock to control the frame rate.

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
