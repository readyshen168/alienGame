import sys
import pygame
from ship import Ship
from setting import Settings
from alien import Alien
from game_stats import GameStats
from button import Button

'''增加一个test用来调试新功能'''
'''游戏难度并没有按预期增加'''


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        # 创建一个用于存储游戏统计信息的实例
        self.game_stats = GameStats()
        # 引入Settings实例
        self.settings = self.game_stats.settings

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

        # 创建外星战队
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # 创建飞船
        self.ship = Ship(self)

        # 游戏是否结束的标记，默认是False，点击play按钮后开始
        self.game_active = False

        # 创建play按钮
        self.play_button = Button(self, "Play")

    def _check_events(self):
        # 监听键盘和鼠标事件,以及退出条件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            # 检测鼠标单击的位置并执行_check_play_button(mouse_pos)方法
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """鼠标单击位置在按钮范围内时，开始游戏，即game_active = true"""
        # 在分支bug中去掉了game_active的条件判定
        # 去掉了game_active的判定，会导致按钮范围的点击持续有效
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.game_active = True
            # 重置游戏的统计信息
            self.game_stats.reset_stat()
            # 清空外星人和子弹列表
            self.aliens.empty()
            self.ship.bullets.empty()
            # 创建新的外星舰队，并把飞船放在屏幕底部中央
            self._recreate_fleet()
            self.ship.center_ship()

            # 隐藏光标
            pygame.mouse.set_visible(False)
            # 还原游戏设置 initialize_dynamic_settings()
            self.settings.initialize_dynamic_settings()

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
        while current_y < (self.settings.screen_height - 30 * alien_height):
            while current_x < (self.settings.screen_width - 10 * alien_width):
                # 根据x坐标生成新的外星飞船
                self._create_alien(current_x, current_y)
                # 当前x坐标加上两倍的间距
                current_x += 2 * alien_width
            # 新的一行需要重置x坐标
            current_x = alien_width
            # 当前y坐标加上2倍的间距
            current_y += 2 * alien_height

    # 若外星舰队被消灭，则生成新的舰队
    def _recreate_fleet(self):
        if not self.aliens:
            self._create_fleet()
            # 清空飞船的子弹
            self.ship.bullets.empty()

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

    # 在有外星飞船到达屏幕边缘时采取相应的措施：
    # 外星舰队的飞行规则：水平持续飞行，碰到屏幕边缘则向下移动并改变水平飞行方向
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    # 将外星舰队向下移动，并改变水平移动方向
    def _change_fleet_direction(self):
        # 当外星舰队中某只飞船到达屏幕边缘，则整体舰队向下移动
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
            # alien.rect.y = alien.y
        self.settings.fleet_direction *= -1

    # 更新外星舰队状态
    def _update_aliens(self):
        # 外星飞船绘制
        # self.alien.draw_alien()

        # 更新外星舰队状态
        self._check_fleet_edges()
        self.aliens.update()
        # 外星舰队绘制
        self.aliens.draw(self.screen)
        # 若外星舰队被消灭，则生成新的舰队
        self._recreate_fleet()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            # 调用处理飞船与外星人相撞的方法
            self._ship_hit()
            # 调用外星人到达屏幕下方边缘的方法
            self._check_aliens_bottom()

    def _update_ship(self):
        # 飞船状态更新
        self.ship.update()
        # 飞船绘制
        self.ship.blitme()

    # 每次循环重绘屏幕
    def _update_screen(self):
        # 背景色重绘
        self.screen.fill(self.bg_color)

        # 游戏继续进行的条件
        if self.game_active:
            # 更新飞船状态
            self._update_ship()
            # 更新外星舰队状态
            self._update_aliens()

        # 如果game_active是False,则绘制Play按钮
        else:
            self.play_button.draw_button()
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    # 处理飞船与外星人相撞的方法:
    def _ship_hit(self):
        if self.game_stats.ships_left > 0:
            # 将game_stats中的ships_left减1
            self.game_stats.ships_left -= 1
            # 清空外星人
            self.aliens.empty()

            # 创建新的外星人舰队（会清空子弹）），并将飞船重置于屏幕底部中央ship.center_ship()
            self._recreate_fleet()
            self.ship.center_ship()

            # 暂停
            # pygame.time.delay(500)
        else:
            self.game_active = False
            # 显示光标
            pygame.mouse.set_visible(True)

    # 检测是否有外星人到达屏幕下边缘
    def _check_aliens_bottom(self):
        # 像飞船被撞到一样处理_ship_hit
        if self.ship.rect.bottom >= self.screen.get_rect().bottom:
            self._ship_hit()

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
