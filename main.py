import pygame

import Customize
from Customize import Color, Images, Resolution, Dimensions
from Base import Tower
from Enemy import EnemyLogic
from Player import Controller, Resources
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

player_resources = Resources()
player_resources.add_start()

while running:
    clock.tick(Resolution.FPS)
    screen.blit(background, (0, 0))
    Controller.keyboard(player_tower, player_resources)
    # Move blocks
    player_tower.take_dmg(enemy_tower)
    enemy_tower.take_dmg(player_tower)
    Enemy.enemy_spawn_timer_setter(1)
    Resources.add_solar_energy(player_resources)
    Enemy.spawn_pattern(enemy_tower, player_resources)
    # Draw everythingc
    player_tower.draw(screen)
    enemy_tower.draw(screen)
    player_resources.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), player_tower.rect, 2)
    pygame.draw.rect(screen, (255, 0, 0), enemy_tower.rect, 2)
    # Update and draw player blocks
    for char in player_tower.block[:]:  # Iterate over a copy of the list
        char.update(screen, player_tower, player_tower.block, enemy_tower.block)
        if char.dead:  # Check if the unit is ready to be removed
            player_tower.block.remove(char)
            # Remove the unit from the list
        # pygame.draw.rect(screen, (255, 0, 0), char.rect, 2)  # Draw hitbox for debugging

    # Update and draw enemy blocks
    for unit in enemy_tower.block[:]:  # Iterate over a copy of   ccz                                                                                                                                                                                                                          the list
        unit.update(screen, enemy_tower, enemy_tower.block, player_tower.block)
        if unit.dead:
            enemy_tower.block.remove(unit)  # Remove the unit from the list
        # pygame.draw.rect(screen, (255, 0, 0), unit.rect, 2)  # Draw hitbox for debugging

    # Check win condition
    running = player_tower.dead_tower(enemy_tower)
    pygame.display.flip()
pygame.quit()
