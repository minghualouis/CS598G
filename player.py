import pygame
import util
from pygame.locals import *
from resources import *

red = pygame.Color(255, 0, 0, 0)


class Player(pygame.sprite.Sprite):
    """The class that holds the main player, and controls how they jump.
    nb. The player doens't move left or right, the world moves around them"""

    def __init__(self, start_x, start_y, width, height, player_images, sounds):
        pygame.sprite.Sprite.__init__(self)
        self.images = {}
        self.image = None
        self.load_sprite_dir(player_images, 'up', width, height)
        self.load_sprite_dir(player_images, 'down', width, height)
        self.load_sprite_dir(player_images, 'left', width, height)
        self.load_sprite_dir(player_images, 'right', width, height)
        self.step = 0
        self.direction = self.images['down']
        self.image = self.direction[self.step]
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed_y = 0
        self.base = pygame.Rect(start_x, start_y + height, width, 2)
        self.sound = sounds
        self.invincible = False
        self.blank = pygame.transform.scale(pygame.image.load(blank), (width, height))
        self.moment = 0
        self.renderer = pygame.sprite.RenderPlain(self)
        self.living = True
        self.jumping = False
        self.jump_offset = 0
        self.health = 600
        self.run_speed = 0
        self.death_stage = 0
        self.death_stage_duration = 0
        self.death_stage_max_duration = 5
        self.death = [self.images['left'][1],
                      self.images['up'][2],
                      self.images['right'][0],
                      self.images['down'][1],
                      self.images['left'][2],
                      self.images['up'][0],
                      self.images['right'][1],
                      self.images['down'][2],
                      self.images['left'][0],
                      self.images['up'][1],
                      self.images['right'][2],
                      self.images['down'][0],
                      self.images['right'][1],
                      self.images['down'][2],
                      self.images['left'][0],
                      self.images['up'][1],
                      self.images['right'][2],
                      self.images['down'][0],
                      util.get_image_scaled(explosion1, width, height),
                      util.get_image_scaled(explosion2, width, height),
                      util.get_image_scaled(explosion3, width, height),
                      util.get_image_scaled(explosion4, width, height),
                      util.get_image_scaled(explosion5, width, height),
                      util.get_image_scaled(explosion6, width, height),
                      util.get_image_scaled(flicker1,width, height),
                      util.get_image_scaled(flicker2,width, height),
                      util.get_image_scaled(flicker3,width, height),
                      util.get_image_scaled(flicker4,width, height),
                      util.get_image_scaled(flicker5,width, height),
                      util.get_image_scaled(flicker1,width, height),
                      util.get_image_scaled(flicker4,width, height),
                      util.get_image_scaled(flicker2,width, height),
                      util.get_image_scaled(flicker3,width, height),
                      util.get_image_scaled(flicker5,width, height)]

    def load_sprite_dir(self, image_list, direction, width, height):
        for i in image_list[direction]:
            if direction not in self.images:
                self.images[direction] = []
            self.images[direction].append(util.get_image_scaled(i, width, height))

    def move_ip(self, x, y):
        '''this calculates the y-axis movement for the player in the current speed'''
        # collided_y = world.collided_get_y(self.base)
        # if self.speed_y <= 0 or collided_y < 0:
        #     self.rect.y = self.rect.y + self.speed_y
        #     self.speed_y = self.speed_y + world.constants.gravity
        # if collided_y > 0 and self.speed_y > 0:
        #     self.rect.y = collided_y
        # self.base.y = self.rect.y + self.rect.height

    def jump(self, world, speed):
        '''This sets the player to jump, but it only can if its feet are on the floor'''
        if self.jumping:
            return
        self.jumping = True
        self.jump_offset = 11
        self.sound["jump"].play()

    def turnInvincible(self, yes):
        if self.invincible is yes:
            return
        self.invincible = yes
        if yes:
            self.image = None
        else:
            self.image = self.blank

    def set_direction(self, key_state):
        if key_state[K_LEFT]:
            self.direction = self.images['left']
        elif key_state[K_UP]:
            self.direction = self.images['up']
        elif key_state[K_DOWN]:
            self.direction = self.images['down']
        elif key_state[K_RIGHT]:
            self.direction = self.images['right']

    def take_step(self, moved):
        self.moment += 1
        self.moment %= 7
        if moved:
            self.step += 1
            self.step %= 3
        if self.invincible and self.moment is 6:
            self.image = self.blank
        else:
            self.image = self.direction[self.step]

    def is_dead(self):
        return self.health < 0

    def set_dead(self):
        self.living = False

    def get_jump_offset(self):
        self.jump_offset -= 1
        if self.jump_offset == -10:
            self.jumping = False
            self.jump_offset = 11
            return -10

        return self.jump_offset

    def hurt(self, damage):
        self.health -= int(damage)

    def update(self, screen, player):
        pygame.draw.rect(screen, red, (0, 0, self.health, 10), 0)

    def speeding_up(self):
        self.run_speed = 5

    def reset_speed(self):
        self.run_speed = 0

    def dying(self):
        self.image = self.death[self.death_stage]
        self.death_stage_duration += 1
        if self.death_stage_duration >= self.death_stage_max_duration:
            self.death_stage_duration = 0
            self.death_stage += 1
            if not self.death_stage_max_duration <=2:
                self.death_stage_max_duration-=1


    def done_dying(self):
        return self.death_stage == len(self.death)
