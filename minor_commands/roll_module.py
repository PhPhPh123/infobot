"""
    Данный модуль осуществляет ролл кубиков
"""
import string

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


def roll_func(dice_string: str) -> str:
    """
    Проблемы:
    1)Нет метода lower для разделителя
    2)Нет вывода об неправильном вводе
    3)Большие числа вешают программу, нужна проверка на макс число
    4)Отсутствие связей с реальной логикой
    5)Воспринимает отрицательные числа


    Данная функция осуществляет ролл кубика
    :param dice_string: строка ролла, по типу '3d6' или '10d10'
    :return: результат сложения бросков кубика
    """
    # Разбивает строку по разделителю d, где нулевой элемент это количество брошенных кубиков, а первый - количество
    # граней кубика

    try:  # проверяю корректность введенных данных
        dice_list = dice_string.split(sep='d')

        assert len(dice_list) == 2
        assert dice_string
        int(dice_list[0])
        int(dice_list[1])
    except (ValueError, AssertionError, AttributeError):  # если вылетает исключение, то данные некорректные
        return 'Кубик нужно кидать по образцу: !roll 3d6'

    result = 0  # инициализация результата

    # беру нулевой элемент из списка и использую его как количество бросков в виде range
    for dice in range(int(dice_list[0])):
        # бросаю каждый кубик отдельно (первый элемент) и добавляю его результат к сумме
        roll = random.randint(1, int(dice_list[1]))
        result += roll

    return str(result)


