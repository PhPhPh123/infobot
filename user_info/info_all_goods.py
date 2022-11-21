"""
    Данный модуль отвечает за обработку команды !infoallgoods и выводит список всех товаров, посколько для эспорта и
    импорта они аналогичны, то принято соглашение использовать экспортный список
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


def to_control_other_functions() -> str:
    """
    Данная функция реализует шаблон проектирования фасад и вызывает другие функции
    @return: строка ответа ботом
    """
    all_goods_tuple = execute_sql()
    final_string = form_string_answer(all_goods_tuple)
    return final_string


def execute_sql() -> tuple:
    """
    Данная функция осуществляет доступ в основную базу данных, на основе глобальной переменной курсора и формирует из
    нее кортеж со списком товаров
    @return: кортеж с кортежами товаров
    """
    sql_string = "SELECT export_name FROM trade_export WHERE export_name NOT IN ('Экспорт-отсутствует', 'Ваааааах!')"
    all_goods_tuple = tuple(global_bd_sqlite3_cursor.execute(sql_string))
    return all_goods_tuple


def form_string_answer(all_goods_tuple: tuple) -> str:
    """
    Данная функция формирует итоговою строку с ответом бота
    @param all_goods_tuple: кортеж с кортежами товаров
    @return: итоговая строка с ответом бота
    """
    final_str = ''
    for good in all_goods_tuple:
        # поскольку в общем кортеже идут, также, кортежи с одни значением, то его нужно изъять через good[0]
        final_str += f'{good[0]}\n'
    return final_str
