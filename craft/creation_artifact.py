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
        self.name = 'Артефакт'
        self.grade = 'Зеленый'
        self.weight = 1
        self.unique_prefix = self.get_prefix()
        self.unique_suffix = ''
        self.stat_requeriments = 'Требования отсутствуют'
        self.gear_score = grade_modifier

    def get_random_type_of_artifact(self, artifact_group):
        chosen_artifact = tuple(self.cursor.execute(f'''
    SELECT art_type_name FROM artifact_type
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

    def get_suffix(self, art_type):
        suffix_tuple = tuple(self.cursor.execute(f'''
SELECT unique_suffix.effect_name, unique_suffix.effect_text 
FROM unique_suffix
INNER JOIN unique_suffix_art_type_relations ON unique_suffix.effect_name == unique_suffix_art_type_relations.effect_name
INNER JOIN artifact_type ON unique_suffix_art_type_relations.art_type_name == artifact_type.art_type_name
WHERE artifact_type.art_type_name == '{art_type}'
ORDER BY RANDOM()
LIMIT 1'''))
        return suffix_tuple

    def get_name(self, prefix, art_type, suffix):
        self.name = f'{prefix[0][0]} {art_type} {suffix[0][0]}'

    def get_weight(self):
        pass

    def get_requiriments(self):
        pass


class Weapon(Artifact):
    def __init__(self, grade_modifier, cursor):
        super().__init__(grade_modifier, cursor)
        self.damage = 18
        self.penetration = 'Отсутствует'
        self.prescision_modifier = 0

    def get_damage(self, weapon_type, grade_modifier):
        random_modifier = random.uniform(0.9, 1.1)

        base_damage = tuple(self.cursor.execute(f'''
SELECT art_damage FROM artifact_type
WHERE art_type_name == '{weapon_type}'
        '''))[0][0]

        final_damage = int(base_damage * random_modifier * grade_modifier)

        return final_damage

    def get_penetration(self, weapon_type):
        luck = random.randint(1, 100)

        if weapon_type in ('мельтаган', 'мельтапистолет',
                           'одноручный-силовой-меч', 'двуручный-силовой-меч'):
            self.penetration = 'Игнор ВУ'
        elif weapon_type in ('плазмаган', 'плазма-пистолет') or luck <= 3:
            if weapon_type not in ('лазган', 'лазпистолет'):
                self.penetration = 'Игнор половины ВУ'
        else:
            self.penetration = 'Пробитие отсутствует'
        return self.penetration

    def get_prescision(self, weapon_type):
        luck = random.randint(1, 100)

        base_prescision = tuple(self.cursor.execute(f'''
        SELECT art_prescision FROM artifact_type
        WHERE art_type_name == '{weapon_type}'
                '''))[0][0]
        final_prescision = base_prescision + 1 if luck <= 10 else base_prescision

        return final_prescision


class Armor(Artifact):
    def __init__(self, grade_modifier, armor_type, cursor):
        super().__init__(grade_modifier, cursor)
        self.speed_modifier = 0
        self.evasion_modifier = 0
        self.art_type = armor_type if armor_type != 'random' else self.get_random_type_of_artifact('броня')
        self.unique_suffix = self.get_suffix(self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.armor = self.get_armor(self.art_type, grade_modifier)

    def get_armor(self, armor_type, grade_modifier):
        base_armor = tuple(self.cursor.execute(f'''
SELECT art_armor FROM artifact_type
WHERE art_type_name == '{armor_type}'
        '''))[0][0]

        final_armor = int(base_armor * grade_modifier)

        return final_armor

    def get_speed_bonus(self):
        pass

    def get_evasion(self):
        pass


class Jewerly(Artifact):
    def __init__(self, grade_modifier, jewelry_type, cursor):
        super().__init__(grade_modifier, cursor)
        self.jewerly_bonus = 'Отсутствует'
        self.art_type = jewelry_type if jewelry_type != 'random' else self.get_random_type_of_artifact('бижутерия')
        self.unique_suffix = self.get_suffix(self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)

    def get_jewelry_bonus(self):
        pass


class RangeWeapon(Weapon):
    def __init__(self, grade_modifier, weapon_type, cursor):
        super().__init__(grade_modifier, cursor)
        self.weapon_range = 10
        self.attack_speed = 1
        self.art_type = weapon_type if weapon_type != 'random' else self.get_random_type_of_artifact('оружие-дб')
        self.unique_suffix = self.get_suffix(self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.damage = self.get_damage(self.art_type, grade_modifier)
        self.penetration = self.get_penetration(weapon_type)
        self.prescision_modifier = self.get_prescision(weapon_type)

    def get_range(self):
        pass

    def get_attack_speed(self):
        pass


class CloseCombatWeapon(Weapon):
    def __init__(self, grade_modifier, weapon_type, cursor):
        super().__init__(grade_modifier, cursor)
        self.parry_bonus = 0
        self.art_type = weapon_type if weapon_type != 'random' else self.get_random_type_of_artifact('оружие-бб')
        self.unique_suffix = self.get_suffix(self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.damage = self.get_damage(self.art_type, grade_modifier)
        self.penetration = self.get_penetration(weapon_type)
        self.prescision_modifier = self.get_prescision(weapon_type)

    def get_parry_bonus(self):
        pass
