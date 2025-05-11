# At the top of GameStats.py
import csv
import time
from datetime import datetime
import pygame
from Customize import Resolution
import matplotlib.pyplot as plt
import io

class GameStats:
    def __init__(self):
        self.filename = "Graphs/game_stats.csv"
        self._create_csv_if_not_exists()
        self.reset_stats()
        self.last_battle_duration = 0
        self.bg_image = pygame.image.load("img/backgrounds/Cartoon_Forest_BG_02.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (Resolution.WIDTH, Resolution.HEIGHT))

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
        self.damage_to_units[unit_type] = round(self.damage_to_units.get(unit_type, 0) + amount, 2)

    def record_tower_damage(self, unit_type, amount):
        self.damage_to_towers[unit_type] = round(self.damage_to_towers.get(unit_type, 0) + amount, 2)

    def record_resource_used(self, resource_type, amount):
        self.resources_used[resource_type] = round(self.resources_used.get(resource_type, 0) + amount, 2)

    def record_outcome(self, won):
        self.battle_outcome = "win" if won else "loss"
        self.last_battle_duration = time.time() - self.start_time
        self._save_to_csv()

    def record_unit_deployed(self, unit_type):
        self.units_deployed[unit_type] = self.units_deployed.get(unit_type, 0) + 1

    def _save_to_csv(self):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                self.level,
                self.battle_outcome or 'unknown',
                round(self.last_battle_duration, 2),
                str(self.units_deployed),
                str(self.damage_to_units),
                str(self.damage_to_towers),
                str(self.resources_used)
            ])

    def draw_stats_screen(self, screen):
        # Calculate stats
        duration = round(self.last_battle_duration, 2)
        total_units = sum(self.units_deployed.values()) if self.units_deployed else 0
        total_damage_units = sum(self.damage_to_units.values()) if self.damage_to_units else 0
        total_damage_towers = sum(self.damage_to_towers.values()) if self.damage_to_towers else 0
        total_damage = total_damage_units + total_damage_towers

        # Draw background
        screen.blit(self.bg_image, (0, 0))

        # Add semi-transparent overlay
        overlay = pygame.Surface((Resolution.WIDTH, Resolution.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Font setup with smaller sizes
        try:
            font_large = pygame.font.SysFont('Arial', 50, bold=True)
            font_medium = pygame.font.SysFont('Arial', 28)
            font_small = pygame.font.SysFont('Arial', 22)
        except:
            font_large = pygame.font.SysFont(None, 50, bold=True)
            font_medium = pygame.font.SysFont(None, 28)
            font_small = pygame.font.SysFont(None, 22)

        # Colors
        victory_color = (100, 255, 100) if self.battle_outcome == 'win' else (255, 100, 100)
        accent_color = (100, 200, 255)
        text_color = (240, 240, 240)
        highlight_color = (255, 255, 150)

        # Main header
        result_text = "VICTORY" if self.battle_outcome == 'win' else "DEFEAT"
        result_surf = font_large.render(result_text, True, victory_color)
        result_rect = result_surf.get_rect(center=(Resolution.WIDTH // 2, 70))
        screen.blit(result_surf, result_rect)

        # LEFT COLUMN - Battle Summary (simple text layout)
        left_x = 30
        current_y = 140

        # Section header
        header_left = font_medium.render("BATTLE SUMMARY", True, accent_color)
        screen.blit(header_left, (left_x, current_y))
        current_y += 40

        # Format large numbers for display
        def format_number(num):
            if isinstance(num, (int, float)):
                if num >= 1000000:
                    return f"{num / 1000000:.1f}M"
                elif num >= 1000:
                    return f"{num / 1000:.1f}K"
            return str(num)

        # Summary metrics
        metrics = [
            ("Level:", str(self.level)),
            ("Duration:", f"{duration}s"),
            ("Units Deployed:", format_number(total_units)),
            ("Total Damage:", format_number(total_damage))
        ]

        for title, value in metrics:
            # Render title and value
            title_surf = font_small.render(title, True, text_color)
            val_surf = font_small.render(value, True, highlight_color)

            # Draw with consistent spacing
            screen.blit(title_surf, (left_x, current_y))
            screen.blit(val_surf, (left_x + 150, current_y))  # Fixed value position

            current_y += 32

        # RIGHT COLUMN - Detailed Statistics
        right_x = Resolution.WIDTH // 2 + 20
        current_y = 140

        # Section header
        header_right = font_medium.render("DETAILED STATS", True, accent_color)
        screen.blit(header_right, (right_x, current_y))
        current_y += 40

        # Function to draw a stat category
        def draw_stat_category(title, stats_dict):
            nonlocal current_y
            if not stats_dict:
                return

            # Category title
            cat_surf = font_small.render(title + ":", True, accent_color)
            screen.blit(cat_surf, (right_x, current_y))
            current_y += 30

            # Stats items
            for name, value in stats_dict.items():
                # Truncate long names and format values
                display_name = name if len(name) < 18 else name[:15] + "..."
                display_value = format_number(value)

                # Render stat line
                stat_text = f"  {display_name}: {display_value}"
                stat_surf = font_small.render(stat_text, True, text_color)
                screen.blit(stat_surf, (right_x, current_y))

                current_y += 26

        # Draw all stat categories
        draw_stat_category("Units", self.units_deployed)
        draw_stat_category("Damage to Units", self.damage_to_units)
        draw_stat_category("Damage to Towers", self.damage_to_towers)
        draw_stat_category("Resources Used", self.resources_used)

        # Continue prompt at bottom
        continue_text = font_medium.render("Press SPACE to continue...", True, (200, 200, 255))
        screen.blit(continue_text, (
        Resolution.WIDTH // 2 - continue_text.get_width() // 2, Resolution.HEIGHT - 60))

        # Add subtle divider line between columns
        pygame.draw.line(screen, (100, 100, 100, 150),
                         (Resolution.WIDTH // 2, 130),
                         (Resolution.WIDTH // 2, Resolution.HEIGHT - 80), 1)

game_stats = GameStats()
