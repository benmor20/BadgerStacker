from abc import ABC, abstractmethod
import pygame
import pygame.locals as locals


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
        for event in pygame.event.get(locals.KEYUP):
            if event.key == locals.K_SPACE:
                if self._game.last_badger.rect.right < self._game.sar.rect.left:
                    self._game.last_badger.stop()
                    self._game.create_badger()
