"""
    Данный модуль отвечает за рандомизацию и выдачу в чат небольших случайных квестов
"""
import random

from settings_imports_globalVariables import *
import craft.main_artifact_builder


def control_quests():
    """
    Данная функция осуществляет общее управление другими функциями
    """

    chones_quest = choise_quest()

    quest_tuple = form_quests_query(chones_quest)

    form_quest_object(chones_quest, quest_tuple)


def choise_quest():
    """
    Данная функция выбирает случайный тип квеста
    """
    chones_quest = random.choice(['artifact_quest', 'kill_quest', 'delivery_quest', 'escort_quest'])
    return chones_quest


def form_quests_query(quest_type):
    """
    Данная функция делает запрос в БД и получает кортеж со значениями
    """
    pass


def form_quest_object(quest_type: str, quest_tuple: tuple):
    """
    Данная функция получает значения из БД и создает экземляры класса на их основе
    """
    pass


class Quest:
    """
    Данный класс является базовым и содержит в себе аттрибуты и методы, характерные для всех квестов
    """

    def load_quest_to_file(self):
        """
        Данный метод будет записывать в файл текст квеста
        """

    def finalize_quest_string(self):
        """
        Данный метод будет окончательное готовить квестовую строку
        """
        pass


class ArtifactQuest(Quest):
    """
    Данный класс отвечает за формирование квестом поиска артефактов. Он создает запрос в соседний модуль на
    формирование артефакта и выдачу квестом его названия, а параметры сохраняются в отдельном тестовом файле
    для ГМа
    """

    def __init__(self):
        self.art_name = ""

    def form_artifact(self):
        request_dict = {}
        artifact = craft.main_artifact_builder.choise_class_objects(request_dict)
        self.art_name = ""

    def form_artifact_quest(self):
        """
        Данный метод будет формировать строку с квестом
        """
        pass


class KillQuest(Quest):
    """
    Данный класс отвечает за формирование заказов на убийство и зачистку врагов
    """

    def __init__(self):
        pass

    def form_kill_quest(self):
        """
        Данный метод будет формировать строку с квестом
        """
        pass


class DeliveryQuest(Quest):
    """
    Данный класс отвечает за формирование заказов на доставку торгового груза на определенный мир с повышенной
    стоимостью оплаты
    """

    def __init__(self):
        pass

    def form_delivery_quest(self):
        """
        Данный метод будет формировать строку с квестом
        """
        pass


class EscortQuest(Quest):
    """
    Данный класс отвечает за формирование заказов на перевозку пассажира с одного мира на другой
    """

    def __init__(self):
        pass

    def form_escort_quest(self):
        """
        Данный метод будет формировать строку с квестом
        """
        pass
