"""
    Данный модуль осуществляет ролл кубиков
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


def roll_func_without_statistics(dice_string: str) -> str:
    """
    Данная функция осуществляет ролл кубика в любых произвольных видах в пределах нормальных значений бросков
    :param dice_string: строка ролла, по типу '3d6' или '10d10'
    :return: результат сложения бросков кубика
    """
    # Разбивает строку по разделителю d, где нулевой элемент это количество брошенных кубиков, а первый - количество
    # граней кубика

    try:  # проверяю корректность введенных данных

        # Должно получится 2 элемента. Нулевой индекс это количество кубиков, первый индекс это количество граней кубика
        # если к команде не дадут параметры, то тут будет исключение AttributeError т.к. к None будет метод split
        dice_list = dice_string.split(sep='d')

        # если элементы не равны двум, значит проблема с разделителем
        assert len(dice_list) == 2

        # кубики это числовые значения и если любое другое, то ValueError вылетит
        int(dice_list[0])
        int(dice_list[1])

        # количество кубиков не может быть меньше 1, а количество граней у кубика не может быть меньше 2
        assert int(dice_list[0]) >= 1
        assert int(dice_list[1]) >= 2

        # значения брошенных кубиков, как и их грани не могут быть дробными числами
        assert float(dice_list[0]) == int(dice_list[0])
        assert float(dice_list[1]) == int(dice_list[1])

        # слишком большое количество кубиков или их граней повесят программу
        if int(dice_list[0]) > 10000 or int(dice_list[1]) > 10000:
            return 'Большие числа в в гранях или количестве кубиков недопустимы'

    except (ValueError, AssertionError, AttributeError):  # если вылетает исключение, то данные некорректные
        return 'Кубик нужно кидать по образцу: !roll 3d6'

    result = 0  # инициализация результата

    # беру нулевой элемент из списка и использую его как количество бросков в виде range
    for dice in range(int(dice_list[0])):
        # бросаю каждый кубик отдельно (первый элемент) и добавляю его результат к сумме
        roll = random.randint(1, int(dice_list[1]))
        result += roll

    return str(result)
