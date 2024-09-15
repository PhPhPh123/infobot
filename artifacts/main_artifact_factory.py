"""
Данный модуль является основным управляющим модулем пакета, он создает на основе полученных данных необходимый
экземляр класса, а также создает итоговую строку на основе готового экземляра класса. Модуль построен на основе
шаблона проектирования Фасад(получение словаря с данными ->возврат итоговой строки) и Фабричный метод(выбор экземляра
класса на основе полученных данных)
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *
from artifacts.artifact_groups.armor import Armor
from artifacts.artifact_groups.jewerly import Jewelry
from artifacts.artifact_groups.weapons.close_combat_weapon import CloseCombatWeapon
from artifacts.artifact_groups.weapons.range_weapon import RangeWeapon


def choise_class_objects(art_user_dict: dict) -> str:
    """
    Данная функция получает модификатор грейда от нижестоящей функции count_grade_modifier
    осуществляет случайный или неслучайный выбор класса, для которого будет формироваться
    объект и отправляет итоговый словарь __dict__ в функцию подготовки строкового ответа, а затем высылает ее в
    основной модуль для отправки в чат. Функция носит контролирующую задачу

    :param art_user_dict: словарь, хранящий базовую информацию о первоначальном запросе в чате и указывающий
    какой тип артефакта должен быть создан или все отдается на волю рандома. В словарь входят следующие ключ-значения:
    грейд: качество предмета представленное одним из 4х цветов, зеленым, синим, фиолетовым или красным
    группа: общая группа артефактов, броня, оружие-бб, оружие-дб, бижутерия
    тип: внутри каждой группы подтип, например тяжелая броня, легкая броня
    особенность: конкретная суффиксная особенность
    Все параметры словаря, кроме грейда, имеют значения по умолчанию random и будут в нижестоящих модулях выбираться
    случайно
    :return: итоговая строка ответа для бота
    """

    # Данная структура возвращает строковое сообщение об ошибке ботом, если запрашиваются данные типы и группы сильных
    # артефактов со слишком низким грейдом. В билдере ниже они также исключаются из рандома при запросе в БД
    # в модуле base_artifact
    excluded_artifact_types = ('одноручный-силовой-меч', 'двуручный-силовой меч',
                               'мельтаган', 'мельта-пистолет',
                               'болтер', 'болт-пистолет',
                               'плазмаган', 'плазма-пистолет',
                               'силовая-броня')

    if art_user_dict['грейд'] == 'зеленый' and art_user_dict['тип'] in excluded_artifact_types:
        return 'С зеленым грейдом нельзя создавать данный тип артефакта т.к. он слишком мощный'
    if art_user_dict['грейд'] in 'зеленый' and art_user_dict['группа'] == 'бижутерия':
        return 'Бижутерия с зеленым грейдом не роллится обычным способом, только если на рандоме повезет'
    if art_user_dict['грейд'] != 'красный' and art_user_dict['тип'] == 'реликвия':
        return 'Реликвии могут быть лишь красного грейда либо выпасть на рандоме если повезет'

    #  float модификатор, который используется для умножения некоторых числовых характеристик артефактов
    art_user_dict['грейд_модификатор'] = count_grade_modifier(art_user_dict['грейд'])

    if art_user_dict['грейд'] not in ('зеленый', 'синий', 'фиолетовый', 'красный'):
        return "Некорректное название грейда"

    """
    Структура ниже осуществляет выбор типа артефакта, если он есть, или случайный выбор, если его нет
    и создает экземляр соответствующего класса отправляя в них их модификатор грейда, тип артефакта(если выбран, если
    не выбран то random)
    """

    if art_user_dict['группа'] == 'броня':
        art_object = Armor(art_user_dict['грейд_модификатор'], art_user_dict['тип'],
                           art_user_dict['префикс'], art_user_dict['суффикс'])

    elif art_user_dict['группа'] == 'оружие-дб':
        art_object = RangeWeapon(art_user_dict['грейд_модификатор'], art_user_dict['тип'],
                                 art_user_dict['префикс'], art_user_dict['суффикс'])
    elif art_user_dict['группа'] == 'оружие-бб':
        art_object = CloseCombatWeapon(art_user_dict['грейд_модификатор'], art_user_dict['тип'],
                                       art_user_dict['префикс'], art_user_dict['суффикс'])
        # строчка ниже исключает бижутерию из ролла для зеленых типов артефактов, хотя, если очень повезет,
        # то можно будет получить

    elif art_user_dict['группа'] == 'бижутерия':
        art_object = Jewelry(art_user_dict['грейд_модификатор'], art_user_dict['тип'],
                             art_user_dict['префикс'], art_user_dict['суффикс'], grade_name=art_user_dict['грейд'])

    elif art_user_dict['группа'] == 'random':
        rand_list = [Armor(art_user_dict['грейд_модификатор'], art_user_dict['тип'],
                           art_user_dict['префикс'], art_user_dict['суффикс']),
                     RangeWeapon(art_user_dict['грейд_модификатор'], art_user_dict['тип'],
                                 art_user_dict['префикс'], art_user_dict['суффикс']),
                     CloseCombatWeapon(art_user_dict['грейд_модификатор'], art_user_dict['тип'],
                                       art_user_dict['префикс'], art_user_dict['суффикс'])]
        if art_user_dict['грейд'] not in ('зеленый', 'синий'):
            rand_list.append(Jewelry(art_user_dict['грейд_модификатор'], art_user_dict['тип'],
                                     art_user_dict['префикс'], art_user_dict['суффикс'], grade_name=art_user_dict['грейд']))

        art_object = random.choice(rand_list)

    else:
        return 'Некорректное название группы, типа артефакта'

    # Итоговая строка ответа
    final_string = form_string_answer(art_object.__dict__)

    logger.info('\n' + '[artifact]' '\n' + final_string)
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
        grade_modifier = 0.97
    elif grade == 'синий':
        grade_modifier = 1.08
    elif grade == 'фиолетовый':
        grade_modifier = 1.20
    elif grade == 'красный':
        grade_modifier = 1.3
    else:
        return None

    # Выбирает случайное float-число в данном диапазоне с целью внесения фактора рандома
    balance_mod = random.uniform(0.95, 1.1)

    # Кидаю кубик на критудачу и критнеудачу, если она прокает то модификатор дополнительно изменяет итоговое значение
    # Значение luck_mod-а ниже 5 это критудача, значение выше 95 это критнеудача
    luck_mod = 1.0
    luck_roll = random.randint(1, 100)
    if luck_roll < 5:
        luck_mod = 1.10
    elif luck_roll > 95:
        luck_mod = 0.9

    return grade_modifier * balance_mod * luck_mod


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
        final_string += f"Модификатор шагов(дистанция бега): {artifact_dict['speed_modifier']}\n"

    # Создание строк, характерных для бижутерии
    if artifact_dict['group_name'] == 'artifact_jewelry':
        final_string += f"Бонус бижутерии: {artifact_dict['jewerly_bonus'][0]}\n"
        final_string += f"Описание бонуса: {artifact_dict['jewerly_bonus'][1]}\n"

    # Создание строк, характерных для всех артефактов независимо от группы
    final_string += f"Требования силы: {artifact_dict['str_requeriments']}\n"
    final_string += f"Weight: {artifact_dict['weight']}кг\n"

    final_string += f"Особенность: 1 раз в сессию удача для навыка {artifact_dict['unique_prefix'][0][1]}\n"
    final_string += f"Особенность: {artifact_dict['unique_suffix'][0][1]}"

    flamethrower_mec_string = """\n\nРаботает механика огнемёта: атаковать можно в конусе примерно 30градусов. 
Количество затронутых целей и время горения зависит от разницы между точностью и кубом. 
Можно попасть даже при неудаче"""
    if artifact_dict['art_type'] == 'огнемёт':
        final_string += flamethrower_mec_string

    return final_string
