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

FULL_WINDOW = 1900, 1000
FPS = 60
cords = [700, 500]

pygame.init()
sc = pygame.display.set_mode(FULL_WINDOW)
clock = pygame.time.Clock()
font = pygame.font.SysFont('calibri', 30)
rotatetext = font.render('Rotate: [Z][C]', True, (0,0,0))
scaletext = font.render('Scale: [A][D]', True, (0,0,0))

deck = pygame.transform.scale(pygame.image.load('deck.png').convert_alpha(), (500,500))
scale = 1
ang = 0


def check_win():
    for i in range(3):
        if table[i][0] != 0 and table[i][0] == table[i][1] and table[i][1] == table[i][2]:
            return True
        if table[0][i] != 0 and table[0][i] == table[1][i] and table[1][i] == table[2][i]:
            return True
    if table[0][0] != 0 and table[0][0] == table[1][1] and table[1][1] == table[2][2]:
        return True
    if table[0][2] != 0 and table[0][2] == table[1][1] and table[1][1] == table[2][0]:
        return True
    return False

sc.fill(WHITE)
while True:
    pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            if event.key == pygame.K_z:
                ang += 45/4
            if event.key == pygame.K_c:
                ang -= 45/4
            if event.key == pygame.K_a:
                scale -= 0.1
                deck = pygame.transform.scale(deck, (int(deck.get_width() * scale), int(deck.get_height() * scale)))
            if event.key == pygame.K_d:
                scale += 0.1
                deck = pygame.transform.scale(deck, (int(deck.get_width() * scale), int(deck.get_height() * scale)))
        if event.type == pygame.MOUSEMOTION:
            cords = [cords[0]+event.rel[0], cords[1]+event.rel[1]]

    deck = pygame.transform.rotate(deck, ang)
    sc.blit(deck, (cords[0]-deck.get_width()//2, cords[1]-deck.get_height()//2))

    sc.blit(rotatetext, (200, 20))
    sc.blit(font.render(str(round(ang,2)), True, (0,0,255)), (380, 20))
    sc.blit(scaletext, (200, 60))
    sc.blit(font.render(str(round(scale,2)), True, (200,0,0)), (380, 60))
    pygame.display.flip()
    clock.tick(FPS)



