from settings_and_imports import *


def access_main_news(curs, db):

    chosen_world = select_world(curs)

    update_access = update_access_granted_form(chosen_world)
    curs.execute(update_access)
    db.commit()

    access_responce = access_responce_form(chosen_world)
    return access_responce


def select_world(curs):
    access_select_string = '''
    SELECT world_name FROM worlds 
    WHERE access_level < 3
    ORDER BY RANDOM()
    LIMIT 1
    '''
    selected_world = tuple(curs.execute(access_select_string))[0][0]
    return selected_world


def update_access_granted_form(world):
    update_access_temp = Template('''
    UPDATE worlds
    SET access_level =+ 1
    WHERE world_name == '{{ world }}'
    ''')
    update_access_render = update_access_temp.render(world=world)
    return update_access_render


def access_responce_form(world):
    responce_access_list = [f'''
Невероятная удача! Приняты астропатические данные о информационном доступе к миру {world}.
Уровень доступа повышен на 1''',
                            f'''
Один из членов команды нашел на корабле кем то случайно оставленный планшет с данными по миру {world}.
Уровень доступа повышен на 1''',
                            f'''
Хорошие новости! Информационно-логическая система проанализировала астропатические данные в субсекторе и смогла
собрать дополнительные данные по миру {world}.Уровень доступа повышен на 1''']
    return random.choice(responce_access_list)
