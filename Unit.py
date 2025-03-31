from os import remove

import Base
from Customize import *
hero = Hero()
enemy = Enemies()


class Unit:
    def __init__(self, x=0, y=0):
        self.health = 100
        self.attack_power = 1
        self.speed = -1  # Horizontal speed
        self.cost = 20
        self.original_speed = -1
        self.tower_dmg = 10
        self.measurement = [72, 1, [100, 200]]  # Updated frame size
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, Dimensions.BLOCK_SIZE1, Dimensions.BLOCK_SIZE1)
        self.attack_rect = pygame.Rect(self.x - 20, self.y, 80, 150)
        self.sprite_sheet = pygame.image.load("img/swamp enemy/1 Centipede/Centipede_fullsheet.png")  # Default sprite sheet
        self.animation_steps = [4, 6, 6, 4, 4, 2, 4, 6, 4]
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        self.animation_cooldown = 100  # Default cooldown for normal animations
        self.dying_cooldown = 1200 # Slower cooldown for dying animation
        self.attacking = False
        self.dead = False

    def add_x_y(self, x, y):
        self.x = x
        self.y = y

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
                        pygame.transform.scale(temp_img, (frame_width * scale, frame_height * scale)))
                else:
                    print(f"Warning: Skipping frame at x={x}, y={y} (outside sprite sheet bounds)")
                    continue  # Skip this frame

            animation_list.append(temp_img_list)
        return animation_list

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x, self.rect.y))  # Draw image at rect position

    def update(self, screen, tower, own_units=[], other_units=[], ):
        # Use dying_cooldown if the unit is in the dying state
        self.move()
        if self.action == 2:  # Dying state
            animation_cooldown = self.dying_cooldown
        else:
            animation_cooldown = self.animation_cooldown

        # Update image
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            # Check if animation reached the last frame
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0  # Loop animation smoothly
                if self.action == 2:  # If dying animation is complete
                    self.unit_die()  # Mark the unit as no longer dying
                    self.dead = True  # Mark the unit as ready for removal
                    self.health = 0  # Mark the unit as dead

        self.attack(other_units)
        self.draw(screen)

    def move(self, screen_width=Resolution.WIDTH, screen_height=Resolution.HEIGHT):
        # Move horizontally
        dx = self.speed
        # Update position
        self.rect.x += dx
        # Check screen boundaries
        if self.rect.left + dx < 0:
            self.rect.left = 0
        if self.rect.right + dx > screen_width:
            self.rect.right = screen_width
        # Update position
        self.attack_rect.x += dx
        # Check screen boundaries
        if self.attack_rect.left + dx < 0:
            self.attack_rect.left = 0
        if self.attack_rect.right + dx > screen_width:
            self.attack_rect.right = screen_width

    def attack(self, targets):
        collision_detected = False  # Flag to track if any collision is detected

        # Draw the hitbox for debugging
        # Check for collisions with all targets
        if isinstance(targets, Base.Tower):
            print(True)
            if self.rect.colliderect(targets.rect):
                collision_detected = True
                self.speed = 0  # Stop moving when attacking
                if self.frame_index >= self.animation_steps[1]:
                    self.frame_index = 0
                self.action = 1  # Attack animation for other units
        else:
            for target in targets:
                if self.rect.colliderect(target.rect):
                    collision_detected = True
                    self.speed = 0  # Stop moving when attacking
                    if self.frame_index >= self.animation_steps[1]:
                        self.frame_index = 0
                    self.action = 1  # Attack animation for other units
                    dmg = self.attack_power
                    target.health -= dmg
                    if target.health <= 0:
                        target.unit_die()
                        self.moving()  # Resume moving if the target is defeated

        # If no collision is detected, go back to walking
        if not collision_detected:
            self.moving()  # Reset to walking state
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



class Centipede(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize Unit class
        self.measurement = [72, 2, [100, 200]]  # Updated frame size
        self.speed = -5
        self.original_speed = -5
        self.health = 80
        self.attack_power = 0.3
        self.animation_steps = [4, 6, 4, 4, 4, 2, 4, 6, 4]  # Confirmed steps
        self.sprite_sheet = Enemies.Centipede # Centipede sprite sheet
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 72))
        self.rect = pygame.Rect(x, y, 80, 120)  # Initialize rect
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-50, self.rect.y))  # Draw image at rect position


class CentipedeBoss(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize Unit class
        self.measurement = [72, 2, [100, 200]]  # Updated frame size
        self.speed = -3.5
        self.original_speed = -3.5
        self.health = 550
        self.attack_power = 0.5
        self.tower_dmg = 30
        self.animation_steps = [4, 6, 4, 4, 4, 2, 4, 6, 4]  # Confirmed steps
        self.sprite_sheet = Enemies.Centipede # Centipede sprite sheet
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 72))
        self.rect = pygame.Rect(x, y, 80, 120)  # Initialize rect
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, 4)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-50, self.rect.y-150))  # Draw image at rect position


class BigBloated(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Now Unit.__init__() will use the correct sprite_sheet
        self.x = x
        self.y = y
        self.speed = -1.5
        self.original_speed = -1.5
        self.health = 150
        self.attack_power = 0.25
        self.measurement = [72, 2, [100, 200]]  # Updated frame size
        self.animation_steps = [6, 6, 5, 6, 4, 2, 4, 4, 6]  # Confirmed steps
        self.sprite_sheet = Enemies.Big_bloated  # Centipede sprite sheet
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 72))
        self.rect = pygame.Rect(self.x+20, self.y, 80, 150)
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-50, self.rect.y))  # Draw image at rect position


class BigBloatedBoss(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Now Unit.__init__() will use the correct sprite_sheet
        self.x = x
        self.y = y
        self.speed = -1
        self.original_speed = -1
        self.health = 800
        self.tower_dmg = 40
        self.attack_power = 0.8
        self.measurement = [72, 2, [100, 200]]  # Updated frame size
        self.animation_steps = [6, 6, 5, 6, 4, 2, 4, 4, 6]  # Confirmed steps
        self.sprite_sheet = Enemies.Big_bloated  # Centipede sprite sheet
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 72))
        self.rect = pygame.Rect(self.x+20, self.y, 80, 150)
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, 4)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-50, self.rect.y -150))  # Draw image at rect position


class Bullet(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.attack_power = 10
        self.x = x
        self.y = y
        self.speed = -5  # Default speed (will be adjusted by turtle)
        self.sprite = Projectile.bullet1
        self.body = pygame.transform.scale(self.sprite, (50, 72), )
        self.rect = pygame.Rect(self.x, self.y, 15, 15)  # Smaller hitbox for bullet
        self.flip = False
        self.lifetime = 2000  # 2 seconds lifetime in milliseconds
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen):
        img = pygame.transform.scale(self.sprite, (30,  18))
        screen.blit(img, (self.rect.x, self.rect.y))

    def move(self, screen_width=Resolution.WIDTH, screen_height=Resolution.HEIGHT):
        self.rect.x += self.speed

        # Remove if out of screen bounds
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.dead = True

        # Remove if lifetime expired
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.dead = True

    def attack(self, targets):
        current_time = pygame.time.get_ticks()

        # Remove if lifetime expired
        if current_time - self.spawn_time > self.lifetime:
            self.dead = True
            return

        for target in targets:
            if self.rect.colliderect(target.rect):
                target.health -= self.attack_power
                self.dead = True  # Bullet should disappear after hitting
                if target.health <= 0:
                    target.unit_die()
                break  # Stop checking other targets after first hit


class BattleTurtle(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.speed = -1
        self.original_speed = -1
        self.health = 150
        self.attack_power = 0.25
        self.measurement = [72, 2, [100, 200]]
        self.animation_steps = [4, 4, 4, 6, 4, 2, 4, 4, 6]
        self.sprite_sheet = Enemies.Battle_turtle
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 72))
        self.rect = pygame.Rect(self.x + 20, self.y, 80, 150)
        self.attack_rect = pygame.Rect(self.x - 220, self.y, 240, 150)
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]
        self.last_attack_time = 0
        self.attack_cooldown = 2000
        self.bullets = []  # List to store active bullets

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x - 50, self.rect.y))
        # Draw hitboxes for debugging
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)  # Red rectangle for main hitbox
        # pygame.draw.rect(screen, (0, 255, 0), self.attack_rect,1)  # Green rectangle for attack hitbox

        # Draw all bullets
        for bullet in self.bullets:
            bullet.draw(screen)

    def update(self, screen, tower, own_units=[], other_units=[]):
        super().update(screen, tower, own_units, other_units)

        # Update all bullets
        for bullet in self.bullets[:]:  # Use slice copy to safely modify list during iteration
            bullet.move()
            bullet.attack(other_units)

            # Remove dead bullets
            if bullet.dead:
                self.bullets.remove(bullet)

    def attack(self, targets):
        current_time = pygame.time.get_ticks()
        collision_detected = False

        if isinstance(targets, Base.Tower):
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

                    # Check if cooldown has passed
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
        # Create bullet at turtle's position
        bullet = Bullet(self.rect.x, self.rect.y + 70)
        bullet.flip = self.flip  # Match the turtle's direction
        bullet.speed = -5 if not self.flip else 5  # Adjust speed based on direction

        # Add bullet to turtle's bullet list
        self.bullets.append(bullet)
        print(f"Bullet spawned at ({bullet.rect.x}, {bullet.rect.y})")  # Debug print


class LumberJack(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize Unit class
        self.speed = 2.5
        self.original_speed = 2.5
        self.attack_power = 0.3
        self.cost = [2, 0, 0]
        self.health = 90
        self.tower_dmg = 10
        self.measurement = [96, 2, [100, 200]]  # Updated frame size
        self.animation_steps = [6, 4, 4, 4, 4, 4, 4, 5, 2, 4]  # Confirmed steps
        self.sprite_sheet = Hero.Lumberjack # Viking sprite sheet
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 96))
        self.rect = pygame.Rect(x, y+50, 60, 136)  # Initialize rect
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-50, self.rect.y-50))  # Draw image at rect position


class Pantheon(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize Unit class
        self.speed = 1.5
        self.original_speed = 1.5
        self.attack_power = 0.75
        self.cost = [0, 4, 1]
        self.health = 325
        self.tower_dmg = 15
        self.measurement = [96, 2, [100, 200]]  # Updated frame size
        self.animation_steps = [6, 4, 4, 4, 4, 4, 4, 5, 2, 4]  # Confirmed steps
        self.sprite_sheet = Hero.Pantheon  # Viking sprite sheet
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 96))
        self.rect = pygame.Rect(x, y+50, 60, 136)  # Initialize rect
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-50, self.rect.y-50))  # Draw image at rect position


class BrownBeard(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize Unit class
        self.speed = 2
        self.original_speed = 2
        self.attack_power = 0.5
        self.health = 150
        self.cost = [4, 0, 0]
        self.tower_dmg = 10
        self.measurement = [96, 2, [100, 200]]  # Updated frame size
        self.animation_steps = [6, 4, 4, 4, 4, 4, 4, 5, 2, 4]  # Confirmed steps
        self.sprite_sheet = Hero.BrownBeard  # Viking sprite sheet
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 96))
        self.rect = pygame.Rect(x, y+50, 60, 136)  # Initialize rect
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-50, self.rect.y-50))  # Draw image at rect position


class Kitsune(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize Unit class
        self.speed = 1
        self.original_speed = 1
        self.attack_power = 1.175
        self.health = 450
        self.cost = [8, 8, 2]
        self.tower_dmg = 30
        self.measurement = [128, 1.5, [100, 200]]  # Updated frame size
        self.animation_steps = [8, 10, 9, 10, 10, 10, 7, 6, 2, 9]  # Confirmed steps
        self.sprite_sheet = Hero.Kitsune  # Viking sprite sheet
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 128))
        self.rect = pygame.Rect(x, y+50, 60, 136)  # Initialize rect
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, 1.75)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-50, self.rect.y-80))  # Draw image at rect position


class YamabushiTengu(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize Unit class
        self.speed = 5
        self.original_speed = 5
        self.attack_power = 0.9
        self.health = 300
        self.cost = [0, 10, 1]
        self.tower_dmg = 20
        self.measurement = [128, 2, [100, 200]]  # Updated frame size
        self.animation_steps = [8, 6, 6, 4, 4, 4, 4, 5, 2, 4]  # Confirmed steps
        self.sprite_sheet = Hero.Yamabushi_tengu  # Viking sprite sheet
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 128))
        self.rect = pygame.Rect(x, y+50, 60, 136)  # Initialize rect
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, 1.5)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-50, self.rect.y-50))  # Draw image at rect position


class KarasuTengu(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize Unit class
        self.speed = 6
        self.original_speed = 6
        self.attack_power = 0.25
        self.health = 100
        self.cost = [0, 2, 0]
        self.tower_dmg = 5
        self.measurement = [128, 2, [100, 200]]  # Updated frame size
        self.animation_steps = [8, 6, 6, 4, 4, 4, 4, 5, 2, 4]  # Confirmed steps
        self.sprite_sheet = Hero.Karasu_tengu
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 128))
        self.rect = pygame.Rect(x, y+50, 60, 136)  # Initialize rect
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, 1.5)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-50, self.rect.y-50))


class SwordMaster(Unit):
    def __init__(self, x, y):
        super().__init__(x, y)  # Initialize Unit class
        self.speed = 7
        self.original_speed = 7
        self.attack_power = 1
        self.health = 500
        self.cost = [20, 5, 2]
        # self.cost = [0, 0, 0]
        self.tower_dmg = 30
        self.measurement = [96, 2, [100, 200]]  # Updated frame size
        self.animation_steps = [16, 7, 4]  # Confirmed steps
        self.sprite_sheet = Hero.SwordMaster
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 96))
        self.rect = pygame.Rect(x, y+50, 60, 136)  # Initialize rect
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps, 4)
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x-160, self.rect.y-80))
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)  # Red rectangle for main hitbox