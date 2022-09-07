"""
    Данный модуль содержит в себе класс нательной брони
"""
from settings_imports_globalVariables import *
from craft.base_artifact import Artifact


class Armor(Artifact):
    """
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """
    def __init__(self, grade_modifier, armor_type):
        super().__init__(grade_modifier)
        self.group_name = 'artifact_armor'
        self.art_type = armor_type if armor_type != 'random' else self.get_random_type_of_artifact(self.group_name)
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.armor = self.get_armor(grade_modifier)
        self.speed_modifier = self.get_speed_bonus()
        self.evasion_modifier = self.get_evasion()
        self.get_weight()
        self.get_requiriments()

    def get_armor(self, grade_modifier):
        base_armor = tuple(bd_sqlite3_cursor.execute(f'''
SELECT art_armor FROM artifact_armor
WHERE art_type_name == '{self.art_type}'
        '''))[0][0]

        final_armor = int(base_armor * grade_modifier)

        return final_armor

    def get_speed_bonus(self):
        base_speed_mod = tuple(bd_sqlite3_cursor.execute(f'''
        SELECT art_speed FROM artifact_armor
        WHERE art_type_name == '{self.art_type}'
                '''))[0][0]
        random_mod = 1 if random.randint(0, 100) <= 5 else 0

        final_speed_mod = base_speed_mod + random_mod

        return final_speed_mod

    def get_evasion(self):
        base_evasion = tuple(bd_sqlite3_cursor.execute(f'''
        SELECT art_evasion FROM artifact_armor
        WHERE art_type_name == '{self.art_type}'
                '''))[0][0]
        random_mod = 1 if random.randint(0, 100) <= 5 else 0

        final_speed_mod = base_evasion + random_mod

        return final_speed_mod
