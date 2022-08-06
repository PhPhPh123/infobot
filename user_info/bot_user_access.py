"""
    Данный модуль полностью обрабатывает команду !infoaccess и отправляет в основной модуль bot_main
    строковую информацию для вывода боту. Модуль запрашивает у БД информацию и формирует из нее строковый ответ.
    Вывод выглядит в формате перечисления названий миров
"""
from settings_and_imports import *


def form_tuple_in_db(alch_connect, alch_worlds) -> str:
    """
    Функция осуществляет запрос в БД через ORM получая кортежи с данными, а затем получает готовую строку путем отправки
    кортежа в нижестоящую функцию
    :param alch_worlds:
    :param alch_connect:
    :return: итоговая строка ответа бота
    """
    # Создание запроса к БД
    system_tuple_temp = sqlalchemy.sql.select(alch_worlds.c.world_name,
                                              alch_worlds.c.access_level).where(alch_worlds.c.access_level > 0)
    # Экзекьют в БД для получения кортежей
    system_tuple = tuple(alch_connect.execute(system_tuple_temp))

    # Запрос к нижестоящей функции и получение строки ответа
    system_ans = form_string_answer(system_tuple)

    return system_ans


def form_string_answer(sys_tuple: tuple) -> str:
    """
    Данная функция принимает кортеж из кортежей и на их основе, с помощью шаблонизатора, формирует строковый ответ
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
