import pygame
from Customize import Color, Resolution
import Unit


class Tower:
    def __init__(self, x, color, team, tower):
        self.font1 = pygame.font.Font(None, 80)
        self.width = 200
        self.height = 400
        self.rect = pygame.Rect(x, Resolution.HEIGHT-75 - self.height-75, self.width, self.height,)
        self.hp = 100
        self.color = color
        self.team_text = self.font1.render(team, True, color)
        self.block = []
        self.image = pygame.image.load(tower)  # Replace with actual file name
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        hp_text = self.font1.render(str(self.hp), True, (255, 255, 0))  # Yellow
        screen.blit(hp_text, (self.rect.x + 20, self.rect.y - 450))
        screen.blit(self.team_text, (self.rect.x + 20, self.rect.y - 500))

    def dead_tower(self, enemy_tower):
        if enemy_tower.hp <= 0:
            print("You win!")
            return False
        if self.hp <= 0:
            print("You lose!")
            return False
        return True  # Keep the game running

    def take_dmg(self, enemy_tower):
        for block in self.block[:]:
            block.move()
            if block.rect.colliderect(enemy_tower.rect):
                if isinstance(block, Unit.BigBloated_Boss) :
                    enemy_tower.hp -= 40
                elif isinstance(block, Unit.Pantheon):
                    enemy_tower.hp -= 15
                if isinstance(block, Unit.Centipede_Boss) :
                    enemy_tower.hp -= 30
                else:
                    enemy_tower.hp -= 10
                # block.attack(self)
                self.block.remove(block)

