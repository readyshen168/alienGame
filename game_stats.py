from setting import Settings


# 跟踪游戏的统计信息
class GameStats:
    def __init__(self):
        # 初始化统计信息settings、reset_stat()
        self.high_sore = None
        self.score = None
        self.ships_left = None
        self.settings = Settings()
        self.reset_stat()
        # 最高分
        self.highest_score = 16888
        # 等级
        self.level = None

        self.reset_stat()

    # reset_stat() self.ships_left同步settings里的ship_limit值
    def reset_stat(self):
        """初始化一些统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

