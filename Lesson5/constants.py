#!/usr/bin/env python3

# Created by Ryan Chung Kam Chung
# Created in January 2021
# Constants file for code.py


# Pybadge screen is 10x8 sprites (16x16)
SCREEN_GRID_X = 10
SCREEN_GRID_Y = 8
SPRITE_SIZE = 16

# Pybadge screen is 160x128 pixels
SCREEN_X = 160
SCREEN_Y = 128

# Frames per second that the game will run on
FPS = 60

# How fast the sprites move
SPRITE_MOVEMENT_SPEED = 1

# Button state
button_state = {
    "button_up": "up",
    "button_just_pressed": "just pressed",
    "button_still_pressed": "still pressed",
    "button_released": "released"
}

# Cap of bullets
TOTAL_NUMBER_OF_BULLETS = 5

# Bullet Speed
BULLET_SPEED = 2

# When a bullet goes back to "staging"
OFF_SCREEN_X = -100
OFF_SCREEN_Y = -100
OFF_TOP_SCREEN = -1 * SPRITE_SIZE
OFF_BOTTOM_SCREEN = SCREEN_Y + SPRITE_SIZE
