import pygame
from tile import Tile


class Constants():
    def __init__(self, gravity=1):
        self.gravity = gravity


class World():
    '''This will hold the platforms and the goal.
    nb. In this game, the world moves left and right rather than the player'''

    def __init__(self, level, block_size, colour_platform, colour_goals, tile_look_up, intractibles,
                 consts=Constants()):
        self.platforms = []
        self.goals = []
        self.posn_y = 0
        self.colour = colour_platform
        self.colour_goals = colour_goals
        self.block_size = block_size
        self.constants = consts
        self.intractible = intractibles

        for line in level:
            self.posn_x = 0
            for block in line:
                self.platforms.append(
                    Tile(self.posn_x, self.posn_y, block_size, block_size, tile_look_up[block], None, block))
                self.posn_x = self.posn_x + block_size
            self.posn_y = self.posn_y + block_size
        self.tile_renderer = pygame.sprite.RenderPlain(self.platforms)

    def move_ip(self, x, y):
        '''move the world dist pixels right (a negative dist means left)'''
        for block in self.platforms + self.goals:
            block.move_ip(x, y)

    def collided(self, player):
        '''get the y value of the platform the player is currently on'''
        return_y = -1
        for block in self.platforms:
            if block.key in self.intractible:
                if block.collided(player):
                    return True
        return False

    def at_goal(self, player_rect):
        '''return true if the player is currently in contact with the goal. False otherwise'''
        for block in self.goals:
            if block.colliderect(player_rect):
                return True
        return False

    def update(self, screen):
        '''draw all the rectangles onto the screen'''
        self.tile_renderer.draw(screen)
        for block in self.goals:
            pygame.draw.rect(screen, self.colour_goals, block, 0)
