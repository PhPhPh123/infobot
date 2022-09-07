"""
    Данный модуль содержит в себе класс оружия дальнего боя
"""

from settings_imports_globalVariables import *
from craft.artifact_groups.weapons.base_weapons import Weapon


class RangeWeapon(Weapon):
    """
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """
    def __init__(self, grade_modifier, weapon_type):
        super().__init__(grade_modifier)
        self.group_name = 'artifact_range_weapon'
        self.art_type = weapon_type if weapon_type != 'random' else self.get_random_type_of_artifact(self.group_name)
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.damage = self.get_damage(self.group_name, self.art_type, grade_modifier)
        self.penetration = self.get_penetration(self.art_type)
        self.prescision_modifier = self.get_prescision(self.group_name, self.art_type)

        self.attack_speed = self.get_attack_speed()
        self.range = self.get_range()
        self.get_weight()
        self.get_requiriments()

    def get_range(self):

        base_range = tuple(bd_sqlite3_cursor.execute(f'''
                SELECT art_range FROM artifact_range_weapon
                WHERE art_type_name == '{self.art_type}'
                        '''))[0][0]

        final_range = 10

        if base_range <= 7:
            final_range = random.randint((base_range - 1), (base_range + 1))
        elif 8 <= base_range <= 14:
            final_range = random.randint((base_range - 1), (base_range + 3))
        elif base_range >= 15:
            final_range = random.randint((base_range - 2), (base_range + 4))

        return final_range

    def get_attack_speed(self):

        base_attack_speed = tuple(bd_sqlite3_cursor.execute(f'''
                SELECT art_attack_speed FROM artifact_range_weapon
                WHERE art_type_name == '{self.art_type}'
                '''))[0][0]

        final_attack_speed = 1

        if base_attack_speed == 1:
            pass
        elif 2 <= base_attack_speed <= 5:
            final_attack_speed = random.randint((base_attack_speed - 1), (base_attack_speed + 1))
        elif 6 <= base_attack_speed <= 10:
            final_attack_speed = random.randint((base_attack_speed - 2), (base_attack_speed + 3))
        elif 11 <= base_attack_speed <= 15:
            final_attack_speed = random.randint((base_attack_speed - 2), (base_attack_speed + 4))
        elif base_attack_speed >= 16:
            final_attack_speed = random.randint((base_attack_speed - 3), (base_attack_speed + 5))

        return final_attack_speed
