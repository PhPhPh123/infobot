"""
    Данный модуль полностью обрабатывает команду !infosystem *название системы* и отправляет в основной модуль bot_main
    строковую информацию для вывода боту. Работа модуля основываетсмя на приеме строки с выбранной системой,
    доступа в базу данных, формированию строки запросов по нескольким пунктам через шаблонизатор, получения из БД
    кортежей и формированию на их основе готового строкового ответа. Текст SQL-запроса берется из модуля sql_queries
"""
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


def to_control_other_functions_and_returns_bot_answer(system_name: str) -> str:
    """
    Данная функция осуществляет экзекьют в базу данных используя МЕЖМОДУЛЬНУЮ ГЛОБАЛЬНУЮ
    переменную курсора bd_sqlite3_cursor
    :param system_name: название системы
    :return: готовая строка для ответа со строкой, перечисляющей список миров в системе
    """
    # Формирование строки для запроса в БД
    select_systems = form_query_to_db(system_name)

    # Получение кортежа с данными
    system_tuple = tuple(global_bd_sqlite3_cursor.execute(select_systems))

    # Формирование строкового ответа для бота
    system_ans = form_string_answer(system_tuple)
    return system_ans


def form_query_to_db(select_form_systems_name: str) -> str:
    """
    Данная функция формирует строковый заброс в БД используя шаблорнизатор
    :param select_form_systems_name: название системы
    :return: строка для запроса в БД
    """
    select_temp_systems = Template('''
    SELECT worlds.world_name FROM worlds
    INNER JOIN systems_worlds_relations ON worlds.world_name == systems_worlds_relations.world_name
    INNER JOIN systems ON systems_worlds_relations.system_name == systems.system_name
    WHERE systems.system_name == '{{ system_name }}'
    ''')
    select_render_systems = select_temp_systems.render(system_name=select_form_systems_name)
    return select_render_systems


def form_string_answer(sys_tuple: tuple) -> str:
    """
    Данная функция формирует итоговую строку для ответа ботом
    :param sys_tuple: кортеж с кортежами по результатам работы БД
    :return: строка для ответа ботом
    """
    # Посколько это кортеж с кортежами, то извлекаем в цикле значение по нулевому индексу
    answer_systems_temp = Template('''
    Миры внутри системы:
    {% for world in sys_tuple %}
        {{ world[0] }}
    {% endfor %}
    ''')

    answer_render_systems = answer_systems_temp.render(sys_tuple=sys_tuple)

    if not sys_tuple:  # Если названия системы не существует то отправляем в чат сообщение об ошибки написания
        answer_render_systems = 'Некорректное название системы'
    return answer_render_systems


if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
