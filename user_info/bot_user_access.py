"""
    Данный модуль полностью обрабатывает команду !infoaccess и отправляет в основной модуль bot_main
    строковую информацию для вывода боту. Модуль запрашивает у БД информацию и формирует из нее строковый ответ.
    Вывод выглядит в формате перечисления названий миров
"""
from settings_and_imports import *


def db_select_access(curs: sqlite3.Cursor) -> str:
    """
    Функция осуществяет запрос в БД получая кортежи с данными, а затем получает готовую строку путем отправки их
    в нижестоящую функцию
    :param curs: объект курсора
    :return: итоговая строка ответа бота
    """

    # Строка для запроса в БД. Миры, уровень доступа которых равен 0 не выводятся
    select_access = '''
    SELECT world_name, access_level
    FROM worlds
    WHERE access_level > 0
    '''
    # Запрос к БД и получения кортежей
    system_tuple = tuple(curs.execute(select_access).fetchall())

    # Запрос к нижестоящей функции и получение строки ответа
    system_ans = str_form_access(system_tuple)

    return system_ans


def str_form_access(sys_tuple: tuple) -> str:
    """
    Данная функция принимает кортеж из кортежей из на их основе, с помощью шаблонизатора, формирует строковый ответ
    :param sys_tuple: кортеж с данными
    :return: строковый ответ бота
    """
    message = 'Уровень доступа на мирах'

    # world[0] выводит название мира, а world[1] уровень доступа, от 1 до 3
    answer_access_temp = Template('''
    {{ message }}:
    {% for world in sys_tuple %}
        {{ '{} - доступ {}'.format(world[0], world[1]) }}
    {% endfor %}
    ''')

    answer_render_access = answer_access_temp.render(sys_tuple=sys_tuple, message=message)
    return answer_render_access
