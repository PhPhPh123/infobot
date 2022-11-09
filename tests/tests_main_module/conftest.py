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
    Фикстура, которая подключается к базе тестовой данных и создает объекты курсора и коннекта, абсолютный путь
    берет из файла настроек
    :return: объекты курсора и коннекта
    """
    db_name = 'base_for_testing.db'
    abspath = get_bot_dir() + os.path.sep + db_name  # Формирование абсолютного пути для файла базы данных
    connect = sqlite3.connect(abspath)  # Подключение к базе данных
    cursor = connect.cursor()  # Создание курсора
    return cursor


@pytest.fixture(scope='session')
def all_worlds_names_fixture(connect_to_db_sqlite3):
    """
    Данная фикстура собирается имена всех миров из тестовой базы данных
    @param connect_to_db_sqlite3: фикстура коннекта к БД
    @return: список имен миров
    """
    all_worlds_names = [elem[0] for elem in connect_to_db_sqlite3.execute(
        "SELECT world_name FROM worlds WHERE class_name NOT IN ('Мир-Горка-Стопудова', 'Мир-смерти')")]
    return all_worlds_names


@pytest.fixture(scope='session')
def all_subtypes_fixture(connect_to_db_sqlite3):
    """
    Фикстура для всех названий квестовых паттернов. Например 'павший воин', 'зачистка', 'доставка'
    @param connect_to_db_sqlite3: фикстура подключения к БД
    @return: список названий квестовых паттернов
    """
    all_quest_subtypes = [elem[0] for elem in connect_to_db_sqlite3.execute("SELECT quest_name FROM quest_patterns")]
    return all_quest_subtypes


@pytest.fixture(scope='session')
def all_danger_names_fixture(connect_to_db_sqlite3):
    """
    Фикстура для всех уровней опаности зон, например 'Нулевая угроза', 'Красная угроза'
    @param connect_to_db_sqlite3: фикстура подключения к БД
    @return: список всех уровней опасности
    """
    all_danger_zone_names = [elem[0] for elem in connect_to_db_sqlite3.execute("SELECT danger_name FROM danger_zone")]
    return all_danger_zone_names


@pytest.fixture(scope='session')
def all_imperial_classes_fixture(connect_to_db_sqlite3):
    """
    Фикстура всех классов миров, например 'Военно-мануфактурный мир', 'Мир-смерти', 'Боевая зона'
    @param connect_to_db_sqlite3: фикстура подключения к БД
    @return: список всех классов миров
    """
    all_imperial_classes_names = [elem[0] for elem in connect_to_db_sqlite3.execute(
        "SELECT class_name FROM imperial_class WHERE class_name NOT IN ('Мир-Горка-Стопудова', 'Мир-смерти')")]
    return all_imperial_classes_names


@pytest.fixture(scope='session')
def all_enemies_names_fixture(connect_to_db_sqlite3):
    """
    Фикстура всех типов угроз врагов, например 'угроза мутантов 1', 'угроза друкхари 4', 'угроза демонов 5'
    @param connect_to_db_sqlite3:
    @return: список все врагов
    """
    all_enemy_names = [elem[0] for elem in connect_to_db_sqlite3.execute(
        "SELECT enemy_name FROM enemies WHERE enemy_name NOT IN ('Никто', 'Кароч пиши никто, они придут, а мы им вломим, чисто мо Морковски')")]
    return all_enemy_names


@pytest.fixture(scope='session')
def all_goods_fixture(connect_to_db_sqlite3):
    """
    Фикстура всех названий товаров(экспортные и импортные товары идентичны, поэтому фикстура общая), например
    'Деликатесы', 'Металлы', 'Опасные-вещества'
    @param connect_to_db_sqlite3:
    @return: список всех товаров
    """
    all_goods = [elem[0] for elem in connect_to_db_sqlite3.execute(
        "SELECT import_name FROM trade_import WHERE base_price NOT NULL")]
    return all_goods


