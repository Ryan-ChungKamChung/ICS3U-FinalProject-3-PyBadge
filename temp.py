        numbers_x = list(range(ship.x - 3 * constants.SPRITE_SIZE,
                               ship.x, ship.x + 3 * constants.SPRITE_SIZE))
        numbers_y = list(range(ship.y - 3 * constants.SPRITE_SIZE,
                               ship.y, ship.y + 3 * constants.SPRITE_SIZE))
        random_x = random.choice([element for elementin range(-1 * constants.SPRITE_SIZE
                                                              constants.SCREEN_X
                                                              + constants.SPRITE_SIZE) if element != numbers_x])
        random_y = random.choice([element for element in range(-1 * constants.SPRITE_SIZE,
                                                               constants.SCREEN_Y
                                                               + constants.SPRITE_SIZE) if element != numbers_y])

        for alien_number in range(len(aliens)):
            if aliens[alien_number].x < -1 * constants.SPRITE_SIZE:
                aliens[alien_number].move(random_x, random_y)
                break
