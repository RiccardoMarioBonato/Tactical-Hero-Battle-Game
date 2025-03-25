import pygame
from Unit import LumberJack, Pantheon, BrownBeard
from Customize import Color, Images, Resolution, Dimensions
import time


class Controller:
    @staticmethod
    def keyboard(player_tower, resources):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SystemExit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if resources.solar_energy >= 3:
                        player_tower.block.append(LumberJack(player_tower.rect.right,
                                                             Resolution.HEIGHT - 300 - Dimensions.BLOCK_SIZE1 // 2))
                        resources.remove_solar_energy(3)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if resources.solar_energy >= 8:
                        player_tower.block.append(Pantheon(player_tower.rect.right,
                                                              Resolution.HEIGHT - 300 - Dimensions.BLOCK_SIZE1 // 2))
                        resources.remove_solar_energy(8)
                if event.key == pygame.K_v:
                    if resources.solar_energy >= 5:
                        player_tower.block.append(BrownBeard(player_tower.rect.right,
                                                          Resolution.HEIGHT - 300 - Dimensions.BLOCK_SIZE1 // 2))
                        resources.remove_solar_energy(5)


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