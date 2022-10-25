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

----------------------------------------------------------------------------------------------------------------------
    Глоссарий специфический названий и обозначений использующихся в группе модулей:

    Артефакт: уникальный, процедурно генерируемый предмет высокой редкости с уникальными особенностями

    Грейд/grade: качество артефакта выращающееся в его цвете(синий, зеленый, фиолетовый, красный)

    Группа артефактов/group_name: 4 основных группы, на которые делятся артефакты, броня, бижутерия, оружие-бб(оружие ближнего боя)
    , оружие-дб(оружие дальнего боя)

    Тип артефакта/ art_type: конкретный вид артефакта внутри группы, например внутри оружия-бб могут быть одноручные пиломечи,
    силовые мечи, обычные клинки, пилотопоры,  а в бижутерии серьги, амулеты, кольца итд

    Модификатор грейда/grade_modifier: множитель, на который умножаются некоторые численные характеристики артефакта

    Имя артефакта/name: процедурно сгенерированное имя на основе префикса, типа артефакта и суффикса, например
    Разведовательный лазган добивания

    Префикс/unique_prefix: первая уникальная особенность артефакта, выраженная в бонусе Удачи(возможности дважды бросик кубик навыка)
     к одной из характеристик согласно системе GURPS

    Суффикс/unique_suffix: вторая уникальная особенность артефакта, выраженное в уникальном боевом эффекте список которых разный
    для разных типов артефактов

    Требования/Требования силы/str_requeriments: необходимое количество силы, нужное для использования
    артефакта без штрафов

    Вес/ weight: масса артефакта

    Бонус бижутерии/jewelry_bonus: уникальный эффект, свойственный исключительно для бижутерии

    Броня, ВУ, Вычет урона, armor: модификатор брони, на который уменьшается весь входящий урон по игрокам/мобам

    Модификатор скорости/speed_modifier: модификатор бонуса/штрафа к передвижению для брони

    Модификатор уклонения/evasion_modifier модификатор бонуса/штрафа к уклонению для брони

    Урон/damage: повреждения оружия выращающиеся либо в int значении либо в преобразованном для ролки значении типа 10d6

    Пробитие/Игнор ВУ/penetration: модификатор полностью либо в 50% игнорирующий параметр брони

    Точность/prescision_modifier: модификатор добавляющий или снижающий точность в игре

    Скорость атаки/attack_speed: скорость стрельбы оружия дальнего боя

    Дальность/range: дальность стрельбы оружия дальнего боя

    Модификатор парирования/ parry_modifier: модификатор дающий бонус/штраф для парирования в игре в ближнем бою
-----------------------------------------------------------------------------------------------------------------------
    Структура отвечающей за формирование артефактов таблиц в базе данных:

    Таблицы базовой информации о группах артефактов и их основных характеристиках:

    ###artifact_armor### --- Броня
    Содержит столбцы с:
    названием типа брони, названием группы, базовой броней(ВУ),
    базовым весом, базовым требованием силы, базовой скоростью, базовым уклонением

    ###artifact_close_combat### --- Оружие ближнего боя
    Содержит столбцы с:
    названием типа оружия, названием группы, базовым уроном,
    базовой точностью, базовым бонусом к парированию, базовым весом, базовым требованием силы

    ###artifact_range_weapon### --- Оружие дальнего боя
    Содержит столбцы с:
    названием типа оружия, названием группы, базовым уроном,
    базовой точностью, базовой дальностью, базовой скоростью атаки, базовым весом, базовым требованием силы

    ###artifact_jewelry### --- Бижутерия
    Содержит столбцы с:
    названием типа бижутерии, названием группы, базовым весом, базовым требованием силы

    ###unique_suffix### - Суффиксы артефактов
    Содержит столбцы с:
    названием эффекта, текстовым описанием эффекта

    ###unique_prefix### - Префиксы артефактов
    Содержит столбцы с:
    названием эффекта, скиллом, на который он влияет

    Группа таблиц ###unique_suffix_*название группы артефактов*_relations
    Связующие таблицы многие ко многим связывающие типа артефактов с названиями суффиксов, которые могут быть
    выданы для нужного типа артефакта

    ###unique_jewelry_bonuses### - собственные бонусы бижутерии
    Содержит столбцы с:
    названием бонуса, текстовым описанием бонуса

    ###artifact_jewelry_unique_jewelry_bonuses_relations###
    Таблица со связью многие ко многим, обеспечивающая связь между названием типа бижутерии из таблицы artifact_jewelry
    и названием доступного ей бонуса из таблицы unique_jewelry_bonuses
-----------------------------------------------------------------------------------------------------------------------
"""

from settings_imports_globalVariables import *
from craft.artifact_groups.armor import Armor
from craft.artifact_groups.jewerly import Jewelry
from craft.artifact_groups.weapons.close_combat_weapon import CloseCombatWeapon
from craft.artifact_groups.weapons.range_weapon import RangeWeapon


def choise_class_objects(art_user_dict: dict) -> str:
    """
    Данная функция получает модификатор грейда от нижестоящей функции count_grade_modifier
    осуществляет случайный или неслучайный выбор класса, для которого будет формироваться
    объект и отправляет итоговый словарь __dict__ в функцию подготовки строкового ответа, а затем высылает ее в
    основной модуль для отправки в чат. Функция носит контролирующую задачу

    :param art_user_dict: словарь, хранящий базовую информацию о первоначальном запросе в чате и указывающий
    какой тип артефакта должен быть создан или все отдается на волю рандома
    :return: итоговая строка ответа для бота
    """
    print(art_user_dict)

    # Данная структура возвращает строковое сообщение об ошибке ботом, если запрашиваются данные типы и группы сильных
    # артефактов. В билдере ниже они также исключаются из рандома при запросе в БД в модуле base_artifact
    excluded_artifact_types = ('одноручный-силовой-меч', 'двуручный-силовой меч',
                               'мельтаган', 'мельта-пистолет',
                               'болтер', 'болт-пистолет',
                               'плазмаган', 'плазма-пистолет',
                               'силовая-броня')

    if art_user_dict['грейд'] == 'зеленый' and art_user_dict['тип'] in excluded_artifact_types:
        return 'С зеленым грейдом нельзя создавать данный тип артефакта т.к. он слишком мощный'
    if art_user_dict['грейд'] in ('зеленый', 'синий') and art_user_dict['группа'] == 'бижутерия':
        return 'Бижутерия с зеленым грейдом не роллится обычным способом, только если на рандоме очень повезет'

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
        art_object = Armor(art_user_dict['грейд_модификатор'], art_user_dict['тип'])

    elif art_user_dict['группа'] == 'оружие-дб':
        art_object = RangeWeapon(art_user_dict['грейд_модификатор'], art_user_dict['тип'])

    elif art_user_dict['группа'] == 'оружие-бб':
        art_object = CloseCombatWeapon(art_user_dict['грейд_модификатор'], art_user_dict['тип'])
        # строчка ниже исключает бижутерию из ролла для зеленых типов артефактов, хотя, если очень повезет,
        # то можно будет получить

    elif art_user_dict['группа'] == 'бижутерия':
        art_object = Jewelry(art_user_dict['грейд_модификатор'], art_user_dict['тип'])

    elif art_user_dict['группа'] == 'random':
        rand_list = [Armor(art_user_dict['грейд_модификатор'], art_user_dict['тип']),
                     RangeWeapon(art_user_dict['грейд_модификатор'], art_user_dict['тип']),
                     CloseCombatWeapon(art_user_dict['грейд_модификатор'], art_user_dict['тип'])]
        if art_user_dict['грейд'] not in ('зеленый', 'синий'):
            rand_list.append(Jewelry(art_user_dict['грейд_модификатор'], art_user_dict['тип']))

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


if __name__ == '__main__':
    raise NotCallableModuleException
