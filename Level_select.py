import pygame
import sys
from pygame.locals import *
from Customize import Hero
from Unit import *
# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (100, 100, 100)
LOCKED_COLOR = (150, 150, 150)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hero Selector with Level Progression")
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)
font_tiny = pygame.font.SysFont('Arial', 16)


class GameState:
    def __init__(self):
        self.unlocked_levels = 1  # Start with level 1 unlocked
        self.selected_team = []
        self.player_progress = {
            "level1_completed": False,
            "level2_completed": False,
            "level3_completed": False,
            # Add more levels as needed
        }


class LevelSelect:
    def __init__(self, game_state):
        self.game_state = game_state
        self.levels = [
            {"name": "Forest", "number": 1, "rect": pygame.Rect(300, 300, 300, 200),
             "locked": False},
            {"name": "Dungeon", "number": 2, "rect": pygame.Rect(700, 300, 300, 200),
             "locked": True},
            {"name": "Castle", "number": 3, "rect": pygame.Rect(1100, 300, 300, 200),
             "locked": True},
            {"name": "Volcano", "number": 4, "rect": pygame.Rect(300, 600, 300, 200),
             "locked": True},
            {"name": "Sky Temple", "number": 5, "rect": pygame.Rect(700, 600, 300, 200),
             "locked": True},
            {"name": "Final Battle", "number": 6, "rect": pygame.Rect(1100, 600, 300, 200),
             "locked": True}
        ]
        self.back_button = pygame.Rect(50, 950, 200, 80)
        self.update_locked_status()


    def update_locked_status(self):
        for level in self.levels:
            level["locked"] = level["number"] > self.game_state.unlocked_levels

    def draw(self, screen):
        screen.fill(WHITE)

        # Draw title
        title = font_large.render("SELECT LEVEL", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Draw levels
        for level in self.levels:
            color = BLUE if not level["locked"] else LOCKED_COLOR
            pygame.draw.rect(screen, color, level["rect"])

            # Level name
            name = font_medium.render(level["name"], True, WHITE)
            screen.blit(name, (level["rect"].x + level["rect"].width // 2 - name.get_width() // 2,
                               level["rect"].y + 40))

            # Level number
            num = font_large.render(f"Level {level['number']}", True, WHITE)
            screen.blit(num, (level["rect"].x + level["rect"].width // 2 - num.get_width() // 2,
                              level["rect"].y + 80))

            # Lock icon if locked
            if level["locked"]:
                lock = font_large.render("🔒", True, WHITE)
                screen.blit(lock,
                            (level["rect"].x + level["rect"].width // 2 - lock.get_width() // 2,
                             level["rect"].y + 120))

        # Draw back button
        pygame.draw.rect(screen, GRAY, self.back_button)
        back_text = font_medium.render("Back", True, BLACK)
        screen.blit(back_text,
                    (self.back_button.x + self.back_button.width // 2 - back_text.get_width() // 2,
                     self.back_button.y + self.back_button.height // 2 - back_text.get_height() // 2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Check level selection
                for level in self.levels:
                    if level["rect"].collidepoint(mouse_pos) and not level["locked"]:
                        return f"level{level['number']}"  # Return level identifier

                # Check back button
                if self.back_button.collidepoint(mouse_pos):
                    return "back"

        return None


class CharacterSelect:
    all_hero_dict = {"Lumberjack": LumberJack, "Pantheon": Pantheon,
                      "BrownBeard": BrownBeard}

    def __init__(self, game_state):
        self.game_state = game_state
        self.characters = self.create_character_list()
        self.back_button = pygame.Rect(50, 950, 200, 80)
        self.start_button = pygame.Rect(1670, 950, 200, 80)
        self.selected_characters = []
        self.max_selection = 3


    def create_character_list(self):
        characters = []
        positions = [
            # Row 1
            (100, 200), (350, 200), (600, 200), (850, 200), (1100, 200), (1350, 200),
            # Row 2
            (100, 450), (350, 450), (600, 450), (850, 450), (1100, 450), (1350, 450),
            # Row 3
            (100, 700), (350, 700), (600, 700), (850, 700), (1100, 700), (1350, 700)
        ]

        # Character image mapping - replace with your actual image paths
        character_images = {
            "Lumberjack": "Heros/LumberJack/lumberjack_select_photo.webp",
            "Pantheon": "Heros/LumberJack/lumberjack_select_photo.webp",
            "BrownBeard": "Heros/LumberJack/lumberjack_select_photo.webp",
            # Add all other characters with their corresponding image paths
        }

        class_data = [
            ("Pantheon", "Warrior"), ("Lumberjack", "Warrior"), ("BrownBeard", "Warrior"),
            ("Mage", "Wizard"), ("Rogue", "Assassin"), ("Cleric", "Healer"),
            ("Knight", "Paladin"), ("Ninja", "Stealth"), ("Alchemist", "Support"),
            ("Berserker", "Brawler"), ("Druid", "Shapeshifter"), ("Engineer", "Builder"),
            ("Samurai", "Duelist"), ("Necromancer", "Summoner"), ("Monk", "Martial Artist"),
            ("Bard", "Buffer"), ("Gunslinger", "Marksman"), ("Witch", "Debuffer")
        ]

        for i, ((x, y), (name, char_class)) in enumerate(zip(positions, class_data)):
            # Load character image
            try:
                image = pygame.image.load(character_images[name]).convert_alpha()
                image = pygame.transform.scale(image, (180, 220))
            except:
                # Fallback to colored rectangle if image fails to load
                image = pygame.Surface((180, 220))
                color = (200, 200, 200)  # Default gray
                image.fill(color)
                # Add character number as fallback
                char_num = font_tiny.render(f"#{i + 1}", True, BLACK)
                image.blit(char_num, (5, 5))

            characters.append({
                "name": name,
                "class": char_class,
                "image": image,  # Now using actual image instead of colored surface
                "selected": False,
                "rect": pygame.Rect(x, y, 200, 250),
                "locked": i >= 6 and self.game_state.unlocked_levels < 2
            })

        return characters

    def draw(self, screen):
        screen.fill(WHITE)

        # Draw title
        title = font_large.render("SELECT YOUR TEAM (MAX 3 HEROES)", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Draw selection counter
        counter = font_medium.render(
            f"Selected: {len(self.selected_characters)}/{self.max_selection}", True, BLACK)
        screen.blit(counter, (SCREEN_WIDTH // 2 - counter.get_width() // 2, 120))

        # Draw characters
        for char in self.characters:
            # Draw character image (darker if locked)
            char_image = char["image"].copy()
            if char["locked"]:
                char_image.fill((100, 100, 100, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(char_image, (char["rect"].x + 10, char["rect"].y + 10))

            # Draw character name and class
            name = font_small.render(char["name"], True, BLACK)
            screen.blit(name, (char["rect"].x + char["rect"].width // 2 - name.get_width() // 2,
                               char["rect"].y + char["rect"].height - 50))

            char_class = font_tiny.render(char["class"], True, BLACK)
            screen.blit(char_class,
                        (char["rect"].x + char["rect"].width // 2 - char_class.get_width() // 2,
                         char["rect"].y + char["rect"].height - 25))

            # Draw selection border or lock status
            if char["locked"]:
                pygame.draw.rect(screen, LOCKED_COLOR, char["rect"], 3)
                lock = font_medium.render("🔒", True, BLACK)
                screen.blit(lock, (char["rect"].x + char["rect"].width // 2 - lock.get_width() // 2,
                                   char["rect"].y + char[
                                       "rect"].height // 2 - lock.get_height() // 2))
            elif char["selected"]:
                pygame.draw.rect(screen, GREEN, char["rect"], 3)
            else:
                pygame.draw.rect(screen, BLACK, char["rect"], 1)

        # Draw buttons
        pygame.draw.rect(screen, GRAY, self.back_button)
        back_text = font_medium.render("Back", True, BLACK)
        screen.blit(back_text,
                    (self.back_button.x + self.back_button.width // 2 - back_text.get_width() // 2,
                     self.back_button.y + self.back_button.height // 2 - back_text.get_height() // 2))

        # Start button (only enabled with selections)
        start_btn_color = GREEN if self.selected_characters else DARK_GRAY
        pygame.draw.rect(screen, start_btn_color, self.start_button)
        start_text = font_medium.render("Start", True, BLACK)
        screen.blit(start_text, (
            self.start_button.x + self.start_button.width // 2 - start_text.get_width() // 2,
            self.start_button.y + self.start_button.height // 2 - start_text.get_height() // 2))

        # Draw selected team preview
        if self.selected_characters:
            team_text = font_medium.render("Your Team:", True, BLACK)
            screen.blit(team_text, (50, 900))

            for i, char_name in enumerate(self.selected_characters):
                char_info = font_small.render(f"{i + 1}. {char_name}", True, BLACK)
                screen.blit(char_info, (50 + i * 300, 930))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Check character selection
                for char in self.characters:
                    if char["rect"].collidepoint(mouse_pos) and not char["locked"]:
                        if char["selected"]:
                            # Deselect
                            char["selected"] = False
                            self.selected_characters.remove(char["name"])
                        else:
                            # Select if under max limit
                            if len(self.selected_characters) < self.max_selection:
                                char["selected"] = True
                                self.selected_characters.append(char["name"])
                            else:
                                # Show max selection feedback
                                feedback = font_medium.render("Max 3 heroes selected!", True, RED)
                                screen.blit(feedback,
                                            (SCREEN_WIDTH // 2 - feedback.get_width() // 2, 170))
                                pygame.display.flip()
                                pygame.time.delay(1000)

                # Check back button
                if self.back_button.collidepoint(mouse_pos):
                    return "back"

                # Check start button
                if self.start_button.collidepoint(mouse_pos) and self.selected_characters:
                    self.game_state.selected_team = self.selected_characters
                    nl = []
                    for i in self.game_state.selected_team:
                        nl.append(CharacterSelect.all_hero_dict[i])
                    self.game_state.selected_team = nl
                    return "level_select"  # Proceed to level select
                # all_hero_dict = {"Lumberjack": LumberJack, "Pantheon": Pantheon,
                #                  "BrownBeard": BrownBeard}

        return None


class SelectGame:
    def __init__(self):
        self.state = GameState()
        self.current_screen = "character_select"
        self.character_select = CharacterSelect(self.state)
        self.level_select = LevelSelect(self.state)

    def selecting(self):
        running_chr = True
        while running_chr:
            result = None

            if self.current_screen == "character_select":
                result = self.character_select.handle_events()
                self.character_select.draw(screen)

                if result == "level_select":
                    self.current_screen = "level_select"

            elif self.current_screen == "level_select":
                result = self.level_select.handle_events()
                self.level_select.draw(screen)

                if result == "back":
                    self.current_screen = "character_select"
                elif result and result.startswith("level"):
                    level_num = int(result[5:])
                    print(f"Starting Level {level_num} with team: {self.state.selected_team}")
                    # Here you would actually start the level
                    # For demo, we'll just unlock next level when completing
                    if level_num == self.state.unlocked_levels:
                        self.state.unlocked_levels += 1
                        self.level_select.update_locked_status()
                        # Unlock more characters when reaching level 2
                        if level_num == 2:
                            for char in self.character_select.characters:
                                char["locked"] = False
                    return [level_num, self.state.selected_team]

            pygame.display.flip()
            clock.tick(60)


