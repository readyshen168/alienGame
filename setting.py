import pygame
from PIL import Image
import io


class Settings:
    def __init__(self):
        # 初始化游戏设置
        self.bullets_capacity = 1000
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 118, 230)
        self.shipSpeed = 5

        # 子弹数据：
        self.bullet_speed = 10.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

    def load_image(self, file):
        im = Image.open(file)
        im = im.convert('RGBA')
        io_string = io.BytesIO()
        im.save(io_string, format='PNG')
        io_string.seek(0)
        return pygame.image.load(io_string)

