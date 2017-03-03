import pygame


class Interactable(pygame.sprite.Sprite):
    """

    """

    def interact(self, player):
        """
        perform an action
        :return:
        """

class Interactables():

    def __init__(self):
        self.things = []

    def append(self, thing):
        self.things.append(thing)

    def move_ip(self,x,y):
        for thing in self.things:
            thing.rect.move_ip(x,y)
