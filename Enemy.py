import pygame
from Customize import *
from GameManager import Block
from Unit import Unit, Centipede, BigBloated
import random


class EnemyLogic:
    def __init__(self):
        self.enemy_spawn_timer = 0

    def spawn_pattern(self, tower):
        if self.enemy_spawn_timer > 90:  # 10 = 1/6 sec
            # tower.block.append(Block(tower.rect.left - Dimensions.BLOCK_SIZE1, Resolution.HEIGHT - 200 - Dimensions.BLOCK_SIZE1 // 2, -5))
            mobs = [Centipede(tower.rect.left - Dimensions.BLOCK_SIZE1,
                    Resolution.HEIGHT - 250 - Dimensions.BLOCK_SIZE1 // 2)]
                    # BigBloated(tower.rect.left - Dimensions.BLOCK_SIZE1,
                    # Resolution.HEIGHT - 250 - Dimensions.BLOCK_SIZE1 // 2)]
            tower.block.append(random.choice(mobs))
            self.enemy_spawn_timer = 0

    def enemy_spawn_timer_setter(self, add_value):
        self.enemy_spawn_timer += add_value
