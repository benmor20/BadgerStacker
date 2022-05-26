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

        if not self._game.running:
            score = constants.SCORE_FONT.render(f'Score is {self._game.score}', True, constants.TEXT)
            self.screen.blit(score, score.get_rect(center=constants.SCORE_CENTER))
            self.screen.blit(constants.REPLAY, constants.REPLAY.get_rect(center=constants.REPLAY_CENTER))
            self.screen.blit(constants.QUIT, constants.QUIT.get_rect(center=constants.QUIT_CENTER))
