import pygame
from Level_select import SelectGame, GameProgress
from Customize import Color, Images, Resolution, Fonts
from Base import Tower
from Enemy import EnemyLogic
from Player import Controller, Resources
from AssetLoader import AssetLoader
from GameStats import game_stats
import multiprocessing

multiprocessing.set_start_method('spawn', force=True)
# Initialize pygame
pygame.init()
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
font_medium = Fonts.ARIAL_32
font_large = Fonts.ARIAL_48
font_small = Fonts.ARIAL_24
font_tiny = Fonts.ARIAL_16
player_resources = Resources()
clock = pygame.time.Clock()
level_num = 1
selected_hero_classes = []
game_progress = GameProgress()


# Game states
class GameState:
    CHARACTER_SELECT = 0
    MAIN_GAME = 1
    LEVEL_COMPLETE = 2


# Initialize game state
current_state = GameState.CHARACTER_SELECT
selected_characters = []
cr_select = SelectGame(game_progress)
exit_button_rect = Resources.draw_exit_button(screen, font_small)
# Main game loop
running = True
while running:
    clock.tick(Resolution.FPS)

    if current_state == GameState.CHARACTER_SELECT:
        # Character selection
        game_stats.reset_stats()
        selection_result = cr_select.selecting()
        if selection_result:
            level_num, selected_hero_classes = selection_result
            game_stats.level = level_num
            current_state = GameState.MAIN_GAME
            player_tower = Tower(PLAYER_TOWER_X, Color.BLUE, "Me", "img/castle/png/1/Asset 27.png")
            enemy_tower = Tower(ENEMY_TOWER_X, Color.RED, "Enemy", "img/castle/png/1/Asset 27.png")
        pygame.display.flip()

    elif current_state == GameState.MAIN_GAME:
        # Gameplay
        player_resources.add_start()
        Controller.keyboard(player_tower, player_resources, selected_hero_classes[:3], exit_button_rect)
        spawn, background = Enemy.pick_level(level_num, enemy_tower, player_resources)
        screen.blit(background, (0, 0))
        player_tower.take_dmg(enemy_tower)
        enemy_tower.take_dmg(player_tower)
        player_tower.draw(screen)
        enemy_tower.draw(screen)
        player_resources.draw(screen)
        player_resources.draw_selected_heroes(screen, selected_hero_classes[:3], font_small)
        exit_button_rect = Resources.draw_exit_button(screen, font_small)

        for char in player_tower.block[:]:
            char.update(screen, player_tower, player_tower.block, enemy_tower.block)
            if char.dead:
                player_tower.block.remove(char)
            else:
                for enemy_unit in enemy_tower.block[:]:
                    if char.rect.colliderect(enemy_unit.rect):
                        game_stats.record_unit_damage(char.__class__.__name__, char.attack_power)

        for unit in enemy_tower.block[:]:
            unit.update(screen, enemy_tower, enemy_tower.block, player_tower.block)
            if unit.dead:
                enemy_tower.block.remove(unit)

        # Transition logic
        if enemy_tower.hp <= 0:
            current_state = GameState.LEVEL_COMPLETE
            game_stats.record_outcome(True)
            game_progress.complete_level(level_num)
        elif player_tower.hp <= 0:
            current_state = GameState.LEVEL_COMPLETE
            game_stats.record_outcome(False)

        pygame.display.flip()

    elif current_state == GameState.LEVEL_COMPLETE:
        # Show results screen and wait for next round
        game_stats.draw_stats_screen(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_stats.reset_stats()
                player_resources.resources_reset()
                current_state = GameState.CHARACTER_SELECT
                cr_select = SelectGame(game_progress)

pygame.quit()

if __name__ == "__main__":
    game = SelectGame()
    game.selecting()
