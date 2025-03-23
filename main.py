import pygame
import random
from Customize import Color, Images, Resolution, Dimensions
from Base import Tower
from Enemy import EnemyLogic
from Unit import SmallViking
from Player import Controller
# Initialize pygame
pygame.init()

# Load images
background = pygame.transform.scale(Images.bg, (Resolution.WIDTH, Resolution.HEIGHT))
# Tower positions
PLAYER_TOWER_X = 0
ENEMY_TOWER_X = Resolution.WIDTH - 200

# Initialize screen
screen = pygame.display.set_mode((Resolution.WIDTH, Resolution.HEIGHT))
pygame.display.set_caption("Block Battle Game")

# Game loop setup
player_tower = Tower(PLAYER_TOWER_X, Color.BLUE, "Me", "img/castle/png/1/Asset 27.png")
enemy_tower = Tower(ENEMY_TOWER_X, Color.RED, "Enemy", "img/castle/png/1/Asset 27.png")
clock = pygame.time.Clock()
running = True
enemy_spawn_timer = 0
Enemy = EnemyLogic()

while running:
    clock.tick(Resolution.FPS)
    screen.blit(background, (0, 0))
    Controller.keyboard(player_tower)

    # Move blocks
    player_tower.take_dmg(enemy_tower)
    enemy_tower.take_dmg(player_tower)

    # Enemy spawns blocks periodically
    Enemy.enemy_spawn_timer_setter(1)
    Enemy.spawn_pattern(enemy_tower)

    # Draw everything
    player_tower.draw(screen)
    enemy_tower.draw(screen)
    for char in player_tower.block:
        if char.health <= 0:
            player_tower.block.remove(char)
        char.move()
        char.update(player_tower.block)
        char.attack(enemy_tower.block, screen)
        char.draw(screen)
        pygame.draw.rect(screen, (255, 0, 0), char.rect, 2)  # Draw hitbox for debugging
    for unit in enemy_tower.block:
        if unit.health <= 0:
            enemy_tower.block.remove(unit)
        unit.move()
        unit.update(enemy_tower.block)
        unit.attack(player_tower.block, screen)
        unit.draw(screen)
        pygame.draw.rect(screen, (255, 0, 0), unit.rect, 2)  # Draw hitbox for debugging

    # Check win condition
    running = player_tower.dead_tower(enemy_tower)
    pygame.display.flip()
pygame.quit()