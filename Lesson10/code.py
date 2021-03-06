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


def game_scene():
    # this function is the main game scene

    # SCORE
    score = 0

    score_text = stage.Text(width=29, height=14)
    score_text.clear()
    score_text.cursor(0, 0)
    score_text.move(0, 1)
    score_text.text("Score: {0}".format(score))

    # FUNCTION DEFINITION

    def show_alien():
        random_x = random.randint(2 * constants.SPRITE_SIZE,
                                  constants.SCREEN_X
                                  - 2 * constants.SPRITE_SIZE)

        random_y = random.randint(2 * constants.SPRITE_SIZE,
                                      constants.SCREEN_Y
                                  - 2 * constants.SPRITE_SIZE)

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

    # List of bullets
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
    difficulty_value = 1

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

        # USER MOVEMENT
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
                    # sound.play(pew_sound)
                    break

        # SET DIFFICULTY
        alien_speed = difficulty / 10
        if score < 10:
            alien_speed = 0.3
        if score % 10 == 0:
            difficulty += 0.05

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

            if bullets[bullet_number].y > ship.y + 2 * constants.SPRITE_SIZE:
                bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                            constants.OFF_SCREEN_Y)

            if bullets[bullet_number].y < ship.y - 2 * constants.SPRITE_SIZE:
                bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                            constants.OFF_SCREEN_Y)

        # ALIEN MOVEMENT
        # Alien movement towards character
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
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
                            show_alien()
                            show_alien()
                            score = score + 1
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
                        # alien hit the ship
                        sound.stop()
                        # sound.play(crash_sound)
                        time.sleep(3.0)
                        game_over_scene(score)       

        # RENDER AND REDRAW
        # Renders and redraws the ship
        game.render_sprites(aliens + bullets + [ship])
        # Waits until refresh rate finishes
        game.tick()


def game_over_scene(final_score):
    # this function is the game over scene

    # SOUND
    # turn off sound from last scene
    sound = ugame.audio
    sound.stop()

    # IMAGE BANKS
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # BACKGROUND
    # sets the background to image 0 in the image Bank
    background = stage.Grid(image_bank_2, constants.SCREEN_GRID_X,
                            constants.SCREEN_GRID_Y)

    # TEXT
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

    # STAGE AND RENDER
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    # LOGIC LOOP
    while True:
        # USER INPUT
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_START != 0:
            # Reloads game
            supervisor.reload()

        # Update game logic
        # Waits until refresh rate finishes
        game.tick()


# Makes this file run as the main file of the program, and runs game_scene()
if __name__ == "__main__":
    game_scene()
