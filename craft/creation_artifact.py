"""
    Данный модуль занимается формированием артефактов и подготовкой строковой информации для вывода ботов в чат.
    За вывод отвечает команда !arfifact. Команда требует как минимум указания грейда артефакта(цвета), а остальные
    две характеристики(группа артефакта, тип артефакта) по умолчанию выбираются случайно или указывается через пробел
    в строке команды. Работа модуля основана на создание объекта одного из 4х классов(броня, оружие-бб, оружие-дб
    бижутерия) которые наследуются от базового класса artifact, а классы оружия еще и от промежуточного базового класса
    оружие. В экземляры классов передаются некоторые параметры в виде модификатора грейда, который используется для
    усиления параметров артефактов, функция count_grade_modifier, а финальная обработка и подготовка строки идет в
    функции form_string_answer на основе итогового словаря __dict__. Данные об артефактах, их параметры и все остальное
    хранится в БД и запрашивается оттуда соответствующими методами классов
"""


from settings_and_imports import *


def choise_class_objects(art_user_dict: dict, cursor: sqlite3.Cursor) -> str:
    """
    Данная функция получает модификатор грейда от нижестоящей функции count_grade_modifier
    осуществляет случайный или неслучайный выбор класса, для которого будет формироваться
    объект и отправляет итоговый словарь __dict__ в функцию подготовки строкового ответа, а затем высылает ее в
    основной модуль для отправки в чат. Функция носит контролирующую задачу

    :param art_user_dict: словарь, хранящий базовую информацию о первоначальном запросе в чате и указывающий
    какой тип артефакта должен быть создан или все отдается на волю рандома
    :param cursor: объект курсора БД
    :return: итоговая строка ответа для бота
    """
    #  float модификатор, который используется для умножения некоторых числовых характеристик артефактов
    art_user_dict['грейд'] = count_grade_modifier(art_user_dict['грейд'])
    if not art_user_dict['грейд']:
        return "Некорректное название грейда"

    """
    Структура ниже осуществляет выбор типа артефакта, если он есть, или случайный выбор, если его нет
    и создает экземляр соответствующего класса отправляя в них их модификатор грейда, тип артефакта(если выбран, если
    не выбран то random и объект курсора для доступа в БД)
    """
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
        return 'Некорректное название группы или типа артефакта'

    # Итоговая строка ответа
    final_string = form_string_answer(art_object.__dict__)

    return final_string


def count_grade_modifier(grade: str) -> Optional[float]:
    """
    Данная функция приобразует цвет артефакта(зеленый, синий, фиолетовый, красный) в float-модификатор с применением
    некоторой степени рандома. В случае некорректного названия грейда возвращет None для формирования ответа о
    некорректном запросе
    :param grade: строка с цветом артефакта(это строковым грейдом)
    :return: итоговый float-модификатор для применения на числовых характеристиках
    """
    if grade == 'зеленый':
        grade_modifier = 1
    elif grade == 'синий':
        grade_modifier = 1.1
    elif grade == 'фиолетовый':
        grade_modifier = 1.2
    elif grade == 'красный':
        grade_modifier = 1.3
    else:
        return None

    # Выбирает случайное float-число в данном диапазоне с целью внесения фактора рандома
    luck_mod = random.uniform(0.95, 1.1)

    return grade_modifier * luck_mod


def form_string_answer(artifact_dict: dict) -> str:
    """
    Данная функция формирует итоговую строку ответа для бота на основе словаря __dict__ полученного из
    экземляра соответствующего класса. Функция работает по принципу конкатенации к изначально пустой строке
    кусков строк отформатированный методом формат и представляющих характеристики артефакта. Условные контрукции
    осеивают характеристики по типу итогогово выбранного типа артефакта т.к. у разных артефактов много разных свойств
    , но есть и общие
    :artifact_dict: итоговый словарь __dict__
    :return: строка ответа для бота
    """

    final_string = ''  # Инициализация строки ответа

    final_string += f"{artifact_dict['name'].capitalize()}\n"  # Создание имени артефакта, с большой буквы

    # Создание строк, характерных для всех групп оружия
    if artifact_dict['group_name'] in ('artifact_close_combat', 'artifact_range_weapon'):
        final_string += f"Урон: {artifact_dict['damage'] // 6}d6 + {artifact_dict['damage'] % 6}\n"
        final_string += f"Точность: {artifact_dict['prescision_modifier']}\n"
        final_string += f"Пробитие ВУ: {artifact_dict['penetration']}\n"

        # Создание строк, характерных для дальнобойного оружия
        if artifact_dict['group_name'] == 'artifact_range_weapon':
            final_string += f"Дистанция: {artifact_dict['range']}\n"
            final_string += f"Скорость стрельбы: {artifact_dict['attack_speed']}\n"

        # Создание строк, характерных для оружия ближнего боя
        if artifact_dict['group_name'] == 'artifact_close_combat':
            final_string += f"Модификатор парирования: {artifact_dict['parry_modifier']}\n"

    # Создание строк, характерных для брони
    if artifact_dict['group_name'] == 'artifact_armor':
        final_string += f"ВУ: {artifact_dict['armor']}\n"
        final_string += f"Модификатор уворота: {artifact_dict['evasion_modifier']}\n"
        final_string += f"Модификатор скорости: {artifact_dict['speed_modifier']}\n"

    # Создание строк, характерных для бижутерии
    if artifact_dict['group_name'] == 'artifact_jewelry':
        final_string += f"Бонус бижутерии: {artifact_dict['jewerly_bonus'][0]}\n"
        final_string += f"Описание бонуса: {artifact_dict['jewerly_bonus'][1]}\n"

    # Создание строк, характерных для всех артефактов независимо от группы
    final_string += f"Требования силы: {artifact_dict['str_requeriments']}\n"
    final_string += f"Вес: {artifact_dict['weight']}\n"
    final_string += f"Особенность: 1 раз в сессию удача для навыка {artifact_dict['unique_prefix'][0][1]}\n"
    final_string += f"Особенность: {artifact_dict['unique_suffix'][0][1]}"

    return final_string


class Artifact:
    """
    Базовый класс, инициализирующий характеристики по умолчанию, свойственные для всех групп артефактов, а также
    содержащий методы для их создания дочерними классами, которые наследуют данный родительский класс. Сам по себе он
    не вызывается, лишь содержит наследуемые методы
    """
    def __init__(self, grade_modifier, cursor):
        self.cursor = cursor
        self.unique_prefix = self.get_prefix()
        self.grade_modifier = grade_modifier

        self.name = None
        self.art_type = None
        self.group_name = None
        self.weight = 1
        self.unique_suffix = ''
        self.str_requeriments = None

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
        self.name = f'{prefix[0][0]} {art_type} {suffix[0][0]}'

    def get_weight(self):
        art_weight = tuple(self.cursor.execute(f'''
SELECT art_weight FROM {self.group_name}
WHERE art_type_name == '{self.art_type}'
'''))[0][0]
        random_mod = random.uniform(1, 1.2)
        self.weight = int(art_weight * (1 - (self.grade_modifier - 1)) * random_mod)

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
        self.art_type = armor_type if armor_type != 'random' else self.get_random_type_of_artifact(self.group_name,
                                                                                                   'броня')
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.armor = self.get_armor(grade_modifier)
        self.speed_modifier = self.get_speed_bonus()
        self.evasion_modifier = self.get_evasion()
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
        base_evasion = tuple(self.cursor.execute(f'''
        SELECT art_evasion FROM artifact_armor
        WHERE art_type_name == '{self.art_type}'
                '''))[0][0]
        random_mod = 1 if random.randint(0, 100) <= 5 else 0

        final_speed_mod = base_evasion + random_mod

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
