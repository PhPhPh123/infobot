"""
    Данный модуль хранит функции подключения к базам данных. Его импортирует модуль imports_globalVariables.py который
    из формирует глобальные курсоры и коннекты к этим базам
"""

import sqlite3
import os
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException


def get_bot_dir() -> str:
    """
    Функция собирающая абсолютный путь к текущей директории
    :return: возвращает этот путь
    """
    abs_path = os.path.abspath(__file__)  # полный путь к файлу скрипта
    return os.path.dirname(abs_path)


def connect_sqlite(db_path, row_factory=False) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """
    Функция, которая подключается к базе данных и создает объекты курсора и коннекта, абсолютный путь берет из
    соответствующей функции
    :return: объекты курсора и коннекта
    """
    abspath = get_bot_dir() + os.path.sep + db_path  # Формирование вабсолютного пути для файла базы данных
    connect = sqlite3.connect(abspath)  # Подключение к базе данных

    if row_factory:
        connect.row_factory = sqlite3.Row

    cursor = connect.cursor()  # Создание курсора
    return cursor, connect
