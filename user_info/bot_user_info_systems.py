from settings_and_imports import *


def db_select_systems(curs, system_name):
    select_systems = select_form_systems(system_name)
    system_tuple = tuple(curs.execute(select_systems))
    system_ans = str_form_systems(system_tuple)
    return system_ans


def select_form_systems(select_form_systems_name):
    select_temp_systems = Template('''
    SELECT worlds.world_name FROM worlds
    INNER JOIN systems_worlds_relations ON worlds.world_name == systems_worlds_relations.world_name
    INNER JOIN systems ON systems_worlds_relations.system_name == systems.system_name
    WHERE systems.system_name == '{{ system_name }}'
    ''')
    select_render_systems = select_temp_systems.render(system_name=select_form_systems_name)
    return select_render_systems


def str_form_systems(sys_tuple):
    answer_systems_temp = Template('''
    Миры внутри системы:
    {% for world in sys_tuple %}
        {{ world[0] }}
    {% endfor %}
    ''')

    answer_render_systems = answer_systems_temp.render(sys_tuple=sys_tuple)
    return answer_render_systems
