"""
    Данный модуль содержит в себе класс оружия ближнего боя
"""

from settings_imports_globalVariables import *
from craft.artifact_groups.weapons.base_weapons import Weapon


class CloseCombatWeapon(Weapon):
    def __init__(self, grade_modifier, weapon_type, cursor):
        super().__init__(grade_modifier, cursor)
        self.group_name = 'artifact_close_combat'
        self.art_type = weapon_type if weapon_type != 'random' else self.get_random_type_of_artifact(self.group_name,
                                                                                                     'оружие-бб')
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.damage = self.get_damage(self.group_name, self.art_type, grade_modifier)
        self.penetration = self.get_penetration(weapon_type)
        self.prescision_modifier = self.get_prescision(self.group_name, self.art_type)
        self.parry_modifier = self.get_parry_bonus()
        self.get_weight()
        self.get_requiriments()

    def get_parry_bonus(self):
        luck_modifier = random.randint(1, 100)
        parry_modifier = 0

        art_parry = tuple(self.cursor.execute(f'''
                    SELECT art_parry_bonus FROM artifact_close_combat
                    WHERE art_type_name == '{self.art_type}'
'''))[0][0]

        if luck_modifier <= 5:
            parry_modifier = 2
        elif 6 <= luck_modifier <= 10:
            parry_modifier = 1
        elif luck_modifier >= 90:
            parry_modifier = -1

        return parry_modifier + art_parry
