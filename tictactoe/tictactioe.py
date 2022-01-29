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

FULL_WINDOW = 1000, 600
FPS = 60
TILE_SIZE = 170

pygame.init()
sc = pygame.display.set_mode(FULL_WINDOW)
clock = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 30)

table = [[(), (), ()],
         [(), (), ()],
         [(), (), ()]]
turn = 2
winner = None
font2 = pygame.font.SysFont('times_new_roman', 72)
wintext = font2.render('Победа', True, BLACK)
tietext = font2.render('Ничья', True, BLACK)
xtext = font2.render('X', True, RED)
otext = font2.render('O', True, LIGHT_GREEN)


def check_win():
    for i in range(3):
        if table[i][0] != () and table[i][0] == table[i][1] and table[i][1] == table[i][2]:
            return True
        if table[0][i] != () and table[0][i] == table[1][i] and table[1][i] == table[2][i]:
            return True
    if table[0][0] != () and table[0][0] == table[1][1] and table[1][1] == table[2][2]:
        return True
    if table[0][2] != () and table[0][2] == table[1][1] and table[1][1] == table[2][0]:
        return True
    return False


while True:
    sc.fill(WHITE)
    pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for i in range(3):
                for j in range(3):
                    if 455+j*TILE_SIZE < pos[0] < 455+(j+1)*TILE_SIZE and 60+i*TILE_SIZE < pos[1] < 60+(i+1)*TILE_SIZE:
                            # Мы же не можем поставить фигуру на клетку, где уже есть крестик или нолик?
                        table[i][j] = tuple(list(table[i][j])+[turn])  # Здесь у нас записано, чей сейчас ход
                        if check_win():  # Проверяем, победил ли игрок, сделавший ход
                            winner = turn  # Тот, кто ходил последний, и будет победителем
                        else:
                            turn = 1 if turn == 2 else 2  # И только после этого передаём ход следующему игроку

    pygame.draw.rect(sc, BLACK, (455, 60, 510, 510), 10)
    for i in range(1,3):
        pygame.draw.line(sc, BLACK, (455+i*TILE_SIZE, 60), (455+i*TILE_SIZE, 60+510), 10)
        pygame.draw.line(sc, BLACK, (455, 60+i*TILE_SIZE), (455+510, 60+i*TILE_SIZE), 10)

    for i in range(3):
        for j in range(3):
            for k in range(len(table[i][j])):
                size = 0.9**k
                if table[i][j][k] == 1:
                    pygame.draw.line(sc, RED, (455+j*TILE_SIZE+10, 60+i*TILE_SIZE+10), (455+(j+1)*TILE_SIZE-10, 60+(i+1)*TILE_SIZE-10), 10)
                    pygame.draw.line(sc, RED, (455+(j+1)*TILE_SIZE-10, 60+i*TILE_SIZE+10), (455+j*TILE_SIZE+10, 60+(i+1)*TILE_SIZE-10), 10)
                elif table[i][j][k] == 2:
                    pygame.draw.circle(sc, LIGHT_GREEN, (455+(j+0.5)*TILE_SIZE, 60+(i+0.5)*TILE_SIZE), 75*size, int(10*size))

    if winner:
        sc.blit(wintext, (100, 250))
        if winner == 1:
            sc.blit(xtext, (340, 250))
        else:
            sc.blit(otext, (340, 250))

    sc.blit(font.render(str(pos), True, BLACK), (FULL_WINDOW[0] - 200, 10))
    sc.blit(font.render(str(int(clock.get_fps())), True, BLACK), (FULL_WINDOW[0] - 50, 10))
    pygame.display.flip()
    clock.tick(FPS)



