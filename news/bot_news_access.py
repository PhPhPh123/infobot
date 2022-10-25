"""
    Данный модуль формирует новости, связанные с повышением уровня доступа в случайном мире и возвращает строку
    в управляющий модуль bot_news_main
"""
from settings_imports_globalVariables import *
import exceptions


def control_other_func() -> str:
    """
    Данная функция управляет остальными функция и осуществляет их работу в 3 этапа:
    1 этап это выбор случайного мира, в котором будет повышаться уровень доступа
    2 этап это update в базу данных и изменение параметра уровень доступа для этого мира
    3 этап это формирование строкового ответа для ответа ботом

    Объект курсора bd_sqlite3_cursor и объект коннекта bd_sqlite3_connect это МЕЖМОДУЛЬНЫЕ ГЛОБАЛЬНЫЕ переменные:
    :return: строка ответа ботом
    """
    # 1 этап
    chosen_world = select_world(global_bd_sqlite3_cursor)

    # 2 этап
    update_access = form_update_string(chosen_world)
    global_bd_sqlite3_cursor.execute(update_access)
    global_bd_sqlite3_connect.commit()

    # 3 этап
    access_responce = form_string_answer(chosen_world)
    return access_responce


def select_world(curs: sqlite3.Cursor) -> str:
    """
    Данная функция выбирает случайный мир, в котором будет повышен уровень доступа
    :param curs: объект курсора
    :return: название мира в виде строки
    """
    # Данный селект выбирает мир, в котором уровень доступа меньше 3 (т.е. в котором есть смысл его повышать)
    # мир выбирается случайно функцией рандом и лимитируется 1 значением
    access_select_string = '''
    SELECT world_name FROM worlds 
    WHERE access_level < 3
    ORDER BY RANDOM()
    LIMIT 1
    '''
    # [0][0] нужно, чтобы извлеч из кортежа с кортежом элемент с названием мира
    selected_world = tuple(curs.execute(access_select_string))[0][0]
    return selected_world


def form_update_string(world: str) -> str:
    """
    Данная функция формирует строку для аптейда в БД с помощью шаблонизатора
    :param world: название мира
    :return: строка для аптейда в БД
    """
    update_access_temp = Template('''
    UPDATE worlds
    SET access_level =+ 1
    WHERE world_name == '{{ world }}'
    ''')
    update_access_render = update_access_temp.render(world=world)
    return update_access_render


def form_string_answer(world: str) -> str:
    """
    Данная функция случайно выбирает один из ответов, вставляю туда название мира и отправляя ответ для вывода
    в чат ботом
    :param world: название мира
    :return: строка итогового ответа
    """
    responce_access_list = [f'''
[ПОВЫШЕНИЕ УРОВНЯ ДОСТУПА] Невероятная удача! Приняты астропатические данные о информационном доступе к миру {world}.
 Уровень доступа повышен на 1''',
                            f'''
[ПОВЫШЕНИЕ УРОВНЯ ДОСТУПА] Один из членов команды нашел на корабле кем то случайно оставленный планшет с 
данными по миру {world}. Уровень доступа повышен на 1''',
                            f'''
[ПОВЫШЕНИЕ УРОВНЯ ДОСТУПА] Хорошие новости! Информационно-логическая система проанализировала астропатические данные 
в субсекторе и смогла собрать дополнительные данные по миру {world}. Уровень доступа повышен на 1''']
    return random.choice(responce_access_list)


if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
