import random
import re
import pygame

pygame.init()
blue = (56, 110, 156)

def check_colour(rgb):
    if rgb[0] > 156:
        rgb[0] = 156
    if rgb[1] > 210:
        rgb[1] = 210
    if rgb[2] > 255:
        rgb[2] = 255
    """
    for i in range(0, 3):
        if rgb[i] < 0:
            rgb[i] = 0
        elif rgb[i] > 250:
            if i == 0 or i == 1:
                rgb[i] = 105
            else:
                rgb[i] = 255
    """
    return rgb

font = pygame.font.SysFont(None, 30)


def message_to_screen(msg, color, x, y):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x, y])


def display_high_scores():
    gameDisplay.fill(white)
    file = open('jnake_scores.txt', 'r')
    contents = file.read()
    contents = contents.split('\n')
    file.close()
    message_to_screen('High Scores', blue, display_width//3, display_height//3)
    height = display_height//3 + 40
    for line in contents:
        message_to_screen(line, blue, display_width//3, height)
        height += 30


def update_scores(name, score):
    file = open('jnake_scores.txt', 'r')
    contents = file.read()
    contents = contents.split('\n')
    contents = contents[:-1]

    scoreboard = []
    for line in contents:
        line = line.split()
        scoreboard += [[line[0], line[1], int(line[2])]]
    scoreboard += [[None, name, score]]
    scoreboard = sorted(scoreboard, key=lambda x: x[2])
    scoreboard.reverse()

    file = open('jnake_scores.txt', 'w')
    place = 1
    for i in scoreboard[0:5]:
        file.write("{}. {} {}\n".format(place, i[1], i[2]))
        place += 1
    file.close()
    file = open('jnake_scores.txt', 'r')
    new_contents = file.read()
    print("-"*10
          + "\n"
          + new_contents
          + "-"*10
          + "\n"
    )
    file.close()



display_width = 800
display_height = 600
block_size = 10
FPS = 15

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake')

blue = (56, 110, 156)
white = (255, 255, 255)
yellow = (255, 207, 63)
red = (255, 0, 0)
magenta = (211, 2, 132)


def gameLoop():
    gameExit = False
    gameOver = False
    type_high_score = False
    clock = pygame.time.Clock()
    move = False
    direction = None
    score = 0
    name = ''

    lead_x = display_width // 2
    lead_y = display_height // 2
    lead_x_change = 0
    lead_y_change = 0
    snake_length = 5
    prev = []
    fruit_x = random.randint(0, display_width - block_size)
    fruit_y = random.randint(0, display_height - block_size)
    big_fruit_size = 3
    big_fruit_x = random.randint(0, display_width - block_size * big_fruit_size)
    big_fruit_y = random.randint(0, display_height - block_size * big_fruit_size)
    big_fruit_constant = 30
    big_fruit_time = big_fruit_constant
    eaten = []
    dissipate_time = 20;

    while not gameExit:
        while gameOver:
            display_high_scores()
            if name == '':
                valid = False
                while not valid:
                    name = input('Enter name: ')
                    if not re.match("^[a-z]*$", name):
                        print("Error! Only letters a-z allowed! Please enter name again!")
                    else:
                        break
                update_scores(name, score)
            display_high_scores()
            """message_to_screen('Q to quit, C to continue', red, display_width/3, display_height/2)"""
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return None
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if direction != 'right':
                        lead_x_change = -1 * block_size
                        lead_y_change = 0
                        move = True
                        direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    if direction != 'left':
                        lead_x_change = block_size
                        lead_y_change = 0
                        move = True
                        direction = 'right'
                elif event.key == pygame.K_UP:
                    if direction != 'down':
                        lead_y_change = -1 * block_size
                        lead_x_change = 0
                        move = True
                        direction = 'up'
                elif event.key == pygame.K_DOWN:
                    if direction != 'up':
                        lead_y_change = block_size
                        lead_x_change = 0
                        move = True
                        direction = 'down'
                elif event.key == pygame.K_u:
                    snake_length += 1

        gameDisplay.fill(white)

        #display score
        message_to_screen(str(score), blue, display_width - 50, 10)

        #update direction
        lead_x += lead_x_change
        lead_y += lead_y_change

        #draw lead block
        pygame.draw.rect(gameDisplay, blue, [lead_x, lead_y, block_size, block_size])

        #draw fruit
        pygame.draw.rect(gameDisplay, yellow, [fruit_x, fruit_y, block_size, block_size])

        #draw big fruit
        if big_fruit_time > 0:
            pygame.draw.rect(gameDisplay, magenta, [big_fruit_x, big_fruit_y, block_size * big_fruit_size, block_size * big_fruit_size])
            big_fruit_time -= 1
        else:
            big_fruit_x = random.randint(0, display_width - block_size)
            big_fruit_y = random.randint(0, display_height - block_size)
            big_fruit_time = big_fruit_constant
            pygame.draw.rect(gameDisplay, magenta, [big_fruit_x, big_fruit_y, block_size * big_fruit_size, block_size * big_fruit_size])

            #draw tail and check hit
        for block in prev:
            if block[0] > 0:
                colour = blue
                r = colour[0]+(snake_length*10//block[0])
                g = colour[1]+(snake_length*10//block[0])
                b = colour[2]+(snake_length*10//block[0])
                colour = check_colour([r, g, b])
                pygame.draw.rect(gameDisplay, (colour[0], colour[1], colour[2]), [block[1], block[2], block[3], block[4]])
                block[0] -= 1
            if move:
                if (lead_x, lead_y) == (block[1], block[2]):
                    gameOver = True

        #check eat
        for x in range(lead_x, lead_x + block_size):
            for y in range(lead_y, lead_y + block_size):
                for fx in range(fruit_x, fruit_x + block_size):
                    for fy in range(fruit_y, fruit_y + block_size):
                        if (x, y) == (fx, fy):
                            snake_length += 5
                            score += 5
                            fruit_x = random.randint(0, display_width - block_size)
                            fruit_y = random.randint(0, display_height - block_size)
                            eaten += [[fruit_x, fruit_y, dissipate_time]]
                for fx in range(big_fruit_x, big_fruit_x + block_size * big_fruit_size):
                    for fy in range(big_fruit_y, big_fruit_y + block_size * big_fruit_size):
                        if (x, y) == (fx, fy):
                            snake_length += 10
                            score += 20
                            big_fruit_time = big_fruit_constant
                            big_fruit_x = random.randint(0, display_width - block_size * big_fruit_size)
                            big_fruit_y = random.randint(0, display_height - block_size * big_fruit_size)
                            eaten += [[fruit_x, fruit_y, dissipate_time]]

        #draw dissipation
        """for fruit in eaten:
            if fruit[]"""

        #add to tail
        prev += [[snake_length, lead_x, lead_y, block_size, block_size]]
        prev = [block for block in prev if block[0] > 0]

        #check boundary
        if lead_x < 0:
            lead_x = display_width - block_size
        elif lead_x >= display_width:
            lead_x = 0
        elif lead_y < 0:
            lead_y = display_height - block_size
        elif lead_y >= display_height:
            lead_y = 0

        pygame.display.update()
        clock.tick(FPS)

gameLoop()

pygame.quit()
quit()
