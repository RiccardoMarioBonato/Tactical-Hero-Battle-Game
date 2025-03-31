import pygame
from fontTools.misc.macRes import Resource

from Customize import *
from Unit import Centipede, BigBloated, BigBloatedBoss, CentipedeBoss, BattleTurtle
import random
from Player import Resources


class EnemyLogic:
    def __init__(self):
        self.enemy_spawn_timer = 0
        self.boss_timer = 0
        self.stall_timer = 0
        self.mob_list = []
        # tower.block.append(BigBloatedBoss(tower.rect.left - Dimensions.BLOCK_SIZE1,
        #                                   Resolution.HEIGHT - 250 - Dimensions.BLOCK_SIZE1 // 2))

    def spawn_pattern(self, tower, player_resources):
        # if player_resources.solar_energy >= 18:
        #     # if self.stall_timer > 370:
        #     #     EnemyLogic.spawn_unit(CentipedeBoss, tower)
        #     #     self.stall_timer = 0
        if self.enemy_spawn_timer > 180:
            mobs = [Centipede, BigBloated]
            # mobs = BattleTurtle
            EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(0, 30)
        if self.boss_timer > 3000:
            EnemyLogic.spawn_unit(CentipedeBoss, tower)
            self.boss_timer = random.randint(500, 1000)
        Resources.add_energy(player_resources, [2,0.5,0.1])

    def enemy_spawn_timer_setter(self, add_value):
        self.enemy_spawn_timer += add_value
        self.boss_timer += add_value
        self.stall_timer += add_value

    def add_mobs(self, mob):
        self.mob_list.append(mob)

    def pick_level(self, level, tower, player_resources):
        level_list = [Level1, Level2, Level3, Level4, Level5, Level6]
        bg = [Images.day_default, Images.night_default, Images.swamp_default, ]
        self.enemy_spawn_timer_setter(1)
        return level_list[level-1].spawn_pattern(self, tower, player_resources), pygame.transform.scale(bg[level-1], (Resolution.WIDTH, Resolution.HEIGHT))

    @staticmethod
    def spawn_unit(unit_class, enemy_tower):
        spawn_x = enemy_tower.rect.left
        spawn_y = Resolution.HEIGHT - 250 - Dimensions.BLOCK_SIZE1 // 2
        new_unit = unit_class(spawn_x, spawn_y)
        enemy_tower.block.append(new_unit)


#
# class Level1(EnemyLogic):
#     def spawn_pattern(self, tower, player_resources):
#         if self.enemy_spawn_timer > 180:
#             EnemyLogic.spawn_unit(BattleTurtle, tower)
#             self.enemy_spawn_timer = random.randint(0, 30)
#         if self.boss_timer > 3000:
#             EnemyLogic.spawn_unit(CentipedeBoss, tower)
#             self.boss_timer = random.randint(500, 1000)
#         Resources.add_energy(player_resources, [2,0.5,0.1])
class Level1(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if self.enemy_spawn_timer > 10:
            mobs = [Centipede, BigBloated]
            EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(0, 30)
        if self.boss_timer > 3000:
            EnemyLogic.spawn_unit(CentipedeBoss, tower)
            self.boss_timer = random.randint(500, 1000)
        Resources.add_energy(player_resources, [1, 0.5, 0.1])


class Level2(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if player_resources.solar_energy >= 20:
            if self.stall_timer > 370:
                EnemyLogic.spawn_unit(CentipedeBoss, tower)
                self.stall_timer = 0
        if self.enemy_spawn_timer > 100:
            mobs = [Centipede, BigBloated, ] # BattleTurtle
            EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(0, 30)
        if self.boss_timer > 3400:
            EnemyLogic.spawn_unit(BigBloatedBoss, tower)
            self.boss_timer = random.randint(500, 1000)
        Resources.add_energy(player_resources, [0.25, 1.5, 0.2])


class Level3(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if self.enemy_spawn_timer > 180:
            mobs = [Centipede, BigBloated]
            EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(0, 30)
        if self.boss_timer > 3000:
            EnemyLogic.spawn_unit(CentipedeBoss, tower)
            self.boss_timer = random.randint(500, 1000)
        Resources.add_energy(player_resources, [0.25, 1.5, 0.2])


class Level4(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if player_resources.solar_energy >= 20:
            if self.stall_timer > 370:
                EnemyLogic.spawn_unit(CentipedeBoss, tower)
                self.stall_timer = 0
        if self.enemy_spawn_timer > 200:
            mobs = [Centipede, BigBloated]
            EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(0, 30)
        if self.boss_timer > 3400:
            EnemyLogic.spawn_unit(BigBloatedBoss, tower)
            self.boss_timer = random.randint(500, 1000)


class Level5(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if self.enemy_spawn_timer > 180:
            mobs = [Centipede, BigBloated]
            EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(0, 30)
        if self.boss_timer > 3000:
            EnemyLogic.spawn_unit(CentipedeBoss, tower)
            self.boss_timer = random.randint(500, 1000)


class Level6(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if player_resources.solar_energy >= 20:
            if self.stall_timer > 370:
                EnemyLogic.spawn_unit(CentipedeBoss, tower)
                self.stall_timer = 0
        if self.enemy_spawn_timer > 200:
            mobs = [Centipede, BigBloated]
            EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(0, 30)
        if self.boss_timer > 3400:
            EnemyLogic.spawn_unit(BigBloatedBoss, tower)
            self.boss_timer = random.randint(500, 1000)