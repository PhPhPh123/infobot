from unittest import TestCase, main
import sqlite3
import os
from news.mini_quests import QuestFormer


def get_bot_dir() -> str:
    """
    Функция собирающая абсолютный путь к текущей директории
    :return: возвращает этот путь
    """
    abs_path = os.path.abspath(__file__)  # полный путь к файлу скрипта
    return os.path.dirname(abs_path)


def connect_to_db_sqlite3() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """
    Функция, которая подключается к базе данных и создает объекты курсора и коннекта, абсолютный путь берет из файла
    настроек
    :return: объекты курсора и коннекта
    """
    db_name = 'base_for_testing.db'
    abspath = get_bot_dir() + os.path.sep + db_name  # Формирование вабсолютного пути для файла базы данных
    connect = sqlite3.connect(abspath)  # Подключение к базе данных
    cursor = connect.cursor()  # Создание курсора
    return cursor, connect


bd_sqlite3_cursor, bd_sqlite3_connect = connect_to_db_sqlite3()


def test_quest_former():
    art_obj = QuestFormer('artifact_quest')
    kill_obj = QuestFormer('kill_quest')
    delivery_obj = QuestFormer('delivery_quest')
    escort_obj = QuestFormer('escort_quest')

    obj_tuple = (art_obj, kill_obj, delivery_obj, escort_obj)
    all_worlds_names = [elem[0] for elem in bd_sqlite3_cursor.execute("SELECT world_name FROM worlds")]

    assert len(art_obj.quest_tuple) == 3
    assert len(kill_obj.quest_tuple) == 4
    assert len(delivery_obj.quest_tuple) == 4
    assert len(escort_obj.quest_tuple) == 2

    for obj in obj_tuple:
        world_name = obj.quest_tuple[0]
        assert world_name in all_worlds_names

        for elem in obj.quest_tuple:
            assert type(elem) == str






# class QuestFormerTest(TestCase):
#     pass
#
#
# class QuestTest(TestCase):
#     pass
#
#
# class ArtifactQuestTest(TestCase):
#     pass
#
#
# class KillQuestTest(TestCase):
#     pass
#
#
# class DeliveryQuestTest(TestCase):
#     pass
#
#
# class EscortQuestTest(TestCase):
#     pass


if __name__ == '__main__':
    main()
