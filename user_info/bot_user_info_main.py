"""
Данный модуль полностью обрабатывает и отправляет в основной модуль bot_main строковую информацию для вывода боту.
Работа модуля основываетсмя на приеме строки с выбранным миром, доступа в базу данных, формированию строки запросов по
нескольким пунктам через шаблонизатор, получения из БД кортежей и формированию на их основе готового строкового ответа
"""

from settings_and_imports import *
from . import sql_queries


def returns_string_for_infoworld_command(world_name: str) -> str:
    """
    Функция, которая подключается к базе данных, вызывает нижестоящие функции для формирования итогового ответа
    и возвращает его в вышестоящий модуль и функцию
    :param world_name: название мира
    :return: готовая строка, для отправки ботом в чате в вышестоящем модуле и функции
    """
    db_name = 'infobot_db.db'
    abspath = get_script_dir() + path.sep + db_name  # Формирование абсолютного пути для файла базы данных
    db = sqlite3.connect(abspath)  # Подключение к базе данных
    cursor = db.cursor()  # Создание курсора

    bot_answer = to_control_other_functions(cursor, world_name)

    return bot_answer


def to_control_other_functions(curs: sqlite3.Cursor, world_name: str) -> str:
    """
    Функция осуществляет контроль основых операций для получения итоговой строки:
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
    tuple_worlds = tuple(curs.execute(select_main))
    tuple_terrains = tuple(curs.execute(select_terrains))
    tuple_enemies = tuple(curs.execute(select_enemies))
    tuple_export = tuple(curs.execute(select_export))
    tuple_import = tuple(curs.execute(select_import))

    # 3 этап
    final_dict = form_dict(tuple_worlds, tuple_terrains, tuple_enemies, tuple_export, tuple_import)

    # 4 этап
    final_str = str_form(final_dict)

    return final_str


def form_query(world_name: str, sql_table: str) -> str:
    """
    Шаблонизаторная функция для формирования текста запросов. Функция берет основное тело запроса из модуля sql_queties
    :param sql_table: название таблички, для которой будет формироваться запрос
    :param world_name: название мира
    :return: строку для sql-экзекьюта в БД
    """
    format_name = '{{ name_world }}'  # Строка для вставки в шаблонизатор

    # Данная строка создает темплейт строки в который через format вставляет format_name для дальнейшего рендеринга
    select_temp_main = Template(sql_queries.info_main_query_dict[sql_table].format(format_name))

    # Рендериться строка, подставляя вместо name_world аргумент world_name, в котором строка с названием мира
    select_render_main = select_temp_main.render(name_world=world_name)

    return select_render_main


def form_dict(tuple_worlds, tuple_terrains, tuple_enemies, tuple_export, tuple_import):
    """
    Данная функция создает из кортежей, полученных по результатам запросов в БД, один общий словарь
    :param tuple_worlds: кортеж из основного запроса в табличку worlds
    :param tuple_terrains: кортеж из запроса в табличку terrains
    :param tuple_enemies: кортеж из запроса в табличку enemies
    :param tuple_export: кортеж из запроса в табличку export
    :param tuple_import: кортеж из запросав табличку import
    :return: один готовый словарь
    """
    main_dict_keys = ('Наименование мира', 'Дополнительное описание', 'Уровень опасности', 'Имперский класс',
                      'Население', 'Имперская власть', 'Уровень доступа', 'Родительская система', 'Нужда в импорте',
                      'Экспортное перепроизводство')  # Список ключей для словаря

    # Сдесь просто связываются ключ-значение т.к. у каждого ключа может быть лишь одно значение, у кортежа берется
    # индекс 0 потому что это кортеж с одним значением
    worlds_dict = dict(zip(main_dict_keys, tuple_worlds[0]))

    # elem[0] используется везде для того, чтобы вытащить первое значение из элемента(elem) кортежа, так как сам elem
    # тоже является кортежем
    terrains_dict = {'Местность': [elem[0] for elem in tuple_terrains]}

    enemies_dict = {'Угроза врагов': [elem[0] for elem in tuple_enemies]}

    export_dict = {'Экспортные товары': [elem[0] for elem in tuple_export]}

    import_dict = {'Импортные товары': [elem[0] for elem in tuple_import]}

    # Объединение словарей в один
    final_dict = {**worlds_dict, **terrains_dict, **enemies_dict, **export_dict, **import_dict}

    return final_dict


def str_form(str_form_dict):
    """
    :param str_form_dict:
    :return:
    """
    answer = f'''
Уровень доступа: {str_form_dict['Уровень доступа']}
Наименование мира: {str_form_dict['Наименование мира']}
Родительская система: {str_form_dict['Родительская система']}
Имперский класс: {str_form_dict['Имперский класс']}
Имперская власть: {str_form_dict['Имперская власть'] if str_form_dict['Уровень доступа'] > 1 else 'Неизвестно'}
Население: {str_form_dict['Население'] if str_form_dict['Уровень доступа'] > 1 else 'Неизвестно'}
Относительный уровень опасности: {str_form_dict['Уровень опасности']}
Угрожающие враги: {str_form_dict['Угроза врагов'] if str_form_dict['Уровень доступа'] > 1 else 'Неизвестно'}
Основные типы местности: {str_form_dict['Местность'] if str_form_dict['Уровень доступа'] > 1 else 'Неизвестно'}
Экспортные товары: {str_form_dict['Экспортные товары'] if str_form_dict['Уровень доступа'] > 2 else 'Неизвестно'}
Импортные товары: {str_form_dict['Импортные товары'] if str_form_dict['Уровень доступа'] > 2 else 'Неизвестно'}
Эспортное производство: {str_form_dict['Экспортное перепроизводство'] if str_form_dict['Уровень доступа'] > 2 else 'Неизвестно'}
Импортный дефицит: {str_form_dict['Нужда в импорте'] if str_form_dict['Уровень доступа'] > 2 else 'Неизвестно'}
Дополнительное описание и особенности: {str_form_dict['Дополнительное описание'] if str_form_dict['Уровень доступа'] > 2 else 'Неизвестно'}
    '''
    if str_form_dict['Уровень доступа'] == 0:
        answer = 'Вам ничего не известно по этому миру'
    return answer
