import sys
from Unit import *
from Customize import Color, Resolution
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
Exit_to_menu_surface = font_large.render("Exit", True, "black")
Exit_to_menu_surface_rect = Exit_to_menu_surface.get_rect(midbottom=(1840, 80))


class GameProgress:
    def __init__(self):
        self.unlocked_levels = 1  # Start with level 1 unlocked
        self.selected_team = []  # This will store the actual hero classes, not just names

    def complete_level(self, level_num):
        """Call this when a level is completed"""
        if level_num >= self.unlocked_levels:
            self.unlocked_levels = level_num + 1

    def unlock_all(self):
        self.unlocked_levels = 6


class LevelSelect:
    def __init__(self, game_progress):
        self.game_progress = game_progress
        self.levels = [
            {"name": "Forest", "number": 1, "rect": pygame.Rect(400, 300, 300, 200),
             "locked": False},
            {"name": "Dark Forest", "number": 2, "rect": pygame.Rect(800, 300, 300, 200),
             "locked": True},
            {"name": "Swamp", "number": 3, "rect": pygame.Rect(1200, 300, 300, 200),
             "locked": True},
            {"name": "Castle", "number": 4, "rect": pygame.Rect(400, 600, 300, 200),
             "locked": True},
            {"name": "Slums", "number": 5, "rect": pygame.Rect(800, 600, 300, 200),
             "locked": True},
            {"name": "Future", "number": 6, "rect": pygame.Rect(1200, 600, 300, 200),
             "locked": True}
        ]
        # self.levels = [
        #     {"name": "Forest", "number": 1, "rect": pygame.Rect(400, 300, 300, 200),
        #      "locked": False},
        #     {"name": "Dark Forest", "number": 2, "rect": pygame.Rect(800, 300, 300, 200),
        #      "locked": False},
        #     {"name": "Swamp", "number": 3, "rect": pygame.Rect(1200, 300, 300, 200),
        #      "locked": False},
        #     {"name": "Castle", "number": 4, "rect": pygame.Rect(400, 600, 300, 200),
        #      "locked": False},
        #     {"name": "Slums", "number": 5, "rect": pygame.Rect(800, 600, 300, 200),
        #      "locked": False},
        #     {"name": "Future", "number": 6, "rect": pygame.Rect(1200, 600, 300, 200),
        #      "locked": False}
        # ]

        self.back_button = pygame.Rect(50, 950, 200, 80)
        self.update_locked_status()

    def update_locked_status(self):
        for level in self.levels:
            level["locked"] = level["number"] > self.game_progress.unlocked_levels

    def draw(self, game_screen):
        screen.fill(Color.WHITE)

        # Draw title
        title = font_large.render("SELECT LEVEL", True, Color.BLACK)
        game_screen.blit(title, (Resolution.WIDTH // 2 - title.get_width() // 2, 100))

        # Draw levels
        for level in self.levels:
            color = Color.BLUE if not level["locked"] else Color.LOCKED_COLOR
            pygame.draw.rect(screen, color, level["rect"])

            # Level name
            name = font_medium.render(level["name"], True, Color.WHITE)
            game_screen.blit(name, (level["rect"].x + level["rect"].width // 2 - name.get_width() // 2,
                               level["rect"].y + 40))

            # Level number
            num = font_large.render(f"Level {level['number']}", True, Color.WHITE)
            game_screen.blit(num, (level["rect"].x + level["rect"].width // 2 - num.get_width() // 2,
                              level["rect"].y + 80))

            # Lock icon if locked
            if level["locked"]:
                lock = font_large.render("🔒", True, Color.WHITE)
                game_screen.blit(lock,
                            (level["rect"].x + level["rect"].width // 2 - lock.get_width() // 2,
                             level["rect"].y + 120))

        # Draw back button
        pygame.draw.rect(game_screen, Color.GRAY, self.back_button)
        back_text = font_medium.render("Back", True, Color.BLACK)
        game_screen.blit(back_text,
                    (self.back_button.x + self.back_button.width // 2 - back_text.get_width() // 2,
                     self.back_button.y + self.back_button.height // 2 - back_text.get_height() // 2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
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
                     "BrownBeard": BrownBeard, "Kitsune": Kitsune,
                     "KarasuTengu": KarasuTengu, "YamabushiTengu": YamabushiTengu}

    def __init__(self, game_progress):
        self.game_progress = game_progress
        self.characters = self.create_character_list()
        self.back_button = pygame.Rect(50, 950, 200, 80)
        self.start_button = pygame.Rect(1670, 950, 200, 80)
        self.selected_characters = []
        self.max_selection = 3

    def create_character_list(self):
        characters = []
        positions = [
            # Row 1
            (235, 180), (485, 180), (735, 180), (985, 180), (1235, 180),
            (1485, 180),
            # Row 2
            (235, 430), (485, 430), (735, 430), (985, 430), (1235, 430),
            (1485, 430),
            # Row 3
            (235, 680), (485, 680), (735, 680), (985, 680), (1235, 680),
            (1485, 680)
        ]

        # Character image mapping - replace with your actual image paths
        character_images = {
            "Lumberjack": "Heros/LumberJack/lumberjack_select_photo.webp",
            "Pantheon": "Heros/Pantheon/Pantheon_profile.webp",
            "BrownBeard": "Heros/BrownBeard/Brownbeard_profile.jpg",
            "Kitsune": "Heros/Kitsune/Kitsune_profile_cute.jpg",
            "KarasuTengu": "Heros/KarasuTengu/Karasu_tengu_profile.jpg",
            "YamabushiTengu": "Heros/YamabushiTengu/Yamabushi_tengu_profile.jpg",
            # Add all other characters with their corresponding image paths
        }

        class_data = [
            ("Pantheon", "4 lunar 1 eclipse"), ("Lumberjack", "2 solar"), ("BrownBeard", "4 solar"),
            ("Kitsune", "8 sonar 8 lunar 2 eclipse"), ("KarasuTengu", "2 lunar"), ("YamabushiTengu", "12 lunar 1 eclipse"),
            ("Unknown", "20 sonar 5 lunar 2 eclipse"), ("Ninja", "Stealth"), ("Alchemist", "Support"),
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
                char_num = font_tiny.render(f"#{i + 1}", True, Color.BLACK)
                image.blit(char_num, (5, 5))

            characters.append({
                "name": name,
                "class": char_class,
                "image": image,  # Now using actual image instead of colored surface
                "selected": False,
                "rect": pygame.Rect(x, y, 200, 250),
                "locked": i >= 7 and self.game_progress.unlocked_levels < 2
            })

        return characters

    def draw(self, screen):
        screen.fill(Color.WHITE)

        # Draw title
        title = font_large.render("SELECT YOUR TEAM (MAX 3 HEROES)", True, Color.BLACK)

        screen.blit(title, (Resolution.WIDTH // 2 - title.get_width() // 2, 50))
        screen.blit(Exit_to_menu_surface, Exit_to_menu_surface_rect)

        # Draw selection counter
        counter = font_medium.render(
            f"Selected: {len(self.selected_characters)}/{self.max_selection}", True, Color.BLACK)
        screen.blit(counter, (Resolution.WIDTH // 2 - counter.get_width() // 2, 120))

        # Draw characters
        for char in self.characters:
            # Draw character image (darker if locked)
            char_image = char["image"].copy()
            if char["locked"]:
                char_image.fill((100, 100, 100, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(char_image, (char["rect"].x + 10, char["rect"].y + 10))

            # Draw character name and class
            name = font_medium.render(char["name"], True, Color.WHITE)
            screen.blit(name, (char["rect"].x + char["rect"].width // 2 - name.get_width() // 2,
                               char["rect"].y + char["rect"].height - 50))

            char_class = font_small.render(char["class"], True, Color.BLACK)
            screen.blit(char_class,
                        (char["rect"].x + char["rect"].width // 2 - char_class.get_width() // 2,
                         char["rect"].y + char["rect"].height - 25))

            # Draw selection border or lock status
            if char["locked"]:
                pygame.draw.rect(screen, Color.LOCKED_COLOR, char["rect"], 3)
                lock = font_medium.render("🔒", True, Color.BLACK)
                screen.blit(lock, (char["rect"].x + char["rect"].width // 2 - lock.get_width() // 2,
                                   char["rect"].y + char[
                                       "rect"].height // 2 - lock.get_height() // 2))
            elif char["selected"]:
                pygame.draw.rect(screen, Color.GREEN, char["rect"], 3)
            else:
                pygame.draw.rect(screen, Color.BLACK, char["rect"], 1)

        # Draw buttons
        pygame.draw.rect(screen, Color.GRAY, self.back_button)
        back_text = font_medium.render("Back", True, Color.BLACK)
        screen.blit(back_text,
                    (self.back_button.x + self.back_button.width // 2 - back_text.get_width() // 2,
                     self.back_button.y + self.back_button.height // 2 - back_text.get_height() // 2))

        # Start button (only enabled with selections)
        start_btn_color = Color.GREEN if self.selected_characters else Color.DARK_GRAY
        pygame.draw.rect(screen, start_btn_color, self.start_button)
        start_text = font_medium.render("Start", True, Color.BLACK)
        screen.blit(start_text, (
            self.start_button.x + self.start_button.width // 2 - start_text.get_width() // 2,
            self.start_button.y + self.start_button.height // 2 - start_text.get_height() // 2))

        # Draw selected team preview
        if self.selected_characters:
            team_text = font_medium.render("Your Team:", True, Color.BLACK)
            screen.blit(team_text, (850, 950))

            for i, char_name in enumerate(self.selected_characters):
                char_info = font_medium.render(f"{i + 1}. {char_name}", True, Color.BLACK)
                screen.blit(char_info, (550 + i * 300, 1030))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if Exit_to_menu_surface_rect.collidepoint(pygame.mouse.get_pos()):
                    sys.exit()

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
