"""Трехмерный лабиринт, (c) Sayfullin Ruslan.
Перемещайтесь по лабиринту и попытайтесь выбраться из него... в 3D!
"""

import copy, sys, os

# Задаем константы:
WALL = '#'
EMPTY = ' '
START = 'S'
EXIT = 'E'
BLOCK = chr(9617)    # Символ 9617 соответствует '░'
NORTH = 'NORTH'
SOUTH = 'SOUTH'
EAST = 'EAST'
WEST = 'WEST'


def wallStrToWallDict(wallStr):
    """Получает на входе строковое представление изображения стены
    (например, такое, как в ALL_OPEN и CLOSED) и возвращает ее представление
    в виде ассоциативного массива с кортежами (x, y) в роли ключей
    и строковых значений из одного символа для вывода на этой позиции x, y."""
    wallDict = {}
    height = 0
    width = 0
    for y, line in enumerate(wallStr.splitlines()):
        if y > height:
            height = y
        for x, character in enumerate(line):
            if x > width:
                width = x
            wallDict[(x, y)] = character
    wallDict['height'] = height + 1
    wallDict['width'] = width + 1
    return wallDict

EXIT_DICT = {(0, 0): 'E', (1, 0): 'X', (2, 0): 'I',
                (3, 0): 'T', 'height': 1, 'width': 4}

#   Строковые значения для отображения мы создаем путем преобразования
#   изображений в этих многострочных строковых значениях с помощью
#   wallStrToWallDict(). После чего формируем стенку для позиции
#   и направления движения игрока путем вставки ассоциативных массивов
#   стенок из CLOSED поверх ассоциативного массива стенки из ALL_OPEN.


ALL_OPEN = wallStrToWallDict(r'''
.................
____.........____
...|\......./|...
...||.......||...
...||__...__||...
...||.|\./|.||...
...||.|.X.|.||...
...||.|/.\|.||...
...||_/...\_||...
...||.......||...
___|/.......\|___
.................
.................'''.strip())
# Для удаления символа новой строки в начале этого многострочного
# строкового значения используется вызов strip().
CLOSED = {}
CLOSED['A'] = wallStrToWallDict(r'''
_____
.....
.....
.....
_____'''.strip()) # Вставляем на позиции 6, 4.
CLOSED['B'] = wallStrToWallDict(r'''
.\.
..\
...
...
...
../
./.'''.strip())  # Вставляем на позиции 4, 3.
CLOSED['C'] = wallStrToWallDict(r'''
___________
...........
    ...........
...........
...........
...........
...........
...........
...........
___________'''.strip())  # Вставляем на позиции 3, 1.
CLOSED['D'] = wallStrToWallDict(r'''
./.
/..
...
...
...
\..
.\.'''.strip()) # Вставляем на позиции 10, 3.
CLOSED['E'] = wallStrToWallDict(r'''
..\..
...\_
....|
....|
....|
....|
....|
....|
....|
....|
....|
.../.
../..'''.strip())   # Вставляем на позиции 0, 0.
CLOSED['F'] = wallStrToWallDict(r'''
../..
_/...
|....
|....
|....
|....
|....
|....
|....
|....
|....
.\...
..\..'''.strip())    # Вставляем на позиции 12, 0.


def displayWallDict(wallDict):
    """Отображаем на экране ассоциативный массив стенки,
    возвращаемый wallStrToWallDict()."""
    print(BLOCK * (wallDict['width'] + 2))
    for y in range(wallDict['height']):
        print(BLOCK, end='')
        for x in range(wallDict['width']):
            wall = wallDict[(x, y)]
            if wall == '.':
                wall = ' '
            print(wall, end='')
        print(BLOCK)     # Выводим блок с символом новой строки.
    print(BLOCK * (wallDict['width'] + 2))


def pasteWallDict(srcWallDict, dstWallDict, left, top):
    """Копируем ассоциативный массив представления стенки из
    srcWallDict поверх dstWallDict, смещенный до позиции left, top."""
    dstWallDict = copy.copy(dstWallDict)
    for x in range(srcWallDict['width']):
        for y in range(srcWallDict['height']):
            dstWallDict[(x + left, y + top)] = srcWallDict[(x, y)]
    return dstWallDict


def makeWallDict(maze, playerx, playery, playerDirection, exitx, exity):
    """Создаем ассоциативный массив представления стенки в соответствии
    с расположением и направлением движения игрока в лабиринте (с выходом
    в точке exitx, exity) путем вставки ассоциативных массивов
    стенок поверх ALL_OPEN и возвращаем его."""
    # "Сегменты" A — F (относительно направления движения игрока)
    # показывают, какие стены лабиринта необходимо проверить
    # на предмет необходимости добавить их поверх создаваемого нами
    # ассоциативного массива представления стенок.
    if playerDirection == NORTH:
        # Карта сегментов относительно  A
        # игрока @:                     BCD (игрок смотрит на север)
        #                               E@F
        offsets = (('A', 0, -2), ('B', -1, -1), ('C', 0, -1),
        ('D', 1, -1), ('E', -1, 0), ('F', 1, 0))

    if playerDirection == SOUTH:
        # Карта сегментов относительно  F@E
        # игрока @:                     DCB (игрок смотрит на юг)
        #                               A
        offsets = (('A', 0, 2), ('B', 1, 1), ('C', 0, 1),
        ('D', -1, 1), ('E', 1, 0), ('F', -1, 0))

    if playerDirection == EAST:
        # Карта сегментов относительно  EB
        # игрока @:                     @CA (игрок смотрит на восток)
        #                               FD
        offsets = (('A', 2, 0), ('B', 1, -1), ('C', 1, 0),
        ('D', 1, 1), ('E', 0, -1), ('F', 0, 1))

    if playerDirection == WEST:
        # Карта сегментов относительно  DF
        # игрока @:                     AC@ (игрок смотрит на запад)
        #                               BE
        offsets = (('A', -2, 0), ('B', -1, 1), ('C', -1, 0),
        ('D', -1, -1), ('E', 0, 1), ('F', 0, -1))

    section = {}
    for sec, xOff, yOff in offsets:
        section[sec] = maze.get((playerx + xOff, playery + yOff), WALL)
        if (playerx + xOff, playery + yOff) == (exitx, exity):
            section[sec] = EXIT

    wallDict = copy.copy(ALL_OPEN)
    PASTE_CLOSED_TO = {'A': (6, 4), 'B': (4, 3), 'C': (3, 1),
                        'D': (10, 3), 'E': (0, 0), 'F': (12, 0)}
    for sec in 'ABDCEF':
        if section[sec] == WALL:
            wallDict = pasteWallDict(CLOSED[sec], wallDict,
                PASTE_CLOSED_TO[sec][0], PASTE_CLOSED_TO[sec][1])

    # Рисуем знак EXIT при необходимости:
    if section['C'] == EXIT:
        wallDict = pasteWallDict(EXIT_DICT, wallDict, 7, 9)
    if section['E'] == EXIT:
        wallDict = pasteWallDict(EXIT_DICT, wallDict, 0, 11)
    if section['F'] == EXIT:
        wallDict = pasteWallDict(EXIT_DICT, wallDict, 13, 11)

    return wallDict


print('Maze Runner 3D, by Sayfullin Ruslan')
print('(Maze files are generated by mazemakerrec.py)')


# Получаем от пользователя название файла лабиринта:
while True:
    print('Enter the filename of the maze (or LIST or QUIT):')
    filename = input('> ')

    # Выводим список всех файлов лабиринтов в текущем каталоге:
    if filename.upper() == 'LIST':
        print('Maze files found in', os.getcwd())
        for fileInCurrentFolder in os.listdir():
            if (fileInCurrentFolder.startswith('maze')
            and fileInCurrentFolder.endswith('.txt')):
                print(' ', fileInCurrentFolder)
        continue

    if filename.upper() == 'QUIT':
        sys.exit()
    if os.path.exists(filename):
        break
    print('There is no file named', filename)


# Загружаем лабиринт из файла:
mazeFile = open(filename)
maze = {}
lines = mazeFile.readlines()
px = None
py = None
exitx = None
exity = None
y = 0
for line in lines:
    WIDTH = len(line.rstrip())
    for x, character in enumerate(line.rstrip()):
        assert character in (WALL, EMPTY, START, EXIT), 'Invalid character at column {}, line {}'.format(x + 1, y + 1)
        if character in (WALL, EMPTY):
            maze[(x, y)] = character
        elif character == START:
            px, py = x, y
            maze[(x, y)] = EMPTY
        elif character == EXIT:
            exitx, exity = x, y
            maze[(x, y)] = EMPTY
    y += 1
HEIGHT = y

assert px != None and py != None, 'No start point in file.'
assert exitx != None and exity != None, 'No exit point in file.'
pDir = NORTH


while True:     # Основной цикл игры.
    displayWallDict(makeWallDict(maze, px, py, pDir, exitx, exity))

    while True:  # Получаем ход пользователя.
        print('Location ({}, {}) Direction: {}'.format(px, py, pDir))
        print('                 (W)')
        print('Enter direction: (A) (D) or QUIT.')
        move = input('> ').upper()

        if move == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if (move not in ['F', 'L', 'R', 'W', 'A', 'D']
            and not move.startswith('T')):
            print('Please enter one of F, L, or R (or W, A, D).')
            continue

        # Передвигаем игрока в соответствии с желаемым ходом:
        if move == 'F' or move == 'W':
            if pDir == NORTH and maze[(px, py - 1)] == EMPTY:
                py -= 1
                break
            if pDir == SOUTH and maze[(px, py + 1)] == EMPTY:
                py += 1
                break
            if pDir == EAST and maze[(px + 1, py)] == EMPTY:
                px += 1
                break
            if pDir == WEST and maze[(px - 1, py)] == EMPTY:
                px -= 1
                break
        elif move == 'L' or move == 'A':
            pDir = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}[pDir]
            break
        elif move == 'R' or move == 'D':
            pDir = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}[pDir]
            break
        elif move.startswith('T'):  # Cheat code: 'T x,y'
            px, py = move.split()[1].split(',')
            px = int(px)
            py = int(py)
            break
        else:
            print('You cannot move in that direction.')

    if (px, py) == (exitx, exity):
        print('You have reached the exit! Good job!')
        print('Thanks for playing!')
        sys.exit()