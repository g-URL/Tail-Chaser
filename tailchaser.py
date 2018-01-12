# =========== INFO ===========
#
# Chasing Tails - Custom Game
# CPSC 359
# Assignment 04
# Date: Dec 5 2017
# Version: Keyboard
#
# Game Concept: K. Jorgensen, G. Gonzaga
# Game Implementation (Art & Code): R. Apperley
#
# Runs with Python3 and Pygame 1.9.3
# Put all pngs in a data folder of the same directory
#
# ============================


# imports
import random
import time
import pygame
from pygame.locals import *
from math import *
import os
#import adxl345Driver as accel


# global constants
WINDOW_LENGTH = 640
WINDOW_WIDTH = 640
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
MENU = 0
GAME = 1
PAUSE = 2
OVER = 3
QUIT = 4


# dictionary of all images used in the game
photo_album = {"kitten_black"  : [("kitten_black_north_0.png", "kitten_black_north_1.png"), 
                                  ("kitten_black_east_0.png", "kitten_black_east_1.png"), 
                                  ("kitten_black_south_0.png", "kitten_black_south_1.png"), 
                                  ("kitten_black_west_0.png", "kitten_black_west_1.png")],

               "kitten_grey"   : [("kitten_grey_north_0.png", "kitten_grey_north_1.png"), 
                                  ("kitten_grey_east_0.png", "kitten_grey_east_1.png"), 
                                  ("kitten_grey_south_0.png", "kitten_grey_south_1.png"), 
                                  ("kitten_grey_west_0.png", "kitten_grey_west_1.png")],

               "kitten_orange" : [("kitten_orange_north_0.png", "kitten_orange_north_1.png"), 
                                  ("kitten_orange_east_0.png", "kitten_orange_east_1.png"), 
                                  ("kitten_orange_south_0.png", "kitten_orange_south_1.png"), 
                                  ("kitten_orange_west_0.png", "kitten_orange_west_1.png")],

               "kitten_white"  : [("kitten_white_north_0.png", "kitten_white_north_1.png"), 
                                  ("kitten_white_east_0.png", "kitten_white_east_1.png"), 
                                  ("kitten_white_south_0.png", "kitten_white_south_1.png"), 
                                  ("kitten_white_west_0.png", "kitten_white_west_1.png")],

               "mother_pink"   : [("mother_pink_north_0.png", "mother_pink_north_1.png"), 
                                  ["mother_pink_east_0.png", "mother_pink_east_1.png"], 
                                  ("mother_pink_south_0.png", "mother_pink_south_1.png"), 
                                  ("mother_pink_west_0.png", "mother_pink_west_1.png")],

               "button_game"   : ["button_game_0.png", "button_game_1.png"],
               "button_quit"   : ["button_quit_0.png", "button_quit_1.png"],

               "board"         : ["board.png"],
               "board_red"     : ["board_red.png"],

               "border_north"  : ["border_north.png"],
               "border_south"  : ["border_south.png"],
               "border_east"   : ["border_east.png"],
               "border_west"   : ["border_west.png"],

               "game_title"    : ["game_title.png"],
               "game_over"     : ["game_over.png"],

               "food_bowl"     : ["food_bowl.png"],
               "litter"        : ["litter.png"],

               "tunnel_left"   : ["tunnel_left.png"],
               "tunnel_right"  : ["tunnel_right.png"],
               "tunnel_top"    : ["tunnel_top.png"],
               "tunnel_bottom" : ["tunnel_bottom.png"],

               "yarn"          : ["yarn.png"]
              }


# initializing sprite groups
kitten_group = pygame.sprite.RenderPlain()
mother_group = pygame.sprite.RenderPlain()
tail_group = pygame.sprite.RenderPlain()
obstacles_group = pygame.sprite.RenderPlain()
button_group = pygame.sprite.RenderPlain()
tunnel_top_group = pygame.sprite.RenderPlain()
tunnel_bottom_group = pygame.sprite.RenderPlain()


# format for classes taken from Invasion of the Blobs (course content)
# use of super().__init__() taken from https://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods
# class for cats (mom and kittens)
# cats implemented as a linked list
class Cat(pygame.sprite.Sprite):
    def __init__(self, name, colour, direction, position, next=None):
        super().__init__()
        self.name = name
        self.colour = colour
        self.direction = direction
        self.position = position
        (x,y) = self.position
        self.next = next 
        self.image = load_image(photo_album[self.name+"_"+self.colour][self.direction][0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if name == "mother":
            mother_group.add(self)


# class for obstacles (litter box, food bowl etc...)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, name, position):
        super().__init__()
        self.name = name
        self.position = position
        (x,y) = self.position
        self.image = load_image(photo_album[self.name][0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        obstacles_group.add(self)


# class for tunnel objects
class Tunnel(pygame.sprite.Sprite):
    def __init__(self, name, position):
        super().__init__()
        self.name = name
        self.position = position
        (x,y) = self.position
        self.image = load_image(photo_album[self.name][0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# class for menu buttons
class Button(pygame.sprite.Sprite):
    def __init__(self, name, position):
        super().__init__()
        self.name = name
        self.position = position
        (x,y) = self.position
        self.image = load_image(photo_album[self.name][0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        button_group.add(self)


# function that interprets action based on data from accelerometer
# this is not currently enabled because this version is for keyboard only
'''
def actionData (mode):

    # Obtaining data from custom accelerometer driver
    #data = accel.getData()
    data = [0,0,0]
    x = data[0]
    y = data[1]
    z = data[2] 
    
    x_value = 0
    y_value = 0
    z_value = 0

    if (mode == GAME):
        if (x > 150):
            x_value = K_LEFT
        if (x < -150):
            x_value = K_RIGHT
        if (y > 150):
            y_value = K_DOWN
        if (y < -150):
            y_value = K_UP
        if (z < -200):
            z_value = K_RETURN

    if (mode == PAUSE):
        if (z < -200):
            z_value = K_RETURN

    if (mode == MENU):
        if (y > 100):
            y_value = K_DOWN
        if (y < -100):
            y_value = K_UP
        if (z < -200):
            z_value = K_RETURN

    return [x_value, y_value, z_value]
'''

# flashes the menu buttons
def flash_button(button, screen):
    button.image = load_image(photo_album[button.name][0])           
    button_group.draw(screen)
    pygame.display.update()
    time.sleep(0.25)

    button.image = load_image(photo_album[button.name][1])            
    button_group.draw(screen)
    pygame.display.update() 
    time.sleep(0.25)


# taken from Invasion of the Blobs (course content)
def load_image(filename):
    image = pygame.image.load(os.path.join("data", filename))
    image.set_colorkey((0,255,0), pygame.RLEACCEL)
    return image.convert()


# initializes kittens on the board
def initialize_kittens(min, max, mother, obstacles):
    colour_list = ["black", "grey", "orange", "white"]
    direction_list = [NORTH, EAST, SOUTH, WEST]

    number_of_kittens = random.randrange(min, max)

    for i in range(number_of_kittens):
        # length is reduced to remove white kittens (contrast is distracting)
        colour = colour_list[random.randrange(0, (len(colour_list)-1))]
        x_coordinate = random.randrange(32, WINDOW_LENGTH)
        y_coordinate = random.randrange(32, WINDOW_WIDTH)
        position = (x_coordinate, y_coordinate)
        direction = direction_list[random.randrange(0, len(direction_list))]
        kitten = Cat("kitten", colour, direction, position)

        collision = False
        if kitten.rect.colliderect(mother):
            collision = True

        for obstacle in obstacles:
            if kitten.rect.colliderect(obstacle):
                collision = True

        if collision == False:
            kitten_group.add(kitten)
            kitten_group.update()


# function that adds kittens to the tail_group so they follow mom
def add_kitten(cat, kitten):
    if cat.next == None:
        cat.next = kitten
        tail_group.remove(kitten)

        # makes it impossible to run into the first kitten
        mother_group.add(kitten)

    else:
        while cat.next:
            cat = cat.next
        cat.next = kitten

    if cat.direction == NORTH:
        cat.next.rect.x = cat.rect.x
        cat.next.rect.y = cat.rect.y + 33

    if cat.direction == SOUTH:
        cat.next.rect.x = cat.rect.x
        cat.next.rect.y = cat.rect.y - 33

    if cat.direction == EAST:
        cat.next.rect.x = cat.rect.x - 33
        cat.next.rect.y = cat.rect.y

    if cat.direction == WEST:
        cat.next.rect.x = cat.rect.x + 33
        cat.next.rect.y = cat.rect.y

    cat.next.direction = cat.direction
    cat.next.image = load_image(photo_album[cat.next.name+"_"+cat.next.colour][cat.next.direction][0])


# function that iterates through the linked list of cats to update their position
# while loops handle cat positions based on their distance between themselves and the next cat
def update_tail(cat, screen):
    if cat.next == None:
        return

    distance = get_distance(cat, cat.next)
    if cat.next != None:

        while distance > 32:

            if cat.direction == NORTH:

                while cat.next.rect.x != cat.rect.x and distance > 32:
                    if cat.next.rect.x < cat.rect.x:
                        cat.next.rect.x = cat.next.rect.x + 1
                    else:
                        cat.next.rect.x = cat.next.rect.x - 1
                    distance = get_distance(cat, cat.next)        

                while cat.next.rect.y != cat.rect.y + 32 and distance > 32:
                    if cat.next.rect.y < cat.rect.y:
                        cat.next.rect.y = cat.next.rect.y + 1
                    else:
                        cat.next.rect.y = cat.next.rect.y - 1
                    distance = get_distance(cat, cat.next)

                if cat.next.rect.x == cat.rect.x and cat.next.direction != cat.direction:
                    cat.next.direction = cat.direction 
                    cat.next.image = load_image(photo_album[cat.next.name+"_"+cat.next.colour][cat.next.direction][0])

            if cat.direction == SOUTH:

                while cat.next.rect.x != cat.rect.x and distance > 32:
                    if cat.next.rect.x < cat.rect.x:
                        cat.next.rect.x = cat.next.rect.x + 1
                    else:
                        cat.next.rect.x = cat.next.rect.x - 1
                    distance = get_distance(cat, cat.next)        

                while cat.next.rect.y != cat.rect.y - 32 and distance > 32:
                    if cat.next.rect.y < cat.rect.y:
                        cat.next.rect.y = cat.next.rect.y + 1
                    else:
                        cat.next.rect.y = cat.next.rect.y - 1
                    distance = get_distance(cat, cat.next)

                if cat.next.rect.x == cat.rect.x and cat.next.direction != cat.direction:
                    cat.next.direction = cat.direction  
                    cat.next.image = load_image(photo_album[cat.next.name+"_"+cat.next.colour][cat.next.direction][0])

            elif cat.direction == EAST:

                while cat.next.rect.y != cat.rect.y and distance > 32:
                    if cat.next.rect.y < cat.rect.y:
                        cat.next.rect.y = cat.next.rect.y + 1
                    else:
                        cat.next.rect.y = cat.next.rect.y - 1
                    distance = get_distance(cat, cat.next)

                while cat.next.rect.x != cat.rect.x - 32 and distance > 32:
                    if cat.next.rect.x < cat.rect.x - 32:
                        cat.next.rect.x = cat.next.rect.x + 1
                    else:
                        cat.next.rect.x = cat.next.rect.x - 1
                    distance = get_distance(cat, cat.next)

                if cat.next.rect.y == cat.rect.y and cat.next.direction != cat.direction:
                    cat.next.direction = cat.direction         
                    cat.next.image = load_image(photo_album[cat.next.name+"_"+cat.next.colour][cat.next.direction][0])

            elif cat.direction == WEST:

                while cat.next.rect.y != cat.rect.y and distance > 32:
                    if cat.next.rect.y < cat.rect.y:
                        cat.next.rect.y = cat.next.rect.y + 1
                    else:
                        cat.next.rect.y = cat.next.rect.y - 1
                    distance = get_distance(cat, cat.next)

                while cat.next.rect.x != cat.rect.x + 32 and distance > 32:
                    if cat.next.rect.x < cat.rect.x + 32:
                        cat.next.rect.x = cat.next.rect.x + 1
                    else:
                        cat.next.rect.x = cat.next.rect.x - 1
                    distance = get_distance(cat, cat.next)

                if cat.next.rect.y == cat.rect.y and cat.next.direction != cat.direction:
                    cat.next.direction = cat.direction
                    cat.next.image = load_image(photo_album[cat.next.name+"_"+cat.next.colour][cat.next.direction][0])

    if cat.next.next != None:       
        update_tail(cat.next, screen)


# get distance between cat and preceeding cat
def get_distance(cat1, cat2):
    x = cat1.rect.x - cat2.rect.x
    y = cat1.rect.y - cat2.rect.y
    
    distance = (x**2 + y**2)**(0.5)
    return distance


# code to print score taken from stackoverflow
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
def update_score(screen, myfont, score):
    score_label = myfont.render("Score: " + str(score), False, (255, 255, 255))
    screen.blit(score_label, (464, 82))


# main function that handles game modes
def main():

    game_mode = MENU

    while game_mode != QUIT:

        # how to initialize game taken from tutorial
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_LENGTH,WINDOW_WIDTH))
        pygame.display.set_caption("TAIL CHASER")
        background = load_image(photo_album["board"][0])
        screen.blit(background, (0,0))
        pygame.display.update()

        selected = None
        while game_mode == MENU:

            # initialize objects when the menu is fresh (selected == None)
            if selected == None:
                game_title = load_image(photo_album["game_title"][0])
                screen.blit(game_title, (96,0))
                button_game = Button("button_game", (128, 288))
                button_quit = Button("button_quit", (208,448))
                button_group.update()
                button_group.draw(screen)
                pygame.display.update()
                selected = button_game

            flash_button(selected, screen)

            # method for interpreting accelerometer input
            # disabled for keyboard version
            '''
            hardware_data = actionData(MENU)

            if ((hardware_data[1] == K_DOWN or hardware_data[1] == K_UP) and selected == button_quit):
                selected.image = load_image(photo_album[selected.name][0]) 
                selected = button_game
                selected.image = load_image(photo_album[selected.name][1])  

            elif ((hardware_data[1] == K_DOWN or hardware_data[1] == K_UP) and selected == button_game):
                selected.image = load_image(photo_album[selected.name][0]) 
                selected = button_quit
                selected.image = load_image(photo_album[selected.name][1])  

            elif ((hardware_data[2] == K_RETURN) and (selected == button_quit)):
                game_mode = QUIT
                return

            elif ((hardware_data[2] == K_RETURN) and (selected == button_game)):
                game_mode = GAME
            '''
  
            # method for keylistening taken from Invasion of the Blobs (course content)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if ((event.key == K_UP or event.key == K_w or event.key == K_DOWN or event.key == K_s) and selected == button_quit):
                        selected.image = load_image(photo_album[selected.name][0]) 
                        selected = button_game
                        selected.image = load_image(photo_album[selected.name][1])                   

                    elif ((event.key == K_UP or event.key == K_w or event.key == K_DOWN or event.key == K_s) and selected == button_game):
                        selected.image = load_image(photo_album[selected.name][0])
                        selected = button_quit
                        selected.image = load_image(photo_album[selected.name][1])

                    elif ((event.key == K_RETURN) and selected == button_quit):
                        game_mode = QUIT
                        return

                    elif ((event.key == K_RETURN) and selected == button_game):
                        game_mode = GAME
          
            button_group.draw(screen)
            pygame.display.update()

        # sleep for menu-game transition
        time.sleep(1)
        last_direction = None
        # initiation of animation counter
        animation = 1
        game_fresh = True
        while game_mode == GAME:

            # only initialize if the game is fresh
            if game_fresh == True:

                #screen.blit(background, (0,0))
                score = 0

                # code to print score taken from stackoverflow
                # https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
                pygame.font.init()
                myfont = pygame.font.SysFont("Fixedsys", 30)

                # initializing obstacles
                border_north = Obstacle("border_north", (0,0))
                border_south = Obstacle("border_south", (0,608))
                border_east = Obstacle("border_east", (608,0))
                border_west = Obstacle("border_west", (0,0))
                yarn = Obstacle("yarn", (416,416))
                tunnel_left = Obstacle("tunnel_left", (128,192))
                tunnel_right = Obstacle("tunnel_right", (224, 192)) 
                food_bowl = Obstacle("food_bowl", (32,512))
                litter = Obstacle("litter", (416,32))
                obstacles_group.update()

                # initializing tunnel
                # separate tunnel groups for drawing order
                tunnel_top = Tunnel("tunnel_top", (128,192))
                tunnel_top_group.add(tunnel_top)
                tunnel_top_group.update()            
                tunnel_bottom = Tunnel("tunnel_bottom", (128,192))
                tunnel_bottom_group.add(tunnel_bottom)
                tunnel_bottom_group.update()

                # initializing mom
                mother = Cat("mother", "pink", SOUTH, (32,32))
                mother_group.update()

                # the game is now stale                
                game_fresh = False


            # initializing kittens on the board
            if len(kitten_group) == 0:
                initialize_kittens(10, 15, mother, obstacles_group)

            # detecting mother-kitten collisions
            for kitten in kitten_group:
                if mother.rect.colliderect(kitten):
                    kitten_group.remove(kitten)
                    kitten_group.update()
                    tail_group.add(kitten)
                    tail_group.update()
                    add_kitten(mother, kitten)
                    score = score + 1

            # detecting mother-obstacle collisions
            for obstacles in obstacles_group:
                if mother.rect.colliderect(obstacles):
                    game_mode = OVER

       
            if game_mode != OVER:

                update_tail(mother, screen)
                for tail in tail_group:
                    if mother.rect.colliderect(tail):
                        game_mode = OVER  


                # method for interpreting accelerometer input
                # disabled for keyboard version
                '''
                hardware_data = actionData(GAME)

                if hardware_data[1] == K_DOWN:
                    mother.direction = SOUTH
                    last_direction = SOUTH 

                if hardware_data[1] == K_UP:
                    mother.direction = NORTH
                    last_direction = NORTH 

                if hardware_data[0] == K_LEFT:
                    mother.direction = WEST
                    last_direction = WEST

                if hardware_data[0] == K_RIGHT:
                    mother.direction = EAST
                    last_direction = EAST

                if hardware_data[2] == K_RETURN:
                    game_mode = PAUSE
                '''


                # method for keylistening taken from Invasion of the Blobs (course content)
                for event in pygame.event.get():
                    if event.type == KEYDOWN:

                        if event.key == K_UP or event.key == K_w:
                            mother.direction = NORTH
                            last_direction = NORTH

                        elif event.key == K_DOWN or event.key == K_s:
                            mother.direction = SOUTH
                            last_direction = SOUTH

                        elif event.key == K_RIGHT or event.key == K_d:
                            mother.direction = EAST
                            last_direction = EAST

                        elif event.key == K_LEFT or event.key == K_a:
                            mother.direction = WEST
                            last_direction = WEST

                        elif event.key == K_RETURN:
                            game_mode = PAUSE
                    
                if last_direction == NORTH:
                    mother.rect.y = mother.rect.y - 1

                elif last_direction == SOUTH:
                    mother.rect.y = mother.rect.y + 1

                elif last_direction == EAST:
                    mother.rect.x = mother.rect.x + 1

                elif last_direction == WEST:
                    mother.rect.x = mother.rect.x - 1


                # time delay to control speed of game
                time.sleep(0.01)       

                # idea to use modulous for animation was taken from Invasion of The Blobs (course content)
                # controls speed of animation
                if animation%20 == 0:
                    for mom in mother_group:            
                        mom.image = load_image(photo_album[mom.name+"_"+mom.colour][mom.direction][0])
                    for tail in tail_group:            
                        tail.image = load_image(photo_album[tail.name+"_"+tail.colour][tail.direction][0])
                    
                if animation%20 == 10:
                    for mom in mother_group:            
                        mom.image = load_image(photo_album[mom.name+"_"+mom.colour][mom.direction][1])
                    for tail in tail_group:            
                        tail.image = load_image(photo_album[tail.name+"_"+tail.colour][tail.direction][1])

                animation = animation + 1

                # drawing background
                screen.blit(background, (0,0))
                obstacles_group.draw(screen)
                tunnel_bottom_group.draw(screen)
                update_score(screen, myfont, score)

                # drawing foreground
                mother_group.draw(screen)
                kitten_group.draw(screen)
                tail_group.draw(screen)
                tunnel_top_group.draw(screen)
                pygame.display.update()

            # pauses the game
            while game_mode == PAUSE:

                # method for interpreting accelerometer input
                # disabled for keyboard version
                '''
                hardware_data = actionData(MENU)

                if hardware_data[2] == K_RETURN:
                    game_mode = GAME
                '''

                # method for keylistening taken from Invasion of the Blobs (course content)
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            game_mode = GAME

                time.sleep(0.25)  


        # in game over mode, print game over, display score and clear object groups
        while game_mode == OVER:
            red_background = load_image(photo_album["board_red"][0])
            screen.blit(red_background, (0,0))
            game_over = load_image(photo_album["game_over"][0])
            screen.blit(game_over, (112,96))
            score_label = myfont.render("Score: " + str(score), False, (255, 255, 255))
            screen.blit(score_label, (272, 480))
            pygame.display.update()
            time.sleep(2.5)
            mother_group.empty()
            kitten_group.empty()
            tail_group.empty()
            tunnel_top_group.empty()
            tunnel_bottom_group.empty()
            obstacles_group.empty()
            game_mode = MENU


    pygame.quit()
    return


#accel.openBus()
main()
#accel.closeBus()

