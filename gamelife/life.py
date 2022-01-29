import numpy as np
import os
import pygame


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
DARK_GREY = (64, 64, 64)
RECT_COLOR = WHITE

FULL_WINDOW = 1920, 1080
FPS = 60
filename = 'tilemap'
TILE_SIZE = 10
MAP_SIZE = FULL_WINDOW[1]//TILE_SIZE, FULL_WINDOW[0]//TILE_SIZE
FRAMES_PER_TURN = 4

pygame.init()
sc = pygame.display.set_mode(FULL_WINDOW)
clock = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 30)
font24 = pygame.font.SysFont('calibri', 24)
bck = pygame.transform.scale(pygame.image.load('bck.png').convert_alpha(), FULL_WINDOW)
checks = ((0, 1), (-1, 0), (0, -1), (1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1))
grid = True
autogrid = True
interface = True
settings = False
play = None
playmap = None
lastplaymap = None
toggleoff = font.render('ВЫКЛ', True, RED)
toggleon = font.render('ВКЛ', True, GREEN)
tilemap = np.load(filename+'.npy') if filename+'.npy' in os.listdir('.') else np.zeros(MAP_SIZE, 'int')
if tilemap.shape != MAP_SIZE:
    MAP_SIZE = tilemap.shape
    TILE_SIZE = min([FULL_WINDOW[1]//MAP_SIZE[0], FULL_WINDOW[0]//MAP_SIZE[1]])


def check_neighbours(i, j):
    nbs = 0
    for ci, cj in checks:
        si, sj = i+ci, j+cj
        if not 0 <= si < MAP_SIZE[0] or not 0 <= sj < MAP_SIZE[1]:
            continue
        if lastplaymap[si][sj]:
            nbs += 1
    return nbs


def life_act():
    global lastplaymap
    lastplaymap = playmap.copy()
    for i in range(MAP_SIZE[0]):
        for j in range(MAP_SIZE[1]):
            if not lastplaymap[i][j]:
                if check_neighbours(i, j) == 4:
                    playmap[i][j] = 1
            elif not 1 <= check_neighbours(i, j) <= 8:
                playmap[i][j] = 0


while True:
    sc.fill(WHITE)
    pos = pygame.mouse.get_pos()
    tpos = pos[1]//TILE_SIZE, pos[0]//TILE_SIZE
    pressed = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_g:
                grid = not grid
            if event.key == pygame.K_b:
                autogrid = not autogrid
                if autogrid:
                    grid = play is None
            if event.key == pygame.K_h:
                interface = not interface
            if event.key == pygame.K_q:
                np.save(filename, tilemap)
            if event.key == pygame.K_v:
                settings = not settings
            if event.key == pygame.K_a:
                if FRAMES_PER_TURN > 1:
                    FRAMES_PER_TURN -= 1
            if event.key == pygame.K_z:
                if FRAMES_PER_TURN < 60:
                    FRAMES_PER_TURN += 1
            if event.key == pygame.K_e:
                if play is not None:
                    play = None
                    if autogrid:
                        grid = True
                else:
                    play = 0
                    playmap = tilemap.copy()
                    lastplaymap = playmap
                    if autogrid:
                        grid = False
            if event.key == pygame.K_p:
                tilemap = np.zeros(MAP_SIZE, 'int')
            if event.key == pygame.K_o:
                tilemap = np.random.randint(0, 2, MAP_SIZE)
            if event.key == pygame.K_i:
                tilemap = np.array([np.ones(MAP_SIZE[1]) if i % 2 == 0 else np.zeros(MAP_SIZE[1]) for i in range(MAP_SIZE[0])])

    if not settings and play is None:
        if pressed[0]:
            tilemap[tpos[0]][tpos[1]] = 1
        if pressed[2]:
            tilemap[tpos[0]][tpos[1]] = 0

    if play is not None:
        play += 1
        if play % FRAMES_PER_TURN == 0:
            life_act()

    sc.blit(bck, (0,0))

    if grid:
        for i in range(1, MAP_SIZE[0]):
            pygame.draw.aaline(sc, DARK_GREY, (0, i*TILE_SIZE), (FULL_WINDOW[0], i*TILE_SIZE))
        for i in range(1, MAP_SIZE[1]):
            pygame.draw.aaline(sc, DARK_GREY, (i*TILE_SIZE, 0), (i*TILE_SIZE, FULL_WINDOW[1]))

    if play is None:
        for i in range(MAP_SIZE[0]):
            for j in range(MAP_SIZE[1]):
                if tilemap[i][j]:
                    pygame.draw.rect(sc, RECT_COLOR, (j*TILE_SIZE+1, i*TILE_SIZE+1, TILE_SIZE-1, TILE_SIZE-1))
    else:
        for i in range(MAP_SIZE[0]):
            for j in range(MAP_SIZE[1]):
                if playmap[i][j]:
                    pygame.draw.rect(sc, RECT_COLOR, (j*TILE_SIZE+1, i*TILE_SIZE+1, TILE_SIZE-1, TILE_SIZE-1))

    if interface:
        sc.blit(font.render(str(tpos), True, WHITE), (FULL_WINDOW[0] - 160, 10))
        sc.blit(font.render(str(int(clock.get_fps())), True, WHITE), (FULL_WINDOW[0] - 50, 10))
        sc.blit(font.render('Help: [V]', True, WHITE), (FULL_WINDOW[0] - 125, 50))
        if play is not None:
            pfpt = str(play // FRAMES_PER_TURN)
            sc.blit(font.render(pfpt, True, WHITE), (FULL_WINDOW[0] - 200 - 10*len(pfpt), 10))

    if settings:
        SETTINGS_SIZE = 560, 700
        SETTINGS_CORDS = (FULL_WINDOW[0]-SETTINGS_SIZE[0])//2, 200
        WRITINGS_BASE = SETTINGS_CORDS[0]+20, SETTINGS_CORDS[1]+20
        pygame.draw.rect(sc, DARK_GREY, SETTINGS_CORDS+SETTINGS_SIZE)
        pygame.draw.rect(sc, BLACK, SETTINGS_CORDS+SETTINGS_SIZE, 3)
        sc.blit(font.render('Рисовать: [ЛКМ]', True, WHITE), WRITINGS_BASE)
        sc.blit(font.render('Стирать: [ПКМ]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+40))
        sc.blit(font.render('Старт/стоп: [E]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+80))
        sc.blit(toggleon if play is not None else toggleoff, (WRITINGS_BASE[0]+195, WRITINGS_BASE[1]+80))
        sc.blit(font.render('Сетка: [G]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+160))
        sc.blit(toggleon if grid else toggleoff, (WRITINGS_BASE[0]+130, WRITINGS_BASE[1]+160))
        sc.blit(font.render('Параметры в углу: [H]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+200))
        sc.blit(toggleon if interface else toggleoff, (WRITINGS_BASE[0]+285, WRITINGS_BASE[1]+200))
        sc.blit(font.render('Автовыключение сетки: [B]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+240))
        sc.blit(toggleon if autogrid else toggleoff, (WRITINGS_BASE[0]+350, WRITINGS_BASE[1]+240))
        sc.blit(font.render('Скорость: [A][Z]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+280))
        sc.blit(font.render(str(round(60/FRAMES_PER_TURN, 2)), True, GREEN), (WRITINGS_BASE[0]+205, WRITINGS_BASE[1]+280))
        sc.blit(font.render('Сохранение*: [Q]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+320))
        sc.blit(font.render('Выход: [Esc]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+360))
        sc.blit(font.render('Заполнение:', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+440))
        sc.blit(font.render('Очистить: [P]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+480))
        sc.blit(font.render('Рандом: [O]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+520))
        sc.blit(font.render('Полосы: [I]', True, WHITE), (WRITINGS_BASE[0], WRITINGS_BASE[1]+560))
        sc.blit(font24.render('*Имя файла можно поменять в начале кода', True, WHITE), (WRITINGS_BASE[0], SETTINGS_CORDS[1]+SETTINGS_SIZE[1]-30))

    pygame.display.flip()
    clock.tick(FPS)



