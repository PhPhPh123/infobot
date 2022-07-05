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
    :param args:
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

    tuple_main = curs.execute(select_main)
    tuple_terrains = curs.execute(select_terrains)
    tuple_enemies = curs.execute(select_enemies)
    tuple_export = curs.execute(select_export)
    tuple_import = curs.execute(select_import)

    print(tuple_main)
    return final_string


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


def str_form(str_form_main, str_form_terrains):
    pass