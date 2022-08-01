from settings_and_imports import *


def db_select_goods(curs, db_select_good_name, name_deal):
    select_systems = None

    if name_deal == 'import':
        select_systems = select_form_import(db_select_good_name)
    elif name_deal == 'export':
        select_systems = select_form_export(db_select_good_name)

    system_tuple = tuple(curs.execute(select_systems))
    system_ans = str_form_goods(system_tuple, name_deal)

    return system_ans


def select_form_export(select_form_good_name):
    select_temp_systems = Template('''
    SELECT worlds.world_name
    FROM worlds
    INNER JOIN worlds_trade_export_relations ON worlds.world_name == worlds_trade_export_relations.world_name
    INNER JOIN trade_export ON worlds_trade_export_relations.export_name == trade_export.export_name
    WHERE trade_export.export_name == '{{ good_name }}' AND worlds.access_level == 3
    ''')
    select_render_systems = select_temp_systems.render(good_name=select_form_good_name)
    return select_render_systems


def select_form_import(select_form_good_name):
    select_temp_systems = Template('''
    SELECT worlds.world_name
    FROM worlds
    INNER JOIN worlds_trade_import_relations ON worlds.world_name == worlds_trade_import_relations.world_name
    INNER JOIN trade_import ON worlds_trade_import_relations.import_name == trade_import.import_name
    WHERE trade_import.import_name == '{{ good_name }}' AND worlds.access_level == 3
    ''')
    select_render_systems = select_temp_systems.render(good_name=select_form_good_name)
    return select_render_systems


def str_form_goods(sys_tuple, deal_name):
    message = 'В данных системах покупают этот товар' if deal_name == 'import' else 'В данных система продают этот товар'
    print(sys_tuple)
    answer_systems_temp = Template('''
    {{ message }}:
    {% for world in sys_tuple %}
        {{ '{}'.format(world[0]) }}
    {% endfor %}
    ''')

    answer_render_systems = answer_systems_temp.render(sys_tuple=sys_tuple, message=message)
    return answer_render_systems
