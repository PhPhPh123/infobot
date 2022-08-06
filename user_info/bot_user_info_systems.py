"""
    Данный модуль полностью обрабатывает команду !infosystem *название системы* и отправляет в основной модуль bot_main
    строковую информацию для вывода боту. Работа модуля основываетсмя на приеме строки с выбранной системой,
    доступа в базу данных, формированию строки запросов по нескольким пунктам через шаблонизатор, получения из БД
    кортежей и формированию на их основе готового строкового ответа. Текст SQL-запроса берется из модуля sql_queries
"""
from settings_and_imports import *


def db_select_systems(curs: sqlite3.Cursor, system_name: str) -> str:
    select_systems = select_form_systems(system_name)
    system_tuple = tuple(curs.execute(select_systems))
    system_ans = str_form_systems(system_tuple)
    return system_ans


def select_form_systems(select_form_systems_name: str) -> str:
    select_temp_systems = Template('''
    SELECT worlds.world_name FROM worlds
    INNER JOIN systems_worlds_relations ON worlds.world_name == systems_worlds_relations.world_name
    INNER JOIN systems ON systems_worlds_relations.system_name == systems.system_name
    WHERE systems.system_name == '{{ system_name }}'
    ''')
    select_render_systems = select_temp_systems.render(system_name=select_form_systems_name)
    return select_render_systems


def str_form_systems(sys_tuple: tuple) -> str:
    answer_systems_temp = Template('''
    Миры внутри системы:
    {% for world in sys_tuple %}
        {{ world[0] }}
    {% endfor %}
    ''')

    answer_render_systems = answer_systems_temp.render(sys_tuple=sys_tuple)
    return answer_render_systems
