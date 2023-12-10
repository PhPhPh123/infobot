"""
    Данный модуль отвечает за запись информации о проведении игровых сессий для последующей обработки этих данных и
    вывода статистики
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from imports_globalVariables import *


def control_writing(game_hours):

    game_hours, if_error_message = verify_data(game_hours)
    write_statistics(game_hours)
    return if_error_message


def verify_data(game_hours):
    try:
        game_hours = int(game_hours)
        return game_hours, None

    except (ValueError, TypeError):
        return None, 'Игровые часы должны быть целым числом больше 0'


def write_statistics(game_hours) -> None:
    query_string = f"""
    INSERT INTO sessions (session_timestamp, session_hours)
    VALUES (datetime('now'), {game_hours})
    """
    global_game_sessions_cursor.execute(query_string)
    global_game_sessions_connect.commit()
