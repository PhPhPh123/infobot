"""
    Данный класс содержит базовый класс оружия, методы и аттрибуты, характерные для всех видов оружия
"""
from settings_imports_globalVariables import *
from craft.base_artifact import Artifact


class Weapon(Artifact):
    def __init__(self, grade_modifier, cursor):
        super().__init__(grade_modifier, cursor)
        self.damage = 18
        self.penetration = 'Отсутствует'
        self.prescision_modifier = 0

    def get_damage(self, weapon_group, weapon_type, grade_modifier):
        random_modifier = random.uniform(0.9, 1.1)
        base_damage = tuple(self.cursor.execute(f'''
SELECT art_damage FROM {weapon_group}
WHERE art_type_name == '{weapon_type}'
        '''))[0][0]

        final_damage = int(base_damage * random_modifier * grade_modifier)

        return final_damage

    def get_penetration(self, weapon_type):
        luck = random.randint(1, 100)

        if weapon_type in ('мельтаган', 'мельта-пистолет',
                           'одноручный-силовой-меч', 'двуручный-силовой-меч'):
            self.penetration = 'Игнор ВУ'
        elif weapon_type in ('плазмаган', 'плазма-пистолет') or luck <= 3:
            if weapon_type not in ('лазган', 'лаз-пистолет'):
                self.penetration = 'Игнор половины ВУ'
        else:
            self.penetration = 'Пробитие отсутствует'
        return self.penetration

    def get_prescision(self, weapon_group, weapon_type):
        luck = random.randint(1, 100)

        base_prescision = tuple(self.cursor.execute(f'''
        SELECT art_prescision FROM {weapon_group}
        WHERE art_type_name == '{weapon_type}'
                '''))[0][0]
        final_prescision = base_prescision + 1 if luck <= 10 else base_prescision

        return final_prescision