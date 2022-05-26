from abc import ABC, abstractmethod
import pygame
import src.constants as constants


class View(ABC):
    def __init__(self, game):
        self._game = game

    @abstractmethod
    def draw(self):
        pass


class PygameView(View, ABC):
    def __init__(self, game, screen: pygame.Surface):
        super().__init__(game)
        self._screen = screen

    @property
    def screen(self):
        return self._screen

    @abstractmethod
    def draw_on_screen(self):
        pass

    def draw(self):
        self.draw_on_screen()
        pygame.display.flip()


class BadgerStackerView(PygameView):
    def __init__(self, game, screen):
        super().__init__(game, screen)

    def draw_on_screen(self):
        self.screen.fill(constants.GRASS)
        self._game.all_sprites.draw(self.screen)
