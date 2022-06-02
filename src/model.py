import pygame
import src.constants as constants
import src.utils as utils


class Badger(pygame.sprite.Sprite):
    def __init__(self, game, xpos, badger_num, image_path='media/badger.png'):
        super().__init__()
        self.image = pygame.image.load(utils.path_to(image_path)).convert_alpha()
        if badger_num == 1:
            self.rect = self.image.get_rect(center=(xpos, constants.IDEAL_BADGER_HEIGHT))
        else:
            self.rect = self.image.get_rect(center=(xpos, constants.BADGER_SPAWN_HEIGHT))
        self._game = game
        self._speed_scale = badger_num
        self._moving = True
        self.badger_num = badger_num
        print(f'Badger num is {badger_num}')
        print(f'Speed scale is {self._speed_scale}')

    @property
    def moving(self):
        return self._moving

    def update(self):
        super().update()
        print(f'{self._speed_scale}, {self.moving}')
        if self.moving:
            self.rect = self.rect.move(0, constants.BADGER_SPEED_SCALE * self._speed_scale)
            if self._speed_scale > 0 and self.rect.bottom > constants.MAX_BADGER_POS:
                self._speed_scale *= -1
            elif self._speed_scale < 0 and self.rect.top < constants.MIN_BADGER_POS:
                self._speed_scale *= -1
        self.rect = self.rect.move(-constants.SCROLL_SPEED, 0)

    def stop(self):
        self._moving = False


class Player(pygame.sprite.Sprite):
    def __init__(self, game, image_path='media/sar.png'):
        super().__init__()
        self.image = pygame.image.load(utils.path_to(image_path)).convert_alpha()
        self.rect = self.image.get_rect(center=constants.SAR_CENTER)
        self._game = game


class Lightning(pygame.sprite.Sprite):
    def __init__(self, game, sar_left, image_path='media/lightning.png'):
        super().__init__()
        self.image = pygame.image.load(utils.path_to(image_path)).convert_alpha()
        self.rect = self.image.get_rect(midright=(sar_left, constants.SCREEN_HEIGHT // 2))
        self._game = game


class Game:
    def __init__(self):
        self.badgers = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.sar = Player(self)
        self.all_sprites.add(self.sar)

        self.last_badger = None
        self.score = 0

        self.running = True
        self.exit_requested = False

        self.reset()

    @property
    def num_badgers(self):
        return len(self.badgers)

    def reset(self):
        for s in self.all_sprites:
            if isinstance(s, Player):
                continue
            s.kill()
        self.last_badger = Badger(self, constants.SCREEN_WIDTH - 150, 1)
        self.last_badger.stop()
        self.badgers.add(self.last_badger)
        self.all_sprites.add(self.last_badger)
        self.create_badger()
        self.running = True
        self.score = 0

    def create_badger(self):
        new_xpos = self.last_badger.rect.centerx + self.last_badger.rect.width
        badger = Badger(self, new_xpos, self.last_badger.badger_num + 1)
        self.badgers.add(badger)
        self.all_sprites.add(badger)
        self.last_badger = badger

    def lightning_bolt(self):
        lightning = Lightning(self, self.sar.rect.left)
        self.all_sprites.add(lightning)
        self.score = sum(1 for b in self.badgers if lightning.rect.colliderect(b.rect))
        print(f'You hit {self.score} badgers')

    def update(self):
        if self.running:
            for badger in self.badgers:
                badger.update()

            if self.num_badgers >= 10:
                self.running = False
                self.lightning_bolt()
