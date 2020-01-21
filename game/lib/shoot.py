import pygame
from .object import Object

from game.lib.utils import Vector, assets_file


class Shoot(Object):

    def __init__(self, tower, target):
        img_src = assets_file('shoot.png')
        super().__init__(img_src)
        self.speed = 10
        self.tower = tower
        self.rect.centerx = tower.rect.centerx
        self.rect.top = tower.rect.top
        self.target = target

    @property
    def target_vector(self):
        return Vector(sprite=self.target)

    def move(self, direction: Vector):
        self.rect.centerx += direction.x * self.speed 
        self.rect.centery += direction.y * self.speed

    def hit_target(self):
        return pygame.sprite.collide_rect(self, self.target)

    def update(self):
        if self.hit_target():
            self.tower.score_up(self.target.score)
            self.target.hit(self.tower.power)
            self.kill()
        else:
            direction = self.vector.direction_to(self.target_vector)
            self.move(direction)
