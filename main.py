import pygame
import time
import random

pygame.font.init()

# Constants
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load and scale background image
BG_SELECTION = pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/bg_castle.png"), (WIDTH, HEIGHT))
BG_GAME = pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/bg_castle.png"), (WIDTH, HEIGHT))  # Change this if you want a different background for the game

# Character selection sizes
SELECTION_CHARACTER_WIDTH = 150
SELECTION_CHARACTER_HEIGHT = 200

# Game sizes
GAME_CHARACTER_WIDTH = 75
GAME_CHARACTER_HEIGHT = 100

# Load and scale character images for selection
SELECTION_CHARACTER_IMAGES = [
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_inosuke.png"), (SELECTION_CHARACTER_WIDTH, SELECTION_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_tanjiro.png"), (SELECTION_CHARACTER_WIDTH, SELECTION_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_nezuko.png"), (SELECTION_CHARACTER_WIDTH, SELECTION_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_zenitsu.png"), (SELECTION_CHARACTER_WIDTH, SELECTION_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_shinobu.png"), (SELECTION_CHARACTER_WIDTH, SELECTION_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_rengoku.png"), (SELECTION_CHARACTER_WIDTH, SELECTION_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_giyu.png"), (SELECTION_CHARACTER_WIDTH, SELECTION_CHARACTER_HEIGHT))
]

# Load and scale character images for the game
GAME_CHARACTER_IMAGES = [
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_inosuke.png"), (GAME_CHARACTER_WIDTH, GAME_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_tanjiro.png"), (GAME_CHARACTER_WIDTH, GAME_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_nezuko.png"), (GAME_CHARACTER_WIDTH, GAME_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_zenitsu.png"), (GAME_CHARACTER_WIDTH, GAME_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_shinobu.png"), (GAME_CHARACTER_WIDTH, GAME_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_rengoku.png"), (GAME_CHARACTER_WIDTH, GAME_CHARACTER_HEIGHT)),
    pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/player_giyu.png"), (GAME_CHARACTER_WIDTH, GAME_CHARACTER_HEIGHT))
]

# Names of the characters
CHARACTER_NAMES = ["Inosuke", "Tanjiro", "Nezuko", "Zenitsu", "Shinobu", "Rengoku", "Giyu"]

# Constants for demons
DEMON_WIDTH = 75
DEMON_HEIGHT = 95
DEMON_VEL = 4.5
DEMON_IMG = pygame.transform.scale(pygame.image.load("Demon_Slayer-Game/demon_tanjiro.png"), (DEMON_WIDTH, DEMON_HEIGHT))

FONT = pygame.font.SysFont("comicsans", 30)

def draw_selection_screen(selected_index):
    WIN.blit(BG_SELECTION, (0, 0))

    # Display the instruction text above character images
    instruction_text = FONT.render("CHOOSE YOUR CHARACTER TO FIGHT", 1, "yellow")
    WIN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 200))

    instruction_text = FONT.render("DEMON KING TANJIRO", 1, "yellow")
    WIN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 240))

    # Display the selected character
    character_img = SELECTION_CHARACTER_IMAGES[selected_index]
    character_name = CHARACTER_NAMES[selected_index]

    # Center the character image
    x = WIDTH // 2 - SELECTION_CHARACTER_WIDTH // 2
    y = HEIGHT // 2 - SELECTION_CHARACTER_HEIGHT // 2
    WIN.blit(character_img, (x, y))

    # Display the character's name
    name_text = FONT.render(character_name, 1, "white")
    WIN.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, y + SELECTION_CHARACTER_HEIGHT + 10))

    # Instructions to choose
    instruction_text = FONT.render("Use Left/Right Arrow to select, Enter to start", 1, "white")
    WIN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 50))

    pygame.display.update()

def select_character():
    run = True
    selected_index = 0

    while run:
        draw_selection_screen(selected_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(SELECTION_CHARACTER_IMAGES)
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(SELECTION_CHARACTER_IMAGES)
                elif event.key == pygame.K_RETURN:
                    return selected_index

def draw_game(player_img, elapsed_time, demons, player, level):
    WIN.blit(BG_GAME, (0, 0))

    # Display the player image
    WIN.blit(player_img, (player.x, player.y))

    # Display the elapsed time
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "yellow")
    WIN.blit(time_text, (10, 10))

    # Display the level at the top-right corner
    level_text = FONT.render(f"Level: {level}", 1, "yellow")
    WIN.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

    for demon in demons:
        WIN.blit(DEMON_IMG, (demon.x, demon.y))

    pygame.display.update()

def main():
    # Character selection
    selected_index = select_character()
    if selected_index is None:
        return  # Exit if user closes the window

    # Load selected character image for the game
    player_img = GAME_CHARACTER_IMAGES[selected_index]
    PLAYER_WIDTH = player_img.get_width()
    PLAYER_HEIGHT = player_img.get_height()
    PLAYER_VEL = 7

    # Initialize game
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    level = 1

    demon_add_increment = 2000
    demon_count = 0

    demons = []
    hit = False

    while True:
        demon_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if elapsed_time >= 100:  # Check if 100 seconds have passed
            # Display "You Won Level X" message
            WIN.blit(BG_GAME, (0, 0))
            win_text = FONT.render(f"You Won Level {level}!", 1, "yellow")
            WIN.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)  # Display the message for 2 seconds
            
            # Advance to the next level
            level += 1
            start_time = time.time()  # Reset the start time for the next level

        if demon_count > demon_add_increment:
            for _ in range(3):
                demon_x = random.randint(0, WIDTH - DEMON_WIDTH)
                demon = pygame.Rect(demon_x, -DEMON_HEIGHT, DEMON_WIDTH, DEMON_HEIGHT)
                demons.append(demon)

            demon_count = max(200, demon_add_increment - 50)
            demon_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        for demon in demons[:]:
            demon.y += DEMON_VEL
            if demon.y > HEIGHT:
                demons.remove(demon)
            elif demon.y + demon.height >= player.y and demon.colliderect(player):
                demons.remove(demon)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "yellow")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw_game(player_img, elapsed_time, demons, player, level)

    pygame.quit()

if __name__ == "__main__":
    main()
