import pygame
from Unit import *
from Customize import Color, Images, Resolution, Dimensions
import time
import sys
all_hero_dict = {"Lumberjack": LumberJack, "Pantheon": Pantheon, "BrownBeard": BrownBeard}


# Correct mapping that matches your units tuple order
key_unit_mapping = {
    pygame.K_c: 0,  # LumberJack (index 0)
    pygame.K_v: 1,   # Pantheon (index 1)
    pygame.K_b: 2,   # BrownBeard (index 2)
    pygame.K_n: 3,   # Kitsune (index 3)
    pygame.K_m: 4    # YamabushiTengu (index 4)
}

# Make sure this matches exactly with the mapping above
units = (
    LumberJack(0,0),   # index 0 (C)
    Pantheon(0,0),     # index 1 (V)
    BrownBeard(0,0),    # index 2 (B)
    Kitsune(0,0),      # index 3 (N)
    YamabushiTengu(0,0) # index 4 (M)
)


class Controller:
    @staticmethod
    def keyboard(player_tower, resources):
        global key_unit_mapping, units

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in key_unit_mapping:
                    unit_index = key_unit_mapping[event.key]
                    if unit_index is not None and unit_index < len(units):
                        unit = units[unit_index]

                        # Create new instance at correct position
                        spawn_x = player_tower.rect.right
                        spawn_y = Resolution.HEIGHT - 300 - Dimensions.BLOCK_SIZE1 // 2

                        if resources.solar_energy >= unit.cost:
                            new_unit = type(unit)(spawn_x, spawn_y)
                            player_tower.block.append(new_unit)
                            resources.remove_solar_energy(unit.cost)


class selected_hero:
    def __init__(self):
        self.hero1 = LumberJack
        self.hero2 = Pantheon
        self.hero3 = BrownBeard

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
        self.clock = 0  # Store a timestamp (float) here
        self.font1 = pygame.font.Font(None, 36)  # Smaller font for resource display
        self.rect = pygame.Rect(10, 10, 300, 50)  # Position and size of the resource bar
        self.current_time = 0

    def add_solar_energy(self):
         # Calculate the time difference since the last update
         current_time = time.time()
         time_elapsed = current_time - self.clock
         self.solar_energy += time_elapsed
         self.clock = current_time  # Update the timestamp

    def remove_solar_energy(self, cost):
        self.solar_energy -= cost

    def add_lunar_energy(self):
        # Calculate the time difference since the last update
        time_elapsed = self.current_time - self.clock
        self.lunar_energy += time_elapsed/2
        self.clock = self.current_time  # Update the timestamp

    def remove_lunar_energy(self, cost):
        self.lunar_energy -= cost

    def get_solar_energy(self):
        return self.solar_energy
    def add_eclipse_energy(self):
        # Calculate the time difference since the last update
        time_elapsed = self.current_time - self.clock
        self.eclipse_energy += time_elapsed/10
        self.clock = self.current_time  # Update the timestamp

    def remove_eclipse_energy(self, cost):
        self.eclipse_energy -= cost

    def add_start(self):
        # Initialize the clock with the current time
        self.clock = time.time()

    def draw(self, screen):
        # Create a background rectangle for the resource bar

        # Display the resource values
        solar_text = self.font1.render(f"Solar: {int(self.solar_energy)}", True, (255, 255, 0))  # Yellow
        lunar_text = self.font1.render(f"Lunar: {int(self.lunar_energy)}", True, (0, 255, 255))  # Cyan
        eclipse_text = self.font1.render(f"Eclipse: {int(self.eclipse_energy)}", True, (255, 0, 255))  # Magenta

        # Position the text within the resource bar
        screen.blit(solar_text, (self.rect.x + 770, self.rect.y + 10))
        screen.blit(lunar_text, (self.rect.x + 890, self.rect.y + 10))
        screen.blit(eclipse_text, (self.rect.x + 1010, self.rect.y + 10))

    def all_add(self):
        pass
        # self.add_lunar_energy()
        # self.add_solar_energy()
        # self.add_eclipse_energy()