import pygame
from Customize import *


class Unit:
    def __init__(self, x, y):
        self.health = 100
        self.attack_power = 10
        self.speed = 1
        self.cost = 20
        self.measurement = [0, 1, [100, 200]]
        self.rect = pygame.Rect(x, y, Dimensions.BLOCK_SIZE1, Dimensions.BLOCK_SIZE1)
        self.sprite_sheet = pygame.image.load("img/swamp enemy/1 Centipede/Centipede_fullsheet.png")
        self.animation_steps = [4, 6, 6, 4, 4, 2, 4, 6, 4]
        self.animation_list = self.load_images(self.sprite_sheet, self.animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.flip = False
        self.update_time = pygame.time.get_ticks()

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.measurement[0], y * self.measurement[0], self.measurement[0], self.measurement[0])
                temp_img_list.append(pygame.transform.scale(temp_img, (self.measurement[0] * self.measurement[1], self.measurement[0] * self.measurement[1])))
            animation_list.append(temp_img_list)
        return animation_list

    def draw(self, screen):
        img = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(img, (self.rect.x - (self.measurement[0] * self.measurement[1]),
                           self.rect.y - (self.measurement[1] * self.measurement[1])))

    def update(self):
        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # if the player is dead then end the animation
            self.frame_index = 0


# Player1_spawn = Player(1, 200, 1120, False, Player1_data,
#                        Player1_spritesheet, Player1_step,
#                        Player1_attack, attack_style_p1)

class Centipede(Unit):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100

        self.height = 50
        self.measurement = [100, 1, 0]

        # Set sprite sheet and animation steps BEFORE calling super()
        self.sprite_sheet = pygame.image.load("img/swamp enemy/1 Centipede/Centipede_fullsheet.png")
        self.animation_steps = [4, 6, 6, 4, 4, 2, 4, 6, 4]

        # Now call super().__init__()
        super().__init__(x, y)

        # Scale the image
        self.body = pygame.transform.scale(self.sprite_sheet, (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += self.speed