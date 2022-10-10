import random

import pytest
import os
import sqlite3


def get_bot_dir() -> str:
    """
    Функция собирающая абсолютный путь к текущей директории
    :return: возвращает этот путь
    """
    abs_path = os.path.abspath(__file__)  # полный путь к файлу скрипта
    return os.path.dirname(abs_path)


@pytest.fixture(scope='session')
def connect_to_db_sqlite3() -> sqlite3.Cursor:
    """
    Функция, которая подключается к базе данных и создает объекты курсора и коннекта, абсолютный путь берет из файла
    настроек
    :return: объекты курсора и коннекта
    """
    db_name = 'base_for_testing.db'
    abspath = get_bot_dir() + os.path.sep + db_name  # Формирование абсолютного пути для файла базы данных
    connect = sqlite3.connect(abspath)  # Подключение к базе данных
    cursor = connect.cursor()  # Создание курсора
    return cursor


@pytest.fixture(scope='session')
def all_worlds_names_fixture(connect_to_db_sqlite3):
    all_worlds_names = [elem[0] for elem in connect_to_db_sqlite3.execute("SELECT world_name FROM worlds")]
    return all_worlds_names


@pytest.fixture(scope='session')
def all_subtypes_fixture(connect_to_db_sqlite3):
    all_quest_subtypes = [elem[0] for elem in connect_to_db_sqlite3.execute("SELECT quest_name FROM quest_patterns")]
    return all_quest_subtypes


@pytest.fixture(scope='session')
def all_danger_names(connect_to_db_sqlite3):
    all_danger_zone_names = [elem[0] for elem in connect_to_db_sqlite3.execute("SELECT danger_name FROM danger_zone")]
    return all_danger_zone_names


@pytest.fixture(scope='session')
def all_imperial_classes(connect_to_db_sqlite3):
    all_imperial_classes_names = [elem[0] for elem in connect_to_db_sqlite3.execute("SELECT class_name FROM imperial_class")]
    return all_imperial_classes_names


@pytest.fixture(scope='session')
def reward_fixture():
    reward_list = []
    for _ in range(20):
        reward_list.append(random.randint(100000, 320000))
