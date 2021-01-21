#!/usr/bin/env python3

# Created by Ryan Chung Kam Chung
# Created in January 2021
# Adding shooting and sound


# Libraries that will enable us to render and stage assets
import ugame
import stage
import random
import supervisor
import time

# Constants file
import constants


def splash_scene():
    # this function is the splash scene

    # get sound ready
    coin_sound = open("coin.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    # image bank
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # sets bg to image 0 in the image bank
    background = stage.Grid(image_bank_mt_background,
                            constants.SCREEN_X, constants.SCREEN_Y)

    # used this program to split the image into tile:
    #   https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png
    background.tile(2, 2, 0)  # blank white
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)
    background.tile(7, 2, 0)  # blank white

    background.tile(2, 3, 0)  # blank white
    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)
    background.tile(7, 3, 0)  # blank white

    background.tile(2, 4, 0)  # blank white
    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)
    background.tile(7, 4, 0)  # blank white

    background.tile(2, 5, 0)  # blank white
    background.tile(3, 5, 0)
    background.tile(4, 5, 13)
    background.tile(5, 5, 14)
    background.tile(6, 5, 0)
    background.tile(7, 5, 0)  # blank white

    # creates stage and sets it to 60fps
    game = stage.Stage(ugame.display, constants.FPS)

    # sets the layers of all sprites, in order
    game.layers = [background]

    # renders all sprites, only once
    game.render_block()

    while True:
        time.sleep(2.0)
        menu_scene()


def menu_scene():
    # this function is the menu scene
    
    # image bank
    image_bank_mt_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    
    # add text objects
    text = []
    text1 = stage.Text(width=29, height=12, font=None, palette=constants.NEW_PALETTE, 
                       buffer=None)
    text1.move(20, 10)
    text1.text("MT Game Studios")
    text.append(text1)
    
    text2 = stage.Text(width=29, height=12, font=None, palette=constants.NEW_PALETTE,
                       buffer=None)
    text2.move(40,110)
    text2.text("PRESS START")
    text.append(text2)
    
    # sets bg to image 0 in the image bank
    background = stage.Grid(image_bank_mt_background,
                            constants.SCREEN_X, constants.SCREEN_Y)
    
    # creates stage and sets it to 60fps
    game = stage.Stage(ugame.display, constants.FPS)

    # sets the layers of all sprites, in order
    game.layers = text + [background]

    # renders all sprites, only once
    game.render_block()
    
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        
        # select start button
        if keys & ugame.K_START != 0:
            game_scene()
        
        # update game logic
        game.tick()


def game_scene():
    # Main game scene

    # SCORE
    score = 0

    score_text = stage.Text(width=29, height=14)
    score_text.clear()
    score_text.cursor(0, 0)
    score_text.move(0, 1)
    score_text.text("Score: {0}".format(score))

    # FUNCTION DEFINITION
    def show_alien():
        numbers_x = list(range(ship.x - 3 * constants.SPRITE_SIZE,
                               ship.x, ship.x + 3 * constants.SPRITE_SIZE))
        numbers_y = list(range(ship.y - 3 * constants.SPRITE_SIZE,
                               ship.y, ship.y + 3 * constants.SPRITE_SIZE))
        random_x = random.choice([element for element in range(-1 * constants.SPRITE_SIZE,
                                                              constants.SCREEN_X
                                                              + constants.SPRITE_SIZE) if element != numbers_x])
        random_y = random.choice([element for element in range(-1 * constants.SPRITE_SIZE,
                                                               constants.SCREEN_Y
                                                               + constants.SPRITE_SIZE) if element != numbers_y])

        for alien_number in range(len(aliens)):
            aliens[alien_number].move(random_x, random_y)
            break

    # IMAGE BANKS
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # BACKGROUND
    # Sets background to the 0th image in the image bank
    # 10x8 grid
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X,
                              constants.SCREEN_GRID_Y)

    # Sets the floor as the 1st image in the image bank, the walls are still going
    # to be the 0th image
    for x_location in range(1, constants.SCREEN_GRID_X - 1):
        for y_location in range(1, constants.SCREEN_GRID_Y - 1):
            tile_picked = 1
            background.tile(x_location, y_location, tile_picked)

    #SOUND SETUP
    # Shooting sound
    pew_sound = open("pew.wav", 'rb')
    # Lasers hitting aliens
    crash_sound = open("crash.wav", 'rb')
    # Aliens hitting ship
    boom_sound = open("boom.wav", 'rb')

    # Sound setup
    sound = ugame.audio
    # Stop all sound
    sound.stop()
    # Unmute
    sound.mute(True)

    # BUTTON STATES
    # Buttons with state information
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # SPRITES CREATION
    # Ship sprite being displayed
    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)

    bullets = []
    bullet_direction = []
    for bullets_number in range(constants.TOTAL_NUMBER_OF_BULLETS):
        a_single_bullet = stage.Sprite(image_bank_sprites, 10,
                                     constants.OFF_SCREEN_X,
                                     constants.OFF_SCREEN_Y)
        bullets.append(a_single_bullet)
        # Sets bullet direction
        bullet_direction.append("")
        direction = "Up"

    aliens = []
    for alien_number in range(constants.TOTAL_NUMBER_OF_ALIENS):
        a_single_alien = stage.Sprite(image_bank_sprites, 9,
                                      constants.OFF_SCREEN_X,
                                      constants.OFF_SCREEN_Y)
        aliens.append(a_single_alien)

    show_alien()

    # DIFFICULTY
    difficulty = 1

    # STAGE AND RENDER
    # Creates a stage for the background
    # Sets frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)

    # Sets sprite layers and show up in order
    game.layers = [score_text] + bullets + [ship] + aliens + [background]

    # Renders all sprites
    # Usually you should render background once per scene
    game.render_block()

    # GAME LOOP
    while True:

        # USER MOVEMENT + SHOOTING
        keys = ugame.buttons.get_pressed()

        # Button states to fire
        if keys & ugame.K_X != 0:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]
        if keys & ugame.K_RIGHT:
            # Move right with constraints of the right border
            if ship.x <= constants.SCREEN_X - 2 * constants.SPRITE_SIZE:
                ship.move(ship.x + constants.SPRITE_MOVEMENT_SPEED, ship.y)
            else:
                ship.move(constants.SCREEN_X - 2 * constants.SPRITE_SIZE, ship.y)
            direction = "Right"
        if keys & ugame.K_LEFT:
            # Move left with constraints of the left border
            if ship.x >= constants.SCREEN_X - 9 * constants.SPRITE_SIZE:
                ship.move(ship.x - constants.SPRITE_MOVEMENT_SPEED, ship.y)
            else:
                ship.move(constants.SPRITE_SIZE, ship.y)
            direction = "Left"
        if keys & ugame.K_UP:
            # Moves down with constraints of the ceiling
            if ship.y >= constants.SPRITE_SIZE:
                ship.move(ship.x, ship.y - constants.SPRITE_MOVEMENT_SPEED)
            else:
                ship.move(ship.x, constants.SPRITE_SIZE)
            direction = "Up"
        if keys & ugame.K_DOWN:
            # Moves down with constraints of the ground
            if ship.y <= constants.SCREEN_Y - 2 * constants.SPRITE_SIZE:
                ship.move(ship.x, ship.y + constants.SPRITE_MOVEMENT_SPEED)
            else:
                ship.move(ship.x, constants.SCREEN_Y - 2 * constants.SPRITE_SIZE)
            direction = "Down"

        # Shoot with sound
        if a_button == constants.button_state["button_just_pressed"]:
            for bullet_number in range(len(bullets)):
                if bullets[bullet_number].x < 0:
                    bullets[bullet_number].move(ship.x, ship.y)
                    bullet_direction[bullet_number] = direction
                    sound.play(pew_sound)
                    break

        # SET DIFFICULTY
        alien_speed = difficulty / 10
        if score % 10 == 0:
            difficulty += 0.025

        # BULLET MOVEMENT
        # When bullets get shot, check if they are off the screen.
        for bullet_number in range(len(bullets)):
            if bullets[bullet_number].x > -1 * constants.SPRITE_SIZE:
                if bullet_direction[bullet_number] == "Up": 
                    bullets[bullet_number].move(bullets[bullet_number].x,
                                                bullets[bullet_number].y
                                                - constants.BULLET_SPEED)
                if bullet_direction[bullet_number] == "Down":
                    bullets[bullet_number].move(bullets[bullet_number].x,
                                                bullets[bullet_number].y
                                                + constants.BULLET_SPEED)
                if bullet_direction[bullet_number] == "Left":
                    bullets[bullet_number].move(bullets[bullet_number].x
                                                - constants.BULLET_SPEED,
                                                bullets[bullet_number].y)
                if bullet_direction[bullet_number] == "Right":
                    bullets[bullet_number].move(bullets[bullet_number].x
                                                + constants.BULLET_SPEED,
                                                bullets[bullet_number].y)

            # Move back bullets to "staging" if they are too far from the ship
            # Right
            if bullets[bullet_number].x > ship.x + 2 * constants.SPRITE_SIZE:
                bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                            constants.OFF_SCREEN_Y)
            # Right
            if bullets[bullet_number].x < ship.x - 2 * constants.SPRITE_SIZE:
                bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                            constants.OFF_SCREEN_Y)
            # Down
            if bullets[bullet_number].y > ship.y + 2 * constants.SPRITE_SIZE:
                bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                            constants.OFF_SCREEN_Y)
            # Up
            if bullets[bullet_number].y < ship.y - 2 * constants.SPRITE_SIZE:
                bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                            constants.OFF_SCREEN_Y)

        # ALIEN MOVEMENT
        # Alien movement towards character
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > -1 * constants.SPRITE_SIZE:
                # Right of ship (horizontal)
                if aliens[alien_number].x > ship.x:
                    aliens[alien_number].move(aliens[alien_number].x
                                              - alien_speed,
                                              aliens[alien_number].y)
                # Left of ship (horizontal)
                if aliens[alien_number].x < ship.x:
                    aliens[alien_number].move(aliens[alien_number].x
                                              + alien_speed,
                                              aliens[alien_number].y)
                # Under ship (vertical)
                if aliens[alien_number].y > ship.y:
                    aliens[alien_number].move(aliens[alien_number].x,
                                              aliens[alien_number].y
                                              - alien_speed)
                # Over ship (vertical)
                if aliens[alien_number].y < ship.y:
                    aliens[alien_number].move(aliens[alien_number].x,
                                              aliens[alien_number].y
                                              + alien_speed)
                # Stay if the same
                if aliens[alien_number].x == ship.x:
                    aliens[alien_number].move(aliens[alien_number].x,
                                              aliens[alien_number].y)
                # Stay if the same
                if aliens[alien_number].y == ship.y:
                    aliens[alien_number].move(aliens[alien_number].x,
                                              aliens[alien_number].y)

        # HIT COLLISION
        # Bullets hitting aliens
        for bullet_number in range(len(bullets)):
            if bullets[bullet_number].x > 0:
                for alien_number in range(len(aliens)):
                    if aliens[alien_number].x > 0:
                        if stage.collide(bullets[bullet_number].x + 6,
                                         bullets[bullet_number].y + 2,
                                         bullets[bullet_number].x + 11,
                                         bullets[bullet_number].y + 12,
                                         aliens[alien_number].x + 1,
                                         aliens[alien_number].y,
                                         aliens[alien_number].x + 15,
                                         aliens[alien_number].y + 15):
                            aliens[alien_number].move(constants.OFF_SCREEN_X,
                                                      constants.OFF_SCREEN_Y)
                            bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                                      constants.OFF_SCREEN_Y)
                            sound.stop()
                            sound.play(boom_sound)
                            show_alien()
                            score += 1
                            score_text.clear()
                            score_text.cursor(0,0)
                            score_text.move(1,1)
                            score_text.text("Score: {0}".format(score))

        # Aliens hitting the ship
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                if stage.collide(aliens[alien_number].x + 1,
                                 aliens[alien_number].y,
                                 aliens[alien_number].x + 15,
                                 aliens[alien_number].y + 15,
                                 ship.x, ship.y,
                                 ship.x + 15, ship.y + 15):
                    sound.stop()
                    sound.play(crash_sound)
                    time.sleep(1.0)
                    game_over_scene(score)

        # RENDER AND REDRAW
        # Renders and redraws the ship
        game.render_sprites(aliens + bullets + [ship])
        # Waits until refresh rate finishes
        game.tick()


def game_over_scene(final_score):
    # this function is the game over scene

    # turn off sound from last scene
    sound = ugame.audio
    sound.stop()

    # image banks for CPython
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # sets the background to image 0 in the image Bank
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X,
                            constants.SCREEN_GRID_Y)

    # Text boxes
    text = []
    text1 = stage.Text(width=29, height=12, font=None,
                       palette=constants.NEW_PALETTE, buffer=None)
    text1.move(22, 20)
    text1.text("Final Score: {:0>2d}".format(final_score))
    text.append(text1)

    text2 = stage.Text(width=29, height=14, font=None,
                       palette=constants.NEW_PALETTE, buffer=None)
    text2.move(43, 60)
    text2.text("GAME OVER")
    text.append(text2)

    text3 = stage.Text(width=29, height=14, font=None,
                       palette=constants.NEW_PALETTE, buffer=None)
    text3.move(32, 110)
    text3.text("PRESS SELECT")
    text.append(text3)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    while True:
        # get user input
        keys = ugame.buttons.get_pressed()

        # Start button pressed
        if keys & ugame.K_START != 0:
            supervisor.reload()

        # update game logic
        game.tick()


# Makes this file run as the main file of the program, and runs menu_scene()
if __name__ == "__main__":
    splash_scene()
