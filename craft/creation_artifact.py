"""

"""
from settings_and_imports import *


def choise_class_objects(art_user_dict, cursor):
    art_user_dict['грейд'] = count_grade_modifier(art_user_dict['грейд'])

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


def count_grade_modifier(grade):
    if grade == 'зеленый':
        grade_modifier = 1
    elif grade == 'синий':
        grade_modifier = 1.1
    elif grade == 'фиолетовый':
        grade_modifier = 1.2
    elif grade == 'красный':
        grade_modifier = 1.3
    else:
        raise ValueError('Неверное название грейда')

    luck_mod = random.uniform(0.9, 1.1)

    return grade_modifier * luck_mod


class Artifact:
    def __init__(self, grade_modifier, cursor):
        self.cursor = cursor
        self.name = None
        self.art_type = None
        self.group_name = None
        self.weight = 1
        self.unique_prefix = self.get_prefix()
        self.unique_suffix = ''
        self.str_requeriments = None
        self.gear_score = grade_modifier

    def get_random_type_of_artifact(self, table_name, artifact_group):
        chosen_artifact = tuple(self.cursor.execute(f'''
    SELECT art_type_name FROM {table_name}
    WHERE art_group_name == '{artifact_group}'
    ORDER BY RANDOM()
    LIMIT 1'''))[0][0]
        return chosen_artifact

    def get_prefix(self):
        prefix_tuple = tuple(self.cursor.execute('''
SELECT * FROM unique_prefix
ORDER BY RANDOM()
LIMIT 1'''))
        return prefix_tuple

    def get_suffix(self, art_group, art_type):
        suffix_tuple = tuple(self.cursor.execute(f'''
SELECT unique_suffix.effect_name, unique_suffix.effect_text 
FROM unique_suffix
INNER JOIN unique_suffix_{art_group}_relations ON unique_suffix.effect_name == unique_suffix_{art_group}_relations.effect_name
INNER JOIN {art_group} ON unique_suffix_{art_group}_relations.art_type_name == {art_group}.art_type_name
WHERE {art_group}.art_type_name == '{art_type}'
ORDER BY RANDOM()
LIMIT 1'''))
        return suffix_tuple

    def get_name(self, prefix, art_type, suffix):
        print(prefix, art_type, suffix)
        self.name = f'{prefix[0][0]} {art_type} {suffix[0][0]}'

    def get_weight(self):
        art_weight = tuple(self.cursor.execute(f'''
SELECT art_weight FROM {self.group_name}
WHERE art_type_name == '{self.art_type}'
'''))[0][0]
        random_mod = random.uniform(1, 1.2)
        self.weight = int(art_weight * (1 - (self.gear_score - 1)) * random_mod)

    def get_requiriments(self):
        art_reqs = tuple(self.cursor.execute(f'''
SELECT art_str_req FROM {self.group_name}
WHERE art_type_name == '{self.art_type}'
'''))[0][0]
        luck_mod = random.randint(0, 100)
        if luck_mod >= 90:
            art_reqs += 1
        self.str_requeriments = art_reqs


class Weapon(Artifact):
    def __init__(self, grade_modifier, cursor):
        super().__init__(grade_modifier, cursor)
        self.damage = 18
        self.penetration = 'Отсутствует'
        self.prescision_modifier = 0

    def get_damage(self, weapon_group, weapon_type, grade_modifier):
        random_modifier = random.uniform(0.9, 1.1)
        print(weapon_group, weapon_type, grade_modifier)
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


class Armor(Artifact):
    def __init__(self, grade_modifier, armor_type, cursor):
        super().__init__(grade_modifier, cursor)
        self.group_name = 'artifact_armor'
        self.evasion_modifier = 0
        self.art_type = armor_type if armor_type != 'random' else self.get_random_type_of_artifact(self.group_name,
                                                                                                   'броня')
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.armor = self.get_armor(grade_modifier)
        self.speed_modifier =  self.get_speed_bonus()
        self.get_weight()
        self.get_requiriments()

    def get_armor(self, grade_modifier):
        base_armor = tuple(self.cursor.execute(f'''
SELECT art_armor FROM artifact_armor
WHERE art_type_name == '{self.art_type}'
        '''))[0][0]

        final_armor = int(base_armor * grade_modifier)

        return final_armor

    def get_speed_bonus(self):
        base_speed_mod = tuple(self.cursor.execute(f'''
        SELECT art_speed FROM artifact_armor
        WHERE art_type_name == '{self.art_type}'
                '''))[0][0]
        random_mod = 1 if random.randint(0, 100) <= 5 else 0

        final_speed_mod = base_speed_mod + random_mod

        return final_speed_mod

    def get_evasion(self):
        base_evation = tuple(self.cursor.execute(f'''
        SELECT art_evasion FROM artifact_armor
        WHERE art_type_name == '{self.art_type}'
                '''))[0][0]
        random_mod = 1 if random.randint(0, 100) <= 5 else 0

        final_speed_mod = base_evation + random_mod

        return final_speed_mod


class Jewerly(Artifact):
    def __init__(self, grade_modifier, jewelry_type, cursor):
        super().__init__(grade_modifier, cursor)
        self.group_name = 'artifact_jewelry'
        self.art_type = jewelry_type if jewelry_type != 'random' else self.get_random_type_of_artifact(self.group_name,
                                                                                                       'бижутерия')
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.jewerly_bonus = self.get_jewelry_bonus()
        self.get_weight()
        self.get_requiriments()

    def get_jewelry_bonus(self):
        jewerly_bonus = tuple(self.cursor.execute(f'''
                SELECT * FROM unique_jewerly_bonuses
                ORDER BY RANDOM()
                LIMIT 1'''))[0]
        return jewerly_bonus


class RangeWeapon(Weapon):
    def __init__(self, grade_modifier, weapon_type, cursor):
        super().__init__(grade_modifier, cursor)
        self.group_name = 'artifact_range_weapon'
        self.art_type = weapon_type if weapon_type != 'random' else self.get_random_type_of_artifact(self.group_name,
                                                                                                     'оружие-дб')
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

        base_range = tuple(self.cursor.execute(f'''
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

        base_attack_speed = tuple(self.cursor.execute(f'''
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
