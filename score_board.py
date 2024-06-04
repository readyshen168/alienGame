import pygame.font
from pygame.sprite import Group

from ship import Ship

"""记分板，分数来源于game_stats"""


class ScoreBoard:

    def __init__(self, ai_game):
        # 屏幕、game stats、字体、颜色
        self.img_level_rect = None
        self.img_level = None
        self.img_highest_score_rect = None
        self.img_highest_score = None
        self.img_score_rect = None
        self.img_score = None
        self.str_score = None
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.ai_game = ai_game
        self.ships = Group()

        self.game_stats = ai_game.game_stats

        self.score_color = (30, 30, 30)
        self.font = pygame.font.SysFont('None', 48)

    # 转换分数为图像、定位分数图像的位置
    def score_img(self):
        # 把分数转换为字符串
        self.str_score = str(self.game_stats.score)
        # 图像化分数
        self.img_score = self.font.render(self.str_score, True, self.score_color)
        # 定位分数图像的位置在屏幕右上角
        self.img_score_rect = self.img_score.get_rect()
        self.img_score_rect.right = self.screen_rect.right - 20
        self.img_score_rect.top = 20

    def high_score_img(self):
        if self.game_stats.score > self.game_stats.highest_score:
            self.game_stats.highest_score = self.game_stats.score

        # 最高分四舍五入
        highest_score = round(self.game_stats.highest_score, -1)
        str_highest_score = f"Best: {highest_score:,}"

        self.img_highest_score = self.font.render(str_highest_score, True, self.score_color)
        self.img_highest_score_rect = self.img_highest_score.get_rect()
        self.img_highest_score_rect.centerx = self.screen_rect.centerx
        self.img_highest_score_rect.bottom = self.img_score_rect.bottom

    # 等级
    def level_img(self):
        str_level = f"Level: {self.game_stats.level}"
        self.img_level = self.font.render(str_level, True, self.score_color)

        self.img_level_rect = self.img_level.get_rect()
        self.img_level_rect.top = 10 + self.img_score_rect.bottom
        self.img_level_rect.x = self.img_score_rect.x

    # 剩余飞船的示意图：
    def prep_ships(self):
        for ship_num in range(self.game_stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship.rect.width * ship_num
            ship.rect.y = 10
            self.ships.add(ship)

    # 把分数显示出来
    def score_show(self):
        # 更新最新的分数图片
        self.score_img()
        # 更新最高分
        self.high_score_img()
        # 更新等级
        self.level_img()
        # 更新剩余飞船状态
        self.prep_ships()

        # 显示分数、等级和飞船数量
        self.screen.blit(self.img_score, self.img_score_rect)
        self.screen.blit(self.img_highest_score, self.img_highest_score_rect)
        self.screen.blit(self.img_level, self.img_level_rect)
        # 在左上角画出剩余的飞船
        self.ships.draw(self.screen)
