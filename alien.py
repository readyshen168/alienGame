import pygame
from pygame.sprite import Sprite
from setting import Settings


class Alien(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.aliens = None
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
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

    # 在有外星飞船到达屏幕边缘时采取相应的措施: 水平持续飞行，碰到屏幕边缘则向下移动并改变水平飞行方向
    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    # 外星飞船触底则返回True
    def aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.y > self.screen_rect.height:
                return True

    # 将外星舰队向下移动，并改变水平移动方向
    def change_fleet_direction(self):
        # 当外星舰队中某只飞船到达屏幕边缘，则整体舰队向下移动
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
            # alien.rect.y = alien.y
        self.settings.fleet_direction *= -1

    # 由队长创建舰队
    def create_fleet(self):
        # 队长创建精灵组
        self.aliens = pygame.sprite.Group()
        # 以飞船长宽值为间距
        current_x, current_y = self.rect.width, self.rect.height

        # 在x、y轴方向上排布外星飞船
        while current_y < self.screen_rect.height - 30 * self.rect.height:
            while current_x < self.screen_rect.width - 10 * self.rect.width:
                # 新建一艘对应坐标的外星飞船并加入精灵组aliens
                self.aliens.add(self.create_alien(current_x, current_y))
                # x轴方向按一定间距排布
                current_x += 2 * self.rect.width

            # 新行需重置x坐标
            current_x = self.rect.x
            # y轴方向按一定间距排布
            current_y += 2 * self.rect.height

    # 根据坐标新建外星飞船
    def create_alien(self, x, y):
        new_alien = Alien(self.ai_game)
        new_alien.x = x
        new_alien.y = y
        new_alien.rect.x = x
        new_alien.rect.y = y
        return new_alien

        # 绘制外星飞船

    def draw_alien(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 水平移动外星飞船
        self.x += self.speed * self.settings.fleet_direction
        self.rect.x = self.x

    # 外星队长更新整个舰队
    def update_aliens(self):
        # 外星队长检查舰队是否碰到边缘，若碰到则下移且改变水平移动方向
        self.check_fleet_edges()
        # 更新舰队状态
        self.aliens.update()
        # 外星舰队绘制
        self.aliens.draw(self.screen)
