import sys
import time

import pygame
import fireball
from pygame.locals import *

import levels
from buttons import Button
from doom import Doom
from interactable import Interactables
from player import Player
from resources import *
from tileset import TileMap
from world import World

# initialise pygame.mixer
pygame.mixer.pre_init(44100, -16, 8, 2048)
pygame.mixer.init()

for player_num in range(len(players)):

    ##########OPTIONS###########
    screen_x = 600
    screen_y = 420
    fireball_number = 10
    game_name = "Awesome Raspberry Pi Platformer"
    player_spawn_x = screen_x / 2
    player_spawn_y = screen_y / 2
    player_speed = 5
    jump_speed = -10

    platform_colour = (100, 100, 100)
    goal_colour = (0, 0, 255)
    doom_colour = (255, 0, 0)

    dungeon_map = TileMap(dungeon_dict, dungeon_tiles_res).tiles
    magecity_map = TileMap(magecity_dict, magecity_tiles_res).tiles

    magecity_level = levels.magecity
    magecity_walls = levels.city_walls

    player_sound_map = {"jump": pygame.mixer.Sound(jump_sound)}
    # initialise variables
    player = Player(player_spawn_x, player_spawn_y, 32, 36, players[player_num], player_sound_map)
    fireball.fireball_high_speed=7
    fireball.maxsize=6
    doom = Doom(fireball_number, 10, doom_colour, screen_x, screen_y, fireball_images)
    button_locations = [(180, 212), (53, 52), (390, 390)]
    buttons = [Button(yellow_buttons), Button(red_buttons), Button(green_buttons)]

    interact = Interactables()

    for i in range(len(buttons)):
        buttons[i].reset_location(button_locations[i])
        interact.append((buttons[i], 1));

    world = World(magecity_level, magecity_map, (player, 2), magecity_walls, [(doom, 2)], [], interact, 32,
                  levels.magecity_splitter)

    # initialise pygame
    pygame.init()

    font = pygame.font.Font(None, 50)

    level = 0
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption(game_name)
    screen = pygame.display.get_surface()
    print(sys.argv)
    # load game_name
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            level = f.readlines()

    finished = False
    clock = pygame.time.Clock()
    bg_1_x = 0
    bg_2_x = screen_x - 100
    bg_1_y = 0
    bg_2_y = screen_y - 100

    # For pausing-the-game feature by Minghua Liu
    toPause = True

    score = 0
    time_steps = 0
    iterations_passed = 0
    speed_step=50 # fireballs speed up every X ticks
    size_step=20 # fireballs grow larger every X tick
    fireball_addition=50 # add an additional fireball to the fireball list every X ticks
    clock_speed = 20
    while not finished:

        # blank screen
        screen.fill((0, 0, 0))

        # check events
        for event in pygame.event.get():
            if event.type == QUIT:
                finished = True
        # check which keys are held
        key_state = pygame.key.get_pressed()

        # player walking
        x_step = 0
        y_step = 0

        if player.is_dead() and not player.done_dying():
            player.dying()
        else:
            # move left and right
            if key_state[K_LEFT]:
                x_step = player_speed
            if key_state[K_RIGHT]:
                x_step = -player_speed
            if key_state[K_UP]:
                y_step = player_speed
            if key_state[K_DOWN]:
                y_step = -player_speed

            if key_state[K_SPACE]:
                player.jump(world, jump_speed)

            player.set_direction(key_state)
            player.take_step((x_step is not 0 or y_step is not 0))

            if key_state[K_RSHIFT] or key_state[K_LSHIFT]:
                y_step *= player.run_speed
                x_step *= player.run_speed
                player.speeding_up()
            else:
                player.reset_speed()

        if not world.collided(player):
            world.move_ip(x_step, y_step)
        if world.collided(player):
            world.move_ip(-x_step, -y_step)

        # --------------Pausing-the-game feature; by Minghua Liu start---------------
        if key_state[K_p]:
            while toPause:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        finished = True
                key_state = pygame.key.get_pressed()
                if key_state[K_c]:
                    print("I'm in second p")
                    break
                time.sleep(.1)

        # --------------Pausing-the-game feature; by Minghua Liu end---------------


        # render the frame
        #    screen.blit(background, (bg_1_x, bg_1_y))
        #    screen.blit(background, (bg_2_x, bg_2_y))
        world.update(screen)

        #
        if world.game_over():
            label1 = font.render("Game Over!", 1, (255, 0, 0))
            label2 = font.render("You Lose!", 1, (255, 0, 0))
            label3 = font.render("Final Score: " + str(score), 1, (255, 0, 0))
            screen.blit(label1, (0, screen_y / 2))
            screen.blit(label2, (0, screen_y / 2 + 50))
            screen.blit(label3, (0, screen_y / 2 + 100))
            print "Game Over: Score: " + str(score)
            if player.done_dying():
                finished = True
        else:
            label = font.render("Score: " + str(score), 0, (0, 255, 0))
            screen.blit(label, (0, 0))

        pygame.display.update()

        if world.game_over() and player.done_dying():
            time.sleep(1.5)

        # set the speed1
        clock.tick(clock_speed)
        iterations_passed += 1
        if iterations_passed is 20:
            iterations_passed = 0
            clock_speed += 1

        if time_steps % size_step == 0:
            fireball.maxsize += 1
        if time_steps % speed_step == 0:
            fireball.fireball_high_speed += 1
        if time_steps % fireball_addition == 0:
            doom.addFireball()

        if clock_speed > 40:
            clock_speed = 40

        # uncomment to see how it's running
        # print(clock.get_fps())

        if not player.invincible and not player.is_dead():
            time_steps += 1
            score += player.health * time_steps
        print "Fireball count: "+ str(len(doom.fireballs))