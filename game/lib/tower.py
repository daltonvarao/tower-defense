import time
import pygame
import pygame.gfxdraw

from .object import Object
from .shoot import Shoot
from .utils import Vector, assets_file


class Tower(Object):

    price = 100

    def __init__(self, pos_xy: tuple = None, dragging=True, player=None):
        img_src = assets_file('tower.png')
        super().__init__(img_src, pos_xy)
        self.dragging = dragging
        self.radius = 80
        self.last_shoot = None
        self.power = 5
        self.level = 1
        self.player = player
        self.selected = False
        self.shoot_group = pygame.sprite.Group()

    def upgrade(self):
        self.level_up()
        self.radius += 10
        self.selected = False
        self.player.upgrade_clicked = False

    def level_up(self):
        self.level += 1

    def mouse_drag(self, pos: tuple):
        if self.rect.collidepoint(*pos):
            self.dragging = not self.dragging

    def select_tower(self, pos: tuple):
        if self.rect.collidepoint(*pos):
            self.selected = True

    def move(self, pos: tuple):
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

    def draw_radius(self, display):
        pygame.gfxdraw.filled_circle(
            display, 
            self.rect.centerx, 
            self.rect.centery,
            self.radius,
            (0, 0, 110, 100)
        )

    def update(self):
        if self.selected and self.player.pay(self):
            self.upgrade()
        else:
            self.selected = False

    def update_move(self, mouse_pos):
        if self.dragging:
            self.move(mouse_pos)

    def draw_shoots(self, display):
        self.shoot_group.draw(display)
        self.shoot_group.update()

    def shoot(self, target):
        self.last_shoot = time.time()
        self.shoot_group.add(Shoot(tower=self, target=target))

    def score_up(self, score):
        self.groups()[0].player.score_up(score)


class Towers(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def not_dragging_sprites(self):
        return [s for s in self.sprites() if not s.dragging]

    def dragging_sprites(self):
        return [s for s in self.sprites() if s.dragging]

    def dragging(self, drag):
        for sprite in self.sprites():
            sprite.dragging = drag

    def update_move(self, pos: tuple):
        for sprite in self.sprites():
            sprite.update_move(pos)

    def mouse_drag(self, pos: tuple):
        for sprite in self.sprites():
            sprite.mouse_drag(pos)

    def draw_radius(self, display):
        for sprite in self.dragging_sprites():
            sprite.draw_radius(display)
    
    def draw_shoots(self, display):
        for sprite in self.sprites():
            sprite.draw_shoots(display)

    def select_tower(self, pos: tuple):
        for sprite in self.sprites():
            sprite.select_tower(pos)

    def shoot_on_enemy(self, enemy_group):
        for sprite in self.not_dragging_sprites():
            for enemy in enemy_group.sprites():
                if pygame.sprite.collide_circle(sprite, enemy):
                    if sprite.last_shoot:
                        if (time.time() - sprite.last_shoot) > 0.5:
                            sprite.shoot(enemy)
                    else:
                        sprite.shoot(enemy)
