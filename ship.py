import pygame
from setting import Settings
from bullet import Bullet
from empty_bullet import EmptyBullet


class Ship:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.imageFile = 'images/spaceShip.png'

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 使用pygame内置方法加载飞船的png图像
        # self.image = pygame.image.load(self.imageFile)

        # 使用pillow库来转换图像给pygame
        self.image = self.settings.load_image(self.imageFile)

        # 获取飞船图像的矩形框
        self.rect = self.image.get_rect()

        # 使用surface对象的矩形框来定位飞船图像的位置
        self.rect.midbottom = self.screen_rect.midbottom

        # 按键状态的标志
        self.moveRight = False
        self.moveLeft = False
        self.moveUp = False
        self.moveDown = False

        # 飞船速度：
        self.speed = self.settings.shipSpeed

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 子弹：
        self.fire_bullet = False
        # 即刻发射的子弹
        self.bullets = pygame.sprite.Group()
        # 上颗子弹相对飞船的预设位置
        self.expected_last_bullet_distance = 0
        # 外星飞船舰队：
        self.aliens = ai_game.aliens

    # 根据按键状态来更新飞船的运动状态
    def update(self):
        # 根据移动状态来判定飞船的最新位置
        if self.moveRight and self.rect.right < self.screen_rect.right:
            self.x += self.speed
        if self.moveLeft and self.rect.left > 0:
            self.x -= self.speed
        if self.moveUp and self.rect.top > 0:
            self.y -= self.speed
        if self.moveDown and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.speed

        # 更新子弹状态
        self._update_bullets()

        # 把self.x赋值给self.rect.x
        self.rect.x = self.x
        self.rect.y = self.y

    # 更新子弹集合的状态
    def _update_bullets(self):
        # 上颗子弹的预设距离（飞船状态每更新一次，即增加一次预设距离）
        self.expected_last_bullet_distance += self.settings.bullet_speed
        # 按下空格键后决定如何发射子弹（连续发射子弹模式）
        if self.fire_bullet:
            self._fire_bullet()

        # 更新子弹状态（位置、删除出界的）
        for bullet in self.bullets.copy():
            bullet.update()
            # 删除已出界的子弹
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        # 在终端打出屏幕上剩余的子弹数量
        print(len(self.bullets))

        # 删除被子弹击中的外星飞船
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    def _fire_bullet(self):

        bullet_count = len(self.bullets)
        # 第一颗子弹：
        if bullet_count == 0:
            self.bullets.add(Bullet(self))
            # 重置上颗子弹与飞船的预设距离
            self.expected_last_bullet_distance = 0

        # 发射子弹的条件必须满足上颗子弹与飞船在y方向上的预设距离大于一个子弹的高度
        elif (bullet_count < self.settings.bullets_capacity and
              self.expected_last_bullet_distance > 5 * self.settings.bullet_height):
            # 让子弹相隔发射
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            # 重置上颗子弹与飞船的预设距离
            self.expected_last_bullet_distance = 0

    # 复制飞船和子弹图像到屏幕surface对象上
    def blitme(self):
        self.screen.blit(self.image, self.rect)
        # 绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
