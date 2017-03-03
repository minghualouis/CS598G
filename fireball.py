import pygame
from random import randint

fireball_low_speed=3
fireball_high_speed=7
fireball_size=10

class Fireball(pygame.sprite.Sprite):
    '''this class holds the fireballs that fall from the sky'''


    def __init__(self, fireball_images, screen_x, screen_y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.screen_x=screen_x
        self.screen_y = screen_y
        for i in range(4):
            self.images.append(
                pygame.transform.scale(pygame.image.load(fireball_images[i]), (fireball_size, fireball_size)))
        self.rect = self.images[0].get_rect()
        self.reset()
        self.step = randint(0, 3)
        self.image = self.images[self.step]

    def reset(self):
        '''re-generate the fireball a random distance along the screen and give them a random speed'''
        self.y = 0
        self.speed_y = randint(fireball_low_speed, fireball_high_speed)
        self.x = randint(0, self.screen_x)
        self.rect.topleft = self.x, self.y

    def move_ip(self, x, y):
        '''move the fireballs dist pixels to the right (negative dist means left)
        if the fireball goes more than fifty pixels off the left of the screen, or off the right,
        they regenerate'''
        self.rect.move_ip(x,y)
        if self.rect.x < -50 or self.rect.x > self.screen_x or self.rect.y > self.screen_y:
            self.reset()