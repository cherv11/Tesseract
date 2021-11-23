# Пишем шахматы. Часть 2: Перемещение, меню, ИИ
Привет-привет! [Продолжаем](https://cherv11.github.io/Tesseract/pics_and_shapes) писать шахматы. Сегодня мы:
- Допишем основной код программы
- Создадим меню, из которого будут открываться разные игровые режимы
- Найдём хороший искусственный интеллект для наших шахмат (спойлер: не найдём)

## Анализ доски и перемещение фигур
На прошлой паре мы закончили всё, не считая двух функций — `move()` и `canmove()`. Давайте в них разберёмся.  
Функции применяются только три раза вот в этих случаях:  
![image](https://user-images.githubusercontent.com/56085790/142756446-3b9953d0-8147-42c3-bac0-372d771bad7a.png)

Отсюда видно, что функция `move()` принимает координаты, откуда и куда переместить фигуру, и должна **только** переместить её с одного места в другое. Какую фигуру куда можно, а куда нельзя перемещать, решает функция `canmove()`.  
```py
def move(sh, pos):
    shape = board[sh[0]][sh[1]]
    board[pos[0]][pos[1]] = shape
    board[sh[0]][sh[1]] = ''
 ```
 Но правила шахмат не ограничиваются одним лишь перемещением фигур. В эту функцию необходимо добавить такие вещи, как превращение пешки в ферзя, если она добралась до конца поля:
 ```py
     if shape[0] == 'p':
        if (shape.endswith('0') and bottomteam == '0') or (shape.endswith('1') and bottomteam == '1'): 
            if pos[0] == 0:
                board[pos[0]][pos[1]] = 'Q'+shape[1]
        else:  # Этот if/else зависит от того, какая команда начинает внизу
            if pos[0] == 7:
                board[pos[0]][pos[1]] = 'Q'+shape[1]
 ```
 А вы задумывались, как игра должна закончится? Нужно добавить выход из игры (или в меню, или не выход, а надпись какую) при убийстве короля:
 ```py
    enemy = '0' if shape.endswith('1') else '1'  # Скажи мне, кто твой враг, и я скажу, кто ты...
    eking = ()
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'K'+enemy:  # Находим вражеского короля на поле
                eking = (i,j)
    if not eking:  # Если его нет, значит, его убили))
        exit()
 ```
 Итак, мы получили это:
 ```py
 def move(sh, pos):
    shape = board[sh[0]][sh[1]]
    board[pos[0]][pos[1]] = shape
    board[sh[0]][sh[1]] = ''

    if shape[0] == 'p':
        if (shape.endswith('0') and bottomteam == '0') or (shape.endswith('1') and bottomteam == '1'):
            if pos[0] == 0:
                board[pos[0]][pos[1]] = 'Q'+shape[1]
        else:
            if pos[0] == 7:
                board[pos[0]][pos[1]] = 'Q'+shape[1]

    enemy = '0' if shape.endswith('1') else '1'
    eking = ()
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'K'+enemy:
                eking = (i,j)
    if not eking:
        exit()
````
Теперь определимся с путями. Функция `canmove()` занимает целых 120 строк, в ней есть не только расчёт клеток, но ещё и такие вещи, как старт пешки на две клетки (и должна быть рокировка). Давайте посмотрим на часть этого кода:
```py
def canmove(cords):
    shape = board[cords[0]][cords[1]]  # Это наша фигура
    res = []  # Это список её ходов, пока пустой
    enemy = '0' if shape.endswith('1') else '1'  # Определяем вражеский цвет
    if shape.startswith('Q') or shape.startswith('R'):  # Для ладьи с королевой
    
        # 4 направления, куда может ходить ладья — 4 цикла for
        # Обратите внимание, что нам надо считать клетки по порядку,
        #  потому что любая фигура может перегородить движение нашей
        #  и дальше она пройти не сможет. Идя влево, мы считаем клетки справа налево.
        for i in range(0, cords[0])[::-1]:  
            if board[i][cords[1]]:  # Если на пути стоит фигура
                if board[i][cords[1]].endswith(enemy):  # Если она вражеская
                    res.append((i, cords[1], 1))  # Добавляем её в список с пометкой 1 (красный квадратик)
                break # Ни союзная, ни вражеская фигура на пути не дадут нам пройти дальше
            else:  # Если клетка пустая
                res.append((i, cords[1], 0))  # Добавляем её в список с пометкой 0 (зелёный квадратик)

        # Стоит отметить, что код внутри циклов for одинаковый, так что дальше отличается только начало цикла
        # Идём вправо, затем так же вверх и вниз
        for i in range(cords[0]+1, 8):  
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

        for i in range(cords[1]+1, 8):
            if board[cords[0]][i]:
                if board[cords[0]][i].endswith(enemy):
                    res.append((cords[0], i, 1))
                break
            else:
                res.append((cords[0], i, 0))
                
    return res  # Не забываем вернуть список
```
Это ход ладьи и часть хода королевы (очень рекомендую [сериал](https://www.netflix.com/ru/title/80234304)). Почему вместе? Если подумать над тем, как ходят фигуры в шахматах, можно заметить, что ход королевы — это совмещение ходов ладьи и слона. То есть, мы можем написать код для ладьи и слона, а потом сказать, что всё это может королева! Аналогично написаны слон, конь, король и пешка. 
## Сделаем меню
Для того, чтобы сделать меню, нам теперь нужно сделать для части управления и рисования условие: работать только в конкретном режиме. То есть у нас будет режим меню, где работают только кнопки, и режим игры, где работает всё остальное. Давайте сделаем переменную для режима и загрузим какую-нибудь стильную кнопку:
```py
button = pygame.transform.scale(pygame.image.load('button.png').convert_alpha(), (300, 100))
gamemode = 'mainmenu'
```
Напишем функцию для смены режима игры:
```py
def changemode(mode):
    global gamemode
    global bckgr
    gamemode = mode
    if gamemode.startswith('game'):  # Будем менять фон каждый раз, когда начинаем новую партию
        bckgr = pygame.transform.scale(pygame.image.load('bckgr\\' + random.choice(os.listdir('bckgr'))).convert_alpha(), (1920, 1080))
```
А теперь создаём кнопки меню. Сделаем такую структуру меню:  
![image](https://user-images.githubusercontent.com/56085790/142863424-86c6ef83-5ff1-4a2c-aabb-99a7b18b0a4f.png)  

В части управления нужно сделать нажатие на эти самые кнопки. Вот такой код получится в итоге:
```py
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if gamemode.startswith('game'):
                    changemode('mainmenu')
        if event.type == pygame.MOUSEBUTTONUP:
            if gamemode == 'mainmenu':  # Мы находимся в главном меню
                if event.button == 1:
                    if 810 < pos[0] < 1110:  # По этим координатам расположены на экране три наших кнопки
                        if 300 < pos[1] < 400:
                            changemode('aimenu')  # Запускаем игру с ИИ
                        if 400 < pos[1] < 500:
                            changemode('game2p')  # Запускаем игру на 2 игрока
                            fill_board('0')
                            AIteam = None
                        if 500 < pos[1] < 600:  # Выход из игры
                            exit()
            elif gamemode == 'aimenu':  # Мы выбрали игру с ИИ
                if event.button == 1:
                    if 810 < pos[0] < 1110:
                        if 300 < pos[1] < 400:
                            changemode('gameai')  # Мы ходим белыми
                            AIteam = '1'
                            fill_board('0')
                        if 400 < pos[1] < 500:
                            changemode('gameai')  # ИИ ходит белыми, и он уже тут делает первый ход
                            AIteam = '0'
                            fill_board('1')
                            what, where = aimove()
                            move(what, where)
                            turn = '1'
                        if 500 < pos[1] < 600:
                            changemode('mainmenu')  # Обратно в меню
            elif gamemode.startswith('game'):
                # Здесь весь код игры, который мы делали ранее
```
А в части рисования остаётся только сделать кнопки и надписи на них:
```py
    sc.blit(bckgr, (0, 0)) # Фон есть всегда

    if gamemode == 'mainmenu':  # Кнопки в главном меню
        sc.blit(button, (810, 300))
        sc.blit(font.render('Игра с ИИ', True, pygame.Color('white')), (902, 330))
        sc.blit(button, (810, 400))
        sc.blit(font.render('2 игрока', True, pygame.Color('white')), (913, 430))
        sc.blit(button, (810, 500))
        sc.blit(font.render('Выход', True, pygame.Color('white')), (920, 530))
    if gamemode == 'aimenu':  # Кнопки, когда мы нажали на игру с ИИ
        sc.blit(button, (810, 300))
        sc.blit(font.render('Белыми', True, pygame.Color('white')), (916, 330))
        sc.blit(button, (810, 400))
        sc.blit(font.render('Чёрными', True, pygame.Color('white')), (913, 430))
        sc.blit(button, (810, 500))
        sc.blit(font.render('Назад', True, pygame.Color('white')), (925, 530))
    elif gamemode.startswith('game'):
        # Код игры (рисование доски, фигур и подсветки)

    # Тоже какие-то общие вещи, которые есть всегда
    sc.blit(font.render(str(pos), True, pygame.Color('white')), (1680, 10)) 
    sc.blit(font.render(str(int(clock.get_fps())), True, pygame.Color('white')), (1850, 10))
    pygame.display.flip()
    clock.tick(FPS)
```
Получаем вот такую красоту:
![image](https://user-images.githubusercontent.com/56085790/142865807-eaf4b2c6-167d-4aef-9344-b69e80eb8808.png)  

## Подключаем ИИ
Как только мы сделали ход, ИИ должен сразу сделать свой. На том месте, где мы делали ход, то есть там, где располагается функция `move()` располагаем следующий код:
```py
AIteam = None  #  Нужна новая переменная в части определения
# Мы меняем её на '0' или '1', когда запускаем игру с ИИ по кнопке


move(selected_shape, (i,j)) 
turn = '1' if turn == '0' else '0'  # Это мы уже написали
if AIteam:  # А вот здесь ходит компьютер
    what, where = aimove()
    move(what, where)
    turn = '1' if turn == '0' else '0'
```
Итак, у нас есть неизвестная функция `aimove()`, которая возвращает фигуру и место, куда её поставить, а мы затем помещаем эти данные в обычную функцию `move()`, словно ход сделали мы сами. В свою очередь в функции `aimove()` может быть что угодно. Можно сделать так, чтобы она выбирала рандомную фигуру и делала ей столь же рандомный ход:
```py
def aimove():
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j].endswith(AIteam): # Находим каждую фигуру компьютера
                emoves = canmove((i,j))
                for m in emoves:  # И все её возможные ходы добавляем в один большой список
                    moves.append(((i,j), (m[0],m[1])))
    if not moves:  # А это мы выходим в меню, если игра закончилась
        changemode('mainmenu')
        return (0,0), (0,0)
    return random.choice(moves) # Случайный ход
 ```
 Я пытался найти алгоритм, который мог бы рассчитывать возможные ходы (его называют шахматным движком, по крайней мере, это его часть), но ничего нет(( Так что останемся с нашим примитивным алгоритмом, улучшив его, чтобы тот мог есть фигуры:
 ```py
def aimove():
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i][j].endswith(AIteam):
                emoves = canmove((i,j))
                for m in emoves:
                    moves.append(((i,j), (m[0],m[1])))
    if not moves:
        changemode('mainmenu')
        return (0,0), (0,0)
        
    # Придаём фигурам веса, т.е. ценность для убийцы
    vs = {'Q': 90, 'K': 1000, 'B': 30, 'N': 30, 'R': 50, 'p': 10} 
    move = None
    value = 0
    for shape, pos in moves:
        if board[pos[0]][pos[1]]: # Ищем, можем ли мы убить какую-то фигуру
            if vs[board[pos[0]][pos[1]][0]] > value: # Если можем убить несколько фигур, надо выбрать самую ценную
                value = vs[board[pos[0]][pos[1]][0]] # Для этого находим максимальное значение
                move = (shape, pos)
        
    if not move: # Если мы не можем убить фигуру на этом ходу, играем на рандом
        return random.choice(moves)
    return move
 ```
 Если нажать на игру чёрными против ИИ, мы сразу увидим нечто подобное:
 ![image](https://user-images.githubusercontent.com/56085790/142875602-bd1da531-3235-493b-a9ee-30843ac5a7e6.png)
