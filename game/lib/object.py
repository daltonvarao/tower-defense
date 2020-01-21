import pygame
import math

from .utils import Vector


class Object(pygame.sprite.Sprite):

    def __init__(self, img_src: tuple = None, pos_xy: tuple = None):
        pygame.sprite.Sprite.__init__(self)
        
        if img_src:
            self.image = pygame.image.load(img_src)
            self.rect = self.image.get_rect()

        if pos_xy:
            self.rect.centerx = pos_xy[0]
            self.rect.centery = pos_xy[1]

    @property
    def vector(self):
        return Vector(sprite=self)


