import pygame.font

"""记分板，分数来源于game_stats"""


class ScoreBoard:

    def __init__(self, ai_game):
        # 屏幕、game stats、字体、颜色
        self.img_score_rect = None
        self.img_score = None
        self.str_score = None
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

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

    # 把分数显示出来
    def score_show(self):
        # 更新最新的分数图片
        self.score_img()
        # 显示分数
        self.screen.blit(self.img_score, self.img_score_rect)
