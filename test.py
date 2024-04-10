import pygame
import PIL
from PIL import Image

# 查看pygame是否支持加载PNG图像
# print(pygame.image.get_extended())

print(PIL.__version__)

im = Image.new(mode='RGB', size=(100,200), color=(73, 109, 137))
im.save('images/test_image.png')