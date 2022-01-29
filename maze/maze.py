import pygame
import random
from collections import defaultdict
import time

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

FULL_WINDOW = 1920, 1080
FPS = 60
MAZE_SIZE_X, MAZE_SIZE_Y = 64, 64
MAZE_START_CORDS = 180, 110
TILE_SIZE = (FULL_WINDOW[1]-200)//MAZE_SIZE_Y
START_POINT = MAZE_SIZE_X//2, 0
HORIZONTAL_LINES_CHANCE = 35
VERTICAL_LINES_CHANCE = 50
horizontal_lines = []
vertical_lines = []

pygame.init()
sc = pygame.display.set_mode(FULL_WINDOW)
clock = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 30)
minifont = pygame.font.SysFont('calibri', 10)
bck = pygame.transform.scale(pygame.image.load('bck.png').convert_alpha(), FULL_WINDOW)
bck2 = pygame.transform.scale(pygame.image.load('bck2.png').convert_alpha(), FULL_WINDOW)

maze_square = pygame.Surface((TILE_SIZE*MAZE_SIZE_X, TILE_SIZE*MAZE_SIZE_Y))
maze_square.fill(BLACK)
maze_square.set_alpha(128)
cur_square = pygame.Surface((TILE_SIZE-2, TILE_SIZE-2))
cur_square.fill(PEACH)
cur_square.set_alpha(180)
sch_square = pygame.Surface((TILE_SIZE-2, TILE_SIZE-2))
sch_square.fill(LIGHT_BLUE)
sch_square.set_alpha(100)
slv_square = pygame.Surface((TILE_SIZE-2, TILE_SIZE-2))
slv_square.fill(PINK)
slv_square.set_alpha(220)

play = True
frames = 0
speed = 3

searched_points = []
current_points = [START_POINT]
paths = defaultdict(list)
paths[START_POINT] = []
solved = 0
regen_if_solved = True


def chance(a, b=100):
    if random.randint(1, b) <= a:
        return True
    return False


def solve_maze():
    global searched_points
    global current_points
    global paths
    global solved
    new_points = []

    if not current_points:
        if len(searched_points) < MAZE_SIZE_X:
            solved = frames + 10
        else:
            solved = frames + 180
        return
    for i,j in current_points:
        if j == MAZE_SIZE_Y:
            solved = frames + 180
            return
    for i,j in current_points:
        if j > 0 and (i,j) not in horizontal_lines and (i, j-1) not in searched_points:
            if (i, j-1) not in new_points:
                new_points.append((i, j-1))
                paths[(i, j-1)] = paths[(i,j)]+[(i,j)]
        if i > 0 and (i,j) not in vertical_lines and (i-1, j) not in searched_points:
            if (i-1, j) not in new_points:
                new_points.append((i-1, j))
                paths[(i-1, j)] = paths[(i,j)]+[(i,j)]
        if i < MAZE_SIZE_X-1 and (i+1,j) not in vertical_lines and (i+1, j) not in searched_points:
            if (i+1, j) not in new_points:
                new_points.append((i+1, j))
                paths[(i+1, j)] = paths[(i, j)]+[(i,j)]
        if j < MAZE_SIZE_Y and (i,j+1) not in horizontal_lines and (i, j+1) not in searched_points:
            if (i, j+1) not in new_points:
                new_points.append((i, j+1))
                paths[(i, j+1)] = paths[(i, j)]+[(i,j)]
    searched_points += current_points
    current_points = new_points


def generate_maze():
    global horizontal_lines
    global vertical_lines
    horizontal_lines = []
    vertical_lines = []
    for i in range(MAZE_SIZE_X):
        for j in range(MAZE_SIZE_Y):
            if chance(HORIZONTAL_LINES_CHANCE):
                horizontal_lines.append((i,j))
            if chance(VERTICAL_LINES_CHANCE):
                vertical_lines.append((i,j))


generate_maze()


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
                generate_maze()
                searched_points = []
                current_points = [START_POINT]
                paths = defaultdict(list)
                paths[START_POINT] = []
                solved = 0
            if event.key == pygame.K_g:
                play = not play
            if event.key == pygame.K_h:
                solve_maze()
            if event.key == pygame.K_a:
                if speed > 1:
                    speed -= 1
            if event.key == pygame.K_z:
                if speed < 20:
                    speed += 1

    if play:
        frames += 1
        if frames % speed == 0:
            if solved:
                if solved < frames and regen_if_solved:
                    generate_maze()
                    searched_points = []
                    current_points = [START_POINT]
                    paths = defaultdict(list)
                    paths[START_POINT] = []
                    solved = 0
            else:
                solve_maze()

    sc.blit(bck, (0,0))
    if solved and solved >= frames:
        for i, j in current_points:
            if j == MAZE_SIZE_Y:
                sc.blit(bck2, (0,0))
                break
    sc.blit(maze_square, MAZE_START_CORDS)
    for i,j in vertical_lines:
        pygame.draw.line(sc, BLACK, (MAZE_START_CORDS[0]+i*TILE_SIZE, MAZE_START_CORDS[1]+j*TILE_SIZE), (MAZE_START_CORDS[0]+i*TILE_SIZE, MAZE_START_CORDS[1]+(j+1)*TILE_SIZE), 2)
    for i,j in horizontal_lines:
        pygame.draw.line(sc, BLACK, (MAZE_START_CORDS[0]+i*TILE_SIZE, MAZE_START_CORDS[1]+j*TILE_SIZE), (MAZE_START_CORDS[0]+(i+1)*TILE_SIZE, MAZE_START_CORDS[1]+j*TILE_SIZE), 2)
    for i,j in current_points:
        sc.blit(cur_square, (MAZE_START_CORDS[0]+i*TILE_SIZE+2, MAZE_START_CORDS[1]+j*TILE_SIZE+2))
    for i,j in searched_points:
        sc.blit(sch_square, (MAZE_START_CORDS[0]+i*TILE_SIZE+2, MAZE_START_CORDS[1]+j*TILE_SIZE+2))
        sc.blit(minifont.render(str(len(paths[(i,j)])), True, BLACK), (MAZE_START_CORDS[0]+i*TILE_SIZE+2, MAZE_START_CORDS[1]+j*TILE_SIZE+2))
    if solved and solved >= frames:
        for i, j in current_points:
            if j == MAZE_SIZE_Y:
                for ii, jj in paths[(i,j)]:
                    sc.blit(slv_square, (MAZE_START_CORDS[0] + ii * TILE_SIZE + 2, MAZE_START_CORDS[1] + jj * TILE_SIZE + 2))

    sc.blit(font.render(str(pos), True, BLACK), (FULL_WINDOW[0] - 200, 10))
    sc.blit(font.render(str(int(clock.get_fps())), True, BLACK), (FULL_WINDOW[0] - 50, 10))
    sc.blit(font.render('Скорость: '+str(21-speed), True, BLACK), (FULL_WINDOW[0] - 200, 200))
    sc.blit(font.render(str(frames), True, BLACK), (FULL_WINDOW[0] - 300, 100))
    pygame.display.flip()
    clock.tick(FPS)



