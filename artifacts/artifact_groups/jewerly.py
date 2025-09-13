"""
    Данный модуль содержит в себе класс бижутерии(серьги, кольца, амулеты). В __init__ реализован шаблон проектирования
    Строитель путем самосбора
"""
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *
from artifacts.base_artifact import Artifact


class Jewelry(Artifact):
    """
    Данный артефактный класс создает объект и является конечным в цепочке наследования. Он формирует бижутерию и
    наследуюется от класса Artifact
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """

    def __init__(self, grade_modifier: float, jewelry_type: str, prefix: str, suffix: str, grade_name: str, game_mode):
        super().__init__(grade_modifier, prefix, grade_name)

        self.group_name = 'artifact_jewelry'  # статичная инициализация группы артефакта

        # Данная строчка отвечает за выбор типа артефакта если он явно указан в запросе, иначе вызывается метод
        # родительского класса, который выбирает случайный тип
        self.art_type = jewelry_type if jewelry_type != 'random' else self.get_random_type_of_artifact(self.group_name)

        # Данные методы берутся из родительского класса Artifact
        self.unique_suffix = suffix if suffix != 'random' else self.get_suffix(self.group_name, self.art_type, suffix)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.get_weight()
        self.get_requiriments()
        self.game_mode = game_mode

        # Собственные методы
        self.jewerly_bonus = self.get_jewelry_bonus()

    def get_jewelry_bonus(self) -> tuple:
        """
        Статический метод, получающий из БД случайный тип ювелирного бонуса на основе выбранного типа бижутерии
        :return: кортеж с ювелирным бонусом, где [0] элемент это название бонуса, а [0] это текст его описания
        """

        jewerly_bonus = tuple(global_artifacts_cursor.execute(f'''
SELECT * FROM unique_jewelry_bonuses
INNER JOIN artifact_jewelry_unique_jewelry_bonuses_relations ON unique_jewelry_bonuses.jewelry_bonus_name == 
artifact_jewelry_unique_jewelry_bonuses_relations.jewelry_bonus_name
INNER JOIN artifact_jewelry ON artifact_jewelry_unique_jewelry_bonuses_relations.art_type_name == 
artifact_jewelry.art_type_name
WHERE artifact_jewelry.art_type_name == '{self.art_type}'
ORDER BY RANDOM()
LIMIT 1'''))[0]  # поскольку из БД собираются кортежи с кортежами то из внешнего кортежа берется
        # вложенный кортеж с 2 значениями

        return jewerly_bonus
