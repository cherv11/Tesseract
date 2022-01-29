import pygame
import os
import random

FULL_WINDOW = 1920, 1080
FPS = 60
TILE_SIZE = 95
GREEN = (136, 228, 16)
RED = (226, 88, 102)

pygame.init()
sc = pygame.display.set_mode(FULL_WINDOW)
clock = pygame.time.Clock()

font = pygame.font.SysFont('arial', 30)
deck = pygame.image.load('deck100.png').convert_alpha()
bckgr = pygame.transform.scale(pygame.image.load('bckgr\\'+random.choice(os.listdir('bckgr'))).convert_alpha(), (1920, 1080))
button = pygame.transform.scale(pygame.image.load('button.png').convert_alpha(), (300, 100))
square_icon = pygame.transform.scale(pygame.image.load('sq.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
rect_icon = pygame.transform.scale(pygame.image.load('sr.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
deck = pygame.transform.scale(deck, (1080, 1080))
board = [['' for _ in range(10)] for _ in range(10)]
bottomteam = '0'
selected_shape = None
selected_shape_ways = []
log = []
turn = '0'
gamemode = 'mainmenu'
AIteam = None

shapes = {i.split('.png')[0]: pygame.image.load('shapes\\'+i).convert_alpha() for i in os.listdir('shapes')}
for k in shapes:
    v = shapes[k]
    shapes[k] = pygame.transform.scale(v, (int(v.get_width()/v.get_height()*TILE_SIZE), TILE_SIZE))


def fill_board(sd='0'):
    global board
    global bottomteam
    board = [['' for _ in range(10)] for _ in range(10)]
    fs = 'RNBNKQNBNR'
    if sd == '0':
        board[0] = [f'{i}1' for i in fs]
        board[1] = [f'p1' for _ in range(10)]
        board[8] = [f'p0' for _ in range(10)]
        board[9] = [f'{i}0' for i in fs[::-1]]
    else:
        board[0] = [f'{i}0' for i in fs[::-1]]
        board[1] = [f'p0' for _ in range(10)]
        board[8] = [f'p1' for _ in range(10)]
        board[9] = [f'{i}1' for i in fs]
    bottomteam = sd

fill_board()


def canmove(cords):
    shape = board[cords[0]][cords[1]]
    res = []
    enemy = '0' if shape.endswith('1') else '1'
    if shape.startswith('Q') or shape.startswith('R'):
        for i in range(0, cords[0])[::-1]:
            if board[i][cords[1]]:
                if board[i][cords[1]].endswith(enemy):
                    res.append((i, cords[1], 1))
                break
            else:
                res.append((i, cords[1], 0))
        for i in range(cords[0]+1, 10):
            if board[i][cords[1]]:
                if board[i][cords[1]].endswith(enemy):
                    res.append((i, cords[1], 1))
                break
            else:
                res.append((i, cords[1], 0))
        for i in range(0, cords[1])[::-1]:
            if board[cords[0]][i]:
                if board[cords[0]][i].endswith(enemy):
                    res.append((cords[0], i, 1))
                break
            else:
                res.append((cords[0], i, 0))
        for i in range(cords[1]+1, 10):
            if board[cords[0]][i]:
                if board[cords[0]][i].endswith(enemy):
                    res.append((cords[0], i, 1))
                break
            else:
                res.append((cords[0], i, 0))
    if shape.startswith('Q') or shape.startswith('B') or shape.startswith('K'):
        for dct in range(4):
            for c in range(1,10):
                if c > 1 and shape.startswith('K'):
                    break
                if dct == 0:
                    i,j = cords[0]-c, cords[1]-c
                elif dct == 1:
                    i,j = cords[0]+c, cords[1]-c
                elif dct == 2:
                    i,j = cords[0]-c, cords[1]+c
                else:
                    i,j = cords[0]+c, cords[1]+c
                if i < 0 or i > 9 or j < 0 or j > 9:
                    break
                if board[i][j]:
                    if board[i][j].endswith(enemy):
                        res.append((i, j, 1))
                    break
                else:
                    res.append((i, j, 0))
    if shape.startswith('K'):
        for dct in range(4):
            if dct == 0:
                i, j = cords[0]-1, cords[1]
            elif dct == 1:
                i, j = cords[0]+1, cords[1]
            elif dct == 2:
                i, j = cords[0], cords[1]+1
            else:
                i, j = cords[0], cords[1]-1
            if i < 0 or i > 9 or j < 0 or j > 9:
                continue
            if board[i][j]:
                if board[i][j].endswith(enemy):
                    res.append((i, j, 1))
            else:
                res.append((i, j, 0))
    if shape.startswith('N'):
        offsets = [(1, 2), (2, 1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1, -2), (-2, -1)]
        for dct in range(8):
            i, j = cords[0]+offsets[dct][0], cords[1]+offsets[dct][1]
            if i < 0 or i > 9 or j < 0 or j > 9:
                continue
            if board[i][j]:
                if board[i][j].endswith(enemy):
                    res.append((i, j, 1))
            else:
                res.append((i, j, 0))
    if shape.startswith('p'):
        if (shape.endswith('0') and bottomteam == '0') or (shape.endswith('1') and bottomteam == '1'):
            for c in range(1,3):
                if c > 1 and not cords[0] == 8:
                    break
                i, j = cords[0]-c, cords[1]
                if i < 0 or i > 9 or j < 0 or j > 9:
                    continue
                if not board[i][j]:
                    res.append((i, j, 0))
                else:
                    break
            for c in [-1, 1]:
                i, j = cords[0]-1, cords[1]+c
                if i < 0 or i > 9 or j < 0 or j > 9:
                    continue
                if board[i][j]:
                    if board[i][j].endswith(enemy):
                        res.append((i, j, 1))
        else:
            for c in range(1,3):
                if c > 1 and not cords[0] == 1:
                    break
                i, j = cords[0]+c, cords[1]
                if i < 0 or i > 9 or j < 0 or j > 9:
                    continue
                if not board[i][j]:
                    res.append((i, j, 0))
                else:
                    break
            for c in [-1, 1]:
                i, j = cords[0]+1, cords[1]+c
                if i < 0 or i > 9 or j < 0 or j > 9:
                    continue
                if board[i][j]:
                    if board[i][j].endswith(enemy):
                        res.append((i, j, 1))
    return res


def move(sh, pos):
    shape = board[sh[0]][sh[1]]
    oldshape = board[pos[0]][pos[1]]
    board[pos[0]][pos[1]] = shape
    board[sh[0]][sh[1]] = ''
    log.append((shape, sh, pos, oldshape))

    if shape[0] == 'p':
        if (shape.endswith('0') and bottomteam == '0') or (shape.endswith('1') and bottomteam == '1'):
            if pos[0] == 0:
                board[pos[0]][pos[1]] = 'Q'+shape[1]
        else:
            if pos[0] == 9:
                board[pos[0]][pos[1]] = 'Q'+shape[1]

    enemy = '0' if shape.endswith('1') else '1'
    eking = ()
    for i in range(10):
        for j in range(10):
            if board[i][j] == 'K'+enemy:
                eking = (i,j)
    if not eking:
        changemode('mainmenu')


def bestmove(moves):
    vs = {'Q': 90, 'K': 1000, 'B':30, 'N':30, 'R':50, 'p':10}
    move = None
    value = 0
    for shape, pos in moves:
        if board[pos[0]][pos[1]]:
            if vs[board[pos[0]][pos[1]][0]] > value:
                value = vs[board[pos[0]][pos[1]][0]]
                move = (shape, pos)
    if not move:
        return random.choice(moves)
    return move


def aimove():
    moves = []
    for i in range(10):
        for j in range(10):
            if board[i][j].endswith(AIteam):
                emoves = canmove((i,j))
                for m in emoves:
                    moves.append(((i,j), (m[0],m[1])))
    if not moves:
        changemode('mainmenu')
        return (0,0), (0,0)
    return bestmove(moves)


def changemode(mode):
    global gamemode
    global board
    global bckgr
    gamemode = mode
    if gamemode.startswith('game'):
        bckgr = pygame.transform.scale(pygame.image.load('bckgr\\' + random.choice(os.listdir('bckgr'))).convert_alpha(), (1920, 1080))


while True:
    sc.fill(pygame.Color('black'))
    pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if gamemode.startswith('game'):
                    changemode('mainmenu')
        if event.type == pygame.MOUSEBUTTONUP:
            if gamemode == 'mainmenu':
                if event.button == 1:
                    if 810 < pos[0] < 1110:
                        if 300 < pos[1] < 400:
                            changemode('aimenu')
                        if 400 < pos[1] < 500:
                            changemode('game2p')
                            fill_board('0')
                            AIteam = None
                        if 500 < pos[1] < 600:
                            exit()
            elif gamemode == 'aimenu':
                if event.button == 1:
                    if 810 < pos[0] < 1110:
                        if 300 < pos[1] < 400:
                            changemode('gameai')
                            AIteam = '1'
                            fill_board('0')
                        if 400 < pos[1] < 500:
                            changemode('gameai')
                            AIteam = '0'
                            fill_board('1')
                            what, where = aimove()
                            move(what, where)
                            turn = '1'
                        if 500 < pos[1] < 600:
                            changemode('mainmenu')
            elif gamemode.startswith('game'):
                if selected_shape:
                    if event.button == 1:
                        for i in range(10):
                            for j in range(10):
                                if 908 + TILE_SIZE * j < pos[0] < 908 + TILE_SIZE * j + TILE_SIZE and 65 + TILE_SIZE * i < pos[1] < 65 + TILE_SIZE * i + TILE_SIZE:
                                    ways = canmove(selected_shape)
                                    for w in ways:
                                        if w[0] == i and w[1] == j:
                                            move(selected_shape, (i,j))
                                            turn = '1' if turn == '0' else '0'
                                            if AIteam:
                                                what, where = aimove()
                                                move(what, where)
                                                turn = '1' if turn == '0' else '0'
                        selected_shape = None
                    if event.button == 3:
                        selected_shape = None
                else:
                    if event.button == 1:
                        for i in range(10):
                            for j in range(10):
                                if 908 + TILE_SIZE * j < pos[0] < 908 + TILE_SIZE * j + TILE_SIZE and 65 + TILE_SIZE * i < pos[1] < 65 + TILE_SIZE * i + TILE_SIZE:
                                    if board[i][j].endswith(turn):
                                        selected_shape = (i, j)
                                        selected_shape_ways = canmove(selected_shape)

    sc.blit(bckgr, (0, 0))

    if gamemode == 'mainmenu':
        sc.blit(button, (810, 300))
        sc.blit(font.render('Игра с ИИ', True, pygame.Color('white')), (902, 330))
        sc.blit(button, (810, 400))
        sc.blit(font.render('2 игрока', True, pygame.Color('white')), (913, 430))
        sc.blit(button, (810, 500))
        sc.blit(font.render('Выход', True, pygame.Color('white')), (920, 530))
    if gamemode == 'aimenu':
        sc.blit(button, (810, 300))
        sc.blit(font.render('Белыми', True, pygame.Color('white')), (916, 330))
        sc.blit(button, (810, 400))
        sc.blit(font.render('Чёрными', True, pygame.Color('white')), (913, 430))
        sc.blit(button, (810, 500))
        sc.blit(font.render('Назад', True, pygame.Color('white')), (925, 530))
    elif gamemode.startswith('game'):
        sc.blit(deck, (840, 0))

        if selected_shape:
            for i,j,k in selected_shape_ways:
                if k:
                    sc.blit(rect_icon, (908 + TILE_SIZE * j, 65 + TILE_SIZE * i, TILE_SIZE, TILE_SIZE))
                else:
                    sc.blit(square_icon, (908 + TILE_SIZE * j, 65 + TILE_SIZE * i, TILE_SIZE, TILE_SIZE))

        for i in range(10):
            for j in range(10):
                if board[i][j]:
                    sc.blit(shapes[board[i][j]], (939+TILE_SIZE*j,65+TILE_SIZE*i))

    sc.blit(font.render(str(pos), True, pygame.Color('white')), (1680, 10))
    sc.blit(font.render(str(int(clock.get_fps())), True, pygame.Color('white')), (1850, 10))
    pygame.display.flip()
    clock.tick(FPS)