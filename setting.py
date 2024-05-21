import pygame
from PIL import Image
import io


class Settings:
    def __init__(self):
        # 初始化游戏设置
        self.bullets_capacity = 5
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 118, 230)

        # 飞船设置
        self.shipSpeed = 5
        self.ship_limit = 3

        # 子弹数据：
        self.bullet_speed = 10.0
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # 外星飞船数据：
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1

        #以什么倍率加快游戏的节奏speedup_scale

        # 重置动态数据 initialize_dynamic_settings()


    """重置动态数据的方法"""
    def initialize_dynamic_settings(self):
        #把各项速度值、外星人移动方向在这里重置


    """提高各项速度的方法"""
    def increase_speed(self):


    # 加载图像的方法
    def load_image(self, file, scale_factor=1):
        im = Image.open(file)
        im = im.convert('RGBA')
        io_string = io.BytesIO()
        im.save(io_string, format='PNG')
        io_string.seek(0)

        image = pygame.image.load(io_string)
        # 缩放原图像
        scale_factor = scale_factor
        new_width = int(image.get_width() * scale_factor)
        new_height = int(image.get_height() * scale_factor)
        image = pygame.transform.scale(image, (new_width, new_height))

        return image
