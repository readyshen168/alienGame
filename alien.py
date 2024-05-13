import pygame
from pygame.sprite import Sprite
from setting import Settings


class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = Settings()
        self.imageFile = 'images/UFO.png'
        self.speed = self.settings.alien_speed

        # 加载外星人图像并设置其rect属性
        self.image = self.settings.load_image(self.imageFile, 0.02)
        self.rect = self.image.get_rect()

        # 每个外星人最初位置在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    # 检测外星飞船是否到达屏幕边缘
    def check_edges(self):
        return (self.rect.right >= self.settings.screen_width) or (self.rect.left <= 0)

    # 绘制外星飞船
    def draw_alien(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 水平移动外星飞船
        self.x += self.speed * self.settings.fleet_direction
        self.rect.x = self.x
