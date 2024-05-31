import sys
import pygame
from ship import Ship
from setting import Settings
from alien import Alien
from game_stats import GameStats
from button import Button
from score_board import ScoreBoard

'''增加一个test用来调试新功能'''
'''游戏难度并没有按预期增加'''
"""加入计分模块"""
"""把外星人相关的代码都归入外星人类中处理，在分支test_alien上"""
"""大部分功能在分支test_alien上已实现，但子弹无法击落外星飞船"""


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

        '''创建外星舰队队长，负责管理外星舰队的各类行为'''
        self.alien_captain = Alien(self)
        # 创建外星战队
        self.alien_captain.create_fleet()

        # 创建飞船
        self.ship = Ship(self)

        # 游戏是否结束的标记，默认是False，点击play按钮后开始
        self.game_active = False

        # 创建play按钮
        self.play_button = Button(self, "Play")

        # 创建记分板
        self.score_board = ScoreBoard(self)

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

    def _check_play_button(self, mouse_pos):
        """鼠标单击位置在按钮范围内时，开始游戏，即game_active = true"""
        # 在分支bug中去掉了game_active的条件判定
        # 去掉了game_active的判定，会导致按钮范围的点击持续有效
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.game_active = True
            # 重置游戏的统计信息
            self.game_stats.reset_stat()
            # 重建外星人舰队和我方飞船及还原游戏难度、隐藏光标
            self._recreate_fleet_ship()

    # 提升游戏难度
    def _upgrade_difficulty(self):
        # 提升速度
        self.settings.increase_speed()
        # 新建外星舰队
        # self._create_fleet()
        self.alien_captain.create_fleet()
        # 清空飞船的子弹
        self.ship.bullets.empty()

    # 重置外星舰队、我方飞船、还原游戏难度、隐藏光标
    def _recreate_fleet_ship(self):
        self.alien_captain.aliens.empty()
        self.ship.bullets.empty()
        # self._create_fleet()
        self.alien_captain.create_fleet()
        self.ship.center_ship()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 还原游戏难度设置 initialize_dynamic_settings()
        self.settings.initialize_difficulty_settings()

    # 结束本轮游戏，并重新生成外星舰队、我方飞船、play按钮的方法，调用该方法时，self.game_active为True
    def _end_round(self):
        # 若外星舰队被消灭，则生成新的外星舰队,且提升游戏难度(增加各项速度),本轮继续
        if not self.alien_captain.aliens:
            self._upgrade_difficulty()

        # 若外星人和飞船发生碰撞，或者外星人舰队触底，且我方飞船还有数量，则本轮继续
        if ((pygame.sprite.spritecollideany(self.ship, self.alien_captain.aliens) or
                                             self.alien_captain.aliens_bottom()) and
                                                    self.game_stats.ships_left > 0):
            print("Ship hit!!!")

            self.game_stats.ships_left -= 1
            # 创建新的外星人舰队（会清空子弹）），并将飞船重置于屏幕底部中央ship.center_ship()
            self._recreate_fleet_ship()

        # 若外星人和飞船发生碰撞，且我方飞船数量耗光，则结束本轮
        elif self.game_stats.ships_left <= 0:
            # 结束本轮
            self.game_active = False
            # 显示光标
            pygame.mouse.set_visible(True)

    # 更新外星舰队状态
    def _update_aliens(self):
        # 由外星队长更新外星舰队的位置
        self.alien_captain.update_aliens()

    def _update_ship(self):
        # 飞船状态更新
        self.ship.update()
        # 飞船绘制
        self.ship.blitme()

    # 每次循环重绘屏幕
    def _update_screen(self):
        # 背景色重绘
        self.screen.fill(self.bg_color)

        # 显示记分板
        self.score_board.score_show()

        # 游戏继续进行的条件
        if self.game_active:
            # 更新飞船状态
            self._update_ship()
            # 更新外星舰队状态
            self._update_aliens()
            # 检测是否结束本轮
            self._end_round()

        # 如果game_active是False,则绘制Play按钮
        else:
            self.play_button.draw_button()
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
