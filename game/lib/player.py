import pygame
import time

from .object import Object
from .utils import assets_file


class Player(Object):

    def __init__(self, enemy_group, tower_group, pos_xy=None,):
        img_src = assets_file('player.png')
        super().__init__(pos_xy=pos_xy, img_src=img_src)
        self.enemy_group = enemy_group

        self.tower_group = tower_group
        self.inject(self.tower_group)

        self.wave = 1
        self.score = 100
        self.health = 6
        self.enemy_num = 6
        self.running_wave = False
        self.wave_end = False
        self.show_messages = True
        self.destroyed_lifes = []
        self.upgrade_clicked = False

        self.messages = [
            "Press start button to init new wave.",
            "Buy or upgrade a tower for R$ 100 to hit enemies."
        ]
        self.rects_pos = []
        self.colors = [
            (97, 187, 70),
            (253, 184, 39),
            (245, 130, 31),
            (224, 58, 62),
            (150, 61, 151),
            (0, 157, 220)
        ]

        for i in range(6):
            self.rects_pos.append(pygame.rect.Rect((1040, 420 + i*12), (70, 12)))

    def inject(self, klass):
        klass.player = self

    def clear_messages(self):
        self.messages.clear()

    def new_message(self, message: str = None, messages: (list, tuple) = None):
        if isinstance(message, str):
            self.messages.append(message)
        if isinstance(messages, (list, tuple)):
            [ self.messages.append(m) for m in messages ]

    def new_wave(self):
        self.wave += 1
        self.enemy_num += 2

    def start_wave(self):
        self.running_wave = True
        self.wave_end = False
        self.change_to_pause_button()

    def stop_wave(self):
        self.running_wave = False
        self.wave_end = True
        self.change_to_start_button()

    def score_up(self, score):
        self.score += score

    def next_wave(self):
        self.wave += 1
        self.enemy_num += 2
    
    def has_messages(self):
        return self.messages

    def pay(self, tower):
        if self.score >= tower.price:
            self.score -= tower.price
            return True
        return False

    def enemy_hit(self, index):
        self.health -= 1
        self.destroyed_lifes.append(self.rects_pos[index])

    def restart(self):
        return Player

    def end_game(self):
        self.clear_messages()
        self.new_message(messages=['Game Over! Your base was destroyed.', 'Press start button to play again.'])
        self.kill()

    def game_over(self):
        return self.health == 0

    def update(self, surface):
        enemy_num = len(self.enemy_group)
        if self.game_over():
            self.end_game()

        if self.running_wave and enemy_num == 0 and not self.game_over():
            self.stop_wave()
            self.messages.append('Wave ended, enjoy to buy new or upgrade your towers.')
            self.new_wave()
            self.messages.append('New wave loaded, press start to begin.')

        for i in range(len(self.rects_pos)):
            if self.rects_pos[i] not in self.destroyed_lifes:
                pygame.draw.rect(surface, self.colors[i], self.rects_pos[i])
                for enemy in self.enemy_group:
                    if enemy.rect.colliderect(self.rects_pos[i]):
                        self.enemy_hit(i)
                        enemy.kill()
