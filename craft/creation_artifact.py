"""

"""
from settings_and_imports import *


def choise_class_objects(art_user_dict, cursor):
    art_user_dict['грейд'] = count_gear_score(art_user_dict['грейд'])

    art_object = None

    print(art_user_dict)
    if art_user_dict['группа'] == 'броня':
        art_object = Armor(art_user_dict['грейд'], art_user_dict['тип'], cursor)
    elif art_user_dict['группа'] == 'оружие-дб':
        art_object = RangeWeapon(art_user_dict['грейд'], art_user_dict['тип'], cursor)
    elif art_user_dict['группа'] == 'оружие-бб':
        art_object = CloseCombatWeapon(art_user_dict['грейд'], art_user_dict['тип'], cursor)
    elif art_user_dict['группа'] == 'бижутерия':
        art_object = Jewerly(art_user_dict['грейд'], art_user_dict['тип'], cursor)
    elif art_user_dict['группа'] == 'random':
        art_object = random.choice([
            Armor(art_user_dict['грейд'], art_user_dict['тип'], cursor),
            RangeWeapon(art_user_dict['грейд'], art_user_dict['тип'], cursor),
            CloseCombatWeapon(art_user_dict['грейд'], art_user_dict['тип'], cursor),
            Jewerly(art_user_dict['грейд'], art_user_dict['тип'], cursor)
        ])
    else:
        'Некорректный запрос'

    final_string = art_object.__dict__

    return final_string


def count_gear_score(grade):
    if grade == 'зеленый':
        base_gear_score = 40
    elif grade == 'синий':
        base_gear_score = 60
    elif grade == 'фиолетовый':
        base_gear_score = 80
    elif grade == 'красный':
        base_gear_score = 100
    else:
        return 'Данный грейд отсутствует'

    luck_mod = random.uniform(0.8, 1.2)

    return int(base_gear_score * luck_mod)


class Artifact:
    def __init__(self, gear_score, cursor):
        self.cursor = cursor
        self.name = 'Артефакт'
        self.grade = 'Зеленый'
        self.weight = 1
        self.unique_prefix = ''
        self.unique_suffix = ''
        self.stat_requeriments = 'Требования отсутствуют'
        self.gear_score = gear_score

    def choise_random_type_of_artifact(self, artifact_group):
        chosen_artifact = tuple(self.cursor.execute(f'''
    SELECT art_type_name FROM artifact_type
    WHERE art_group_name == '{artifact_group}'
    ORDER BY RANDOM()
    LIMIT 1'''))[0][0]
        return chosen_artifact

    def choise_prefix(self):
        prefix_tuple = tuple(self.cursor.execute('''
SELECT * FROM unique_prefix
ORDER BY RANDOM()
LIMIT 1'''))
        return prefix_tuple

    def choise_suffix(self, art_type):
        suffix_tuple = tuple(self.cursor.execute(f'''
SELECT unique_suffix.effect_name, unique_suffix.effect_text 
FROM unique_suffix
INNER JOIN unique_suffix_art_type_relations ON unique_suffix.effect_name == unique_suffix_art_type_relations.effect_name
INNER JOIN artifact_type ON unique_suffix_art_type_relations.art_type_name == artifact_type.art_type_name
WHERE artifact_type.art_type_name == '{art_type}'
ORDER BY RANDOM()
LIMIT 1'''))
        return suffix_tuple

    def form_name(self, prefix, art_type, suffix):
        self.name = f'{prefix[0][0]} {art_type} {suffix[0][0]}'


class Weapon(Artifact):
    def __init__(self, gear_score, cursor):
        super().__init__(gear_score, cursor)
        self.damage = 18
        self.penetration = 'Отсутствует'
        self.prescision_modifier = 0

    def get_damage(self, weapon_type, grade):
        random_modifier = random.uniform(0.9, 1.1)

        base_damage = tuple(self.cursor.execute(f'''
SELECT art_damage FROM artifact_type
WHERE art_type_name == '{weapon_type}'
        '''))[0][0]

        print(base_damage)

        final_damage = int(base_damage * random_modifier)

        return final_damage


class Armor(Artifact):
    def __init__(self, gear_score, armor_type, cursor):
        super().__init__(gear_score, cursor)
        self.armor = 0
        self.speed_modifier = 0
        self.evasion_modifier = 0
        self.art_type = armor_type if armor_type != 'random' else self.choise_random_type_of_artifact('броня')
        self.unique_prefix = self.choise_prefix()
        self.unique_suffix = self.choise_suffix(self.art_type)
        self.form_name(self.unique_prefix, self.art_type, self.unique_suffix)

    def get_armor(self):
        pass


class Jewerly(Artifact):
    def __init__(self, gear_score, jewelry_type, cursor):
        super().__init__(gear_score, cursor)
        self.jewerly_bonus = 'Отсутствует'
        self.art_type = jewelry_type if jewelry_type != 'random' else self.choise_random_type_of_artifact('бижутерия')
        self.unique_prefix = self.choise_prefix()
        self.unique_suffix = self.choise_suffix(self.art_type)
        self.form_name(self.unique_prefix, self.art_type, self.unique_suffix)


class RangeWeapon(Weapon):
    def __init__(self, gear_score, weapon_type, cursor):
        super().__init__(gear_score, cursor)
        self.weapon_range = 10
        self.attack_speed = 1
        self.art_type = weapon_type if weapon_type != 'random' else self.choise_random_type_of_artifact('оружие-дб')
        self.unique_prefix = self.choise_prefix()
        self.unique_suffix = self.choise_suffix(self.art_type)
        self.form_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.damage = self.get_damage(self.art_type, self.grade)


class CloseCombatWeapon(Weapon):
    def __init__(self, gear_score, weapon_type, cursor):
        super().__init__(gear_score, cursor)
        self.parry_bonus = 0
        self.art_type = weapon_type if weapon_type != 'random' else self.choise_random_type_of_artifact('оружие-бб')
        self.unique_prefix = self.choise_prefix()
        self.unique_suffix = self.choise_suffix(self.art_type)
        self.form_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.damage = self.get_damage(self.art_type, self.grade)

