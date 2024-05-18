from setting import Settings


# 跟踪游戏的统计信息
class GameStats:
    def __init__(self):
        # 初始化统计信息settings、reset_stat()
        self.settings = Settings()
        self.reset_stat()

    # reset_stat() self.ships_left同步settings里的ship_limit值
    def reset_stat(self):
        self.ships_left = self.settings.ship_limit
