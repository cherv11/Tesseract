import pygame
from unit import *

TILE_SIZE = 10
FPS = 60
ticks = 0

pygame.init()
sc = pygame.display.set_mode(FULL_WINDOW)
clock = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 30)
units = [Unit() for _ in range(100)]
food = [Food() for _ in range(50)]

while True:
    ticks += 1
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

    if pressed[0]:
        pass
    if keys[pygame.K_a]:
        pass

    if ticks % 5 == 0:
        food.append(Food())

    for i in units:
        i.find(food)
        i.move()
        i.live(units)

    for i in units:
        i.blit(sc)
    for i in food:
        i.blit(sc)

    sc.blit(font.render(str(pos), True, BLACK), (FULL_WINDOW[0] - 200, 10))
    sc.blit(font.render(str(int(clock.get_fps())), True, BLACK), (FULL_WINDOW[0] - 50, 10))

    sc.blit(font.render(str(round(sum([i.rad for i in units])/len(units), 2))+' avg rad', True, BLACK), (FULL_WINDOW[0]-170, FULL_WINDOW[1]-350))
    sc.blit(font.render(str(round(sum([i.life for i in units])/len(units), 2))+' avg hp', True, BLACK), (FULL_WINDOW[0]-170, FULL_WINDOW[1]-300))
    sc.blit(font.render(str(round(sum([i.size for i in units])/len(units), 2))+' avg size', True, BLACK), (FULL_WINDOW[0]-170, FULL_WINDOW[1]-250))
    sc.blit(font.render(str(round(sum([i.speed for i in units])/len(units), 2))+' avg spd', True, BLACK), (FULL_WINDOW[0]-170, FULL_WINDOW[1]-200))
    sc.blit(font.render(str(len(food))+' food', True, BLACK), (FULL_WINDOW[0]-170, FULL_WINDOW[1]-150))
    sc.blit(font.render(str(len(units))+' units', True, BLACK), (FULL_WINDOW[0]-170, FULL_WINDOW[1]-100))
    sc.blit(font.render(str(ticks), True, BLACK), (FULL_WINDOW[0]-170, FULL_WINDOW[1]-50))
    pygame.display.flip()
    clock.tick(FPS)



