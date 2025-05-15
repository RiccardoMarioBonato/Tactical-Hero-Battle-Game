import sys
import threading
from Unit import *
from Customize import Color, Resolution
from analytics_window import open_window
import random


def launch_analytics_window():
    def run():
        try:
            open_window()
        except Exception as e:
            print("Failed to open analytics window:", e)

    threading.Thread(target=run, daemon=True).start()


# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((Resolution.WIDTH, Resolution.HEIGHT))
pygame.display.set_caption("Hero Selector with Level Progression")
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)
font_tiny = pygame.font.SysFont('Arial', 16)
Exit_to_menu_surface = font_large.render("Exit", True, "white")
Exit_to_menu_surface_rect = Exit_to_menu_surface.get_rect(midbottom=(1840, 80))


class GameProgress:
    def __init__(self):
        self.unlocked_levels = 1
        self.selected_team = []
        # self.unlocked_heroes = ["Lumberjack", "KarasuTengu", "Peasant", "Convert"]  # Always available
        self.unlocked_heroes = [
            "Lumberjack", "KarasuTengu", "Peasant", "Convert", "Gangster1", "Gangster2", "Wanderer",
            "BrownBeard", "Pantheon", "Countess", "Monk", "Kunoichi", "Gangster3", "LightMage",
            "YamabushiTengu", "Kitsune", "FireMage", "VampireGirl"
        ]

    def complete_level(self, level_num):
        if level_num >= self.unlocked_levels:
            self.unlocked_levels = level_num + 1
        self.unlock_new_characters(level_num)

    def unlock_new_characters(self, level_num):
        all_heroes = [
            "Lumberjack", "KarasuTengu", "Peasant", "Convert", "Gangster1", "Gangster2", "Wanderer",
            "BrownBeard", "Pantheon", "Countess", "Monk", "Kunoichi", "Gangster3", "LightMage",
            "YamabushiTengu", "Kitsune", "FireMage", "VampireGirl"
        ]

        if level_num >= 5:
            self.unlocked_heroes = all_heroes
        else:
            locked = list(set(all_heroes) - set(self.unlocked_heroes))
            new_unlocks = random.sample(locked, min(5, len(locked)))
            self.unlocked_heroes += new_unlocks


class LevelSelect:
    def __init__(self, game_progress):
        self.game_progress = game_progress
        self.levels = [
            {"name": "Forest", "number": 1, "rect": pygame.Rect(400, 300, 300, 200), "locked": False},
            {"name": "Dark Forest", "number": 2, "rect": pygame.Rect(800, 300, 300, 200), "locked": True},
            {"name": "Swamp", "number": 3, "rect": pygame.Rect(1200, 300, 300, 200), "locked": True},
            {"name": "Castle", "number": 4, "rect": pygame.Rect(400, 600, 300, 200), "locked": True},
            {"name": "Slums", "number": 5, "rect": pygame.Rect(800, 600, 300, 200), "locked": True},
            {"name": "Future", "number": 6, "rect": pygame.Rect(1200, 600, 300, 200), "locked": True}
        ]
        self.back_button = pygame.Rect(50, 950, 200, 80)
        self.analytics_button = pygame.Rect(50, 50, 220, 60)
        self.update_locked_status()

    def update_locked_status(self):
        for level in self.levels:
            level["locked"] = level["number"] > self.game_progress.unlocked_levels

    def draw(self, game_screen):
        self.bg2 = pygame.image.load("img/backgrounds/Cartoon_Forest_BG_02.png").convert()
        self.bg2 = pygame.transform.scale(self.bg2, (Resolution.WIDTH, Resolution.HEIGHT))
        screen.blit(self.bg2, (0, 0))

        title = font_large.render("SELECT LEVEL", True, Color.WHITE)
        game_screen.blit(title, (Resolution.WIDTH // 2 - title.get_width() // 2, 100))

        for level in self.levels:
            color = Color.BLUE if not level["locked"] else Color.LOCKED_COLOR
            pygame.draw.rect(screen, color, level["rect"])
            name = font_medium.render(level["name"], True, Color.WHITE)
            game_screen.blit(name, (
            level["rect"].x + level["rect"].width // 2 - name.get_width() // 2,
            level["rect"].y + 40))
            num = font_large.render(f"Level {level['number']}", True, Color.WHITE)
            game_screen.blit(num, (
            level["rect"].x + level["rect"].width // 2 - num.get_width() // 2,
            level["rect"].y + 80))
            if level["locked"]:
                lock = font_large.render("🔒", True, Color.WHITE)
                game_screen.blit(lock, (
                level["rect"].x + level["rect"].width // 2 - lock.get_width() // 2,
                level["rect"].y + 120))

        pygame.draw.rect(game_screen, Color.GRAY, self.back_button)
        back_text = font_medium.render("Back", True, Color.WHITE)
        game_screen.blit(back_text, (
        self.back_button.x + self.back_button.width // 2 - back_text.get_width() // 2,
        self.back_button.y + self.back_button.height // 2 - back_text.get_height() // 2))

        pygame.draw.rect(game_screen, Color.GRAY, self.analytics_button)
        stat_text = font_small.render("Data Analysis", True, Color.WHITE)
        game_screen.blit(stat_text, (
        self.analytics_button.x + self.analytics_button.width // 2 - stat_text.get_width() // 2,
        self.analytics_button.y + self.analytics_button.height // 2 - stat_text.get_height() // 2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for level in self.levels:
                    if level["rect"].collidepoint(mouse_pos) and not level["locked"]:
                        return f"level{level['number']}"
                if self.back_button.collidepoint(mouse_pos):
                    return "back"
                if self.analytics_button.collidepoint(mouse_pos):
                    launch_analytics_window()
        return None


class CharacterSelect:
    all_hero_dict = {
        "Lumberjack": LumberJack,
        "Pantheon": Pantheon,
        "BrownBeard": BrownBeard,
        "Kitsune": Kitsune,
        "KarasuTengu": KarasuTengu,
        "YamabushiTengu": YamabushiTengu,
        "Convert": Convert,
        "Countess": Countess,
        "VampireGirl": VampireGirl,
        "Wanderer": Wanderer,
        "LightMage": LightMage,
        "FireMage": FireMage,
        "Gangster1": Gangster1,
        "Gangster2": Gangster2,
        "Gangster3": Gangster3,
        "Monk": Monk,
        "Peasant": Peasant,
        "Kunoichi": Kunoichi
    }

    def __init__(self, game_progress):
        self.game_progress = game_progress
        self.characters = self.create_character_list()
        self.back_button = pygame.Rect(50, 950, 200, 80)
        self.start_button = pygame.Rect(1670, 950, 200, 80)
        self.analytics_button = pygame.Rect(50, 50, 220, 60)
        self.selected_characters = []
        self.max_selection = 3

    def create_character_list(self):
        characters = []
        positions = [
            (235, 180), (485, 180), (735, 180), (985, 180), (1235, 180), (1485, 180),
            (235, 430), (485, 430), (735, 430), (985, 430), (1235, 430), (1485, 430),
            (235, 680), (485, 680), (735, 680), (985, 680), (1235, 680), (1485, 680)
        ]

        character_images = {
            "Lumberjack": "Heros/LumberJack/lumberjack_select_photo.webp",
            "Pantheon": "Heros/Pantheon/Pantheon_profile.webp",
            "BrownBeard": "Heros/BrownBeard/Brownbeard_profile.jpg",
            "Kitsune": "Heros/Kitsune/Kitsune_profile_cute.jpg",
            "KarasuTengu": "Heros/KarasuTengu/Karasu_tengu_profile.jpg",
            "YamabushiTengu": "Heros/YamabushiTengu/Yamabushi_tengu_profile.jpg",
            "Convert": "Heros/Converted/convert_profile.png",
            "Countess": "Heros/Countess/Countess_profile.png",
            "VampireGirl": "Heros/VampireGirl/vampire_girl_profile.png",
            "Wanderer": "Heros/Wanderer_Magican/wanderer_profile.png",
            "LightMage": "Heros/Light_Magican/Light_Mage_profile.png",
            "FireMage": "Heros/Fire_magican/fire_mage_profile.png",
            "Gangster1": "Heros/Gangster1/496421d1-c2aa-43f2-bb7e-6e39f2f2b5a9.png",
            "Gangster2": "Heros/Gangster2/Gangsters_2_profile.png",
            "Gangster3": "Heros/Gangster3/Gangsters_3_profile.png",
            "Monk": "Heros/Monk/monk_profile.png",
            "Peasant": "Heros/Ninja_Peasant/peasant_profile.png",
            "Kunoichi": "Heros/Kunoichi/Kunoichi_profile.png"
        }

        class_data = [
            ("Lumberjack", "2 solar"),
            ("KarasuTengu", "2 lunar"),
            ("Peasant", "1 solar"),
            ("Convert", "3 lunar"),
            ("Gangster1", "3 solar"),
            ("Gangster2", "2 solar 1 lunar"),
            ("Wanderer", "2 solar 1 lunar"),
            ("BrownBeard", "4 solar"),
            ("Pantheon", "4 lunar 1 eclipse"),
            ("Countess", "2 solar 2 lunar 2 eclipse"),
            ("Monk", "3 solar 2 lunar"),
            ("Kunoichi", "3 lunar 1 solar"),
            ("Gangster3", "3 solar 2 lunar"),
            ("LightMage", "3 solar 1 lunar"),
            ("YamabushiTengu", "10 lunar 1 eclipse"),
            ("Kitsune", "6 solar 6 lunar 2 eclipse"),
            ("FireMage", "5 solar 2 lunar"),
            ("VampireGirl", "6 lunar 2 solar")
        ]

        # Everything except Pantheon, Lumberjack, BrownBeard is locked before level 2
        always_unlocked = [
            "Lumberjack", "KarasuTengu", "Peasant", "Convert"
        ]
        # always_unlocked = [
        #     "Pantheon", "Lumberjack", "BrownBeard", "KarasuTengu",
        #     "Kitsune", "YamabushiTengu", "Convert", "Countess", "VampireGirl",
        #     "Wanderer", "LightMage", "FireMage", "Gangster1", "Gangster2",
        #     "Gangster3", "Monk", "Peasant", "Kunoichi"
        # ]
        for i, ((x, y), (name, char_class)) in enumerate(zip(positions, class_data)):
            try:
                image = pygame.image.load(character_images.get(name, "")).convert_alpha()
                image = pygame.transform.scale(image, (180, 220))
            except:
                image = pygame.Surface((180, 220))
                image.fill((200, 200, 200))
                char_num = font_tiny.render(f"#{i + 1}", True, Color.BLACK)
                image.blit(char_num, (5, 5))

            # Lock if not in always_unlocked and player is below level 2
            is_locked = name not in self.game_progress.unlocked_heroes
            if is_locked:
                grey_overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
                grey_overlay.fill((100, 100, 100, 150))  # semi-transparent gray
                image.blit(grey_overlay, (0, 0))
            characters.append({
                "name": name,
                "class": char_class,
                "image": image,
                "selected": False,
                "rect": pygame.Rect(x, y, 200, 250),
                "locked": is_locked
            })

        return characters

    def draw(self, screen):
        self.bgs = pygame.image.load("img/backgrounds/Cartoon_Forest_BG_02.png").convert()
        self.bgs = pygame.transform.scale(self.bgs, (Resolution.WIDTH, Resolution.HEIGHT))
        screen.blit(self.bgs, (0, 0))

        title = font_large.render("SELECT YOUR TEAM (MAX 3 HEROES)", True, Color.WHITE)
        screen.blit(title, (Resolution.WIDTH // 2 - title.get_width() // 2, 50))
        screen.blit(Exit_to_menu_surface, Exit_to_menu_surface_rect)

        counter = font_medium.render(
            f"Selected: {len(self.selected_characters)}/{self.max_selection}", True, Color.WHITE)
        screen.blit(counter, (Resolution.WIDTH // 2 - counter.get_width() // 2, 120))

        for char in self.characters:
            char_image = char["image"].copy()
            if char["locked"]:
                char_image.fill((100, 100, 100, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(char_image, (char["rect"].x + 10, char["rect"].y + 10))

            name = font_medium.render(char["name"], True, Color.WHITE)
            screen.blit(name, (char["rect"].x + char["rect"].width // 2 - name.get_width() // 2,
                               char["rect"].y + char["rect"].height - 50))

            char_class = font_small.render(char["class"], True, Color.WHITE)
            screen.blit(char_class,
                        (char["rect"].x + char["rect"].width // 2 - char_class.get_width() // 2,
                         char["rect"].y + char["rect"].height - 25))

            if char["locked"]:
                pygame.draw.rect(screen, Color.LOCKED_COLOR, char["rect"], 4)
                lock = font_medium.render("🔒", True, Color.WHITE)
                screen.blit(lock, (char["rect"].x + char["rect"].width // 2 - lock.get_width() // 2,
                                   char["rect"].y + char[
                                       "rect"].height // 2 - lock.get_height() // 2))
            elif char["selected"]:
                pygame.draw.rect(screen, Color.GREEN, char["rect"], 4)
            else:
                pygame.draw.rect(screen, Color.WHITE, char["rect"], 2)

        pygame.draw.rect(screen, Color.GRAY, self.back_button)
        back_text = font_medium.render("Back", True, Color.WHITE)
        screen.blit(back_text,
                    (self.back_button.x + self.back_button.width // 2 - back_text.get_width() // 2,
                     self.back_button.y + self.back_button.height // 2 - back_text.get_height() // 2))

        start_btn_color = Color.GREEN if self.selected_characters else Color.DARK_GRAY
        pygame.draw.rect(screen, start_btn_color, self.start_button)
        start_text = font_medium.render("Start", True, Color.WHITE)
        screen.blit(start_text, (
        self.start_button.x + self.start_button.width // 2 - start_text.get_width() // 2,
        self.start_button.y + self.start_button.height // 2 - start_text.get_height() // 2))

        pygame.draw.rect(screen, Color.GRAY, self.analytics_button)
        analytics_text = font_small.render("View Analytics", True, Color.WHITE)
        screen.blit(analytics_text, (
        self.analytics_button.x + self.analytics_button.width // 2 - analytics_text.get_width() // 2,
        self.analytics_button.y + self.analytics_button.height // 2 - analytics_text.get_height() // 2))

        if self.selected_characters:
            team_text = font_medium.render("Your Team:", True, Color.WHITE)
            screen.blit(team_text, (850, 950))
            for i, char_name in enumerate(self.selected_characters):
                char_info = font_medium.render(f"{i + 1}. {char_name}", True, Color.WHITE)
                screen.blit(char_info, (550 + i * 300, 1030))

    def launch_analytics_window(self):
        try:
            launch_analytics_window()
        except Exception as e:
            print("Failed to open analytics window from CharacterSelect:", e)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if Exit_to_menu_surface_rect.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()

                # Check if analytics button was clicked
                if self.analytics_button.collidepoint(mouse_pos):
                    self.launch_analytics_window()  # Now properly called as an instance method
                # Check character selection
                for char in self.characters:
                    if char["rect"].collidepoint(mouse_pos) and not char["locked"]:
                        if char["selected"]:
                            char["selected"] = False
                            self.selected_characters.remove(char["name"])
                        else:
                            if len(self.selected_characters) < self.max_selection:
                                char["selected"] = True
                                self.selected_characters.append(char["name"])

                # Check start button - only enabled when exactly 3 heroes selected
                if (self.start_button.collidepoint(mouse_pos) and
                    len(self.selected_characters) == self.max_selection):
                    self.game_progress.selected_team = [
                        CharacterSelect.all_hero_dict[name]
                        for name in self.selected_characters
                    ]
                    return "level_select"
        return None

    def unlock_all(self):
        self.levels = [
            {"name": "Forest", "number": 1, "rect": pygame.Rect(400, 300, 300, 200),
             "locked": False},
            {"name": "Dark Forest", "number": 2, "rect": pygame.Rect(800, 300, 300, 200),
             "locked": False},
            {"name": "Swamp", "number": 3, "rect": pygame.Rect(1200, 300, 300, 200),
             "locked": False},
            {"name": "Castle", "number": 4, "rect": pygame.Rect(400, 600, 300, 200),
             "locked": False},
            {"name": "Slums", "number": 5, "rect": pygame.Rect(800, 600, 300, 200),
             "locked": False},
            {"name": "Future", "number": 6, "rect": pygame.Rect(1200, 600, 300, 200),
             "locked": False}
        ]


class SelectGame:
    def __init__(self, game_progress):  # Only need game_progress now
        self.game_progress = game_progress
        self.current_screen = "character_select"
        self.character_select = CharacterSelect(self.game_progress)
        self.level_select = LevelSelect(self.game_progress)

    def selecting(self):
        running_chr = True
        while running_chr:
            result = None
            # self.character_select.unlock_all() #for testing
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
                    # Return both level number AND the selected team from game_progress
                    return [level_num, self.game_progress.selected_team]

            pygame.display.flip()
            clock.tick(60)