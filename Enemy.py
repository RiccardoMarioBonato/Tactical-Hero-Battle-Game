from Customize import *
from Unit import Centipede, BigBloated, BigBloatedBoss, CentipedeBoss, BattleTurtle, GreenSlime, \
    BlueSlime, RedSlime, RedWerewolf, GreyWerewolf, WhiteWerewolf, Gargona1, Gargona2, Gargona3, \
    Homeless2, Homeless3, \
    Homeless1, Destroyer, Infantry, Swordsman
import random
from Player import Resources


class EnemyLogic:
    def __init__(self):
        self.enemy_spawn_timer = 0
        self.boss_timer = 0
        self.stall_timer = 0
        self.mob_list = []

    def spawn_pattern(self, tower, player_resources):
        if self.enemy_spawn_timer > 180:
            mobs = [Centipede, BigBloated]
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
        bg = [Images.day_default, Images.night_default, Images.swamp_default, Images.castle_default, Images.slums_default, Images.Future_default]
        self.enemy_spawn_timer_setter(1)
        return level_list[level-1].spawn_pattern(self, tower, player_resources), pygame.transform.scale(bg[level-1], (Resolution.WIDTH, Resolution.HEIGHT))

    @staticmethod
    def spawn_unit(unit_class, enemy_tower):
        spawn_x = enemy_tower.rect.left
        spawn_y = Resolution.HEIGHT - 250 - Dimensions.BLOCK_SIZE1 // 2
        new_unit = unit_class(spawn_x, spawn_y)
        enemy_tower.block.append(new_unit)


class Level1(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if self.enemy_spawn_timer > 220:
            mobs = [BlueSlime, GreenSlime]
            EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(60, 90)
        if self.boss_timer > 4000:
            EnemyLogic.spawn_unit(RedSlime, tower)
            self.boss_timer = random.randint(800, 1200)
        Resources.add_energy(player_resources, [1.2, 0.3, 0.0])


class Level2(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if self.enemy_spawn_timer > 180:
            mobs = [RedWerewolf, GreyWerewolf]
            EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(50, 70)
        if self.stall_timer > 300 and player_resources.solar_energy >= 15:
            EnemyLogic.spawn_unit(GreyWerewolf, tower)
            self.stall_timer = 0
        if self.boss_timer > 3600:
            EnemyLogic.spawn_unit(WhiteWerewolf, tower)
            self.boss_timer = random.randint(600, 1000)
        Resources.add_energy(player_resources, [0.7, 1.2, 0.3])


class Level3(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if self.enemy_spawn_timer > 150:
            mobs = [Centipede, BigBloated, BlueSlime]
            for _ in range(random.randint(1, 2)):  # Occasionally spawn 2 at once
                EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(40, 60)
        if self.boss_timer > 3000:
            EnemyLogic.spawn_unit(CentipedeBoss, tower)
            self.boss_timer = random.randint(600, 900)
        Resources.add_energy(player_resources, [1, 1, 0.3])


class Level4(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if self.enemy_spawn_timer > 120:
            mobs = [Gargona1, Gargona2, Gargona3]
            for _ in range(2):  # Burst wave
                EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(30, 60)
        if self.stall_timer > 300 and player_resources.lunar_energy > 15:
            EnemyLogic.spawn_unit(CentipedeBoss, tower)
            self.stall_timer = 0
        if self.boss_timer > 3400:
            EnemyLogic.spawn_unit(BigBloatedBoss, tower)
            self.boss_timer = random.randint(500, 900)
        Resources.add_energy(player_resources, [1, 0.5, 0.3])


class Level5(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if self.enemy_spawn_timer > 100:
            mobs = [Homeless1, Homeless2, Homeless3]
            for _ in range(random.randint(2, 3)):
                EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(20, 50)
        if self.boss_timer > 3000:
            EnemyLogic.spawn_unit(Homeless3, tower)
            EnemyLogic.spawn_unit(Gargona2, tower)  # dual boss type
            self.boss_timer = random.randint(400, 700)
        Resources.add_energy(player_resources, [0.8, 0.8, 0.5])


class Level6(EnemyLogic):
    def spawn_pattern(self, tower, player_resources):
        if self.enemy_spawn_timer > 90:
            mobs = [Infantry, Swordsman, Homeless2]
            for _ in range(random.randint(2, 4)):
                EnemyLogic.spawn_unit(random.choice(mobs), tower)
            self.enemy_spawn_timer = random.randint(15, 30)

        if self.stall_timer > 250 and player_resources.solar_energy >= 15:
            EnemyLogic.spawn_unit(Destroyer, tower)
            self.stall_timer = 0

        if self.boss_timer > 3400:
            EnemyLogic.spawn_unit(Destroyer, tower)
            EnemyLogic.spawn_unit(CentipedeBoss, tower)
            self.boss_timer = random.randint(400, 800)

        Resources.add_energy(player_resources, [0.8, 1, 1])
