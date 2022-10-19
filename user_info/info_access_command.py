"""
    Данный модуль полностью обрабатывает команду !infoaccess и отправляет в основной модуль bot_main
    строковую информацию для вывода боту. Модуль запрашивает у БД информацию и формирует из нее строковый ответ.
    Вывод выглядит в формате перечисления названий миров
"""
import openpyxl

from settings_imports_globalVariables import *


def form_tuple_in_db() -> str:
    """
    Функция осуществляет запрос в БД через ORM sqlalchemy объект которой является ГЛОБАЛЬНОЙ МЕЖМОДУЛЬНОЙ ПЕРЕМЕННОЙ,
    которые затем передает в нижестоящие функции, преобразующие их в списки и добавляющие иные данные, а потом
    функция возвращает результат в виде готового ответа ботом
    :return: итоговая строка ответа бота
    """
    # Создание запроса к БД
    access_tuple_temp = sqlalchemy.sql.select(alch_world.c.world_name,
                                              alch_world.c.access_level).where(alch_world.c.access_level > 0)
    # Экзекьют в БД для получения кортежей
    access_tuple = tuple(alch_connect.execute(access_tuple_temp))

    # Отправка кортежа из кортежей для формирования из него списка из списков и добавления во вложенные списки данных
    # о родительских системах миров
    access_list = form_list_and_add_system(access_tuple)

    # Запрос к нижестоящей функции и получение строки ответа
    access_ans = form_string_answer(access_list)

    return access_ans


def form_list_and_add_system(access_tuple: tuple) -> list:
    """
    Данная фунция формирует из кортежа с кортежами список со списками, добавляет во вложенные списки информацию о
    системе, к которой относятся отобранные миры и сортирует список по ключу - названию системы в алфавитном порядке
    :param access_tuple: кортеж с кортежами в котором первом элементом идет название мира, а вторым - уровень доступа
    :return: список со списками с добавлением в каждый вложенный список элементом [2] название системы
    """

    access_list_with_lists = []  # Пустой список, в который будут добавляться списки из кортежа с кортежами

    # Создаю из кортежа с кортежами список со списками
    for tuple_elem in access_tuple:
        access_list_with_lists.append(list(tuple_elem))

    # Итерация, в которой изменяются вложенные списки
    for list_elem in access_list_with_lists:
        world_name = list_elem[0]  # Получаю название мира из текущего вложенного списка, чтобы использовать его для
        # запроса в бд и определения связанной с ним системы(в которой он находится)

        # Вызываю функцию, которая добавит в текущий вложенный список связанную с ним систему, которая отбирается в
        # вызываемой функции
        list_elem.append(select_system(world_name))

    # Создаю новый отсортированный список по ключу - названию системы в алфавитном порядке elem[2]
    sorted_access_list_with_lists = sorted(access_list_with_lists, key=lambda elem: elem[2])

    return sorted_access_list_with_lists


def select_system(world_name: str) -> str:
    """
    Данная функция производит запрос в БД с целью отбора систем, связанных с переданным миром
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    :param world_name: название мира
    :return: название системы
    """

    selected_system = tuple(bd_sqlite3_cursor.execute(f"""
    SELECT systems.system_name FROM systems
    INNER JOIN systems_worlds_relations ON systems.system_name == systems_worlds_relations.system_name
    INNER JOIN worlds ON systems_worlds_relations.world_name == worlds.world_name
    WHERE worlds.world_name == '{world_name}'
    """))[0][0]  # [0][0] нужно, чтобы извлечь название системы из кортежа с кортежами

    return selected_system


def form_string_answer(access_list: list) -> str:
    """
    Данная функция принимает список из списков и на их основе, с помощью шаблонизатора, формирует строковый ответ    
    :param access_list: список со списками, вложенный список которого, представляет собой 
    [0] - название системы
    [1] - уровень доступа
    [2] - родительская система
    :return: строковый ответ бота
    """
    # Сообщение, которое выводится 1 раз в начале строки ответа бота
    message = 'Уровень доступа на мирах'

    # world[0] выводит название мира, а world[1] уровень доступа, от 1 до 3
    wb = openpyxl.Workbook()
    sheet = wb['Sheet']
    for world in access_list:
        sheet.append(world)
    wb.save('access.xlsx')

    # answer_access_temp = Template('''
    # {{ message }}:
    # {% for world in sys_tuple -%}
    #     {{ '{} - доступ {}. Родительская система: {}'.format(world[0], world[1], world[2]) }}
    # {% endfor %}
    # ''')
    #
    # answer_render_access = answer_access_temp.render(sys_tuple=access_list, message=message)
    # return answer_render_access
