from interactable import Interactable
from threading import Thread
import pygame
import time


invincibility_time=5
button_size = 30


class Button(Interactable):

    def __init__(self, color, start_x=0, start_y=0, ):
        pygame.sprite.Sprite.__init__(self)
        self.start_x = start_x
        self.start_y = start_y
        self.images = []

        for i in range(2):
            self.images.append(pygame.transform.scale(pygame.image.load(color[i]), (button_size, button_size)))

        self.rect = self.images[0].get_rect()
        self.reset()
        self.image = self.images[0]

    def reset(self):
        '''re-generate the fireball a random distance along the screen and give them a random speed'''
        self.y = self.start_y
        self.speed_y = 0
        self.x = self.start_x
        self.rect.topleft = self.x, self.y
        self.image = self.images[0]

    def reset_location(self, pt):
        self.start_x = pt[0]
        self.start_y = pt[1]
        self.reset()

    def press(self, player):
        if player.invincible:
            return
        thread = Thread(target=self.waitToRelease, args=[player])
        thread.start()

    def waitToRelease(self, player):
        self.image = self.images[1]
        player.turnInvincible(True)
        print("invincible")
        time.sleep(invincibility_time)
        player.turnInvincible(False)
        self.image = self.images[0]
        print("vincible again!")


    def collided(self, player):
        return self.rect.colliderect(player)

    def move_ip(self, x, y):
        '''move the fireballs dist pixels to the right (negative dist means left)
        if the fireball goes more than fifty pixels off the left of the screen, or off the right,
        they regenerate'''
        self.rect.move_ip(x, y)

    def interact(self,player):
        self.press(player)