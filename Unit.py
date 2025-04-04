import pygame
import json
import os
from Customize import Hero, Enemies, Projectile, Resolution
from Base import Tower
from GameStats import GameStats

game_stats = GameStats()


class UnitConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'unit_config.json')
        with open(config_path, 'r') as f:
            return json.load(f)

    def get_unit_config(self, unit_name):
        return self.config['units'].get(unit_name, None)


class Unit:
    def __init__(self, x=0, y=0, unit_type=None):
        self.config = UnitConfig().get_unit_config(unit_type)
        if not self.config:
            raise ValueError(f"Unit type {unit_type} not found in config")

        # Base stats
        self.health = self.config['health']
        self.attack_power = self.config['attack_power']
        self.speed = self.config['speed']
        self.original_speed = self.config['speed']
        self.tower_dmg = self.config.get('tower_dmg', 10)
        self.cost = self.config.get('cost', [0, 0, 0])

        # Animation properties
        self.measurement = self.config['measurement']
        self.animation_steps = self.config['animation_steps']
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.dying_cooldown = 1200
        self.flip = False
        self.dead = False
        self.attacking = False

        # Position and hitbox
        self.x = x
        self.y = y
        hitbox_w, hitbox_h = self.config['hitbox']
        self.rect = pygame.Rect(x, y, hitbox_w, hitbox_h)
        self.attack_rect = pygame.Rect(self.x - 20, self.y, 80, 150)

        # Load sprite
        self._load_sprite()

    def _load_sprite(self):
        # To be overridden by child classes
        self.sprite_sheet = None
        self.animation_list = []
        self.image = None


    def load_images(self, sprite_sheet, animation_steps, scale=2):
        animation_list = []
        sheet_width, sheet_height = sprite_sheet.get_size()
        frame_width = self.measurement[0]
        frame_height = self.measurement[0]  # Assuming square frames

        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                # Check if the subsurface is within the bounds of the sprite sheet
                if (x * frame_width + frame_width <= sheet_width and
                        y * frame_height + frame_height <= sheet_height):
                    temp_img = sprite_sheet.subsurface(x * frame_width, y * frame_height,
                                                       frame_width, frame_height)
                    temp_img_list.append(
                        pygame.transform.scale(temp_img,
                                               (frame_width * scale, frame_height * scale)))
                else:
                    print(f"Warning: Skipping frame at x={x}, y={y} (outside sprite sheet bounds)")
                    continue  # Skip this frame

            animation_list.append(temp_img_list)
        return animation_list

    def draw(self, screen):
        if not self.image:
            return

        img = pygame.transform.flip(self.image, self.flip, False)
        offset_x, offset_y = self.config['offset']
        screen.blit(img, (self.rect.x + offset_x, self.rect.y + offset_y))

    def update(self, screen, tower, own_units=[], other_units=[]):
        self.move()
        if self.action == 2:  # Dying state
            animation_cooldown = self.dying_cooldown
        else:
            animation_cooldown = self.animation_cooldown

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                if self.action == 2:
                    self.unit_die()
                    self.dead = True
                    self.health = 0

        self.attack(other_units)
        self.draw(screen)

    def move(self, screen_width=Resolution.WIDTH, screen_height=Resolution.HEIGHT):
        dx = self.speed
        self.rect.x += dx
        if self.rect.left + dx < 0:
            self.rect.left = 0
        if self.rect.right + dx > screen_width:
            self.rect.right = screen_width

        self.attack_rect.x += dx
        if self.attack_rect.left + dx < 0:
            self.attack_rect.left = 0
        if self.attack_rect.right + dx > screen_width:
            self.attack_rect.right = screen_width

    def attack(self, targets):
        collision_detected = False

        if isinstance(targets, Tower):
            if self.rect.colliderect(targets.rect):
                collision_detected = True
                self.speed = 0
                if self.frame_index >= self.animation_steps[1]:
                    self.frame_index = 0
                self.action = 1
        else:
            for target in targets:
                if self.rect.colliderect(target.rect):
                    collision_detected = True
                    self.speed = 0
                    if self.frame_index >= self.animation_steps[1]:
                        self.frame_index = 0
                    self.action = 1
                    dmg = self.attack_power
                    target.health -= dmg
                    if target.health <= 0:
                        target.unit_die()
                        self.moving()
        game_stats.record_damage(self.__class__.__name__, self.attack_power)

        if not collision_detected:
            self.moving()
            self.animation_cooldown = 100

    def moving(self):
        self.speed = self.original_speed
        if self.frame_index >= self.animation_steps[0]:
            self.frame_index = 0
        self.action = 0

    def unit_die(self):
        self.speed = 0
        if self.frame_index >= self.animation_steps[2]:
            self.frame_index = 0
        self.dead = True
        self.action = 2


# Enemy Units
class Centipede(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Centipede")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Centipede
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class CentipedeBoss(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "CentipedeBoss")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Centipede
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class BigBloated(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "BigBloated")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Big_bloated
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class BigBloatedBoss(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "BigBloatedBoss")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Big_bloated
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Bullet(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Bullet")
        self.sprite = Projectile.bullet1
        self.lifetime = 2000
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen):
        img = pygame.transform.scale(self.sprite, (30, 18))
        screen.blit(img, (self.rect.x, self.rect.y))

    def move(self, screen_width=Resolution.WIDTH, screen_height=Resolution.HEIGHT):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.dead = True
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.dead = True

    def attack(self, targets):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.dead = True
            return

        for target in targets:
            if self.rect.colliderect(target.rect):
                target.health -= self.attack_power
                self.dead = True
                if target.health <= 0:
                    target.unit_die()
                break


class BattleTurtle(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "BattleTurtle")
        self._load_sprite()
        self.last_attack_time = 0
        self.attack_cooldown = self.config.get('attack_cooldown', 2000)
        self.bullets = []

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Battle_turtle
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]

    def update(self, screen, tower, own_units=[], other_units=[]):
        super().update(screen, tower, own_units, other_units)
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.attack(other_units)
            if bullet.dead:
                self.bullets.remove(bullet)

    def attack(self, targets):
        current_time = pygame.time.get_ticks()
        collision_detected = False

        if isinstance(targets, Tower):
            if self.rect.colliderect(targets.rect):
                collision_detected = True
                self.speed = 0
                if self.frame_index >= self.animation_steps[1]:
                    self.frame_index = 0
                self.action = 1
        else:
            for target in targets:
                if self.attack_rect.colliderect(target.rect):
                    collision_detected = True
                    self.speed = 0
                    if self.frame_index >= self.animation_steps[1]:
                        self.frame_index = 0
                    self.action = 1

                    if current_time - self.last_attack_time > self.attack_cooldown:
                        self.spawn_bullet()
                        self.last_attack_time = current_time

                    if target.health <= 0:
                        target.unit_die()
                        self.moving()

        if not collision_detected:
            self.moving()
            self.animation_cooldown = 100

    def spawn_bullet(self):
        bullet = Bullet(self.rect.x, self.rect.y + 70)
        bullet.flip = self.flip
        bullet.speed = -5 if not self.flip else 5
        self.bullets.append(bullet)


# Hero Units
class LumberJack(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "LumberJack")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Hero.Lumberjack
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Pantheon(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Pantheon")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Hero.Pantheon
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]



class BrownBeard(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "BrownBeard")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Hero.BrownBeard
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Kitsune(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Kitsune")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Hero.Kitsune
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class YamabushiTengu(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "YamabushiTengu")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Hero.Yamabushi_tengu
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class KarasuTengu(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "KarasuTengu")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Hero.Karasu_tengu
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class SwordMaster(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "SwordMaster")
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Hero.SwordMaster
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]