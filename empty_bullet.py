from bullet import Bullet


class EmptyBullet(Bullet):
    def __init__(self, ship):
        super().__init__(ship)
        self.color = self.settings.bg_color
