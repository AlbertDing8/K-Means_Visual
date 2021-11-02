import pygame
import os
import random
import math

pygame.init()
pygame.display.init()

# Constants
MULTIPLIER = 2.0
WIDTH, HEIGHT = 120 * MULTIPLIER, 120 * MULTIPLIER
UNIT = 6 * MULTIPLIER
FPS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("K-Means")

red_mean = pygame.transform.scale2x(pygame.image.load(os.path.join('PNG', 'Red_Mean.png')))
green_mean = pygame.transform.scale2x(pygame.image.load(os.path.join('PNG', 'Green_Mean.png')))
blue_mean = pygame.transform.scale2x(pygame.image.load(os.path.join('PNG', 'Blue_Mean.png')))

red_point = pygame.transform.scale2x(pygame.image.load(os.path.join('PNG', 'Red_Data.png')))
green_point = pygame.transform.scale2x(pygame.image.load(os.path.join('PNG', 'Green_Data.png')))
blue_point = pygame.transform.scale2x(pygame.image.load(os.path.join('PNG', 'Blue_Data.png')))

pygame.mixer.music.load('Main Theme.wav')
pygame.mixer.music.set_volume(0.25)

GAME_QUIT = pygame.USEREVENT + 1


# Mean and Point Classes
class Mean:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = red_mean


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = 'red'
        self.image = red_point


# Initialized points and mean placement
def game_init(m, p):
    # Mean random placements
    for mm in m:
        mm.x = random.randint(0, int(WIDTH))
        mm.y = random.randint(0, int(HEIGHT))

    # Point generation
    i = random.randint(1, 3)
    if i == 1:
        # Fun pattern
        p[0].x = 30 * MULTIPLIER
        p[0].y = 30 * MULTIPLIER

        p[1].x = 30 * MULTIPLIER
        p[1].y = 40 * MULTIPLIER

        p[2].x = 30 * MULTIPLIER
        p[2].y = 50 * MULTIPLIER

        p[3].x = 90 * MULTIPLIER
        p[3].y = 30 * MULTIPLIER

        p[4].x = 90 * MULTIPLIER
        p[4].y = 40 * MULTIPLIER

        p[5].x = 90 * MULTIPLIER
        p[5].y = 50 * MULTIPLIER

        p[6].x = 40 * MULTIPLIER
        p[6].y = 80 * MULTIPLIER

        p[7].x = 80 * MULTIPLIER
        p[7].y = 80 * MULTIPLIER

        p[8].x = 55 * MULTIPLIER
        p[8].y = 100 * MULTIPLIER

        p[9].x = 65 * MULTIPLIER
        p[9].y = 100 * MULTIPLIER
    else:
        # All random
        for pp in p:
            pp.x = random.randint(0, int(WIDTH))
            pp.y = random.randint(0, int(HEIGHT))


# Display Game
def game(m, p):
    screen.fill((255, 255, 204))

    for mm in m:
        screen.blit(mm.image, (mm.x, mm.y))

    for pp in p:
        screen.blit(pp.image, (pp.x, pp.y))

    pygame.display.update()


# Updates colors of points and
def update_k(m, p):
    # Update colors of points
    for pp in p:
        if (math.sqrt((pp.x - m[0].x)**2 + (pp.y - m[0].y)**2) < math.sqrt((pp.x - m[1].x)**2 + (pp.y - m[1].y)**2))\
                and (math.sqrt((pp.x - m[0].x)**2 + (pp.y - m[0].y)**2)
                     < math.sqrt((pp.x - m[2].x)**2 + (pp.y - m[2].y)**2)):
            pp.color = 'red'
            pp.image = red_point
        elif (math.sqrt((pp.x - m[1].x)**2 + (pp.y - m[1].y)**2) < math.sqrt((pp.x - m[0].x)**2 + (pp.y - m[0].y)**2))\
                and (math.sqrt((pp.x - m[1].x)**2 + (pp.y - m[1].y)**2)
                     < math.sqrt((pp.x - m[2].x)**2 + (pp.y - m[2].y)**2)):
            pp.color = 'green'
            pp.image = green_point
        else:
            pp.color = 'blue'
            pp.image = blue_point

    # Update means
    x, y, counter, end = 0, 0, 0, 0
    for i in range(len(m)):
        for pp in p:
            if i == 0 and pp.color == 'red':
                x += pp.x
                y += pp.y
                counter += 1
            elif i == 1 and pp.color == 'green':
                x += pp.x
                y += pp.y
                counter += 1
            elif i == 2 and pp.color == 'blue':
                x += pp.x
                y += pp.y
                counter += 1

        if counter != 0:
            new_x = x // counter
            new_y = y // counter

            if new_x == m[i].x:
                end += 1
            else:
                m[i].x = new_x
            if new_y == m[i].y:
                end += 1
            else:
                m[i].y = new_y
        else:
            end += 2

        x, y, counter = 0, 0, 0

    if end == 6:
        pygame.event.post(pygame.event.Event(GAME_QUIT))


# Main
def main():
    pygame.mixer.music.play(-1)

    # Generate Map
    means = [Mean(), Mean(), Mean()]
    means[1].image = green_mean
    means[2].image = blue_mean

    points = [Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point(), Point()]
    game_init(means, points)

    # define a variable to control the main loop
    running = True

    # Creating clock class
    clock = pygame.time.Clock()

    # main loop
    while running:
        # Prevents obscene amounts of game window refreshing
        clock.tick(FPS)

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT or event.type == GAME_QUIT:
                # exit game
                running = False

        # compute new colors and positions
        update_k(means, points)

        game(means, points)

        pygame.time.delay(1000)

    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
