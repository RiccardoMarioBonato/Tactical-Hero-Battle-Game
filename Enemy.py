import pygame
from Customize import *
from GameManager import Block
from Unit import Unit, Centipede


class EnemyLogic:
    def __init__(self):
        self.enemy_spawn_timer = 0

    def spawn_pattern(self, tower):
        if self.enemy_spawn_timer > 90:  # Every 1.5 seconds
            # tower.block.append(Block(tower.rect.left - Dimensions.BLOCK_SIZE1, Resolution.HEIGHT - 200 - Dimensions.BLOCK_SIZE1 // 2, -5))
            # tower.block.append(Centipede(200, 200))
            cen = Centipede(500, 500)
            self.enemy_spawn_timer = 0

    def enemy_spawn_timer_setter(self, add_value):
        self.enemy_spawn_timer += add_value

