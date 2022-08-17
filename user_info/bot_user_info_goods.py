"""
    Данный модуль обрабатывает команды !infoexportgoods и !infoimportgoods и отправляет в основной модуль bot_main
    строковую информацию для вывода боту. Модуль запрашивает у БД информацию и формирует из нее строковый ответ.
    Вывод выглядит в формате перечисления названий миров, покупающих или продающих данный товар
"""
from settings_and_imports import *
import user_info.sql_queries


def choise_deal_and_execute_in_db(curs: sqlite3.Cursor, goods_name: str, name_deal: str) -> str:
    """
    Данная функция выбирает тип сделки, экспорт или импорт, осуществляет экзекьют в базу данных и запрашивает строку у
    нижестоящей функции
    :param curs: объект курсора
    :param goods_name: название товара
    :param name_deal: название сделки, export или import
    :return: строка ответа боту
    """
    select_systems = None

    if name_deal == 'import':
        select_systems = form_import_query(goods_name)
    elif name_deal == 'export':
        select_systems = form_export_query(goods_name)

    tuple_with_worlds = tuple(curs.execute(select_systems))

    final_string = form_string_answer(tuple_with_worlds, name_deal)

    return final_string


def form_export_query(goods_name: str) -> str:
    """
    Данная функция формирует текст запроса в БД для сделки экспорта
    :param goods_name: название товара
    :return: строка для экзекьюта в БД
    """

    # Текст sql-запроса берется из модуля sql_queries
    select_temp_systems = Template(user_info.sql_queries.info_goods_query_dict['export'])
    select_render_systems = select_temp_systems.render(goods_name=goods_name)
    return select_render_systems


def form_import_query(goods_name: str) -> str:
    """
    Данная функция формирует текст запроса в БД для сделки импорта
    :param goods_name: название товара
    :return: строка для экзекьюта в БД
    """

    # Текст sql-запроса берется из модуля sql_queries
    select_temp_systems = Template(user_info.sql_queries.info_goods_query_dict['import'])
    select_render_systems = select_temp_systems.render(goods_name=goods_name)
    return select_render_systems


def form_string_answer(tuple_with_worlds: tuple, deal_name: str) -> str:
    """
    Данная функция формирует итоговую строку с помощью шаблонизатора для ответа ботом
    :param tuple_with_worlds: кортеж из кортежей. Во внутренних кортежах только 1 значение - название мира
    :param deal_name: название сделки, export или import
    :return: итоговая строка ответа бота
    """
    # В зависимости от типа сделки, первичное сообщение будет отличаться
    message = 'В данных системах покупают этот товар' if deal_name == 'import' else 'В данных система продают этот товар'

    # world[0] нужно, чтобы извлечь из кортежа единственный елемент и вставить его в строку с помощью шаблонизатора
    answer_systems_temp = Template('''
    {{ message }}:
    {% for world in sys_tuple %}
        {{ '{}'.format(world[0]) }}
    {% endfor %}
    ''')

    answer_render_systems = answer_systems_temp.render(sys_tuple=tuple_with_worlds, message=message)
    return answer_render_systems
