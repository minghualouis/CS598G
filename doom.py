import pygame
import math
from fireball import Fireball


class Doom():
    '''this class holds all the things that can kill the player'''

    def __init__(self, fireball_num, pit_depth, colour, screen_x, screen_y, fireball_images):
        self.fireballs = []
        self.fireball_images = fireball_images
        for i in range(0, fireball_num):
            self.fireballs.append(Fireball(fireball_images, screen_x, screen_y))
        self.renderer = pygame.sprite.RenderPlain(self.fireballs)

    def move_ip(self, x, y):
        '''move everything right dist pixels (negative dist means left)'''
        for fireball in self.fireballs:
            fireball.move_ip(x, y)

    def update(self, screen, player):
        '''move fireballs down, and draw everything on the screen'''
        for fireball in self.fireballs:
            fireball.move_ip(0, fireball.speed_y)
        self.increment()

        if self.collided(player):
            player.hurt(math.sqrt(fireball.speed_y * fireball.size))

    def collided(self, player):
        '''check if the player is currently in contact with any of the doom.
        nb. shrink the rectangle for the fireballs to make it fairer'''
        if player.invincible:
            return False;
        for fireball in self.fireballs:
            if fireball.rect.colliderect(player.rect):
                return True

    def increment(self):
        for fireball in self.fireballs:
            fireball.image = fireball.images[fireball.step]
            fireball.step = (fireball.step + 1) % 4

    def addFireball(self):
        self.fireballs.append(Fireball(self.fireball_images, self.fireballs[0].screen_x, self.fireballs[0].screen_y))
        self.renderer = pygame.sprite.RenderPlain(self.fireballs)