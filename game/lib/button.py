import pygame

from .object import Object
from .utils import Vector, assets_file


class Button(Object):

    def __init__(self, pos_xy: tuple, img_src):
        super().__init__(assets_file(img_src), pos_xy)

    def mouse_click(self, pos: tuple):
        if self.rect.collidepoint(*pos):
            self.handle_click(pos)

    def handle_click(self, pos):
        pass


class Buttons(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def mouse_click(self, pos):
        for sprite in self.sprites():
            sprite.mouse_click(pos)
