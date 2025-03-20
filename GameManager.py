import pygame
import random

# Initialize pygame
pygame.init()

# Load image
image = pygame.image.load("img/ball.png")
image = pygame.transform.scale(image, (40, 40))  # Scale image to block size
bg = pygame.image.load("img/bg.jpg")
background = pygame.transform.scale(bg, (1600, 800))

# Constants
WIDTH, HEIGHT = 1600, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60

# Block settings
BLOCK_SIZE = 40
BLOCK_SPEED = 5

# Tower settings
TOWER_WIDTH, TOWER_HEIGHT = 100, 200
PLAYER_TOWER_X = 0
ENEMY_TOWER_X = WIDTH - 100

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Battle Game")

# Font
font = pygame.font.Font(None, 30)

# Block class
class Block:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.speed = speed

    def move(self):
        self.rect.x += self.speed

    def draw(self):
        screen.blit(image, (self.rect.x, self.rect.y))

# Tower class
class Tower:
    def __init__(self, x, color, team):
        self.rect = pygame.Rect(x, HEIGHT // 2 - TOWER_HEIGHT // 2, TOWER_WIDTH, TOWER_HEIGHT)
        self.hp = 100
        self.color = color
        self.team = font.render(team, True, color)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        hp_text = font.render(str(self.hp), True, YELLOW)
        screen.blit(hp_text, (self.rect.x + 10, self.rect.y - 20))
        screen.blit(self.team, (self.rect.x + 10, self.rect.y - 40))


# Game loop
player_tower = Tower(PLAYER_TOWER_X, BLUE, "Me")
enemy_tower = Tower(ENEMY_TOWER_X, RED, "Enemy")
player_blocks = []
enemy_blocks = []
clock = pygame.time.Clock()
running = True
enemy_spawn_timer = 0

while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_blocks.append(Block(player_tower.rect.right, HEIGHT // 2 - BLOCK_SIZE // 2, BLOCK_SPEED))

    # Move blocks
    for block in player_blocks[:]:
        block.move()
        if block.rect.colliderect(enemy_tower.rect):
            enemy_tower.hp -= 10
            player_blocks.remove(block)

    for block in enemy_blocks[:]:
        block.move()
        if block.rect.colliderect(player_tower.rect):
            player_tower.hp -= 10
            enemy_blocks.remove(block)

    # Enemy sends blocks periodically
    enemy_spawn_timer += 1
    if enemy_spawn_timer > 90:  # Every 1.5 seconds
        enemy_blocks.append(Block(enemy_tower.rect.left - BLOCK_SIZE, HEIGHT // 2 - BLOCK_SIZE // 2, -BLOCK_SPEED))
        enemy_spawn_timer = 0

    # Draw everything
    player_tower.draw()
    enemy_tower.draw()
    for block in player_blocks:
        block.draw()
    for block in enemy_blocks:
        block.draw()

    # Check win condition
    if enemy_tower.hp <= 0:
        print("You win!")
        running = False
    if player_tower.hp <= 0:
        print("You lose!")
        running = False

    pygame.display.flip()

pygame.quit()
