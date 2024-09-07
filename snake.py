import pygame
import random

pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load background image
background_image = pygame.image.load("jain.jpg").convert()

# Load snake head and food images
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

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
                     (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 1),
                     (GRID_WIDTH // 2, GRID_HEIGHT // 2 + 2)]
        self.direction = None  # Start with no movement
        self.grow_pending = False

    def move(self):
        if self.direction is not None:  # Only move if direction is set
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
                self.body.pop()  # Remove last segment if not growing
            else:
                self.grow_pending = False  # Reset growth flag after growing

    def grow(self):
        self.grow_pending = True

    def draw(self):
        for i, segment in enumerate(self.body):
            if i == 0:
                # Rotate snake head image based on direction
                if self.direction == 'UP':
                    rotated_head = pygame.transform.rotate(snake_head_image, 0)
                elif self.direction == 'DOWN':
                    rotated_head = pygame.transform.rotate(snake_head_image, 180)
                elif self.direction == 'LEFT':
                    rotated_head = pygame.transform.rotate(snake_head_image, 90)
                elif self.direction == 'RIGHT':
                    rotated_head = pygame.transform.rotate(snake_head_image, -90)
                screen.blit(rotated_head, (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE))
            else:
                pygame.draw.rect(screen, SKIN, (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Food class
class Food:
    def __init__(self, snake):
        self.position = self.generate_position(snake)

    def generate_position(self, snake):
        position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        while position in snake.body:  # Ensure food is not on the snake
            position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        return position

    def draw(self):
        screen.blit(food_image, (self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE))

# Main function
def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food(snake)
    running = True
    game_started = False  # Flag to track whether the game has started
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_started:  # Start the game only after first input
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

        # Move the snake only if the game has started
        if game_started:
            # Check if snake eats food
            if snake.body[0] == food.position:
                snake.grow()
                score += 1
                food = Food(snake)
                eat_sound.play()

            # Snake movement
            snake.move()

            # Check for collision with walls or self
            if (snake.body[0][0] < 0 or snake.body[0][0] >= GRID_WIDTH or
                snake.body[0][1] < 0 or snake.body[0][1] >= GRID_HEIGHT or
                snake.body[0] in snake.body[1:]):
                running = False

            # Draw everything
            screen.blit(background_image, (0, 0))
            snake.draw()
            food.draw()

            # Draw the score
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
