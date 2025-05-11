from Unit import *
# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = Resolution.WIDTH, Resolution.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animation Test")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Load a background (optional)
background = pygame.Surface((WIDTH, HEIGHT))
background.fill((30, 30, 30))  # Dark gray background


# Create a unit for testing
class TestUnit(LumberJack):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite_sheet = pygame.image.load("Heros/LumberJack/LumberJack/LumberJack_final.png")  # Replace with your sprite sheet
        self.animation_steps = [6, 4, 4, 4, 4, 4, 4, 5, 2, 4]  # Example animation steps
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]


# Create an instance of the test unit
test_unit = TestUnit(WIDTH // 2, HEIGHT // 2)

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:  # Walk
                test_unit.moving()
            if event.key == pygame.K_a:  # Attack
                test_unit.action = 1  # Set to attack animation
                test_unit.frame_index = 0  # Reset frame index
            if event.key == pygame.K_d:  # Die
                test_unit.unit_die()

    # Update the unit
    test_unit.update(screen)  # Pass an empty list for own_units (not used in this test)
    test_unit.speed = 0
    # Draw the unit
    test_unit.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()