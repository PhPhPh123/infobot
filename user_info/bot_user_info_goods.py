"""
    Данный модуль обрабатывает команды !infoexportgoods и !infoimportgoods и отправляет в основной модуль bot_main
    строковую информацию для вывода боту. Модуль запрашивает у БД информацию и формирует из нее строковый ответ.
    Вывод выглядит в формате перечисления названий миров, покупающих или продающих данный товар
"""
from settings_and_imports import *


def choise_deal_and_execute_in_db(curs: sqlite3.Cursor, good_name: str, name_deal: str) -> str:
    """
    Данная функция выбирает тип сделки, экспорт или импорт, осуществляет экзекьют в базу данных и запрашивает строку у
    нижестоящей функции
    :param curs: объект курсора
    :param good_name: название товара
    :param name_deal: название сделки
    :return: строка ответа боту
    """
    select_systems = None

    if name_deal == 'import':
        select_systems = select_form_import(good_name)
    elif name_deal == 'export':
        select_systems = select_form_export(good_name)

    system_tuple = tuple(curs.execute(select_systems))
    final_string = str_form_goods(system_tuple, name_deal)

    return final_string


def select_form_export(select_form_good_name: str) -> str:
    select_temp_systems = Template('''
    SELECT worlds.world_name
    FROM worlds
    INNER JOIN worlds_trade_export_relations ON worlds.world_name == worlds_trade_export_relations.world_name
    INNER JOIN trade_export ON worlds_trade_export_relations.export_name == trade_export.export_name
    WHERE trade_export.export_name == '{{ good_name }}' AND worlds.access_level == 3
    ''')
    select_render_systems = select_temp_systems.render(good_name=select_form_good_name)
    return select_render_systems


def select_form_import(select_form_good_name: str) -> str:
    select_temp_systems = Template('''
    SELECT worlds.world_name
    FROM worlds
    INNER JOIN worlds_trade_import_relations ON worlds.world_name == worlds_trade_import_relations.world_name
    INNER JOIN trade_import ON worlds_trade_import_relations.import_name == trade_import.import_name
    WHERE trade_import.import_name == '{{ good_name }}' AND worlds.access_level == 3
    ''')
    select_render_systems = select_temp_systems.render(good_name=select_form_good_name)
    return select_render_systems


def str_form_goods(sys_tuple: tuple, deal_name: str) -> str:
    message = 'В данных системах покупают этот товар' if deal_name == 'import' else 'В данных система продают этот товар'
    print(sys_tuple)
    answer_systems_temp = Template('''
    {{ message }}:
    {% for world in sys_tuple %}
        {{ '{}'.format(world[0]) }}
    {% endfor %}
    ''')

    answer_render_systems = answer_systems_temp.render(sys_tuple=sys_tuple, message=message)
    return answer_render_systems
