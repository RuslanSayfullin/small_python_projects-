"""Гексагональная сетка, (c) Sayfullin Ruslan.
Выводит на экран мозаику в виде гексагональной сетки
"""

# Задаем константы:
# (!) Попробуйте изменить эти значения:
X_REPEAT = 19   # Количество ячеек по горизонтали.
Y_REPEAT = 12   # Количество ячеек по вертикали.

for y in range(Y_REPEAT):
    # Выводим верхнюю половину шестиугольника:
    for x in range(X_REPEAT):
        print(r'/ \_', end='')
    print()

    # Выводим нижнюю половину шестиугольника:
    for x in range(X_REPEAT):
        print(r'\_/ ', end='')
    print()
