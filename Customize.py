import pygame


class Color:
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)


class Images:
    bg = pygame.image.load("img/backgrounds/w6BZFE.jpg")


class Resolution:
    WIDTH, HEIGHT = 1920, 1080
    FPS = 60


class Dimensions:
    BLOCK_SIZE1 = 40


class Hero:
    Lumberjack = pygame.image.load("Heros/LumberJack/LumberJack/LumberJack_final.png")
    Pantheon = pygame.image.load("Heros/Pantheon/Pantheon/Pantheon_spritesheet.png")


class Enemies:
    Centipede = pygame.image.load("Enemies/Centipede/Centipede_SpriteSheet.png")
    Big_bloated = pygame.image.load("img/swamp enemy/3 Big bloated/Big_bloated_spritesheet.png")