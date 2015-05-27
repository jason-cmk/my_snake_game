import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Snake')

black = (0, 0, 0)
white = (255, 255, 255)

gameExit = False
clock = pygame.time.Clock()

lead_x = 300
lead_y = 300
lead_x_change = 0
lead_y_change = 0

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change = -5
                lead_y_change = 0
            if event.key == pygame.K_RIGHT:
                lead_x_change = 5
                lead_y_change = 0
            if event.key == pygame.K_UP:
                lead_y_change = -5
                lead_x_change = 0
            if event.key == pygame.K_DOWN:
                lead_y_change = 5
                lead_x_change = 0

    lead_x += lead_x_change
    lead_y += lead_y_change
    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, [lead_x, lead_y, 10, 10])
    pygame.display.update()

    clock.tick(30)
pygame.quit()
quit()