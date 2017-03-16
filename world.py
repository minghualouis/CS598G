import pygame
from tile import Tile


class Constants():
    def __init__(self, gravity=1):
        self.gravity = gravity


class World():
    '''This will hold the platforms and the goal.
    nb. In this game, the world moves left and right rather than the player'''

    def __init__(self, world_definition, tile_look_up, player_character, solids_list,
                 enemies_list, other_characters, interactible_list,
                 block_size, splitter, consts=Constants()):
        self.layers = []
        self.block_size = block_size
        self.constants = consts
        self.solids = solids_list
        self.player = player_character[0]

        self.monsters = enemies_list
        self.npcs = other_characters
        self.objects = interactible_list
        i = 0
        self.renderers = []
        self.posn_x = 0
        self.posn_y = 0

        for layer in world_definition:
            layer_blocks = []
            self.posn_y = 0
            for row in layer:
                self.posn_x = 0
                for cell in splitter(row):
                    layer_blocks.append(
                        Tile(self.posn_x, self.posn_y, block_size, block_size, tile_look_up[cell], None, cell))
                    self.posn_x += block_size
                self.posn_y += block_size
            self.layers.append(layer_blocks)

        layer_cnt = 0
        for layer in self.layers:
            self.renderers.append([])
            for cell in layer:
                self.renderers[i].append(pygame.sprite.RenderPlain(cell))

        self.add_renderables(self.monsters)
        self.add_renderables(self.objects)
        self.add_renderables(self.npcs)
        self.add_renderable(player_character[1], player_character[0].renderer)

    def add_items_to_layer(self, items):
        for item in items:
            self.add_item_to_layer(item[0], item[1])

    def add_item_to_layer(self, to_add, layer_num):
        while layer_num > len(self.layers):
            self.layers.append([])
        self.layers[layer_num].apppend(to_add)

    def add_renderables(self, renderables):
        for renderable in renderables:
            self.add_renderable(renderable[1], renderable[0].renderer)

    def add_renderable(self, layer, renderer):
        while len(self.renderers) <= layer:
            self.renderers.append([])
        self.renderers[layer].append(renderer)

    def move_ip(self, x, y):
        '''move the world dist pixels right (a negative dist means left)'''
        if self.player.jumping:
            y += self.player.get_jump_offset()
        for layer in self.layers:
            for block in layer:
                if block is not self.player:
                    block.move_ip(x, y)
        for enemy in self.monsters:
            enemy[0].move_ip(x, y)
        for object in self.objects:
            object[0].move_ip(x, y)
        for npc in self.npcs:
            npc[0].move_ip(x, y)

    def collided(self, player):
        '''get the y value of the platform the player is currently on'''
        return_y = -1
        for layer in self.layers:
            for block in layer:
                if block.key in self.solids:
                    if block.collided(player):
                        return True
        return False

    def at_goal(self, player_rect):
        '''return true if the player is currently in contact with the goal. False otherwise'''
        return False

    def update(self, screen):
        '''draw all the rectangles onto the screen'''
        for layer_of_renderers in self.renderers:
            for renderer in layer_of_renderers:
                renderer.draw(screen)

        for enemy in self.monsters:
            enemy[0].update(screen, self.player)

        for object in self.objects:
            object[0].update(screen, self.player)

        for npc in self.npcs:
            object[0].update(screen, self.player)

        self.player.update(screen, self.player)

    def game_over(self):
        return self.player.is_dead()
