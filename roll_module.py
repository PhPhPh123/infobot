"""
    Данный модуль осуществляет ролл кубиков
"""
from settings_and_imports import *


def roll_func(dice_string):
    """
    Данная функция осуществляет ролл кубика
    :param dice_string: строка ролла, по типу '3d6' или '10d10'
    :return: результат сложения бросков кубика
    """
    # Разбивает строку по разделителю d, где нулевой индекс это количество брошенных кубиков, а первый - количество
    # граней кубика
    dice_list = dice_string.split(sep='d')
    result = 0  # инициализация результата

    # беру нулевой индекс и использую его как количество бросков в виде range
    for dice in range(int(dice_list[0])):
        # бросаю каждый кубик отдельно и добавляю его результат к сумме
        roll = random.randint(1, int(dice_list[1]))
        result += roll

    return result
