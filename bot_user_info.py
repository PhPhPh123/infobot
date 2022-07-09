from settings_and_imports import *


def get_script_dir() -> str:
    """
    Функция собирающая абсолютный путь к текущей директории
    :return: возвращает этот путь
    """
    abs_path = path.abspath(__file__)  # полный путь к файлу скрипта
    return path.dirname(abs_path)


def bot_user_info_controller(bot_user_info_controller_world):
    """
    Осуществляет вызовы функций SELECT-a и отправки сообщений ботом
    :param bot_user_info_controller_world:
    :return:
    """
    db_name = 'infobot_db.db'
    abspath = get_script_dir() + path.sep + db_name  # Формирование абсолютного пути для файла базы данных
    db = sqlite3.connect(abspath)  # connect to sql base
    cursor = db.cursor()  # Creation sqlite cursor

    result = db_select(cursor, bot_user_info_controller_world)
    return result


def db_select(curs, db_select_world):
    """
    Осуществляет SELECT запрос на основе данных переданных из контроллера
    :param db_select_world:
    :param curs:
    :return:
    """
    select_main = select_form_main(db_select_world)
    select_terrains = select_form_terrains(db_select_world)
    select_enemies = select_form_enemies(db_select_world)
    select_export = select_form_exports(db_select_world)
    select_import = select_form_import(db_select_world)

    tuple_main = tuple(curs.execute(select_main))
    tuple_terrains = tuple(curs.execute(select_terrains))
    tuple_enemies = tuple(curs.execute(select_enemies))
    tuple_export = tuple(curs.execute(select_export))
    tuple_import = tuple(curs.execute(select_import))

    final_dict = dict_form(tuple_main, tuple_terrains, tuple_enemies, tuple_export, tuple_import)
    final_str = str_form(final_dict)

    return final_str


def select_form_main(select_form_world):
    """
    Формирует текст с помощью шаблонизатора jinja для передачи в db_select
    :param select_form_world:
    :return:
    """
    select_temp_main = Template("""
    SELECT * FROM worlds WHERE worlds.world_name == '{{name_world}}'
    """)
    select_render_main = select_temp_main.render(name_world=select_form_world)
    return select_render_main


def select_form_terrains(select_form_world):
    select_temp_terrains = Template("""
    SELECT terrains.terrain_name FROM worlds
    INNER JOIN worlds_terrains_relations ON worlds.world_name==worlds_terrains_relations.world_name
    INNER JOIN terrains ON worlds_terrains_relations.terrain_name==terrains.terrain_name
    WHERE worlds.world_name =='{{name_world}}'
    """)
    select_render_terrains = select_temp_terrains.render(name_world=select_form_world)
    return select_render_terrains


def select_form_enemies(select_form_world):
    select_temp_enemies = Template("""
    SELECT enemies.enemy_name FROM worlds
    INNER JOIN worlds_enemies_relations ON worlds.world_name==worlds_enemies_relations.world_name
    INNER JOIN enemies ON worlds_enemies_relations.enemy_name==enemies.enemy_name
    WHERE worlds.world_name =='{{name_world}}'
    """)
    select_render_enemies = select_temp_enemies.render(name_world=select_form_world)
    return select_render_enemies


def select_form_exports(select_form_world):
    select_temp_export = Template("""
    SELECT trade_export.export_name FROM worlds
    INNER JOIN worlds_trade_export_relations ON worlds.world_name==worlds_trade_export_relations.world_name
    INNER JOIN trade_export ON worlds_trade_export_relations.export_name==trade_export.export_name
    WHERE worlds.world_name =='{{name_world}}'
    """)
    select_render_export = select_temp_export.render(name_world=select_form_world)
    return select_render_export


def select_form_import(select_form_world):
    select_temp_import = Template("""
    SELECT trade_import.import_name FROM worlds
    INNER JOIN worlds_trade_import_relations ON worlds.world_name==worlds_trade_import_relations.world_name
    INNER JOIN trade_import ON worlds_trade_import_relations.import_name==trade_import.import_name
    WHERE worlds.world_name =='{{name_world}}'
    """)
    select_render_import = select_temp_import.render(name_world=select_form_world)
    return select_render_import


def dict_form(dict_form_main, dict_form_terrains, dict_form_enemies, dict_form_export, dict_form_import):
    main_dict_keys = ('Наименование мира', 'Дополнительное описание', 'Уровень опасности', 'Имперский класс',
                      'Население', 'Имперская власть', 'Уровень доступа')
    print(tuple(dict_form_main))
    main_dict = dict(zip(main_dict_keys, dict_form_main[0]))

    terrains_dict = {'Местность': [elem[0] for elem in dict_form_terrains]}

    enemies_dict = {'Угроза врагов': [elem[0] for elem in dict_form_enemies]}

    export_dict = {'Экспортные товары': [elem[0] for elem in dict_form_export]}

    import_dict = {'Импортные товары': [elem[0] for elem in dict_form_import]}

    for dict_elem in terrains_dict, enemies_dict, export_dict, import_dict:
        main_dict.update(dict_elem)

    return main_dict


def str_form(str_form_dict):
    """
    :param str_form_dict:
    :return:
    """
    answer = f'''
    Уровень доступа: {str_form_dict['Уровень доступа']}
    Наименование мира: {str_form_dict['Наименование мира'] if str_form_dict['Уровень доступа'] > 0 else 'Неизвестно'}
    Имперский класс: {str_form_dict['Имперский класс']}
    Имперская власть: {str_form_dict['Имперская власть']}
    Население: {str_form_dict['Население'] if str_form_dict['Уровень доступа'] > 1 else 'Неизвестно'}
    Относительный уровень опасности: {str_form_dict['Уровень опасности']}
    Угрожающие враги: {str_form_dict['Угроза врагов'] if str_form_dict['Уровень доступа'] > 1 else 'Неизвестно'}
    Основные типы местности: {str_form_dict['Местность'] if str_form_dict['Уровень доступа'] > 1 else 'Неизвестно'}
    Экспортные товары: {str_form_dict['Экспортные товары'] if str_form_dict['Уровень доступа'] > 2 else 'Неизвестно'}
    Импортные товары: {str_form_dict['Импортные товары'] if str_form_dict['Уровень доступа'] > 2 else 'Неизвестно'}
    Дополнительное описание и особенности: {str_form_dict['Дополнительное описание'] if str_form_dict['Уровень доступа'] > 2 else 'Неизвестно'}
    '''
    if str_form_dict['Уровень доступа'] == 0:
        answer = 'Вам ничего не известно по этому миру'
    return answer
