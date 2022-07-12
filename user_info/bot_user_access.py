from settings_and_imports import *


def bot_user_info_controller_access():
    """
    Осуществляет вызовы функций SELECT-a и отправки сообщений ботом
    :return:
    """
    db_name = 'infobot_db.db'
    abspath = get_script_dir() + path.sep + db_name  # Формирование абсолютного пути для файла базы данных
    db = sqlite3.connect(abspath)  # connect to sql base
    cursor = db.cursor()  # Creation sqlite cursor
    result = db_select_access(cursor)

    return result


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
