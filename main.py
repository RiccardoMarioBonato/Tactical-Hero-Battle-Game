from tkinter.constants import UNITS

import pygame
from Level_select import LevelSelect, SelectGame
import Customize
from Customize import Color, Images, Resolution, Dimensions
from Base import Tower
from Enemy import EnemyLogic
from Player import Controller, Resources
from Unit import BigBloatedBoss
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
running = True
enemy_spawn_timer = 0
Enemy = EnemyLogic()
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)
font_tiny = pygame.font.SysFont('Arial', 16)
player_resources = Resources()
player_resources.add_start()
clock = pygame.time.Clock()


# Game states
class GameState:
    CHARACTER_SELECT = 0
    MAIN_GAME = 1
    LEVEL_COMPLETE = 2


# Initialize game state
current_state = GameState.CHARACTER_SELECT
selected_characters = []
cr_select = SelectGame()  # This should be your SelectGame instance, not LevelSelect

# Main game loop
running = True
while running:
    clock.tick(Resolution.FPS)

    if current_state == GameState.CHARACTER_SELECT:
        selection_result = cr_select.selecting()
        if selection_result:  # Returns [level_num, selected_characters]
            level_num, selected_hero_classes = selection_result
            current_state = GameState.MAIN_GAME

            # Store selected units for the controller
            selected_units = selected_hero_classes[:3]  # Only take first 3 selected

            # Initialize game state
            player_tower = Tower(PLAYER_TOWER_X, Color.BLUE, "Me", "img/castle/png/1/Asset 27.png")
            enemy_tower = Tower(ENEMY_TOWER_X, Color.RED, "Enemy", "img/castle/png/1/Asset 27.png")
            player_resources = Resources()
            player_resources.add_start()

    elif current_state == GameState.MAIN_GAME:
        screen.blit(background, (0, 0))
        Controller.keyboard(player_tower, player_resources, selected_units)
        # Rest of your game loop...

        # Move blocks
        player_tower.take_dmg(enemy_tower)
        enemy_tower.take_dmg(player_tower)
        Enemy.enemy_spawn_timer_setter(1)
        Resources.add_solar_energy(player_resources)
        Enemy.spawn_pattern(enemy_tower, player_resources)

        # Draw everything
        player_tower.draw(screen)
        enemy_tower.draw(screen)
        player_resources.draw(screen)

        # Update and draw player blocks
        for char in player_tower.block[:]:
            char.update(screen, player_tower, player_tower.block, enemy_tower.block)
            if char.dead:
                player_tower.block.remove(char)

        # Update and draw enemy blocks
        for unit in enemy_tower.block[:]:
            unit.update(screen, enemy_tower, enemy_tower.block, player_tower.block)
            if unit.dead:
                enemy_tower.block.remove(unit)

        # Check win/lose condition
        if not player_tower.dead_tower(enemy_tower):
            current_state = GameState.LEVEL_COMPLETE
        elif enemy_tower.dead_tower(player_tower) <= 0:
            current_state = GameState.LEVEL_COMPLETE

    elif current_state == GameState.LEVEL_COMPLETE:
        # Level complete screen
        screen.fill((0, 0, 0))
        victory_text = font_large.render("Level Complete!", True, (255, 255, 255))
        continue_text = font_medium.render("Press SPACE to continue", True, (255, 255, 255))

        screen.blit(victory_text,
                    (Resolution.WIDTH // 2 - victory_text.get_width() // 2, Resolution.HEIGHT // 2 - 50))
        screen.blit(continue_text,
                    (Resolution.WIDTH // 2 - continue_text.get_width() // 2, Resolution.HEIGHT // 2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_state = GameState.CHARACTER_SELECT  # Return to character select
                cr_select = SelectGame()  # Reset the selection screen

    pygame.display.flip()

pygame.quit()

if __name__ == "__main__":
    game = SelectGame()
    game.selecting()