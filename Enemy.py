import pygame
from Customize import *
from GameManager import Block
from Unit import Unit, Centipede, BigBloated, BigBloated_Boss, Centipede_Boss
import random
import Player


class EnemyLogic:
    def __init__(self):
        self.enemy_spawn_timer = 0
        self.boss_timer = 0
        self.stall_timer = 0

    def spawn_pattern(self, tower, player_resources):
        if player_resources.solar_energy >= 19:
            if self.stall_timer > 350:
                tower.block.append(Centipede_Boss(tower.rect.left - Dimensions.BLOCK_SIZE1,
                    Resolution.HEIGHT - 250 - Dimensions.BLOCK_SIZE1 // 2))
                self.stall_timer = 0
        if self.enemy_spawn_timer > 150:  # 10 = 1/6 sec
            # tower.block.append(Block(tower.rect.left - Dimensions.BLOCK_SIZE1, Resolution.HEIGHT - 200 - Dimensions.BLOCK_SIZE1 // 2, -5))
            mobs = [Centipede(tower.rect.left - Dimensions.BLOCK_SIZE1,
                    Resolution.HEIGHT - 250 - Dimensions.BLOCK_SIZE1 // 2),
                    BigBloated(tower.rect.left - Dimensions.BLOCK_SIZE1,
                    Resolution.HEIGHT - 250 - Dimensions.BLOCK_SIZE1 // 2)]
            tower.block.append(random.choice(mobs))
            self.enemy_spawn_timer = 0
        if self.boss_timer > 2800:
            tower.block.append(BigBloated_Boss(tower.rect.left - Dimensions.BLOCK_SIZE1,
                       Resolution.HEIGHT - 250 - Dimensions.BLOCK_SIZE1 // 2))
            self.boss_timer = random.randint(750, 1300)

    def enemy_spawn_timer_setter(self, add_value):
        self.enemy_spawn_timer += add_value
        self.boss_timer += add_value
        self.stall_timer += add_value