from settings_and_imports import *


def bot_user_info_controller_trade(bot_user_info_controller_system, name_deal):
    """
    Осуществляет вызовы функций SELECT-a и отправки сообщений ботом
    :param name_deal:
    :param bot_user_info_controller_system:
    :return:
    """
    db_name = 'infobot_db.db'
    abspath = get_script_dir() + path.sep + db_name  # Формирование абсолютного пути для файла базы данных
    db = sqlite3.connect(abspath)  # connect to sql base
    cursor = db.cursor()  # Creation sqlite cursor
    result = db_select_systems(cursor, bot_user_info_controller_system, name_deal)

    return result


def db_select_systems(curs, system_name, name_deal):
    select_systems = None

    if name_deal == 'import':
        select_systems = select_form_import(system_name)
    elif name_deal == 'export':
        select_systems = select_form_export(system_name)

    system_tuple = tuple(curs.execute(select_systems))
    system_ans = str_form_systems(system_tuple, name_deal)

    if system_tuple[0][2] != 3:
        system_ans = 'Недостаточный уровень доступа'

    return system_ans


def select_form_export(system_name):
    select_temp_systems = Template('''
    SELECT trade_export.export_name, (base_price * overproduction_multiplier * danger_multiplier_export),
    worlds.access_level
    FROM worlds
    INNER JOIN worlds_trade_export_relations ON worlds.world_name == worlds_trade_export_relations.world_name
    INNER JOIN trade_export ON worlds_trade_export_relations.export_name == trade_export.export_name
    INNER JOIN export_overproduction ON worlds.overproduction_name == export_overproduction. overproduction_name
    INNER JOIN danger_zone ON worlds.danger_name == danger_zone.danger_name
    WHERE worlds.world_name == '{{ system_name }}'
    ''')
    select_render_systems = select_temp_systems.render(system_name=system_name)
    return select_render_systems


def select_form_import(system_name):
    import_profit = 1.25

    select_temp_systems = Template('''
    SELECT trade_import.import_name, (base_price * need_multiplier * danger_multiplier_import * {{ import_profit }}),
    worlds.access_level
    FROM worlds
    INNER JOIN worlds_trade_import_relations ON worlds.world_name == worlds_trade_import_relations.world_name
    INNER JOIN trade_import ON worlds_trade_import_relations.import_name == trade_import.import_name
    INNER JOIN import_needs ON worlds.needs_name == import_needs.needs_name
    INNER JOIN danger_zone ON worlds.danger_name == danger_zone.danger_name
    WHERE worlds.world_name == '{{ system_name }}'
    ''')
    select_render_systems = select_temp_systems.render(system_name=system_name, import_profit=import_profit)
    return select_render_systems


def str_form_systems(sys_tuple, deal_name):
    message = 'Примерная цена покупки импортных товаров' if deal_name == 'import' else 'Примерная цена продажи товаров'

    answer_systems_temp = Template('''
    {{ message }}:
    {% for world in sys_tuple %}
        {{ '{} : {}'.format(world[0], world[1]) }}
    {% endfor %}
    ''')

    answer_render_systems = answer_systems_temp.render(sys_tuple=sys_tuple, message=message)
    return answer_render_systems
