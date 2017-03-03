import pygame
from fireball import fireball_size
from fireball import Fireball


class Doom():
    '''this class holds all the things that can kill the player'''

    def __init__(self, fireball_num, pit_depth, colour, screen_y, screen_x, fireball_images):
        self.base = pygame.Rect(0, screen_y - pit_depth, screen_x, pit_depth)
        self.colour = colour
        self.fireballs = []
        for i in range(0, fireball_num):
            self.fireballs.append(Fireball(fireball_images, screen_x, screen_y))
        self.fireball_plain = pygame.sprite.RenderPlain(self.fireballs)

    def move_ip(self, x, y):
        '''move everything right dist pixels (negative dist means left)'''
        for fireball in self.fireballs:
            fireball.move_ip(x, y)

    def update(self, screen):
        '''move fireballs down, and draw everything on the screen'''
        for fireball in self.fireballs:
            fireball.move_ip(0, fireball.speed_y)
        self.fireball_plain.draw(screen)
        pygame.draw.rect(screen, self.colour, self.base, 0)

    def collided(self, player):
        '''check if the player is currently in contact with any of the doom.
        nb. shrink the rectangle for the fireballs to make it fairer'''
        if player.invincible:
            return False;
        for fireball in self.fireballs:
            if fireball.rect.colliderect(player.rect):
                hit_box = fireball.rect.inflate(-int(fireball_size / 2), -int(fireball_size / 2))
                if hit_box.colliderect(player.rect):
                    return True
        return self.base.colliderect(player.rect)

    def increment(self):
        for fireball in self.fireballs:
            fireball.image = fireball.images[fireball.step]
            fireball.step = (fireball.step + 1) % 4