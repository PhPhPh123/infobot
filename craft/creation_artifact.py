"""

"""
from settings_and_imports import *


def choise_class_objects(art_user_dict, cursor):
    art_user_dict['грейд'] = count_gear_score(art_user_dict['грейд'])

    art_object = None

    if art_user_dict['группа'] == 'броня':
        art_object = Armor(art_user_dict['грейд'], art_user_dict['тип'], cursor)
    elif art_user_dict['группа'] == 'оружие-дб':
        art_object = RangeWeapon(art_user_dict['грейд'], art_user_dict['тип'], cursor)
    elif art_user_dict['группа'] == 'оружие-бб':
        art_object = CloseCombatWeapon(art_user_dict['грейд'], art_user_dict['тип'], cursor)
    elif art_user_dict['группа'] == 'бижутерия':
        art_object = Jewerly(art_user_dict['грейд'], cursor)
    elif art_user_dict['группа'] == 'random':
        art_object = random.choice([
            Armor(art_user_dict['грейд'], art_user_dict['тип'], cursor),
            RangeWeapon(art_user_dict['грейд'], art_user_dict['тип'], cursor),
            CloseCombatWeapon(art_user_dict['грейд'], art_user_dict['тип'], cursor),
            Jewerly(art_user_dict['грейд'], cursor)
        ])
    else:
        'Некорректный запрос'

    final_string = art_object.__dict__

    print(art_user_dict)
    print(final_string)

    return final_string


def count_gear_score(grade):
    base_gear_score = 0
    if grade == 'Зеленый'.lower():
        base_gear_score = 40
    elif grade == 'Синий'.lower():
        base_gear_score = 60
    elif grade == 'Фиолетовый'.lower():
        base_gear_score = 80
    elif grade == 'Красный'.lower():
        base_gear_score = 100
    else:
        return 'Данный грейд отсутствует'

    luck_mod = random.uniform(0.8, 1.2)

    return int(base_gear_score * luck_mod)


class Artifact:
    def __init__(self, gear_score, cursor):
        self.cursor = cursor
        self.name = 'Артефакт по умолчанию'
        self.grade = 'Зеленый'
        self.weight = 10
        self.unique_prefix = 'Особенности отсутствуют'
        self.unique_suffix = self.choise_suffix(self.cursor)
        self.stat_requeriments = 'Требования отсутствуют'
        self.gear_score = gear_score

    def choise_suffix(self, cursor):
        suffix_tuple = list(self.cursor.execute('''
SELECT effect_name, effect_text FROM unique_suffix
ORDER BY RANDOM()
LIMIT 1'''))
        return suffix_tuple


class Armor(Artifact):
    def __init__(self, gear_score, armor_type, cursor):
        super().__init__(gear_score, cursor)
        self.armor = 0
        self.speed_modifier = 0
        self.evasion_modifier = 0
        self.armor_type = armor_type

    def get_armor(self):
        pass


class Weapon(Artifact):
    def __init__(self, gear_score, cursor):
        super().__init__(gear_score, cursor)
        self.damage = 18
        self.penetration = 'Отсутствует'
        self.prescision_modifier = 0

    def get_damage(self, group_of_weapon, grade):
        base_damage_lazgun = 18
        base_damage_lazgpistol = 12
        base_damage_autopistol = 18
        base_damage_autogun = 30

        random_modifier = random.uniform(0.9, 1.1)

        grade_damage = 0
        if grade == 'зеленый':
            grade_damage = 1.05
        elif grade_damage == 'синий':
            grade_damage = 1.10
        elif grade_damage == 'фиолетовый':
            grade_damage = 1.15
        elif grade_damage == 'красный':
            grade_damage = 1.2

        if group_of_weapon == 'Лазган':
            self.damage = base_damage_lazgun * grade_damage * random_modifier
            print(self.damage)


class Jewerly(Artifact):
    def __init__(self, gear_score, cursor):
        super().__init__(gear_score, cursor)
        self.jewerly_bonus = 'Отсутствует'


class RangeWeapon(Weapon):
    def __init__(self, gear_score, weapon_type, cursor):
        super().__init__(gear_score, cursor)
        self.weapon_range = 10
        self.attack_speed = 1
        self.weapon_type = weapon_type if weapon_type != 'random' else self.choise_range_weapon()

    def choise_range_weapon(self):
        chosen_range_weapon = tuple(self.cursor.execute('''
SELECT art_type_name FROM artifact_type
WHERE art_group_name == 'оружие-дб'
ORDER BY RANDOM()
LIMIT 1'''))[0][0]
        return chosen_range_weapon


class CloseCombatWeapon(Weapon):
    def __init__(self, gear_score, weapon_type, cursor):
        super().__init__(gear_score, cursor)
        self.parry_bonus = 0
        self.weapon_type = weapon_type
