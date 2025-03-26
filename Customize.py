import pygame
from pygame.locals import *

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
    bg = pygame.image.load("img/backgrounds/w6BZFE.jpg")


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


class Enemies:
    Centipede = pygame.image.load("Enemies/Centipede/Centipede_SpriteSheet.png")
    Big_bloated = pygame.image.load("Enemies/Big_bloated/Big_bloated_spritesheet.png")
