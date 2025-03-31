import csv
import time
from datetime import datetime
import pygame
import Customize
from Customize import Resolution


class GameStats:
    def __init__(self):
        self.reset_stats()
        self.filename = "game_stats.csv"
        self._create_csv_if_not_exists()

    def reset_stats(self):
        self.start_time = time.time()
        self.units_deployed = {}
        self.damage_dealt = {}
        self.resources_used = {}
        self.battle_outcome = None
        self.level = 1

    def _create_csv_if_not_exists(self):
        try:
            with open(self.filename, 'x', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'level', 'outcome', 'duration',
                    'units_deployed', 'damage_dealt', 'resources_used'
                ])
        except FileExistsError:
            pass

    def record_unit_deployed(self, unit_type):
        self.units_deployed[unit_type] = self.units_deployed.get(unit_type, 0) + 1

    def record_damage(self, unit_type, amount):
        self.damage_dealt[unit_type] = self.damage_dealt.get(unit_type, 0) + amount

    def record_resource_used(self, resource_type, amount):
        self.resources_used[resource_type] = self.resources_used.get(resource_type, 0) + amount

    def record_outcome(self, won):
        self.battle_outcome = "win" if won else "loss"
        self._save_to_csv()

    def _save_to_csv(self):
        duration = time.time() - self.start_time
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                self.level,
                self.battle_outcome,
                duration,
                str(self.units_deployed),
                str(self.damage_dealt),
                str(self.resources_used)
            ])

    def draw_stats_screen(self, screen):
        # Calculate stats
        duration = time.time() - self.start_time
        total_units = sum(self.units_deployed.values())
        total_damage = sum(self.damage_dealt.values())

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
            f"Total Damage Dealt: {total_damage}",
            "",
            "Units Deployed:"
        ]

        # Render basic stats
        for text in texts:
            text_surface = font_medium.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (100, y_pos))
            y_pos += 40

        # Render units deployed breakdown
        for unit_type, count in self.units_deployed.items():
            text = f"- {unit_type}: {count}"
            text_surface = font_medium.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (120, y_pos))
            y_pos += 30

        # Add damage dealt section
        y_pos += 20
        damage_text = font_medium.render("Damage Breakdown:", True, (255, 255, 255))
        screen.blit(damage_text, (100, y_pos))
        y_pos += 40

        for unit_type, damage in self.damage_dealt.items():
            text = f"- {unit_type}: {damage}"
            text_surface = font_medium.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (120, y_pos))
            y_pos += 30

        # Add resource usage section
        y_pos += 20
        resource_text = font_medium.render("Resources Used:", True, (255, 255, 255))
        screen.blit(resource_text, (100, y_pos))
        y_pos += 40

        for res_type, amount in self.resources_used.items():
            text = f"- {res_type}: {amount}"
            text_surface = font_medium.render(text, True, (200, 200, 200))
            screen.blit(text_surface, (120, y_pos))
            y_pos += 30

        # Add continue prompt
        continue_text = font_large.render("Press SPACE to continue", True, (255, 255, 255))
        screen.blit(continue_text, (
        Resolution.WIDTH // 2 - continue_text.get_width() // 2, Resolution.HEIGHT - 100))
