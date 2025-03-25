import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Character Select")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
font = pygame.font.SysFont('Arial', 32)


class CharacterSelect:
    def __init__(self):
        self.characters = [
            {"name": "Pantheon", "image": None, "selected": False,
             "rect": pygame.Rect(150, 200, 200, 300)},
            {"name": "Viking", "image": None, "selected": False,
             "rect": pygame.Rect(450, 200, 200, 300)},
            # Add more characters as needed
        ]
        self.back_button = pygame.Rect(50, 500, 150, 50)
        self.start_button = pygame.Rect(600, 500, 150, 50)
        self.selected_character = None

        # Placeholder for character images (replace with your actual images)
        for char in self.characters:
            # Create a simple colored rectangle as placeholder
            surf = pygame.Surface((180, 250))
            surf.fill(BLUE if char["name"] == "Pantheon" else RED)
            char["image"] = surf

    def draw(self, screen):
        screen.fill(WHITE)

        # Draw title
        title = font.render("SELECT YOUR HERO", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Draw characters
        for char in self.characters:
            # Draw character image
            screen.blit(char["image"], (char["rect"].x + 10, char["rect"].y + 10))

            # Draw character name
            name = font.render(char["name"], True, BLACK)
            screen.blit(name, (char["rect"].x + char["rect"].width // 2 - name.get_width() // 2,
                               char["rect"].y + char["rect"].height - 30))

            # Draw selection border if selected
            if char["selected"]:
                pygame.draw.rect(screen, GREEN, char["rect"], 3)
            else:
                pygame.draw.rect(screen, BLACK, char["rect"], 2)

        # Draw buttons
        pygame.draw.rect(screen, GRAY, self.back_button)
        back_text = font.render("Back", True, BLACK)
        screen.blit(back_text,
                    (self.back_button.x + self.back_button.width // 2 - back_text.get_width() // 2,
                     self.back_button.y + self.back_button.height // 2 - back_text.get_height() // 2))

        pygame.draw.rect(screen, GREEN, self.start_button)
        start_text = font.render("Start", True, BLACK)
        screen.blit(start_text, (
        self.start_button.x + self.start_button.width // 2 - start_text.get_width() // 2,
        self.start_button.y + self.start_button.height // 2 - start_text.get_height() // 2))

        # Draw selection info
        if self.selected_character:
            info = font.render(f"Selected: {self.selected_character}", True, BLACK)
            screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, 500))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Check character selection
                for char in self.characters:
                    if char["rect"].collidepoint(mouse_pos):
                        self.selected_character = char["name"]
                        for c in self.characters:
                            c["selected"] = False
                        char["selected"] = True

                # Check back button
                if self.back_button.collidepoint(mouse_pos):
                    return "back"  # Signal to go back to previous screen

                # Check start button
                if self.start_button.collidepoint(mouse_pos) and self.selected_character:
                    return self.selected_character  # Return selected character name

        return None  # No action taken


# Main game loop
def main():
    clock = pygame.time.Clock()
    char_select = CharacterSelect()

    running = True
    while running:
        result = char_select.handle_events()

        if result == "back":
            print("Going back to main menu")
            # Here you would typically return to the previous screen
            running = False
        elif result in ["Pantheon", "Viking"]:  # Add other character names as needed
            print(f"Starting game with {result}")
            # Here you would initialize the game with the selected character
            running = False

        char_select.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()