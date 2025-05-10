import pygame
from Level_select import SelectGame, GameProgress
from Customize import Color, Images, Resolution, Dimensions
from Base import Tower
from Enemy import EnemyLogic
from Player import Controller, Resources
from AssetLoader import AssetLoader
from GameStats import GameStats
# Initialize pygame
pygame.init()
game_stats = GameStats()
# Load images
background = pygame.transform.scale(Images.day_default, (Resolution.WIDTH, Resolution.HEIGHT))
# Tower positions
PLAYER_TOWER_X = 0
ENEMY_TOWER_X = Resolution.WIDTH - 200
asset_loader = AssetLoader()
game_assets = asset_loader.load_all_assets()
# Initialize screen
screen = pygame.display.set_mode((Resolution.WIDTH, Resolution.HEIGHT))
pygame.display.set_caption("Block Battle Game")
current_mob_list = []
player_tower = Tower(PLAYER_TOWER_X, Color.BLUE, "Me", "img/castle/png/1/Asset 27.png")
enemy_spawn_timer = 0
Enemy = EnemyLogic()
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)
font_tiny = pygame.font.SysFont('Arial', 16)
player_resources = Resources()

clock = pygame.time.Clock()
level_num = 1
selected_hero_classes = []
game_progress = GameProgress()
# game_progress.unlock_all() # for testing


# Game states
class GameState:
    CHARACTER_SELECT = 0
    MAIN_GAME = 1
    LEVEL_COMPLETE = 2


# Initialize game state
current_state = GameState.CHARACTER_SELECT
selected_characters = []
cr_select = SelectGame(game_progress)  # This should be your SelectGame instance, not LevelSelect

# Main game loop
running = True
while running:
    clock.tick(Resolution.FPS)

    if current_state == GameState.CHARACTER_SELECT:
        selection_result = cr_select.selecting()
        if selection_result:  # Returns [level_num, selected_hero_classes]
            level_num, selected_hero_classes = selection_result
            current_state = GameState.MAIN_GAME
            # Initialize game with selected team
            player_tower = Tower(PLAYER_TOWER_X, Color.BLUE, "Me", "img/castle/png/1/Asset 27.png")
            enemy_tower = Tower(ENEMY_TOWER_X, Color.RED, "Enemy", "img/castle/png/1/Asset 27.png")

    elif current_state == GameState.MAIN_GAME:
        player_resources.add_start()

        Controller.keyboard(player_tower, player_resources, selected_hero_classes[:3])
        # Rest of your game loop...
        spawn, background = Enemy.pick_level(level_num, enemy_tower, player_resources)
        screen.blit(background, (0, 0))
        # Move blocks
        player_tower.take_dmg(enemy_tower)
        enemy_tower.take_dmg(player_tower)
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
        if not player_tower.dead_tower(enemy_tower):
            game_stats.record_outcome(True)  # Player won
        else:
            game_stats.record_outcome(False)  # Player lost
        if enemy_tower.dead_tower(player_tower) <= 0:
            # Unlock next level
            game_progress.complete_level(level_num)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and current_state == GameState.LEVEL_COMPLETE:
                    current_state = GameState.CHARACTER_SELECT  # Return to character select
                    cr_select = SelectGame(game_progress)  # Reset the selection screen
            game_stats.draw_stats_screen(screen)
            game_stats.reset_stats()
            player_resources.resources_reset()
            pygame.display.flip()
    pygame.display.flip()

        # game_stats.reset_stats()
        # # Level complete screen
        # screen.fill((0, 0, 0))
        # player_resources.resources_reset()
        # victory_text = font_large.render("Level Complete!", True, (255, 255, 255))
        # continue_text = font_medium.render("Press SPACE to continue", True, (255, 255, 255))
        #
        # screen.blit(victory_text,
        #             (Resolution.WIDTH // 2 - victory_text.get_width() // 2, Resolution.HEIGHT // 2 - 50))
        # screen.blit(continue_text,
        #             (Resolution.WIDTH // 2 - continue_text.get_width() // 2, Resolution.HEIGHT // 2 + 50))

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     elif current_state == GameState.LEVEL_COMPLETE:
        #         # Check if player won
        #         if enemy_tower.dead_tower(player_tower) <= 0:
        #             # Unlock next level
        #             game_progress.complete_level(level_num)
        #
        #     if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #         current_state = GameState.CHARACTER_SELECT  # Return to character select
        #         cr_select = SelectGame(game_progress)  # Reset the selection screen

    # pygame.display.flip()

pygame.quit()

if __name__ == "__main__":
    game = SelectGame()
    game.selecting()