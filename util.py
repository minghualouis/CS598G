import pygame


def add_prefix_to_list(prefix, add_to):
    add_to = [prefix + '{0}'.format(i) for i in add_to]
    return add_to


def get_image_scaled(path, width, height):
    return pygame.transform.scale(pygame.image.load(path), (width, height))
