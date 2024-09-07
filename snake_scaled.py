import pygame
import random
import csv
from datetime import datetime

pygame.init()

# Set up display (scaled size)
WIDTH, HEIGHT = 1200, 800  # Double the original size
GRID_SIZE = 40  # Double the original grid size
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load and scale images
background_image = pygame.image.load("jain.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

snake_head_image = pygame.image.load("tom.jpg")
snake_head_image = pygame.transform.scale(snake_head_image, (GRID_SIZE, GRID_SIZE))

food_image = pygame.image.load("chipotle.png")
food_image = pygame.transform.scale(food_image, (GRID_SIZE, GRID_SIZE))

eat_sound = pygame.mixer.Sound("eat_sound.mp3")

# Colors
WHITE = (255, 255, 255)
SKIN = (255, 224, 189)

# Font
font = pygame.font.Font(None, 36)

# File for storing scores
SCORES_FILE = "snake_scores.csv"

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
                     (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 1),
                     (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 2)]
        self.direction = None  # Start with no movement
        self.grow_pending = False

    def move(self):
        if self.direction is not None:
            x, y = self.body[0]
            if self.direction == 'UP':
                y -= 1
            elif self.direction == 'DOWN':
                y += 1
            elif self.direction == 'LEFT':
                x -= 1
            elif self.direction == 'RIGHT':
                x += 1
            self.body.insert(0, (x, y))

            if not self.grow_pending:
                self.body.pop()
            else:
                self.grow_pending = False

    def grow(self):
        self.grow_pending = True

    def draw(self):
        for i, segment in enumerate(self.body):
            if i == 0:
                if self.direction == 'UP':
                    rotated_head = pygame.transform.rotate(snake_head_image, 0)
                elif self.direction == 'DOWN':
                    rotated_head = pygame.transform.rotate(snake_head_image, 180)
                elif self.direction == 'LEFT':
                    rotated_head = pygame.transform.rotate(snake_head_image, 90)
                elif self.direction == 'RIGHT':
                    rotated_head = pygame.transform.rotate(snake_head_image, -90)
                screen.blit(rotated_head, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE))
            else:
                pygame.draw.rect(screen, SKIN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Food class
class Food:
    def __init__(self, snake):
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        while position in snake.body:
            position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        return position

    def draw(self):
        screen.blit(food_image, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE))

# Save the scores to a CSV file
def save_scores(score, date_time):
    # Read the existing scores
    scores = []
    try:
        with open(SCORES_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                scores.append((int(row[0]), row[1]))  # (score, datetime)
    except FileNotFoundError:
        pass  # If file doesn't exist, start fresh

    # Append the new score
    scores.append((score, date_time))

    # Sort by score, and keep only the top 100, replacing older ones in case of a tie
    scores = sorted(scores, key=lambda x: (-x[0], x[1]))  # Sort by score descending, and by datetime ascending
    unique_scores = {}
    for s, dt in scores:
        unique_scores[s] = dt  # Keeps only the most recent datetime for each score

    # Keep only top 100 scores
    top_scores = sorted(unique_scores.items(), key=lambda x: (-x[0], x[1]))[:100]

    # Write the top 100 scores back to the file
    with open(SCORES_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(top_scores)

# Get the best score and most recent score from the CSV file
def get_scores():
    # Read the existing scores
    scores = []
    try:
        with open(SCORES_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                scores.append((int(row[0]), row[1]))  # (score, datetime)
    except FileNotFoundError:
        return 0, 0  # If file doesn't exist, return 0 for both

    if scores:
        # Sort by score, and keep only the top 100, replacing older ones in case of a tie
        scores = sorted(scores, key=lambda x: (-x[0], x[1]))  # Sort by score descending, and by datetime ascending
        unique_scores = {}
        for s, dt in scores:
            unique_scores[s] = dt  # Keeps only the most recent datetime for each score

        # Keep only top 100 scores
        top_scores = sorted(unique_scores.items(), key=lambda x: (-x[0], x[1]))[:100]
        
        best_score = top_scores[0][0] if top_scores else 0
        most_recent_score = top_scores[-1][0] if top_scores else 0
        
        return best_score, most_recent_score
    return 0, 0

# Main function
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food(snake)
    running = True
    game_started = False
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_started:
                    if event.key == pygame.K_UP:
                        snake.direction = 'UP'
                        game_started = True
                    elif event.key == pygame.K_DOWN:
                        snake.direction = 'DOWN'
                        game_started = True
                    elif event.key == pygame.K_LEFT:
                        snake.direction = 'LEFT'
                        game_started = True
                    elif event.key == pygame.K_RIGHT:
                        snake.direction = 'RIGHT'
                        game_started = True
                elif event.key == pygame.K_UP and snake.direction != 'DOWN':
                    snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                    snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                    snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                    snake.direction = 'RIGHT'

        if game_started:
            if snake.body[0] == food.position:
                snake.grow()
                score += 1
                food = Food(snake)
                eat_sound.play()

            snake.move()

            if (snake.body[0][0] < 0 or snake.body[0][0] >= GRID_WIDTH or
                snake.body[0][1] < 0 or snake.body[0][1] >= GRID_HEIGHT or
                snake.body[0] in snake.body[1:]):
                # Save the score when the game ends
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_scores(score, date_time)
                running = False

            screen.blit(background_image, (0, 0))
            snake.draw()
            food.draw()

            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(10)
    
    # Show final score and best/most recent score
    screen.fill((0, 0, 0))  # Clear the screen
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    best_score, most_recent_score = get_scores()
    best_score_text = font.render(f"Best Score: {best_score}", True, WHITE)
    screen.blit(best_score_text, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.update()  # Update the display
    pygame.time.wait(3000)  # Wait for 
    pygame.quit()

if __name__ == "__main__":
    main()