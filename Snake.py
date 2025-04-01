import pygame
import random

pygame.init()
W, H = 500, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

snake = [[100, 50], [90, 50], [80, 50]]
direction = "RIGHT"
score = 0
speed = 10

fruit = [random.randrange(0, W, 10), random.randrange(0, H, 10)]
fruit_timer = pygame.time.get_ticks()
fruit_lifetime = 10000  # timer for fruit in milliseconds

running = True

def show_score():
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score: {score}", True, (128, 0, 128))
    screen.blit(text, (10, 10))

def game_over():
    font = pygame.font.SysFont(None, 40)
    text = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
    screen.blit(text, (100, 250))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    exit()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
    
    head = snake[0][:]
    if direction == "UP":
        head[1] -= 10
    elif direction == "DOWN":
        head[1] += 10
    elif direction == "LEFT":
        head[0] -= 10
    elif direction == "RIGHT":
        head[0] += 10
    
    if head == fruit:
        score += random.randint(1, 20)
        fruit = [random.randrange(0, W, 10), random.randrange(0, H, 10)]
        fruit_timer = pygame.time.get_ticks()
    else:
        snake.pop()
    
    if pygame.time.get_ticks() - fruit_timer > fruit_lifetime:
        fruit = [random.randrange(0, W, 10), random.randrange(0, H, 10)]
        fruit_timer = pygame.time.get_ticks()
    
    if head in snake or head[0] < 0 or head[0] >= W or head[1] < 0 or head[1] >= H:
        game_over()
    
    snake.insert(0, head)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (*fruit, 10, 10))
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*segment, 10, 10))
    show_score()
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
