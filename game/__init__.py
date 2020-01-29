import pygame
from pygame.locals import *
from functools import partial

from .lib.constants import skull_positions
from .lib.utils import assets_file
from .lib.button import Button, Buttons
from .lib.tower import Tower, Towers
from .lib.skull import Skull, Skulls
from .lib.player import Player


coords = skull_positions

class Game:

    def __init__(self):
        pygame.init()
        self.WIDTH = 1200
        self.HEIGHT = 680
        self.background = pygame.image.load(assets_file('background.png'))
        self.clock = pygame.time.Clock()
        self.paused = False

    def handle_buy_button_click(self, pos):
        self.player.clear_messages()
        if self.player.pay(Tower, 'buy'):
            tower = Tower(pos_xy=pos, dragging=True, player=self.player)
            self.tower_group.add(tower)

    def change_to_start_button(self):
        self.button_group.add(self.start_button)
        self.button_group.remove(self.pause_button)

    def change_to_pause_button(self):
        self.button_group.remove(self.start_button)
        self.button_group.add(self.pause_button)

    def handle_upgrade_button_click(self, pos):
        self.player.clear_messages()

        if len(self.tower_group) > 0:
            self.player.upgrade_clicked = True
            self.player.new_message('Select the tower to upgrade.')
        else:
            self.player.new_message('You don\'t have towers yet, buy first.')

    def handle_start_button_click(self, pos):
        self.player.clear_messages()
        if self.paused:
            self.continue_game()
            self.change_to_pause_button()

        if not self.player.running_wave:
            self.new_wave()
            self.player.start_wave()

        if self.player.game_over():
            self.setup()

    def handle_pause_button_click(self, pos):
        self.player.clear_messages()
        self.player.new_message('Game paused, press start to continue.')
        self.pause_game()
        self.change_to_start_button()

    def pause_game(self):
        self.paused = True

    def continue_game(self):
        self.paused = False

    def new_wave(self):
        for i in range(0, self.player.enemy_num//2):
            skull = Skull(pos_xy=(75, i*(-100)), coords=coords(0))
            self.skull_group.add(skull)

        for i in range(0, self.player.enemy_num//2):
            skull = Skull(pos_xy=(i*(-100), 425), coords=coords(1))
            self.skull_group.add(skull)

    def setup(self):
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Tower Defense')
        self.message_box = pygame.Surface((800, 120))

        self.skull_group = Skulls()
        self.tower_group = Towers()

        self.player = Player(
            enemy_group=self.skull_group,
            tower_group=self.tower_group,
            pos_xy=(1075, 455), 
        )

        self.player_group = pygame.sprite.Group(self.player)
        self.player.change_to_pause_button = self.change_to_pause_button
        self.player.change_to_start_button = self.change_to_start_button

        self.font = pygame.font.Font(assets_file('8bit.ttf'), 50)
        self.message_font = pygame.font.Font(assets_file('8bit.ttf'), 36)
        self.button_group = Buttons()

        buy_button = Button((40, 650), 'buy.png')
        buy_button.handle_click = self.handle_buy_button_click

        upgrade_button = Button((160, 650), 'upgrade.png')
        upgrade_button.handle_click = self.handle_upgrade_button_click

        self.pause_button = Button((1160, 650), 'pause.png')
        self.pause_button.handle_click = self.handle_pause_button_click

        self.start_button = Button((1160, 650), 'start.png')
        self.start_button.handle_click =  self.handle_start_button_click

        self.button_group.add(buy_button)
        self.button_group.add(upgrade_button)
        self.button_group.add(self.start_button)

        self.rect = pygame.rect.Rect(20, 20, 20, 20)

    def get_events(self):
        for self.event in pygame.event.get():
            if self.event.type == QUIT:
                exit(0)

            if self.event.type == MOUSEBUTTONDOWN:
                if not self.player.running_wave:
                    self.tower_group.mouse_drag(self.event.pos)
                if self.player.upgrade_clicked:
                    self.tower_group.select_tower(self.event.pos)
                    self.player.clear_messages()
                    self.player.new_message('Tower upgraded')

                self.button_group.mouse_click(self.event.pos)

            if self.event.type == MOUSEMOTION:
                self.tower_group.update_move(self.event.pos)

    def loop(self):
        while True:
            self.get_events()

            self.cash_text = self.font.render(f'CASH: $ {self.player.score}', False, (0, 0, 0))
            self.enemies_left_text = self.font.render(f'ENEMIES LEFT: {self.player.enemies_left}', False, (0, 0, 0))
            self.wave_text = self.font.render(f'WAVE: #{self.player.wave}', False, (0, 0, 0))
            self.upgrade_text = self.font.render(f'{self.player.wave}', False, (0, 0, 0))

            self.display.blit(self.background, (0, 0))
            self.message_box.fill((255,255, 255))

            self.display.blit(self.cash_text, (230, 632))
            self.display.blit(self.enemies_left_text, (500, 632))
            self.display.blit(self.wave_text, (870, 632))
            self.display.blit(self.upgrade_text, (870, 632))

            self.tower_group.draw_radius(self.display)
            self.tower_group.draw(self.display)
            
            self.tower_group.update()

            for i in range(len(self.player.messages)):
                text_message = self.message_font.render(self.player.messages[i], False, (0, 0, 0))
                self.message_box.blit(text_message, (40, i*40 + 25))

            if self.player.has_messages():
                self.display.blit(self.message_box, (200, 460))

            self.button_group.draw(self.display)

            self.player_group.draw(self.display)
            self.player_group.update(self.display)

            if self.player.game_over():
                self.player.end_game()
                self.change_to_start_button()

            if self.player.running_wave:
                if not self.paused:
                    self.tower_group.shoot_on_enemy(self.skull_group)
                    self.tower_group.draw_shoots(self.display)
                    self.skull_group.update()
                self.skull_group.draw(self.display)

            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        self.setup()
        self.loop()
