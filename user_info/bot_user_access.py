from settings_and_imports import *


def db_select_access(curs):
    select_access = '''
    SELECT world_name, access_level
    FROM worlds
    WHERE access_level > 0
    '''
    system_tuple = tuple(curs.execute(select_access).fetchall())
    system_ans = str_form_access(system_tuple)

    return system_ans


def str_form_access(sys_tuple):
    message = 'Уровень доступа на мирах'

    answer_access_temp = Template('''
    {{ message }}:
    {% for world in sys_tuple %}
        {{ '{} - доступ {}'.format(world[0], world[1]) }}
    {% endfor %}
    ''')

    answer_render_access = answer_access_temp.render(sys_tuple=sys_tuple, message=message)
    return answer_render_access
