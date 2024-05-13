import sys
import pygame
from ship import Ship
from setting import Settings
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        # 引入Settings实例
        self.settings = Settings()
        # 创建一个控制帧率的时钟
        self.clock = pygame.time.Clock()
        # 指定窗口大小后赋给screen一个surface
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 全屏设定：
        '''self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        '''
        # 设置背景色
        self.bg_color = self.settings.bg_color
        # 设置游戏窗口标题
        pygame.display.set_caption("Alien Invasion")
        # 创建飞船
        self.ship = Ship(self)
        # 创建外星战队
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def _check_events(self):
        # 监听键盘和鼠标事件,以及退出条件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moveRight = True
        if event.key == pygame.K_LEFT:
            self.ship.moveLeft = True
        if event.key == pygame.K_UP:
            self.ship.moveUp = True
        if event.key == pygame.K_DOWN:
            self.ship.moveDown = True
        if event.key == pygame.K_SPACE:
            # 连续发射子弹
            self.ship.fire_bullet = True
            # 非连续产生子弹
            # self.ship.bullets.add(Bullet(self))
        # 退出键：
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moveRight = False
        if event.key == pygame.K_LEFT:
            self.ship.moveLeft = False
        if event.key == pygame.K_UP:
            self.ship.moveUp = False
        if event.key == pygame.K_DOWN:
            self.ship.moveDown = False
        if event.key == pygame.K_SPACE:
            # 中断连续发子弹
            self.ship.fire_bullet = False

    # 创建外星舰队
    def _create_fleet(self):
        # 先创建一艘外星飞船
        alien = Alien(self)
        # 飞船之间的间距
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        # 飞船当前的坐标
        current_x, current_y = alien_width, alien_height
        # 开始循环，条件：当前坐标离屏幕边沿保持一定距离
        while current_y < (self.settings.screen_height - 20 * alien_height):
            while current_x < (self.settings.screen_width - alien_width):
                # 根据x坐标生成新的外星飞船
                self._create_alien(current_x, current_y)
                # 当前x坐标加上两倍的间距
                current_x += 2 * alien_width
            # 新的一行需要重置x坐标
            current_x = alien_width
            # 当前y坐标加上2倍的间距
            current_y += 2 * alien_height

    # 根据坐标生成外星飞船并加入舰队
    def _create_alien(self, x, y):
        # 新建一艘飞船，设定其X坐标
        new_alien = Alien(self)
        new_alien.x = x
        new_alien.y = y
        new_alien.rect.x = x
        new_alien.rect.y = y
        # 将飞船加入舰队
        self.aliens.add(new_alien)

    # 每次循环重绘屏幕
    def _update_screen(self):
        # 背景色重绘
        self.screen.fill(self.bg_color)

        # 飞船状态更新
        self.ship.update()
        # 飞船绘制
        self.ship.blitme()
        # 外星飞船绘制
        # self.alien.draw_alien()

        # 更新外星舰队状态
        self.aliens.update()
        # 外星舰队绘制
        self.aliens.draw(self.screen)

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def run_game(self):
        """开始游戏主循环"""
        while True:
            self._check_events()
            self._update_screen()

            # 控制帧率：让该循环每秒恰好运行60次
            self.clock.tick(60)


if __name__ == '__main__':
    alien_invasion = AlienInvasion()
    alien_invasion.run_game()
