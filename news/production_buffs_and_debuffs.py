"""

"""


def form_production_changes_news() -> str:
    """

    Объект курсора bd_sqlite3_cursor и объект коннекта bd_sqlite3_connect это МЕЖМОДУЛЬНЫЕ ГЛОБАЛЬНЫЕ переменные:
    :return: строка ответа ботом
    """
    # 1 этап
    chosen_world = select_world(bd_sqlite3_cursor)

    # 2 этап
    update_access = form_update_string(chosen_world)
    bd_sqlite3_cursor.execute(update_access)
    bd_sqlite3_connect.commit()

    # 3 этап
    access_responce = form_string_answer(chosen_world)
    return access_responce
