"""
    Данный модуль содержит в себе класс бижутерии(серьги, кольца, амулеты)
"""

from settings_imports_globalVariables import *
from craft.base_artifact import Artifact


class Jewelry(Artifact):
    """
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """
    def __init__(self, grade_modifier, jewelry_type):
        super().__init__(grade_modifier)
        self.group_name = 'artifact_jewelry'
        self.art_type = jewelry_type if jewelry_type != 'random' else self.get_random_type_of_artifact(self.group_name)
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.jewerly_bonus = self.get_jewelry_bonus()
        self.get_weight()
        self.get_requiriments()

    @staticmethod
    def get_jewelry_bonus():
        jewerly_bonus = tuple(bd_sqlite3_cursor.execute(f'''
                SELECT * FROM unique_jewerly_bonuses
                ORDER BY RANDOM()
                LIMIT 1'''))[0]
        return jewerly_bonus
