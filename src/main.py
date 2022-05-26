import pygame
import pygame.locals as locals
import src.constants as constants
from src.model import Game
from src.view import BadgerStackerView
from src.controller import BadgerController


def main():
    pygame.init()
    screen = pygame.display.set_mode(constants.SCREEN_SIZE)

    game = Game()
    view = BadgerStackerView(game, screen)
    controller = BadgerController(game)

    clock = pygame.time.Clock()
    exited = False
    while not exited:
        for _ in pygame.event.get(locals.QUIT):
            exited = True

        controller.update()
        game.update()
        view.draw()

        if not game.running:
            break

        clock.tick(constants.FPS)

    for _ in range(constants.FPS * 5):
        view.draw()
        clock.tick(constants.FPS)


if __name__ == '__main__':
    main()
