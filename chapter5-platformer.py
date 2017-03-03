import pygame
from pygame.locals import *
import sys
import time

from world import World
from player import Player
from tileset import TileMap
from doom import Doom
from buttons import Button
from interactable import Interactables
from util import *
from resources import *
import levels
for player_num in range(len(players)):

    ##########OPTIONS###########
    screen_x = 600
    screen_y = 400
    fireball_number = 10
    game_name = "Awesome Raspberry Pi Platformer"
    player_spawn_x = screen_x / 2
    player_spawn_y = screen_y / 2
    player_speed = 5
    jump_speed = -10

    platform_colour = (100, 100, 100)
    goal_colour = (0, 0, 255)
    doom_colour = (255, 0, 0)

    tile_maps = [TileMap(image_res + "DungeonTiles/dungeon_set.txt", image_res + "DungeonTiles/").tiles]
    lvls = [levels.castle]
    intractibles = [levels.castle_intractibles]
    worlds = []

    for i in range(len(lvls)):
        worlds.append(World(lvls[i], 30, platform_colour, goal_colour, tile_maps[i], intractibles[0]))

    # initialise pygame.mixer
    pygame.mixer.pre_init(44100, -16, 8, 2048)
    pygame.mixer.init()

    # initialise pygame
    pygame.init()
    level = 0
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption(game_name)
    screen = pygame.display.get_surface()
    print(sys.argv)
    # load game_name
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            level = f.readlines()

    # initialise variables
    player = Player(player_spawn_x, player_spawn_y, 32, 36, players[player_num],
                    {"jump": pygame.mixer.Sound(jump_sound)})
    world = worlds[0]
    doom = Doom(fireball_number, 10, doom_colour, screen_x, screen_y, fireball_images)
    button_locations = [[(180, 212), (53, 52), (390, 390)], [(180, 212), (52, 52), (390, 390)]]
    buttons = [Button(yellow_buttons), Button(red_buttons), Button(green_buttons)]

    interact = Interactables()

    for i in range(len(buttons)):
        buttons[i].reset_location(button_locations[level][i])
        interact.append(buttons[i]);

    moveables = [world, doom, interact]

    finished = False
    clock = pygame.time.Clock()
    player_plain = pygame.sprite.RenderPlain(player)
    button_plain = pygame.sprite.RenderPlain(buttons)
    # background = pygame.transform.scale(pygame.image.load(background_images[level]), (screen_x, screen_y)).convert()
    bg_1_x = 0
    bg_2_x = screen_x - 100
    bg_1_y = 0
    bg_2_y = screen_y - 100

    # For pausing-the-game feature by Minghua Liu
    toPause = True
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

        for moveable in moveables:
            moveable.move_ip(x_step, y_step)
        if world.collided(player):
            for moveable in moveables:
                moveable.move_ip(-x_step, -y_step)

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
        button_plain.draw(screen)
        doom.update(screen)
        doom.increment()
        for b in buttons:
            b.update(screen)
        player_plain.draw(screen)

        pygame.display.update()

        # check doom
        if doom.collided(player):
            print("You Lose!")
            finished = True

        # check invincibility; by Chase Bonifant
        for b in button_plain:
            if b.collided(player.rect):
                b.press(player)
        #

        # check goal
        if world.at_goal(player.rect):
            print("Winner!")
            finished = True
        # set the speed
        clock.tick(20)

        # uncomment to see how it's running
        #	print(clock.get_fps())
