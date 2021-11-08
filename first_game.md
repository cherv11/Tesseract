# Первая игра на Pygame
Итак, вы изучили основы Питона, скачали pygame и готовы делать игру. Но с чего начать?  
С шаблона кода pygame! Когда вы начинаете любой новый проект, качайте шаблон здесь (файл называется ex.py): https://disk.yandex.ru/d/wueDsYmkqlHs2A  
Давайте разберём его по кусочкам.  
## Шаблон ex.py
```py
import pygame

FULL_WINDOW = 1000, 600  # устанавливаем разрешение окна
FPS = 60  # устанавливаем количество кадров в секунду

pygame.init()  # говорим pygame, чтобы начал свою работу, всё остальное пишем после после этого
sc = pygame.display.set_mode(FULL_WINDOW)  # создаём экран с нашим разрешением, именно на него подаётся изображение
clock = pygame.time.Clock()  # а это часы для показа количества кадров в секунду
font = pygame.font.SysFont('calibri', 30)  # определяем шрифт, которым можно рендерить текст, это вот Calibri размера 30

while True:  # бесконечный цикл, одно прохождение по нему — один кадр в игре
    sc.fill(pygame.Color('white'))  # заполняем дисплей белым, чтобы стереть предыдущий кадр
    pos = pygame.mouse.get_pos()  # в эту переменную записываются координаты мыши
    pressed = pygame.mouse.get_pressed()  # а в эту нажатые клавиши мыши
    keys = pygame.key.get_pressed()  # здесь нажатые клавиши на клавиатуре

    for event in pygame.event.get():  # Ивенты — это события, регистрирующие нажатия клавиш, движение мыши и т.п.
        # Ивенты вызываются только один раз, когда мы делаем какую-то из этих операций
        if event.type == pygame.QUIT: # Позволяет закрыть программу на крестик
            exit()  # выход из программы в Питоне
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Тип ивента — нажатие клавиши, клавиша — Escape
            exit()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:   # Тип ивента — нажатие кнопки мыши, 1 и 3 — сами кнопки
            pass                                                       # 2 — нажатие колёсика, 4-5 — поворот колёсика
        if event.type == pygame.MOUSEMOTION and event.rel:  # Тип ивента — движение мыши, rel — кортеж с указанием, на сколько по x,y сдвинулась мышь
            pass

    if pressed[0]:  # Если нужно, вы можете каждый кадр проверять, нажата ли сейчас кнопка мыши
        pass
    if keys[pygame.K_a]:  # Или клавиша на клавиатуре
        pass
        
    sc.blit(font.render(str(pos), True, (0, 0, 0)), (FULL_WINDOW[0]-200, 10))  # надпись с позицией мыши
    sc.blit(font.render(str(int(clock.get_fps())), True, (0, 0, 0)), (FULL_WINDOW[0]-50, 10))  # надпись с показыванием FPS
    pygame.display.flip()  # говорим pygame вывести следующий кадр на экран
    clock.tick(FPS)  # делаем паузу, чтобы игра не шла слишком быстро
```
