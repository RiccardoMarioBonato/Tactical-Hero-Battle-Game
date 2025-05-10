import pygame


class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (150, 150, 150)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    DARK_GRAY = (100, 100, 100)
    ORANGE = (255, 95, 31)
    LOCKED_COLOR = (150, 150, 150)


class Images:
    day_default = pygame.image.load("img/backgrounds/w6BZFE.jpg")
    night_default = pygame.image.load("img/backgrounds/night.png")
    swamp_default = pygame.image.load("img/backgrounds/Swamp_map.png")


class Resolution:
    WIDTH, HEIGHT = 1920, 1080
    FPS = 60


class Dimensions:
    BLOCK_SIZE1 = 40


class Hero:
    Lumberjack = pygame.image.load("Heros/LumberJack/LumberJack/LumberJack_final.png")
    lumberjack_photo = pygame.image.load("Heros/LumberJack/lumberjack_select_photo.webp")
    Pantheon = pygame.image.load("Heros/Pantheon/Pantheon/Pantheon_spritesheet.png")
    BrownBeard = pygame.image.load("Heros/BrownBeard/BrownBeard_Spritelist.png")
    Kitsune = pygame.image.load("Heros/Kitsune/Kitsune_spritesheet.png")
    Yamabushi_tengu = pygame.image.load("Heros/YamabushiTengu/Yamabushi_tengu_spritesheet.png")
    Karasu_tengu = pygame.image.load("Heros/KarasuTengu/Karasu_tengu_Spritesheet.png")
    SwordMaster = pygame.image.load("Heros/SwordMaster/Sword_Master_spritesheet.png")


class Enemies:
    Centipede = pygame.image.load("Enemies/Centipede/Centipede_SpriteSheet.png")
    Big_bloated = pygame.image.load("Enemies/Big_bloated/Big_bloated_spritesheet.png")
    Battle_turtle = pygame.image.load("Enemies/Battle_turtle/Battle_turtle_spritesheet.png")


class Projectile:
    bullet1 = pygame.image.load("Enemies/Battle_turtle/Bullet1.png")
    bullet2 = pygame.image.load("Enemies/Battle_turtle/Bullet2.png")


class Fonts:
    pygame.font.init()
    ARIAL_16 = pygame.font.SysFont('Arial', 16)
    ARIAL_24 = pygame.font.SysFont('Arial', 24)
    ARIAL_32 = pygame.font.SysFont('Arial', 32)
    ARIAL_36 = pygame.font.SysFont('Arial', 36)
    ARIAL_48 = pygame.font.SysFont('Arial', 48)
    ARIAL_72 = pygame.font.SysFont('Arial', 72)