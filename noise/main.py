import pygame
import time
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import os

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
YELLANGE = (255, 192, 0)
ORANGE = (255, 128, 0)
BLUE = (0, 0, 225)
LIGHT_BLUE = (135, 208, 250)
RED = (255, 0, 0)
DARK_RED = (128, 0, 0)
GREEN = (64, 255, 64)
LIGHT_GREEN = (128, 255, 128)
BLACK = (0, 0, 0)
BROWN = (96, 38, 0)
GREY = (128, 128, 128)

FULL_WINDOW = 1920, 1080
FPS = 60
MAP_SIZE = 100, 100
TILE_SIZE = 10

pygame.init()
sc = pygame.display.set_mode(FULL_WINDOW)
clock = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 30)

mainsc = pygame.Surface((MAP_SIZE[0]*TILE_SIZE, MAP_SIZE[1]*TILE_SIZE))
camera_pos = 0, 0
textures = {i.split('.png')[0]: pygame.transform.scale(pygame.image.load(f'tiles\\{i}').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in os.listdir('tiles') if i.endswith('.png')}
noise = [[]]


def perlin_gen():
    noise1 = PerlinNoise(octaves=3)
    noise2 = PerlinNoise(octaves=6)
    noise3 = PerlinNoise(octaves=12)
    noise4 = PerlinNoise(octaves=24)

    xpix, ypix = MAP_SIZE
    pic = []
    for i in range(ypix):
        row = []
        for j in range(xpix):
            noise_val = noise1([i / xpix, j / ypix])
            noise_val += 0.5 * noise2([i / xpix, j / ypix])
            noise_val += 0.25 * noise3([i / xpix, j / ypix])
            noise_val += 0.125 * noise4([i / xpix, j / ypix])
            row.append(noise_val)
        pic.append(row)

    return pic


def new_sc():
    global noise
    noise = perlin_gen()
    rivers = perlin_gen()
    for i in range(MAP_SIZE[1]):
        for j in range(MAP_SIZE[0]):
            if noise[i][j] < -0.2:
                mainsc.blit(textures['dgrass'], (j * TILE_SIZE, i * TILE_SIZE))
            elif noise[i][j] < -0.05:
                mainsc.blit(textures['grass'], (j*TILE_SIZE, i*TILE_SIZE))
            elif noise[i][j] < 0:
                mainsc.blit(textures['sand'], (j*TILE_SIZE, i*TILE_SIZE))
            elif noise[i][j] > 0.3:
                mainsc.blit(textures['deepwater'], (j*TILE_SIZE, i*TILE_SIZE))
            elif noise[i][j] > 0.2:
                mainsc.blit(textures['deepwater2'], (j*TILE_SIZE, i*TILE_SIZE))
            else:
                mainsc.blit(textures['water2'], (j*TILE_SIZE, i*TILE_SIZE))
            if 0 < rivers[i][j] < 0.1 and noise[i][j] < 0:
                mainsc.blit(textures['water3'], (j * TILE_SIZE, i * TILE_SIZE))



new_sc()


while True:
    sc.fill(WHITE)
    pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_f:
                new_sc()
            if event.key == pygame.K_g:
                plt.imshow(noise, cmap='gray')
                plt.show()
        if event.type == pygame.MOUSEMOTION:
            if pressed[0]:
                camera_pos = camera_pos[0]+event.rel[0], camera_pos[1]+event.rel[1]

    sc.blit(mainsc, camera_pos)
    sc.blit(font.render(str(pos), True, BLACK), (FULL_WINDOW[0] - 200, 10))
    sc.blit(font.render(str(int(clock.get_fps())), True, BLACK), (FULL_WINDOW[0] - 50, 10))
    pygame.display.flip()
    clock.tick(FPS)



