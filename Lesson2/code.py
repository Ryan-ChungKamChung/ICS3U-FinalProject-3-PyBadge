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

    # Creates a stage for the background
    # Sets frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)

    # Sets sprite layers and show up in order
    game.layers = [background_1] + [background_2]

    # Renders all sprites
    # Usually you should render background once per scene
    game.render_block()

    # Placeholder for now to extend the scene time
    while True:
        pass

# Makes this file run as the main file of the program, and runs game_scene()
if __name__ == "__main__":
    game_scene()
