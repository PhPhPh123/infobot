"""
    Данный модуль содержит в себе класс бижутерии(серьги, кольца, амулеты)
"""

from settings_imports_globalVariables import *
from craft.base_artifact import Artifact


class Jewelry(Artifact):
    """
    Данный артефактный класс создает объект и является конечным в цепочке наследования. Он формирует бижутерию и
    наследуюется от класса Artifact
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """
    def __init__(self, grade_modifier: float, jewelry_type: str):
        super().__init__(grade_modifier)

        self.group_name = 'artifact_jewelry'  # статичная инициализация группы артефакта
        # Данная строчка отвечает за выбор типа артефакта если он явно указан в запросе, иначе вызывается метод
        # родительского класса, который выбирает случайный тип
        self.art_type = jewelry_type if jewelry_type != 'random' else self.get_random_type_of_artifact(self.group_name)

        # Данные методы берутся из родительского класса Artifact
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.get_weight()
        self.get_requiriments()

        # Собственные методы
        self.jewerly_bonus = self.get_jewelry_bonus()

    @staticmethod
    def get_jewelry_bonus() -> tuple:
        """
        Статический метод, получающий из БД случайный тип ювелирного бонуса
        :return: кортеж с ювелирным бонусом, где [0] элемент это название бонуса, а [0] это текст его описания
        """
        jewerly_bonus = tuple(bd_sqlite3_cursor.execute(f'''
                SELECT * FROM unique_jewerly_bonuses
                ORDER BY RANDOM()
                LIMIT 1'''))[0]  # поскольку из БД собираются кортежи с кортежами то из внешнего кортежа берется
        # вложенный кортеж с 2 значениями
        return jewerly_bonus
