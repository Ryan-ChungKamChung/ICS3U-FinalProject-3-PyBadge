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

    # Ship sprite being displayed
    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)

    # Creates a stage for the background
    # Sets frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)

    # Sets sprite layers and show up in order
    game.layers = [ship] + [background]

    # Renders all sprites
    # Usually you should render background once per scene
    game.render_block()

    while True:
        # Game loop

        # User input
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_RIGHT:
            # Move right with constraints of the right border
            if ship.x <= constants.SCREEN_X - 2 * constants.SPRITE_SIZE:
                ship.move(ship.x + constants.SPRITE_MOVEMENT_SPEED, ship.y)
            else:
                ship.move(constants.SCREEN_X - 2 * constants.SPRITE_SIZE, ship.y)
        if keys & ugame.K_LEFT:
            # Move left with constraints of the left border
            if ship.x >= constants.SCREEN_X - 9 * constants.SPRITE_SIZE:
                ship.move(ship.x - constants.SPRITE_MOVEMENT_SPEED, ship.y)
            else:
                ship.move(constants.SPRITE_SIZE, ship.y)
        if keys & ugame.K_UP:
            # Moves down with constraints of the ceiling
            if ship.y >= constants.SPRITE_SIZE:
                ship.move(ship.x, ship.y - constants.SPRITE_MOVEMENT_SPEED)
            else:
                ship.move(ship.x, constants.SPRITE_SIZE)
        if keys & ugame.K_DOWN:
            # Moves down with constraints of the ground
            if ship.y <= constants.SCREEN_Y - 2 * constants.SPRITE_SIZE:
                ship.move(ship.x, ship.y + constants.SPRITE_MOVEMENT_SPEED)
            else:
                ship.move(ship.x, constants.SCREEN_Y - 2 * constants.SPRITE_SIZE)

        # Renders and redraws the ship
        game.render_sprites([ship])
        # Waits until refresh rate finishes
        game.tick()


# Makes this file run as the main file of the program, and runs game_scene()
if __name__ == "__main__":
    game_scene()
