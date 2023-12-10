"""

"""

import exceptions

if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


def to_control_other_functions_and_returns_bot_answer(good_name) -> str:
    """
    Данная функция реализует шаблон проектирования фасад и вызывает другие функции
    @good_name: название товара, по умолчанию 'all', это список всех товаров
    @return: строка ответа ботом
    """
    ingame_goods_tuple = execute_to_db(good_name)
    final_answer = form_string(ingame_goods_tuple)
    return final_answer


def execute_to_db(good_name) -> tuple:
    """
    Данная функция осуществляет доступ в основную базу данных, на основе глобальной переменной курсора и формирует из
    нее кортеж со списком товаров
    @return: кортеж с кортежами товаров
    """
    if good_name == 'all':
        sql_string = 'SELECT * FROM ingame_common_goods ORDER BY 1'
    else:
        sql_string = f"SELECT * FROM ingame_common_goods WHERE good_name == '{good_name}'"

    sql_tuple = tuple(global_main_db_cursor.execute(sql_string))

    return sql_tuple


def form_string(ingame_goods_tuple: tuple) -> str:
    ingame_goods_template = Template("""
{% for good in goods -%}
{{ good[0] }} Цена : {{ good[1]}}
{% endfor %} """)

    ingame_goods_render = ingame_goods_template.render(goods=ingame_goods_tuple)
    return ingame_goods_render
