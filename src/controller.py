from abc import ABC, abstractmethod
import pygame
import pygame.locals as locals
import src.constants as constants


class Controller(ABC):
    def __init__(self, game):
        super().__init__()
        self._game = game

    @abstractmethod
    def update(self):
        pass


class BadgerController(Controller):
    def __init__(self, game):
        super().__init__(game)

    def update(self):
        if self._game.running:
            for event in pygame.event.get(locals.KEYUP):
                if event.key == locals.K_SPACE:
                    if self._game.last_badger.rect.right < self._game.sar.rect.left:
                        self._game.last_badger.stop()
                        self._game.create_badger()
        else:
            for _ in pygame.event.get(locals.MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                if constants.REPLAY.get_rect(center=constants.REPLAY_CENTER).collidepoint(*pos):
                    self._game.reset()
                    self._game.running = True
                elif constants.QUIT.get_rect(center=constants.QUIT_CENTER).collidepoint(*pos):
                    self._game.exit_requested = True
