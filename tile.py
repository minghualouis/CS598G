import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, width, height, images, sounds, key):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(len(images)):
            self.images.append(pygame.transform.scale(pygame.image.load(images[i]), (width, height)))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed_y = 0
        self.speed_x = 0
        self.base = pygame.Rect(start_x, start_y + height, width, 2)
        self.sounds = sounds
        self.key = key

    def move_ip(self, x, y):
        #
        self.rect.move_ip(x, y)

    def collided(self, player):
        return self.rect.colliderect(player.rect)
