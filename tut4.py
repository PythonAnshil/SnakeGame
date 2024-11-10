import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("AnshilSnakes")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Function for gradient background
def draw_gradient_background():
    for y in range(screen_height):
        color = (int(255 * (y / screen_height)), int(100 * (y / screen_height)), int(200 * (y / screen_height)))
        pygame.draw.line(gameWindow, color, (0, y), (screen_width, y))

# Function to display text
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Function to plot the snake with a gradient tail
def plot_snake_gradient(gameWindow, snk_list, snake_size, skin):
    for i, (x, y) in enumerate(snk_list):
        if skin == "rainbow":
            color_intensity = int(255 * (i / len(snk_list)))
            snake_color = (0, color_intensity, 255 - color_intensity)
        else:
            snake_color = skin
        pygame.draw.rect(gameWindow, snake_color, [x, y, snake_size, snake_size])

# Countdown timer
def countdown():
    for i in range(3, 0, -1):
        gameWindow.fill(black)
        text_screen(f"Starting in {i}...", green, 350, 250)
        pygame.display.update()
        pygame.time.delay(1000)

# Get player name
def get_player_name():
    gameWindow.fill(black)
    text_screen("Enter Your Name:", green, 250, 200)
    pygame.display.update()
    player_name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(player_name) > 0:
                    return player_name
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
        gameWindow.fill(black)
        text_screen("Enter Your Name:", green, 250, 200)
        text_screen(player_name, green, 250, 300)
        pygame.display.update()

# Select difficulty
def select_difficulty():
    gameWindow.fill(white)
    text_screen("Select Difficulty:", black, 260, 150)
    text_screen("1. Easy  2. Medium  3. Hard", black, 232, 220)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 3  # Easy
                elif event.key == pygame.K_2:
                    return 5  # Medium
                elif event.key == pygame.K_3:
                    return 7  # Hard

# Select snake skin
def select_snake_skin():
    gameWindow.fill(white)
    text_screen("Select Snake Skin:", black, 260, 150)
    text_screen("1. Green  2. Blue  3. Rainbow", black, 232, 220)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return green  # Green Snake
                elif event.key == pygame.K_2:
                    return blue  # Blue Snake
                elif event.key == pygame.K_3:
                    return "rainbow"  # Rainbow effect

# Particle effect for food consumption
particles = []

def draw_particles():
    for particle in particles:
        particle[0][1] += particle[2]  # Update y-position (gravity)
        particle[1] -= 0.2  # Decrease size over time
        pygame.draw.circle(gameWindow, red, particle[0], int(particle[1]))

    particles[:] = [particle for particle in particles if particle[1] > 0]

# Level up notification
def level_up_notification(level):
    gameWindow.fill(black)
    text_screen(f"Level {level}!", green, 350, 250)
    pygame.display.update()
    pygame.time.delay(1000)

# Welcome screen
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        text_screen("Welcome to Snake Game", black, 260, 250)
        text_screen("Press Space Bar To Play", black, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("back2.mp3")
                    pygame.mixer.music.play(-1)  # Start background music
                    player_name = get_player_name()
                    init_velocity = select_difficulty()
                    snake_skin = select_snake_skin()
                    countdown()
                    gameloop(player_name, init_velocity, snake_skin)

        pygame.display.update()
        clock.tick(60)

# Game loop
def gameloop(player_name, init_velocity, snake_skin):
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    # High score initialization
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0,None")

    with open("hiscore.txt", "r") as f:
        data = f.read().strip()
        if "," in data:
            hiscore, highscore_name = data.split(",")
        else:
            hiscore = "0"
            highscore_name = "None"

    # Initializations
    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)
    food_size = random.randint(20, 40)
    food_points = random.randint(5, 20)
    score = 0
    snake_size = 30
    fps = 60
    last_food_time = pygame.time.get_ticks()
    score_multiplier = 1
    current_level = 1
    next_level_score = 50
    day_mode = True

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                if score > int(hiscore):
                    f.write(f"{score},{player_name}")
                else:
                    f.write(f"{hiscore},{highscore_name}")
            gameWindow.fill(white)
            text_screen("Game Over! Press ENTER to play again", red, 100, 200)
            text_screen(f"Your Score: {score}", black, 100, 250)
            text_screen(f"High Score: {hiscore} by {highscore_name}", black, 100, 300)
            if score >= int(hiscore):
                text_screen("New High Score! Well done!", red, 100, 350)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
                    if event.key == pygame.K_q:
                        exit_game = True

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            # Update snake position
            snake_x += velocity_x
            snake_y += velocity_y

            # Teleport the snake if it goes beyond the boundary
            if snake_x < 0:
                snake_x = screen_width
            elif snake_x > screen_width:
                snake_x = 0
            if snake_y < 0:
                snake_y = screen_height
            elif snake_y > screen_height:
                snake_y = 0

            # Check if snake eats the food
            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                current_time = pygame.time.get_ticks()
                if current_time - last_food_time < 3000:
                    score_multiplier += 1
                else:
                    score_multiplier = 1
                score += food_points * score_multiplier
                snk_length += random.randint(3, 7)
                if score > int(hiscore):
                    hiscore = score
                food_x = random.randint(20, screen_width - 20)
                food_y = random.randint(20, screen_height - 20)
                food_size = random.randint(20, 40)
                food_points = random.randint(5, 20)

                # Play eating sound and add particles
                pygame.mixer.Sound("eating.mp3").play()
                for _ in range(20):
                    particles.append([[food_x, food_y], random.randint(4, 7), random.uniform(-1, 1)])

                last_food_time = current_time

            # Level up mechanism
            if score >= next_level_score:
                current_level += 1
                next_level_score += 50
                level_up_notification(current_level)
                init_velocity += 1
                day_mode = not day_mode

            # Draw background and game elements
            if day_mode:
                draw_gradient_background()
            else:
                gameWindow.fill((30, 30, 30))  # Night mode

            text_screen("Score: " + str(score) + "  High Score: " + str(hiscore) + f" by {highscore_name}", red, 5, 5)
            text_screen(f"Player: {player_name}", black, 5, 45)
            draw_particles()
            pygame.draw.rect(gameWindow, red, [food_x, food_y, food_size, food_size])

            # Draw snake
            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # Check for collision with self
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("explosion.mp3")
                pygame.mixer.music.play()

            plot_snake_gradient(gameWindow, snk_list, snake_size, snake_skin)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
