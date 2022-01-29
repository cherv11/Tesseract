import pygame
import random

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
YELLANGE = (255, 192, 0)
ORANGE = (255, 128, 0)
DARK_BLUE = (0, 0, 128)
BLUE = (0, 0, 225)
LIGHT_BLUE = (135, 208, 250)
RED = (255, 0, 0)
DARK_RED = (128, 0, 0)
GREEN = (64, 255, 64)
LIGHT_GREEN = (128, 255, 128)
BLACK = (0, 0, 0)
BROWN = (96, 38, 0)
GREY = (128, 128, 128)
PURPLE = (128, 0, 128)
PINK = (255, 20, 147)
PEACH = (240, 128, 128)
RASPBERRY = (220, 20, 60)
TURQUOISE = (0, 128, 128)
COLORS = [TURQUOISE, PINK, PEACH, RASPBERRY, PURPLE, YELLOW, YELLANGE, ORANGE, DARK_BLUE, BLUE, LIGHT_BLUE, RED, DARK_RED, GREEN, LIGHT_GREEN, BLACK, BROWN, GREY]

MAP_SIZE = 20, 10
TILE_SIZE = 48
FULL_WINDOW = 800, 970
FPS = 60
dx = MAP_SIZE[1]//2


pygame.init()
sc = pygame.display.set_mode(FULL_WINDOW)
clock = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 30)
tfont = pygame.font.Font('tetris.otf', 50)
bck = pygame.image.load('bck.png').convert()
logo = pygame.image.load('logo.png').convert_alpha()
logo = pygame.transform.scale(logo, (200, int(200*logo.get_height()/logo.get_width())))
button = pygame.image.load('button.png').convert_alpha()
button = pygame.transform.scale(button, (150, int(150*button.get_height()/button.get_width())))

shapes = [[(0, 0), (-1, 0), (-2, 0), (1, 0)],
          [(0, 0), (0, -1), (-1, -1), (-1, 0)],
          [(0, 0), (-1, 0), (-1, 1), (0, -1)],
          [(0, 0), (-1, 0), (0, 1), (-1, -1)],
          [(0, 0), (0, -1), (0, 1), (-1, -1)],
          [(0, 0), (0, -1), (0, 1), (1, -1)],
          [(0, 0), (0, -1), (0, 1), (-1, 0)]]
anim_idx = 0
tilemap = [[0 for _ in range(MAP_SIZE[1])] for _ in range(MAP_SIZE[0])]
points = 0


def new_shape():
    global anim_idx
    anim_idx = 0
    gshape = random.choice(shapes)
    gdx = MAP_SIZE[1]-1-max(i[0] for i in gshape) if dx > MAP_SIZE[1]-1-max(i[0] for i in gshape) else -min(i[0] for i in gshape) if dx < -min(i[0] for i in gshape) else dx
    return [[gdx, -min(i[1] for i in gshape)], random.choice(COLORS), gshape]


shape = new_shape()


def move_down():
    global shape
    global points
    if not shape:
        return
    maxy = shape[0][1]+max([i[1] for i in shape[2]])+1
    if maxy < MAP_SIZE[0]:
        collision = False
        for i in range(4):
            y, x = shape[2][i][0] + shape[0][0], shape[2][i][1] + shape[0][1] + 1
            if tilemap[x][y]:
                collision = True
                break
        if collision:
            for i in range(4):
                y, x = shape[2][i][0] + shape[0][0], shape[2][i][1] + shape[0][1]
                tilemap[x][y] = shape[1]
            if shape[0][1] < 2:
                shape = None
                return
            shape = new_shape()
        else:
            shape[0][1] += 1
    else:
        for i in range(4):
            y, x = shape[2][i][0] + shape[0][0], shape[2][i][1] + shape[0][1]
            tilemap[x][y] = shape[1]
        shape = new_shape()
    for i in range(len(tilemap)):
        flag = True
        for j in range(len(tilemap[i])):
            if tilemap[i][j] == 0:
                flag = False
                break
        if flag:
            tilemap[:] = [[0 for _ in range(MAP_SIZE[1])]] + tilemap[:i] + tilemap[i+1:]
            points += 100


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
            if shape is not None:
                if event.key == pygame.K_LEFT:
                    if shape[0][0] > -min([i[0] for i in shape[2]]):
                        collision = False
                        for i in range(4):
                            y, x = shape[2][i][0] + shape[0][0] - 1, shape[2][i][1] + shape[0][1]
                            if tilemap[x][y]:
                                collision = True
                                break
                        if collision:
                            continue
                        dx -= 1
                        shape[0][0] -= 1
                if event.key == pygame.K_RIGHT:
                    if dx < MAP_SIZE[1]-1-max([i[0] for i in shape[2]]):
                        collision = False
                        for i in range(4):
                            y, x = shape[2][i][0] + shape[0][0] + 1, shape[2][i][1] + shape[0][1]
                            if tilemap[x][y]:
                                collision = True
                                break
                        if collision:
                            continue
                        dx += 1
                        shape[0][0] += 1
                if event.key == pygame.K_a:
                    collision = False
                    gshape = [(i[1], -i[0]) for i in shape[2]]
                    gposx = MAP_SIZE[1]-1-max(i[0] for i in gshape) if dx > MAP_SIZE[1]-1-max(i[0] for i in gshape) else -min(i[0] for i in gshape) if dx < -min(i[0] for i in gshape) else dx
                    for i in range(4):
                        y, x = gposx+gshape[i][0], shape[0][1]+gshape[i][1]
                        if tilemap[x][y]:
                            collision = True
                            break
                    if collision:
                        continue
                    shape[2] = [(i[1], -i[0]) for i in shape[2]]
                    shape[0][0] = MAP_SIZE[1]-1-max(i[0] for i in shape[2]) if dx > MAP_SIZE[1]-1-max(i[0] for i in shape[2]) else -min(i[0] for i in shape[2]) if dx < -min(i[0] for i in shape[2]) else dx
                if event.key == pygame.K_d:
                    collision = False
                    gshape = [(-i[1], i[0]) for i in shape[2]]
                    gposx = MAP_SIZE[1] - 1 - max(i[0] for i in gshape) if dx > MAP_SIZE[1] - 1 - max(i[0] for i in gshape) else -min(i[0] for i in gshape) if dx < -min(i[0] for i in gshape) else dx
                    for i in range(4):
                        y, x = gposx + gshape[i][0], shape[0][1] + gshape[i][1]
                        if tilemap[x][y]:
                            collision = True
                            break
                    if collision:
                        continue
                    shape[2] = [(-i[1], i[0]) for i in shape[2]]
                    shape[0][0] = MAP_SIZE[1]-1-max(i[0] for i in shape[2]) if dx > MAP_SIZE[1]-1-max(i[0] for i in shape[2]) else -min(i[0] for i in shape[2]) if dx < -min(i[0] for i in shape[2]) else dx
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if 570 < pos[0] < 570+150 and 360 < pos[1] < 360+150:
                    anim_idx = 0
                    tilemap = [[0 for _ in range(MAP_SIZE[1])] for _ in range(MAP_SIZE[0])]
                    shape = new_shape()
                    points = 0

    if keys[pygame.K_DOWN]:
        move_down()

    anim_idx += 1
    if anim_idx % 60 == 0:
        move_down()

    sc.blit(bck, (0,0))
    sc.blit(logo, (550,50))

    [pygame.draw.aaline(sc, BLACK, (5, i*TILE_SIZE+5), (TILE_SIZE*MAP_SIZE[1]+5, i*TILE_SIZE+5)) for i in range(MAP_SIZE[0]+1)]
    [pygame.draw.aaline(sc, BLACK, (i*TILE_SIZE+5, 5), (i*TILE_SIZE+5, TILE_SIZE*MAP_SIZE[0]+5)) for i in range(MAP_SIZE[1]+1)]

    for i in range(MAP_SIZE[0]):
        for j in range(MAP_SIZE[1]):
            if tilemap[i][j]:
                pygame.draw.rect(sc, tilemap[i][j], (j * TILE_SIZE + 6, i * TILE_SIZE + 6, TILE_SIZE - 1, TILE_SIZE - 1))
    if shape is not None:
        for i in range(4):
            pygame.draw.rect(sc, shape[1], ((shape[2][i][0]+shape[0][0])*TILE_SIZE+6, (shape[2][i][1]+shape[0][1])*TILE_SIZE+6, TILE_SIZE-1, TILE_SIZE-1))
    else:
        sc.blit(tfont.render('Game Over', True, BLACK), (530, 300))
        sc.blit(button, (570, 360))

    sc.blit(tfont.render(str(points), True, BLACK), (640-12*len(str(points)), 250))
    pygame.display.flip()

    clock.tick(FPS)



