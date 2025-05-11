import pygame
from Unit import *
from Customize import Color, Images, Resolution, Dimensions
import time
import sys
from GameStats import game_stats


# Correct mapping that matches your units tuple order
key_unit_mapping = {
    pygame.K_c: 0,
    pygame.K_v: 1,
    pygame.K_b: 2,
    pygame.K_n: 3,
    pygame.K_m: 4
}


class Controller:
    @staticmethod
    def keyboard(player_tower, resources, selected_units, exit_button_rect):
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                # Use the first 3 selected units
                if event.key == pygame.K_c and len(selected_units) > 0:
                    unit_class = selected_units[0]
                    unit_instance = unit_class(0, 0)
                    if (resources.solar_energy >= unit_instance.cost[0] and
                            resources.lunar_energy >= unit_instance.cost[1] and
                            resources.eclipse_energy >= unit_instance.cost[2]):
                        Controller.spawn_unit(unit_class, player_tower, resources)

                if event.key == pygame.K_v and len(selected_units) > 1:
                    unit_class = selected_units[1]
                    unit_instance = unit_class(0, 0)
                    if (resources.solar_energy >= unit_instance.cost[0] and
                            resources.lunar_energy >= unit_instance.cost[1] and
                            resources.eclipse_energy >= unit_instance.cost[2]):
                        Controller.spawn_unit(unit_class, player_tower, resources)

                if event.key == pygame.K_b and len(selected_units) > 2:
                    unit_class = selected_units[2]
                    unit_instance = unit_class(0, 0)
                    if (resources.solar_energy >= unit_instance.cost[0] and
                            resources.lunar_energy >= unit_instance.cost[1] and
                            resources.eclipse_energy >= unit_instance.cost[2]):
                        Controller.spawn_unit(unit_class, player_tower, resources)

    @staticmethod
    def spawn_unit(unit_class, player_tower, resources):
        spawn_x = player_tower.rect.right
        spawn_y = Resolution.HEIGHT - 300 - Dimensions.BLOCK_SIZE1 // 2
        new_unit = unit_class(spawn_x, spawn_y)
        player_tower.block.append(new_unit)
        # Deduct resources
        resources.remove_solar_energy(new_unit.cost[0])
        resources.remove_lunar_energy(new_unit.cost[1])
        resources.remove_eclipse_energy(new_unit.cost[2])
        # Record unit deployed count
        game_stats.record_unit_deployed(unit_class.__name__)
        game_stats.record_resource_used("solar", new_unit.cost[0])
        game_stats.record_resource_used("lunar", new_unit.cost[1])
        game_stats.record_resource_used("eclipse", new_unit.cost[2])


class Resources:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Resources, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.solar_energy = 0
        self.lunar_energy = 0
        self.eclipse_energy = 0
        self.game_clock = 0
        self.clock = None
        self.font1 = pygame.font.Font(None, 36)
        self.font2 = pygame.font.Font(None, 72)
        self.rect = pygame.Rect(10, 10, 300, 50)
        self.current_time = 0

    def add_energy(self, multiplier):
        current_time = time.time()
        time_elapsed = current_time - self.clock
        self.solar_energy += time_elapsed * multiplier[0]
        self.lunar_energy += time_elapsed * multiplier[1]
        self.eclipse_energy += time_elapsed * multiplier[2]
        self.game_clock += time_elapsed
        self.clock = current_time

    def remove_solar_energy(self, cost):
        self.solar_energy -= cost

    def remove_lunar_energy(self, cost):
        self.lunar_energy -= cost

    def get_solar_energy(self):
        return self.solar_energy

    def remove_eclipse_energy(self, cost):
        self.eclipse_energy -= cost

    def add_start(self):
        if self.clock is None:
            self.clock = time.time()

    def resources_reset(self):
        self.clock = None
        self.game_clock = 0
        self.solar_energy = 0
        self.lunar_energy = 0
        self.eclipse_energy = 0

    def draw(self, screen):
        # Draw resource texts
        solar_text = self.font1.render(f"Solar: {int(self.solar_energy)}", True, (255, 255, 0))
        lunar_text = self.font1.render(f"Lunar: {int(self.lunar_energy)}", True, (0, 255, 255))
        eclipse_text = self.font1.render(f"Eclipse: {int(self.eclipse_energy)}", True, (255, 0, 255))
        timer_text = self.font1.render(f"TIME: {int(self.game_clock)}", True, (0, 0, 0))

        screen.blit(timer_text, (self.rect.x + 890, self.rect.y + 10))
        screen.blit(solar_text, (self.rect.x + 770, self.rect.y + 60))
        screen.blit(lunar_text, (self.rect.x + 890, self.rect.y + 60))
        screen.blit(eclipse_text, (self.rect.x + 1010, self.rect.y + 60))

    def draw_selected_heroes(self, screen, selected_hero_classes, font):
        x_start = self.rect.x + 770
        y_start = self.rect.y + 100
        spacing = 25

        color_map = {
            'solar': (255, 255, 0),
            'lunar': (100, 149, 237),
            'eclipse': (138, 43, 226)
        }

        for i, hero_class in enumerate(selected_hero_classes):
            config = UnitConfig().get_unit_config(hero_class.__name__)
            cost = config.get('cost', [0, 0, 0])
            keybinds = ['C', 'V', 'B']
            key_text = font.render(f"[{keybinds[i]}]", True, (255, 255, 255))
            name_text = font.render(f"{hero_class.__name__}", True, (255, 255, 255))
            solar_text = font.render(f"S:{cost[0]}", True, color_map['solar'])
            lunar_text = font.render(f"L:{cost[1]}", True, color_map['lunar'])
            eclipse_text = font.render(f"E:{cost[2]}", True, color_map['eclipse'])
            line_y = y_start + i * spacing
            screen.blit(key_text, (x_start, line_y))
            screen.blit(name_text, (x_start + 40, line_y))
            screen.blit(solar_text, (x_start + 190, line_y))
            screen.blit(lunar_text, (x_start + 270, line_y))
            screen.blit(eclipse_text, (x_start + 350, line_y))

    @staticmethod
    def draw_exit_button(screen, font):
        text = "Exit"
        text_surface = font.render(text, True, (255, 255, 255))

        # Calculate position at bottom center, a little lower
        text_x = (Resolution.WIDTH - text_surface.get_width()) // 2
        text_y = Resolution.HEIGHT - 40  # lower on the screen

        # Draw the text
        screen.blit(text_surface, (text_x, text_y))

        # Return a rect for click detection
        return pygame.Rect(text_x, text_y, text_surface.get_width(), text_surface.get_height())

