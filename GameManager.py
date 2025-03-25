from Customize import *  # Import constants
import pygame
import sys


class GameManager:
    def __init__(self):
        pass


class Block:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, Dimensions.BLOCK_SIZE1, Dimensions.BLOCK_SIZE1)
        self.speed = speed

    def move(self):
        self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, Color.WHITE, self.rect)


