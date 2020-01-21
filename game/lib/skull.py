import pygame
from .object import Object

from game.lib.utils import Vector, assets_file


class Skull(Object):

    def __init__(self, pos_xy: tuple, coords: list):
        img_src = assets_file('skull.png')
        super().__init__(img_src, pos_xy)
        self.speed = 2
        self.coords_index = 0
        self.coords = coords
        self.health = 10
        self.power = 1
        self.score = 1

    @property
    def next_coord_vector(self):
        return Vector(
            x=self.coords[self.coords_index][0],
            y=self.coords[self.coords_index][1]
        )

    def hit(self, power):
        self.health -= power

    def move(self, direction: Vector):
        self.rect.centerx += direction.x * self.speed 
        self.rect.centery += direction.y * self.speed

    def change_coord_index(self):
        if len(self.coords) > self.coords_index + 1:
            self.coords_index += 1

    def update(self):
        distance = self.vector.distance_to(self.next_coord_vector)
        if self.health == 0:
            self.kill()
        if distance <= 1:
            self.change_coord_index()
        else:
            direction = self.vector.direction_to(self.next_coord_vector)
            self.move(direction)

    def __repr__(self):
        return f"<Skull object at {id(self)}>"


class Skulls(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
