import pygame.font


class Button:
    """为游戏创建按钮类"""

    def __init__(self, ai_game, msg):
        """获取ai_game的screen、screen_rect"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        """设置按钮的width200, height50, button_color, text_color, font"""
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 48)

        """创建按钮的rect对象，并使其居中"""
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        """将msg渲染为图像，调用_prep_msg(msg)方法"""
        self._prep_msg(msg)

    """将msg渲染为图像的方法"""
    def _prep_msg(self, msg):
        # msg_image, self.font.render()
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        # msg_image_rect
        self.msg_image_rect = self.msg_image.get_rect()
        # 文字与按钮中心对齐
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮
        pygame.draw.rect(self.screen, self.button_color, self.rect)
        # 用blit方法绘制文本
        self.screen.blit(self.msg_image, self.msg_image_rect)
