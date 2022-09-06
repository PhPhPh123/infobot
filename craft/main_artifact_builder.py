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

from settings_imports_globalVariables import *
from craft.artifact_groups.armor import Armor
from craft.artifact_groups.jewerly import Jewelry
from craft.artifact_groups.weapons.close_combat_weapon import CloseCombatWeapon
from craft.artifact_groups.weapons.range_weapon import RangeWeapon


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
        art_object = Jewelry(art_user_dict['грейд'], art_user_dict['тип'], cursor)
    elif art_user_dict['группа'] == 'random':
        art_object = random.choice([
            Armor(art_user_dict['грейд'], art_user_dict['тип'], cursor),
            RangeWeapon(art_user_dict['грейд'], art_user_dict['тип'], cursor),
            CloseCombatWeapon(art_user_dict['грейд'], art_user_dict['тип'], cursor),
            Jewelry(art_user_dict['грейд'], art_user_dict['тип'], cursor)
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
