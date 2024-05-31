import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, ship):
        super().__init__()
        self.screen = ship.screen
        self.settings = ship.settings
        self.color = self.settings.bullet_color

        # 创建子弹的矩形，再设置到ship的对应位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ship.rect.midtop

        # 精确的子弹位置
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
