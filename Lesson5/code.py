#!/usr/bin/env python3

# Created by Ryan Chung Kam Chung
# Created in January 2021
# Setting background on the PyBadge


# Libraries that will enable us to render and stage assets
import ugame
import stage

# Constants file
import constants


def game_scene():
    # this function is the main game scene

    # Image bank holds all image assets used
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Buttons with state information
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # get sound ready
    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # Sets background to the 0th image in the image bank (will be changed after)
    # 10x7 images of 16x16 wide images (sky)
    background_1 = stage.Grid(image_bank_background, constants.SCREEN_GRID_X,
                              constants.SCREEN_GRID_Y - 1)

    # With for loops, it chooses every 16x16 image and converts it to the 2nd
    # image in the image bank, tile_picked
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y - 1):
            tile_picked = 2
            background_1.tile(x_location, y_location, tile_picked)

    # Sets background to the 0th image in the image bank
    # 10x8 images of 16x16 wide images (only bottom row will show), (ground)
    background_2 = stage.Grid(image_bank_background, constants.SCREEN_GRID_X,
                              constants.SCREEN_GRID_Y)

    # Ship sprite being displayed
    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)

    # List of lasers
    bullets = []
    for bullets_number in range(constants.TOTAL_NUMBER_OF_BULLETS):
        a_single_bullet = stage.Sprite(image_bank_sprites, 10,
                                     constants.OFF_SCREEN_X,
                                     constants.OFF_SCREEN_Y)
        bullets.append(a_single_bullet)


    # Creates a stage for the background
    # Sets frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)

    # Sets sprite layers and show up in order
    game.layers = bullets + [ship] + [background_1] + [background_2]

    # Renders all sprites
    # Usually you should render background once per scene
    game.render_block()

    while True:
        # Game loop

        # User input
        keys = ugame.buttons.get_pressed()

        # A button to fire
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
            if ship.x <= constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(ship.x + constants.SPRITE_MOVEMENT_SPEED, ship.y)
            else:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
        if keys & ugame.K_LEFT:
            # Move left with constraints of the left border
            if ship.x >= 0:
                ship.move(ship.x - constants.SPRITE_MOVEMENT_SPEED, ship.y)
            else:
                ship.move(0, ship.y)
        if keys & ugame.K_UP:
            # Moves down with constraints of the ceiling
            if ship.y >= 0:
                ship.move(ship.x, ship.y - constants.SPRITE_MOVEMENT_SPEED)
            else:
                ship.move(ship.x, 0)
        if keys & ugame.K_DOWN:
            # Moves down with constraints of the ground
            if ship.y <= constants.SCREEN_Y - 2 * constants.SPRITE_SIZE:
                ship.move(ship.x, ship.y + constants.SPRITE_MOVEMENT_SPEED)
            else:
                ship.move(ship.x, constants.SCREEN_Y - 2 * constants.SPRITE_SIZE)

        # Update Game Logic

        # Shoot with sound
        if a_button == constants.button_state["button_just_pressed"]:
            for bullet_number in range(len(bullets)):
                if bullets[bullet_number].x < 0:
                    bullets[bullet_number].move(ship.x, ship.y)
                    sound.play(pew_sound)
                    break

        # When bullets get shot, check if they are off the screen.
        for bullet_number in range(len(bullets)):
            if bullets[bullet_number].x > 0:
                bullets[bullet_number].move(bullets[bullet_number].x,
                                          bullets[bullet_number].y -
                                          constants.BULLET_SPEED)
                if bullets[bullet_number].y < constants.OFF_TOP_SCREEN:
                    bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)

        # Renders and redraws the ship
        game.render_sprites(bullets + [ship])
        # Waits until refresh rate finishes
        game.tick()


# Makes this file run as the main file of the program, and runs game_scene()
if __name__ == "__main__":
    game_scene()
