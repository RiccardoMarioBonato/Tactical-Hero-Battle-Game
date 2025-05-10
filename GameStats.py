import csv
import time
from datetime import datetime
import pygame
from Customize import Resolution

class GameStats:
    def __init__(self):
        self.filename = "game_stats.csv"
        self._create_csv_if_not_exists()
        self.reset_stats()
        self.last_battle_duration = 0

    def reset_stats(self):
        self.start_time = time.time()
        self.units_deployed = {}
        self.damage_to_units = {}
        self.damage_to_towers = {}
        self.resources_used = {}
        self.battle_outcome = None
        self.level = 1

    def _create_csv_if_not_exists(self):
        try:
            with open(self.filename, 'x', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'level', 'outcome', 'duration',
                    'units_deployed', 'damage_to_units', 'damage_to_towers', 'resources_used'
                ])
        except FileExistsError:
            pass

    def record_unit_damage(self, unit_type, amount):
        current = self.damage_to_units.get(unit_type, 0)
        self.damage_to_units[unit_type] = round(current + amount, 2)

    def record_tower_damage(self, unit_type, amount):
        current = self.damage_to_towers.get(unit_type, 0)
        self.damage_to_towers[unit_type] = round(current + amount, 2)

    def record_resource_used(self, resource_type, amount):
        current = self.resources_used.get(resource_type, 0)
        self.resources_used[resource_type] = round(current + amount, 2)

    def record_outcome(self, won):
        self.battle_outcome = "win" if won else "loss"
        self.last_battle_duration = time.time() - self.start_time
        self._save_to_csv()

    def record_unit_deployed(self, unit_type):
        current = self.units_deployed.get(unit_type, 0)
        self.units_deployed[unit_type] = current + 1

    def _save_to_csv(self):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                self.level,
                self.battle_outcome or 'unknown',
                round(self.last_battle_duration, 2),
                str(self.units_deployed if self.units_deployed else {}),
                str(self.damage_to_units if self.damage_to_units else {}),
                str(self.damage_to_towers if self.damage_to_towers else {}),
                str(self.resources_used if self.resources_used else {})
            ])

    def draw_stats_screen(self, screen):
        # Use saved battle duration
        duration = round(self.last_battle_duration, 2)
        total_units = sum(self.units_deployed.values()) if self.units_deployed else 0
        total_damage_units = sum(self.damage_to_units.values()) if self.damage_to_units else 0
        total_damage_towers = sum(self.damage_to_towers.values()) if self.damage_to_towers else 0
        total_damage = total_damage_units + total_damage_towers

        # Set up display
        screen.fill((0, 0, 0))
        font_large = pygame.font.SysFont('Arial', 48)
        font_medium = pygame.font.SysFont('Arial', 32)

        # Display stats
        y_pos = 100
        texts = [
            f"Battle Result: {'VICTORY' if self.battle_outcome == 'win' else 'DEFEAT'}",
            f"Level: {self.level}",
            f"Duration: {duration:.2f} seconds",
            f"Total Units Deployed: {total_units}",
            f"Total Damage to Units: {total_damage_units}",
            f"Total Damage to Towers: {total_damage_towers}",
            f"Total Damage Overall: {total_damage}",
            "",
            "Units Deployed:"
        ]

        for text in texts:
            text_surface = font_medium.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (100, y_pos))
            y_pos += 40

        # Units deployed breakdown
        for unit_type, count in self.units_deployed.items():
            text = f"- {unit_type}: {count}"
            text_surface = font_medium.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (120, y_pos))
            y_pos += 30

        # Damage breakdown
        y_pos += 20
        damage_units_text = font_medium.render("Damage to Units:", True, (255, 255, 255))
        screen.blit(damage_units_text, (100, y_pos))
        y_pos += 40

        for unit_type, damage in self.damage_to_units.items():
            text = f"- {unit_type}: {damage}"
            text_surface = font_medium.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (120, y_pos))
            y_pos += 30

        # Damage to towers
        y_pos += 20
        damage_towers_text = font_medium.render("Damage to Towers:", True, (255, 255, 255))
        screen.blit(damage_towers_text, (100, y_pos))
        y_pos += 40

        for unit_type, damage in self.damage_to_towers.items():
            text = f"- {unit_type}: {damage}"
            text_surface = font_medium.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (120, y_pos))
            y_pos += 30

        # Resources used
        y_pos += 20
        resource_text = font_medium.render("Resources Used:", True, (255, 255, 255))
        screen.blit(resource_text, (100, y_pos))
        y_pos += 40

        for res_type, amount in self.resources_used.items():
            text = f"- {res_type}: {amount}"
            text_surface = font_medium.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (120, y_pos))
            y_pos += 30

        # Continue prompt
        continue_text = font_large.render("Press SPACE to continue", True, (255, 255, 255))
        screen.blit(continue_text,
                    (Resolution.WIDTH // 2 - continue_text.get_width() // 2, Resolution.HEIGHT - 100))


game_stats = GameStats()
