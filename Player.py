import pygame
from Unit import SmallViking
from Customize import Resolution, Dimensions


class Controller:
    @staticmethod
    def keyboard(player_tower):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_tower.block.append(SmallViking(player_tower.rect.right,
                                                          Resolution.HEIGHT - 300 - Dimensions.BLOCK_SIZE1 // 2))
