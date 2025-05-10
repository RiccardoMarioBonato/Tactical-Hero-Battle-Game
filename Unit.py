import pygame
import json
import os
from Customize import Hero, Enemies, Projectile, Resolution
from Base import Tower
from GameStats import GameStats

from GameStats import game_stats


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
    loaded_sprites = {}

    def __init__(self, x=0, y=0, unit_type=None):
        self.config = UnitConfig().get_unit_config(unit_type)
        if not self.config:
            raise ValueError(f"Unit type {unit_type} not found in config")
        self.unit_type = unit_type
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
        if self.unit_type not in Unit.loaded_sprites:
            # Check in Enemies, Hero, or Projectile
            sprite_sheet = None
            if self.unit_type in Enemies.__dict__:
                sprite_sheet = getattr(Enemies, self.unit_type)
            elif self.unit_type in Hero.__dict__:
                sprite_sheet = getattr(Hero, self.unit_type)
            elif self.unit_type in Projectile.__dict__:
                sprite_sheet = getattr(Projectile, self.unit_type)
            else:
                raise ValueError(
                    f"Sprite for {self.unit_type} not found in Enemies, Hero, or Projectile")

            # Skip animation frames if animation_steps is empty
            if not self.animation_steps:
                Unit.loaded_sprites[self.unit_type] = [[sprite_sheet]]
            else:
                scale = self.config['scale']
                animation_list = self.load_images(sprite_sheet, self.animation_steps, scale)
                Unit.loaded_sprites[self.unit_type] = animation_list

        self.animation_list = Unit.loaded_sprites[self.unit_type]
        self.image = self.animation_list[self.action][self.frame_index]

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
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

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

                    # Apply damage and record it
                    dmg = self.attack_power
                    target.health -= dmg
                    if target.health <= 0:
                        target.unit_die()
                        self.moving()

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
class GreenSlime(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "GreenSlime")
        self.flip = True  # ✅ flip sprite horizontally
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.GreenSlime
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class BlueSlime(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "BlueSlime")
        self.flip = True  # ✅ flip sprite horizontally
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.BlueSlime
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class RedSlime(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "RedSlime")
        self.flip = True  # ✅ flip sprite horizontally
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.RedSlime
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class RedWerewolf(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "RedWerewolf")
        self.flip = True  # ✅ flip horizontally
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.RedWerewolf
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class GreyWerewolf(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "GreyWerewolf")
        self.flip = True  # ✅ flip horizontally
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.GreyWerewolf
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class WhiteWerewolf(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "WhiteWerewolf")
        self.flip = True  # ✅ flip horizontally
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.WhiteWerewolf
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]

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
        self.sprite = Projectile.Bullet1
        self.lifetime = 2000  # milliseconds
        self.spawn_time = pygame.time.get_ticks()
        hitbox_w, hitbox_h = self.config['hitbox']
        self.rect = pygame.Rect(x, y, hitbox_w, hitbox_h)
        self.attack_power = self.attack_power  # from config

    def draw(self, screen,):
        img = pygame.transform.scale(self.sprite, (self.rect.width, self.rect.height))
        screen.blit(img, (self.rect.x, self.rect.y))

    def move(self):
        self.rect.x += self.speed

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
        # Define attack range box (attack_rect)
        self.attack_rect = pygame.Rect(self.rect.x - 150, self.rect.y, 300, self.rect.height)

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
            bullet.draw(screen)
            if bullet.dead:
                self.bullets.remove(bullet)

    def attack(self, targets):
        current_time = pygame.time.get_ticks()
        collision_detected = False

        # Defensive hitbox (body collision)
        if isinstance(targets, Tower):
            if self.rect.colliderect(targets.rect):
                collision_detected = True
                self.speed = 0
                if self.frame_index >= self.animation_steps[1]:
                    self.frame_index = 0
                self.action = 1
        else:
            # Attack detection hitbox (attack_rect)
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
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        bullet.flip = self.flip
        bullet.speed = -5 if not self.flip else 5
        self.bullets.append(bullet)



# Update Unit class draw() to support hitbox toggle
def draw(self, screen, show_hitbox=False):
    if not self.image:
        return

    img = pygame.transform.flip(self.image, self.flip, False)
    offset_x, offset_y = self.config['offset']
    screen.blit(img, (self.rect.x + offset_x, self.rect.y + offset_y))

    if show_hitbox:
        pygame.draw.rect(screen, (0, 0, 255), self.rect, 2)  # blue hitbox
        pygame.draw.rect(screen, (255, 0, 0), self.attack_rect, 2)  # red attack range


# Update Unit class update() to pass show_hitbox
def update(self, screen, tower, own_units=[], other_units=[], show_hitbox=False):
    self.move()
    if self.action == 2:
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
    self.draw(screen, show_hitbox)


class Gargona1(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Gargona1")
        self.flip = True
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Gargona1
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Gargona2(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Gargona2")
        self.flip = True
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Gargona2
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Gargona3(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Gargona3")
        self.flip = True
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Gargona3
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Homeless1(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Homeless1")
        self.flip = True
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Homeless1
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Homeless2(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Homeless2")
        self.flip = True
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Homeless2
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Homeless3(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Homeless3")
        self.flip = True
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Homeless3
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Destroyer(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Destroyer")
        self.flip = True
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Destroyer
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Infantry(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Infantry")
        self.flip = True
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Infantry
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]


class Swordsman(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, "Swordsman")
        self.flip = True
        self._load_sprite()

    def _load_sprite(self):
        self.sprite_sheet = Enemies.Swordsman
        scale = self.config['scale']
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, scale)
        self.image = self.animation_list[self.action][self.frame_index]

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