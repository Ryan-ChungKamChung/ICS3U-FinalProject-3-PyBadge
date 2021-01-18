#!/usr/bin/env python3

# Created by Ryan Chung Kam Chung
# Created in January 2021
# Adding shooting and sound


# Libraries that will enable us to render and stage assets
import ugame
import stage

# Constants file
import constants


def game_scene():
    # this function is the main game scene

    # -------------------------------- Assets ----------------------------------
    # Image banks
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")
    
    # ------------------------------ Background --------------------------------
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

    # --------------------------------- Sound -----------------------------------
    # Shooting sound
    pew_sound = open("pew.wav", 'rb')
    
    # Sound setup
    sound = ugame.audio
    # Stop all sound
    sound.stop()
    # Unmute
    sound.mute(False)
    
    # ------------------------------ Button States ------------------------------
    
    # Buttons with state information
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]
    
    # ----------------------------- Sprites creation -----------------------------
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

    # ----------------------------- Stage and render ------------------------------
    # Creates a stage for the background
    # Sets frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)

    # Sets sprite layers and show up in order
    game.layers = bullets + [ship] + [background]

    # Renders all sprites
    # Usually you should render background once per scene
    game.render_block()

    # --------------------------------- Game Loop ----------------------------------
    while True:

    # --------------------------------- User input ---------------------------------
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

    # ----------------------------- Bullet movement ------------------------------
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
            if bullets[bullet_number].x > ship.x + constants.SPRITE_SIZE:
                bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                            constants.OFF_SCREEN_Y)
            # Right
            if bullets[bullet_number].x < ship.x - constants.SPRITE_SIZE:
                bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                            constants.OFF_SCREEN_Y)

            if bullets[bullet_number].y > ship.y + constants.SPRITE_SIZE:
                bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                            constants.OFF_SCREEN_Y)

            if bullets[bullet_number].y < ship.y - constants.SPRITE_SIZE:
                bullets[bullet_number].move(constants.OFF_SCREEN_X,
                                            constants.OFF_SCREEN_Y)

    # ----------------------------- Render and redraw ------------------------------
        # Renders and redraws the ship
        game.render_sprites(bullets + [ship])
        # Waits until refresh rate finishes
        game.tick()


# Makes this file run as the main file of the program, and runs game_scene()
if __name__ == "__main__":
    game_scene()
