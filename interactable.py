import pygame


class Interactable(pygame.sprite.Sprite):
    """

    """

    def interact(self, player):
        """
        perform an action
        :return:
        """


class Interactables(object):
    def __init__(self):
        self.things = []

    def __getitem__(self, item):
        return self.things[item]

    def append(self, thing):
        self.things.append(thing)

    def move_ip(self, x, y):
        for thing in self.things:
            print thing
            thing.rect.move_ip(x, y)

    def __iter__(self):
        return iter(self.things)
