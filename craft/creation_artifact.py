"""

"""
from settings_and_imports import *


def choise_class_objects(art_user_dict):
    art_user_dict['грейд'] = count_gear_score(art_user_dict['грейд'])

    art_object = None

    if art_user_dict['группа'] == 'броня':
        art_object = Armor(art_user_dict['грейд'], art_user_dict['тип'])
    elif art_user_dict['группа'] == 'оружие-дб':
        art_object = RangeWeapon(art_user_dict['грейд'], art_user_dict['тип'])
    elif art_user_dict['группа'] == 'оружие-бб':
        art_object = CloseCombatWeapon(art_user_dict['грейд'], art_user_dict['тип'])
    elif art_user_dict['группа'] == 'бижутерия':
        art_object = Jewerly(art_user_dict['грейд'])
    elif art_user_dict['группа'] == 'random':
        art_object = random.choice([
                                    Armor(art_user_dict['грейд'], art_user_dict['тип']),
                                    RangeWeapon(art_user_dict['грейд'], art_user_dict['тип']),
                                    CloseCombatWeapon(art_user_dict['грейд'], art_user_dict['тип']),
                                    Jewerly(art_user_dict['грейд'])
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
    def __init__(self, gear_score):
        self.name = 'Артефакт по умолчанию'
        self.grade = 'Зеленый'
        self.weight = 10
        self.unique_bonus = 'Особенности отсутствуют'
        self.stat_requeriments = 'Требования отсутствуют'
        self.gear_score = gear_score


class Armor(Artifact):
    def __init__(self, gear_score, armor_type):
        super().__init__(gear_score)
        self.armor = 0
        self.speed_modifier = 0
        self.evasion_modifier = 0

    def get_armor(self):
        pass


class Weapon(Artifact):
    def __init__(self, gear_score):
        super().__init__(gear_score)
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
    def __init__(self, gear_score):
        super().__init__(gear_score)
        self.jewerly_bonus = 'Отсутствует'


class RangeWeapon(Weapon):
    def __init__(self, gear_score, weapon_type):
        super().__init__(gear_score)
        self.weapon_range = 10
        self.attack_speed = 1


class CloseCombatWeapon(Weapon):
    def __init__(self, gear_score, weapon_type):
        super().__init__(gear_score)
        self.parry_bonus = 0
