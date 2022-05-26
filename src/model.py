import pygame
import src.constants as constants
import src.utils as utils


class Badger(pygame.sprite.Sprite):
    def __init__(self, game, xpos, image_path='media/badger.png'):
        super().__init__()
        self.image = pygame.image.load(utils.path_to(image_path)).convert_alpha()
        self.rect = self.image.get_rect(center=(xpos, constants.BADGER_SPAWN_HEIGHT))
        self._game = game
        self._direction = 1
        self._moving = True

    @property
    def moving(self):
        return self._moving

    def update(self):
        if self.moving:
            self.rect = self.rect.move(0, constants.BADGER_SPEED * self._direction)
            if self._direction == 1 and self.rect.bottom > constants.MAX_BADGER_POS:
                self._direction = -1
            elif self._direction == -1 and self.rect.top < constants.MIN_BADGER_POS:
                self._direction = 1
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

        self.last_badger = Badger(self, constants.SCREEN_WIDTH - 150)
        self.last_badger.stop()
        self.badgers.add(self.last_badger)
        self.all_sprites.add(self.last_badger)
        self.create_badger()

        self.running = True

    @property
    def num_badgers(self):
        return len(self.badgers)

    def create_badger(self):
        new_xpos = self.last_badger.rect.centerx + self.last_badger.rect.width
        badger = Badger(self, new_xpos)
        self.badgers.add(badger)
        self.all_sprites.add(badger)
        self.last_badger = badger

    def lightning_bolt(self):
        lightning = Lightning(self, self.sar.rect.left)
        self.all_sprites.add(lightning)
        score = sum(1 for b in self.badgers if lightning.rect.colliderect(b.rect))
        print(f'You hit {score} badgers')

    def update(self):
        for badger in self.badgers:
            badger.update()

        if self.num_badgers >= 10:
            self.running = False
            self.lightning_bolt()
