from util import *

############################
######## RESOURCES #########
############################

res = "resources/"
image_res = res + "images/"
characters_res = image_res + "characters/"
sounds = res + "sounds/"
background_res = image_res + "backgrounds/"

object_res = image_res + "objects/"
fireball_res = object_res + "flames/"
button_res = object_res + "buttons/"

background_images = ["background0.png", "background1.png"]
background_images = add_prefix_to_list(background_res, background_images)

fireball_images = ["flame1.png", "flame2.png", "flame3.png", "flame4.png"]
fireball_images = add_prefix_to_list(fireball_res, fireball_images)

yellow_buttons = ["yel_dep.png", "yel_pre.png"]
yellow_buttons = add_prefix_to_list(button_res, yellow_buttons)

red_buttons = ["red_dep.png", "red_pre.png"]
red_buttons = add_prefix_to_list(button_res, red_buttons)

green_buttons = ["green_dep.png", "green_pre.png"]
green_buttons = add_prefix_to_list(button_res, green_buttons)

jump_sound = sounds + "qubodup-cfork-ccby3-jump.ogg"
up_images = ["0-0.png", "1-0.png", "2-0.png"]
down_images = ["0-1.png", "1-1.png", "2-1.png"]
left_images = ["0-2.png", "1-2.png", "2-2.png"]
right_images = ["0-3.png", "1-3.png", "2-3.png"]

healer_male_prefix = characters_res + "healer_m/healer_m-"
healer_female_prefix = characters_res + "healer_f/healer_f-"
mage_male_prefix = characters_res + "mage_m/mage_m-"
mage_female_prefix = characters_res + "mage_f/mage_f-"
ninja_male_prefix = characters_res + "ninja_m/ninja_m-"
ninja_female_prefix = characters_res + "ninja_f/ninja_f-"
ranger_male_prefix = characters_res + "ranger_m/ranger_m-"
ranger_female_prefix = characters_res + "ranger_f/ranger_f-"
townfolk_male_prefix = characters_res + "townfolk_m/townfolk1_m-"
townfolk_female_prefix = characters_res + "townfolk_f/townfolk1_f-"
warrior_male_prefix = characters_res + "warrior_m/warrior_m-"
warrior_female_prefix = characters_res + "warrior_f/warrior_f-"


def make_player_map(player_prefix):
    player_map = {}
    player_map['up'] = add_prefix_to_list(player_prefix, up_images)
    player_map['right'] = add_prefix_to_list(player_prefix, down_images)
    player_map['down'] = add_prefix_to_list(player_prefix, left_images)
    player_map['left'] = add_prefix_to_list(player_prefix, right_images)
    return player_map


healer_male = make_player_map(healer_male_prefix)
healer_female = make_player_map(healer_female_prefix)
mage_female = make_player_map(mage_female_prefix)
mage_male = make_player_map(mage_male_prefix)
ninja_female = make_player_map(ninja_female_prefix)
ninja_male = make_player_map(ninja_male_prefix)
ranger_female = make_player_map(ranger_female_prefix)
ranger_male = make_player_map(ranger_male_prefix)
townfolk_female = make_player_map(townfolk_female_prefix)
townfolk_male = make_player_map(townfolk_male_prefix)
warrior_female = make_player_map(warrior_female_prefix)
warrior_male = make_player_map(warrior_male_prefix)

blank = image_res + "blank.png"

players = [healer_female, healer_male, mage_female, mage_male, ninja_female, ninja_male, ranger_female,
           ranger_male, townfolk_female, townfolk_male, warrior_female, warrior_male]
print(players)