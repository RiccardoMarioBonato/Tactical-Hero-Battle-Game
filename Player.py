import pygame
from Unit import *
from Customize import Color, Images, Resolution, Dimensions
import time
import sys


# Correct mapping that matches your units tuple order
key_unit_mapping = {
    pygame.K_c: 0,  # LumberJack (index 0)
    pygame.K_v: 1,   # Pantheon (index 1)
    pygame.K_b: 2,   # BrownBeard (index 2)
    pygame.K_n: 3,   # Kitsune (index 3)
    pygame.K_m: 4    # YamabushiTengu (index 4)
}
game_stats = GameStats()
# # Make sure this matches exactly with the mapping above
# units = (
#     LumberJack(0,0),   # index 0 (C)
#     Pantheon(0,0),     # index 1 (V)
#     BrownBeard(0,0),    # index 2 (B)
#     Kitsune(0,0),      # index 3 (N)
#     YamabushiTengu(0,0) # index 4 (M)
# )


class Controller:
    @staticmethod
    def keyboard(player_tower, resources, selected_units):
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Use the first 3 selected units
                if event.key == pygame.K_c and len(selected_units) > 0:
                    unit_class = selected_units[0]
                    unit_instance = unit_class(0, 0)  # Create temporary instance
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
        resources.remove_solar_energy(new_unit.cost[0])
        resources.remove_lunar_energy(new_unit.cost[1])
        resources.remove_eclipse_energy(new_unit.cost[2])
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
        self.clock = None  # Store a timestamp (float) here
        self.font1 = pygame.font.Font(None, 36)  # Smaller font for resource display
        self.font2 = pygame.font.Font(None, 72)
        self.rect = pygame.Rect(10, 10, 300, 50)  # Position and size of the resource bar
        self.current_time = 0

    def add_energy(self, multiplier):
        current_time = time.time()
        time_elapsed = current_time - self.clock
        self.solar_energy += time_elapsed * multiplier[0] * 100
        self.lunar_energy += time_elapsed * multiplier[1]* 100
        self.eclipse_energy += time_elapsed * multiplier[2]* 100
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
        # Initialize the clock with the current time
        if self.clock is None:
            self.clock = time.time()

    def resources_reset(self):
        self.clock = None
        self.game_clock = 0
        self.solar_energy = 0
        self.lunar_energy = 0
        self.eclipse_energy = 0

    def draw(self, screen):
        # Create a background rectangle for the resource bar

        # Display the resource values
        solar_text = self.font1.render(f"Solar: {int(self.solar_energy)}", True, (255, 255, 0))  # Yellow
        lunar_text = self.font1.render(f"Lunar: {int(self.lunar_energy)}", True, (0, 255, 255))  # Cyan
        eclipse_text = self.font1.render(f"Eclipse: {int(self.eclipse_energy)}", True, (255, 0, 255))  # Magenta
        timer_text = self.font1.render(f"TIME: {int(self.game_clock)}", True, (0, 0, 0))

        # Position the text within the resource bar
        screen.blit(timer_text, (self.rect.x + 890, self.rect.y + 10))
        screen.blit(solar_text, (self.rect.x + 770, self.rect.y + 60))
        screen.blit(lunar_text, (self.rect.x + 890, self.rect.y + 60))
        screen.blit(eclipse_text, (self.rect.x + 1010, self.rect.y + 60))
