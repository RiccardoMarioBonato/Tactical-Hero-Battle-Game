import pygame
from Customize import *


class Unit:
    def __init__(self, x, y):
        self.health = 100
        self.attack_power = 10
        self.speed = 1
        self.cost = 20
        self.measurement = [72, 1, [100, 200]]  # Updated frame size
        self.rect = pygame.Rect(x, y, Dimensions.BLOCK_SIZE1, Dimensions.BLOCK_SIZE1)
        self.sprite_sheet = pygame.image.load("img/swamp enemy/1 Centipede/Centipede_fullsheet.png")
        print(f"Sprite Sheet Dimensions: {self.sprite_sheet.get_size()}")
        print(f"Frame Size: {self.measurement[0]}x{self.measurement[0]}")
        self.animation_steps = [4, 6, 6, 4, 4, 2, 4, 6, 4]
        print(f"Animation Steps: {self.animation_steps}")
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.flip = False
        self.update_time = pygame.time.get_ticks()

    def load_images(self, sprite_sheet, animation_steps):
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
                        pygame.transform.scale(temp_img, (frame_width * 2, frame_height * 2)))
                else:
                    print(f"Warning: Skipping frame at x={x}, y={y} (outside sprite sheet bounds)")
                    continue  # Skip this frame

            animation_list.append(temp_img_list)

        return animation_list

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x - (self.measurement[0] * self.measurement[1]),
                           self.rect.y - (self.measurement[1] * self.measurement[1])))

    def update(self):
        animation_cooldown = 100  # ⬆ Increase cooldown to slow down animation

        # Update image
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            # Check if animation reached the last frame
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0  # Loop animation smoothly

        print(f"Action: {self.action}, Frame: {self.frame_index}")  # Debugging


# Player1_spawn = Player(1, 200, 1120, False, Player1_data,
#                        Player1_spritesheet, Player1_step,
#                        Player1_attack, attack_style_p1)

class Centipede(Unit):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.measurement = [72, 2, [100, 200]]  # Updated frame size
        self.sprite_sheet = pygame.image.load("img/swamp enemy/1 Centipede/Centipede_fullsheet.png")
        self.animation_steps = [4, 6, 6, 4, 4, 2, 4, 6, 4]  # Confirmed steps
        super().__init__(x, y)
        self.body = pygame.transform.scale(self.sprite_sheet, (self.measurement[0], 72))
        self.rect = pygame.Rect(self.x, self.y, self.measurement[0], 72)

    def move(self):
        self.x -= self.speed
        print("drawn")
