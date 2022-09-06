"""
    Данный модуль полностью обрабатывает команду !infoworld *название мира* и отправляет в основной модуль bot_main
    строковую информацию для вывода боту. Работа модуля основываетсмя на приеме строки с выбранным миром,
    доступа в базу данных, формированию строки запросов по нескольким пунктам через шаблонизатор, получения из БД
    кортежей и формированию на их основе готового строкового ответа. Текст SQL-запроса берется из модуля sql_queries
"""

from settings_imports_globalVariables import *
from user_info import sql_queries


def to_control_other_functions_and_returns_bot_answer(curs: sqlite3.Cursor, world_name: str) -> str:
    """
    Функция осуществляет контроль основых операций для получения итоговой строки которую отдает в модуль bot_main
    для исполнения функцией и выдачей ответа ботом:
    1 этап: получает строки для sql-запроса в БД через form-функции шаблонизаторы
    2 этап: с помощью экзекьюта в БД через курсор получает результат их работы в виде кортежей
    3 этап: формирует из кортежей единый словарь с помощью функции dict_form
    4 этап: получает итоговую строку с помощью функции str_form
    :param world_name: название мира
    :param curs: объект курсора sqllite3
    :return: готовая строка для ответа со всей информацией
    """
    # 1 этап
    select_main = form_query(world_name, 'worlds')
    select_terrains = form_query(world_name, 'terrains')
    select_enemies = form_query(world_name, 'enemies')
    select_export = form_query(world_name, 'export')
    select_import = form_query(world_name, 'import')

    # 2 этап
    tuple_with_worlds = tuple(curs.execute(select_main))
    if not tuple_with_worlds:  # Если название мира некорректно, то вернется пустой кортеж и нужно вернуть ответ
        return 'Некорректное название мира'
    tuple_with_terrains = tuple(curs.execute(select_terrains))
    tuple_with_enemies = tuple(curs.execute(select_enemies))
    tuple_with_export = tuple(curs.execute(select_export))
    tuple_with_import = tuple(curs.execute(select_import))

    # 3 этап
    final_dict = form_dict(tuple_with_worlds, tuple_with_terrains, tuple_with_enemies,
                           tuple_with_export, tuple_with_import)

    # 4 этап
    final_str = str_form(final_dict)

    return final_str


def form_query(world_name: str, sql_table: str) -> str:
    """
    Шаблонизаторная функция для формирования текста запросов. Функция берет основное тело запроса из модуля sql_queries
    :param sql_table: название таблички, для которой будет формироваться запрос
    :param world_name: название мира
    :return: строку для sql-экзекьюта в БД
    """
    format_name = '{{ name_world }}'  # Строка для вставки в шаблонизатор

    # Данная строка создает темплейт строки в который через format вставляет format_name для дальнейшего рендеринга
    select_temp_main = Template(sql_queries.info_main_query_dict[sql_table].format(format_name))

    # Рендерится строка, подставляя вместо name_world аргумент world_name, в котором строка с названием мира
    select_render_main = select_temp_main.render(name_world=world_name)

    return select_render_main


def form_dict(tuple_with_worlds: tuple, tuple_with_terrains: tuple, tuple_with_enemies: tuple,
              tuple_with_export: tuple, tuple_with_import: tuple) -> dict:
    """
    Данная функция создает из кортежей, полученных по результатам запросов в БД, один общий словарь
    :param tuple_with_worlds: кортеж из основного запроса в табличку worlds
    :param tuple_with_terrains: кортеж из запроса в табличку terrains
    :param tuple_with_enemies: кортеж из запроса в табличку enemies
    :param tuple_with_export: кортеж из запроса в табличку export
    :param tuple_with_import: кортеж из запросав табличку import
    :return: один готовый словарь
    """
    main_dict_keys = ('Наименование мира', 'Дополнительное описание', 'Уровень опасности', 'Имперский класс',
                      'Население', 'Имперская власть', 'Уровень доступа', 'Родительская система', 'Нужда в импорте',
                      'Экспортное перепроизводство')  # Список ключей для словаря

    # Здесь просто связываются ключ-значение т.к. у каждого ключа может быть лишь одно значение, у кортежа берется
    # индекс 0 потому что tuple_worlds это кортеж с одним значением
    worlds_dict = dict(zip(main_dict_keys, tuple_with_worlds[0]))

    # elem[0] используется везде для того, чтобы вытащить первое значение из элемента(elem) кортежа, так как сам elem
    # тоже является кортежем
    terrains_dict = {'Местность': [elem[0] for elem in tuple_with_terrains]}

    enemies_dict = {'Угроза врагов': [elem[0] for elem in tuple_with_enemies]}

    export_dict = {'Экспортные товары': [elem[0] for elem in tuple_with_export]}

    import_dict = {'Импортные товары': [elem[0] for elem in tuple_with_import]}

    # Объединение словарей в один
    final_dict = {**worlds_dict, **terrains_dict, **enemies_dict, **export_dict, **import_dict}

    return final_dict


def str_form(info_dict: dict) -> str:
    """
    Данная функция формирует на основе словаря строку-ответ. В зависимости от значения 'Уровень доступа'
    некоторые значения меняются на неизвестно т.к. уровень определяет уровень видимости этих значений. При нулевом
    уровне доступа ответ будет отрицательным и не выдаст ничего
    :param info_dict: основной словарь со всеми необходимыми значениями
    :return: итоговая строка-ответ для бота
    """

    if info_dict['Уровень доступа'] == 0:
        string_answer = 'Вам ничего не известно по этому миру'
    else:
        string_answer = f'''
Уровень доступа: {info_dict['Уровень доступа']}
Наименование мира: {info_dict['Наименование мира']}
Родительская система: {info_dict['Родительская система']}
Имперский класс: {info_dict['Имперский класс']}
Имперская власть: {info_dict['Имперская власть'] if info_dict['Уровень доступа'] > 1 else 'Неизвестно'}
Население: {info_dict['Население'] if info_dict['Уровень доступа'] > 1 else 'Неизвестно'}
Относительный уровень опасности: {info_dict['Уровень опасности']}
Угрожающие враги: {info_dict['Угроза врагов'] if info_dict['Уровень доступа'] > 1 else 'Неизвестно'}
Основные типы местности: {info_dict['Местность'] if info_dict['Уровень доступа'] > 1 else 'Неизвестно'}
Экспортные товары: {info_dict['Экспортные товары'] if info_dict['Уровень доступа'] > 2 else 'Неизвестно'}
Импортные товары: {info_dict['Импортные товары'] if info_dict['Уровень доступа'] > 2 else 'Неизвестно'}
Эспортное производство: {info_dict['Экспортное перепроизводство'] if info_dict['Уровень доступа'] > 2 else 'Неизвестно'}
Импортный дефицит: {info_dict['Нужда в импорте'] if info_dict['Уровень доступа'] > 2 else 'Неизвестно'}
Дополнительное описание и особенности: {info_dict['Дополнительное описание'] if info_dict['Уровень доступа'] > 2 else 'Неизвестно'}
    '''
    return string_answer
