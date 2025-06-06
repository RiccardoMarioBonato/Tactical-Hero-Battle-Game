import pygame
from Customize import Color, Resolution


class Tower:
    def __init__(self, x, color, team, tower):
        self.font1 = pygame.font.Font(None, 80)
        self.width = 200
        self.height = 400
        self.rect = pygame.Rect(x, Resolution.HEIGHT-75 - self.height-75,
                                self.width, self.height,)
        self.hp = 100
        self.color = color
        self.team_text = self.font1.render(team, True, color)
        self.block = []
        self.image = pygame.image.load(tower)
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))
        self.available_units = []

    def add_available_units(self, units):
        self.available_units.append(units)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        hp_text = self.font1.render(str(self.hp), True, Color.YELLOW)
        screen.blit(hp_text, (self.rect.x + 20, self.rect.y - 450))
        screen.blit(self.team_text, (self.rect.x + 20, self.rect.y - 500))

    def dead_tower(self, enemy_tower):
        if enemy_tower.hp <= 0:
            return False
        if self.hp <= 0:
            return False
        return True  # Keep the game running

    def take_dmg(self, enemy_tower):
        for block in self.block[:]:
            block.move()
            if block.rect.colliderect(enemy_tower.rect):
                enemy_tower.hp -= block.tower_dmg

                # ✅ Record damage done to tower
                from GameStats import game_stats
                game_stats.record_tower_damage(block.__class__.__name__, block.tower_dmg)
                self.block.remove(block)
