import pygame
import random
import pygame.mixer
import os

# Initialize sound
pygame.mixer.init()

current_dir = os.path.dirname(os.path.abspath(__file__))
game_over_sound = pygame.mixer.Sound(os.path.join(current_dir, 'game_over.wav'))
paddle_hit_sound = pygame.mixer.Sound(os.path.join(current_dir, 'paddle_hit.wav'))

# initialize pygame
pygame.init()

# Game variables
GREEN = (0, 255, 0)
WIDTH, HEIGHT = 1200, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 0, 0)
RED = (255, 0, 0)
PADDLE_COLOR = (0, 0, 255)
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
PADDLE_SPEED = 10
FONT_COLOR = WHITE
ICON_SIZE = 30
BALL_SPEED = 4  # Default ball speed
DEFAULT_BALL_SPEED = 4  # Store initial ball speed
score_multiplier = 1  # New variable for score multiplier
score_since_two_balls = 0  # New variable to track score since two balls

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ball and Paddle Game')

# Font settings
font = pygame.font.SysFont('comicsans', 50)
small_font = pygame.font.SysFont('comicsans', 30)

# Load settings icon
settings_icon = pygame.image.load(os.path.join(current_dir, 'gear_icon.png'))
settings_icon = pygame.transform.scale(settings_icon, (ICON_SIZE, ICON_SIZE))

# Reset ball and paddle position
def reset_game():
    global current_ball_count, score_multiplier, score_since_two_balls
    current_ball_count = 1
    score_multiplier = 1
    score_since_two_balls = 0
    return [{'x': WIDTH // 2, 'y': HEIGHT // 2, 'dx': BALL_SPEED * random.choice([1, -1]), 'dy': BALL_SPEED * random.choice([1, -1]), 'main': True}], WIDTH // 2 - PADDLE_WIDTH // 2

# Update the speed of all balls
def update_ball_speeds():
    for ball in balls:
        ball['dx'] = BALL_SPEED * (1 if ball['dx'] > 0 else -1)
        ball['dy'] = BALL_SPEED * (1 if ball['dy'] > 0 else -1)

# Calculate score based on ball's position on paddle and ball speed
def calculate_score(ball_x, paddle_x):
    global score_multiplier
    center_of_paddle = paddle_x + PADDLE_WIDTH // 2
    distance_from_center = abs(ball_x - center_of_paddle)

    if distance_from_center < 10:  # Near the center
        base_score = 100
    elif distance_from_center < 30:  # Close to center
        base_score = 50
    else:
        base_score = 10

    speed_bonus_multiplier = 1 + (BALL_SPEED - DEFAULT_BALL_SPEED) // 2 * 0.5
    return int(base_score * speed_bonus_multiplier * score_multiplier)

# Settings menu
def settings_menu():
    global BALL_SPEED
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        
        # Display settings options
        settings_text = font.render('Settings', True, FONT_COLOR)
        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, 100))

        speed_text = small_font.render(f'Ball Speed: {BALL_SPEED}', True, FONT_COLOR)
        screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, 200))

        increase_speed_text = small_font.render('Press + to Increase Speed', True, FONT_COLOR)
        decrease_speed_text = small_font.render('Press - to Decrease Speed', True, FONT_COLOR)
        screen.blit(increase_speed_text, (WIDTH // 2 - increase_speed_text.get_width() // 2, 250))
        screen.blit(decrease_speed_text, (WIDTH // 2 - decrease_speed_text.get_width() // 2, 300))

        exit_text = small_font.render('Press ESC to Exit Settings', True, FONT_COLOR)
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 350))

        pygame.display.flip()

        # Handle settings menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()  # Close the game
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    BALL_SPEED += 1
                if event.key == pygame.K_MINUS and BALL_SPEED > 1:
                    BALL_SPEED -= 1
                if event.key == pygame.K_ESCAPE:
                    menu_running = False  # Exit settings and return to game
                    update_ball_speeds()  # Apply speed changes immediately after exiting settings

# Ball settings
current_ball_count = 1
balls, paddle_x = reset_game()
paddle_y = HEIGHT - 40
score = 0

# Game loop control
running = True
game_over = False
clock = pygame.time.Clock()

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if WIDTH - ICON_SIZE <= mouse_x <= WIDTH and 0 <= mouse_y <= ICON_SIZE:
                settings_menu()

    if not game_over:
        # Ball movement
        for ball in balls[:]:  # Use a copy of the list to safely remove balls
            ball['x'] += ball['dx']
            ball['y'] += ball['dy']

            # Ball collision with walls
            if ball['x'] - BALL_RADIUS <= 0 or ball['x'] + BALL_RADIUS >= WIDTH:
                ball['dx'] = -ball['dx']
            if ball['y'] - BALL_RADIUS <= 0:
                ball['dy'] = -ball['dy']

            # Ball collision with paddle
            if paddle_y - BALL_RADIUS <= ball['y'] <= paddle_y + PADDLE_HEIGHT and \
                paddle_x - BALL_RADIUS <= ball['x'] <= paddle_x + PADDLE_WIDTH + BALL_RADIUS:
                if ball['dy'] > 0:  # Only bounce if the ball is moving downwards
                    ball['dy'] = -ball['dy']
                    earned_score = calculate_score(ball['x'], paddle_x)
                    score += earned_score
                    if current_ball_count >= 2:
                        score_since_two_balls += earned_score
                    paddle_hit_sound.play()
            
            # Ball out of bounds
            if ball['y'] > HEIGHT:
                if ball['main']:
                    game_over = True
                    game_over_sound.play()
                else:
                    balls.remove(ball)
                    current_ball_count -= 1

        # Increase ball count based on score
        if current_ball_count == 1 and score >= 500:
            current_ball_count = 2
            score_since_two_balls = 0
        elif current_ball_count == 2 and score_since_two_balls >= 500:
            current_ball_count = 3
            score_since_two_balls = 0

        # Add more balls if the number of balls has increased
        while len(balls) < current_ball_count:
            balls.append({
                'x': WIDTH // 2,
                'y': HEIGHT // 2,
                'dx': BALL_SPEED * random.choice([1, -1]),
                'dy': BALL_SPEED * random.choice([1, -1]),
                'main': False
            })

        # Update score multiplier
        if current_ball_count >= 2:
            score_multiplier += 0.1
        else:
            score_multiplier = 1

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle_x + PADDLE_WIDTH < WIDTH:
            paddle_x += PADDLE_SPEED

        # Clear screen
        screen.fill(GREEN)

        # Draw the balls
        for ball in balls:
            pygame.draw.circle(screen, BALL_COLOR, (int(ball['x']), int(ball['y'])), BALL_RADIUS)

        # Draw the paddle
        pygame.draw.rect(screen, PADDLE_COLOR, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

        # Display the score
        score_text = small_font.render(f'Score: {score}', True, FONT_COLOR)
        screen.blit(score_text, (10, 10))

        # Display settings icon
        screen.blit(settings_icon, (WIDTH - ICON_SIZE, 0))

        # Update the display
        pygame.display.flip()

        # Set the frames per second (FPS)
        clock.tick(60)

    else:
        # Clear the screen for Game Over screen
        screen.fill(RED)

        # Display 'Game Over'
        game_over_text = font.render('Game Over', True, FONT_COLOR)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))

        # Display the final score
        final_score_text = small_font.render(f'Your Score: {score}', True, FONT_COLOR)
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))

        # Display restart instruction
        restart_text = small_font.render('Press R to Restart', True, FONT_COLOR)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        # Restart the game if 'R' is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            balls, paddle_x = reset_game()  # Reset the balls and paddle position
            score = 0
            game_over = False

# Quit the game
pygame.quit()
