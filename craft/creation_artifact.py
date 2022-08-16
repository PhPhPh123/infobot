"""

"""

from settings_and_imports import *


def control_art_form(art_dict):
    art_dict['грейд'] = count_gear_score(art_dict['грейд'])
    print(art_dict)
    lz = Lazgun()

    final_string = lz.__dict__
    return final_string


def count_gear_score(grade):
    base_gear_score = 0
    if grade == 'Зеленый'.lower():
        base_gear_score = 100
    elif grade == 'Синий'.lower():
        base_gear_score = 120
    elif grade == 'Фиолетовый'.lower():
        base_gear_score = 140
    elif grade == 'Красный'.lower():
        base_gear_score = 160
    else:
        return 'Данный грейд отсутствует'

    luck_mod = random.uniform(0.8, 1.2)

    return int(base_gear_score * luck_mod)


class Artifact:
    def __init__(self):
        self.name = 'Артефакт по умолчанию'
        self.grade = 'Зеленый'
        self.weight = 10
        self.unique_bonus = 'Особенности отсутствуют'
        self.stat_requeriments = 'Требования отсутствуют'


class Armor(Artifact):
    def __init__(self):
        super().__init__()
        self.armor = 0
        self.speed_modifier = 0
        self.evasion_modifier = 0

    def get_armor(self):
        pass


class Weapon(Artifact):
    def __init__(self):
        super().__init__()
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
    def __init__(self):
        super().__init__()
        self.jewerly_bonus = 'Отсутствует'


class RangeWeapon(Weapon):
    def __init__(self):
        super().__init__()
        self.weapon_range = 10
        self.attack_speed = 1


class Lazgun(RangeWeapon):
    def __init__(self):
        super().__init__()
        self.laz_mechanics = True


class Autogun(RangeWeapon):
    def __init__(self):
        super().__init__()


class Meltagun(RangeWeapon):
    def __init__(self):
        super().__init__()


class Bolter(RangeWeapon):
    def __init__(self):
        super().__init__()


class Hellgun(RangeWeapon):
    def __init__(self):
        super().__init__()


class Plasmagun(RangeWeapon):
    def __init__(self):
        super().__init__()
