"""
    Данный модуль содержит в себе базовый класс артефакта, который наследуют остальные классы
"""
from settings_imports_globalVariables import *


class Artifact:
    """
    Базовый класс, инициализирующий характеристики по умолчанию, свойственные для всех групп артефактов, а также
    содержащий методы для их создания дочерними классами, которые наследуют данный родительский класс. Сам по себе он
    не вызывается, лишь содержит наследуемые методы.
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """
    def __init__(self, grade_modifier):

        # Префикс назначается все артефактам независимо от их типа и вида
        self.unique_prefix = self.get_prefix()
        self.grade_modifier = grade_modifier

        self.name = None
        self.art_type = None
        self.group_name = None
        self.weight = 1
        self.unique_suffix = ''
        self.str_requeriments = None

    def get_random_type_of_artifact(self, table_name: str) -> str:
        """
        Данная функция случайно выбирает один из типов артефактов в случае, если он прямо не указан в запросе
        :param table_name: название таблицы в бд, из которой будет делаться экзекьют. Таблица представляет собой
        одну из групп артефактов(броня, бижутерия, оружие-бб, оружие-дб)
        :return: строка с названием типа артефакта
        """

        excluded_artifact_types = ''
        # данный кортеж и проверка нужны чтобы исключить некоторые особо сильные виды артефактов для низкого грейда
        # чтобы игроки не получали их на слишком ранних этапах игры
        if self.grade_modifier < 1.10:
            excluded_artifact_types = ('одноручный-силовой-меч', 'двуручный-силовой меч',
                                       'мельтаган', 'мельта-пистолет',
                                       'болтер', 'болт-пистолет',
                                       'плазмаган', 'плазма-пистолет',
                                       'силовая-броня')

        chosen_artifact = tuple(bd_sqlite3_cursor.execute(f'''
    SELECT art_type_name FROM {table_name}
    WHERE art_type_name NOT IN {excluded_artifact_types}
    ORDER BY RANDOM()
    LIMIT 1'''))[0][0]  # [0][0] нужно чтобы изъять строку из кортежа с кортежами
        return chosen_artifact

    @staticmethod
    def get_prefix():
        """
         Данная функция случайно выбирает один из префиксов
        :return: кортеж с именем префикса и навыком, на который он влияет
        """
        prefix_tuple = tuple(bd_sqlite3_cursor.execute('''
SELECT * FROM unique_prefix
ORDER BY RANDOM()
LIMIT 1'''))
        return prefix_tuple

    @staticmethod
    def get_suffix(art_group: str, art_type: str) -> tuple:
        """
        Данная функция случайно выбирает один из суффиксов, доступные для выбора
        :param art_group: название группы артефактов, например artifact_armor, данные строки через f-строку
        добавляются в строку запроса БД для формирования JOIN-ов

        :param art_type: название конкретного типа артефакта для добавления в запрос в контрукции WHERE

        :return: строка с кортежом суффикса, где первый элемент это его название, использующееся для формирования имени
        а второй элемент это описание его уникального эффекта
        """
        suffix_tuple = tuple(bd_sqlite3_cursor.execute(f'''
SELECT unique_suffix.effect_name, unique_suffix.effect_text 
FROM unique_suffix
INNER JOIN unique_suffix_{art_group}_relations ON unique_suffix.effect_name == unique_suffix_{art_group}_relations.effect_name
INNER JOIN {art_group} ON unique_suffix_{art_group}_relations.art_type_name == {art_group}.art_type_name
WHERE {art_group}.art_type_name == '{art_type}'
ORDER BY RANDOM()
LIMIT 1'''))
        return suffix_tuple

    def get_name(self, prefix: tuple, art_type: str, suffix: tuple) -> None:
        """
        Данный метод формирует имя артефакта на основе сложнения префикс + тип артифкта + суффикс
        :param: префикс
        :param название типа артефакта
        :param суффикс
        :return: ничего, изменяет self.name
        """
        # Префикс и суффикс идут как кортеж с кортежом с двумя значениями поэтому во вложенном кортеже, поэтому
        # [0][0] используются для извлечения строки названия
        self.name = f'{prefix[0][0]} {art_type} {suffix[0][0]}'

    def get_weight(self) -> None:
        """
        Данный метод формирует вес артефакта на основе запроса в бд с применением случайного модификатора и модификатора
        грейда
        :return: ничего, изменяет self.weight
        """
        art_weight = tuple(bd_sqlite3_cursor.execute(f'''
SELECT art_weight FROM {self.group_name}
WHERE art_type_name == '{self.art_type}'
'''))[0][0]
        random_mod = random.uniform(1, 1.2)  # Случайный float в диапазоне
        # чем меньше вес тем лучше, поэтому грейд модификатор вычисляется данной формулой:
        # (1 - (self.grade_modifier - 1))
        self.weight = int(art_weight * (1 - (self.grade_modifier - 1)) * random_mod)

    def get_requiriments(self) -> None:
        """
        Данный метод формирует требования к силе при использовании артефакта с учетом  случайного модификатора, но
        без учета модификатора грейда
        :return: ничего, изменяет self.str_requeriments
        """
        art_reqs = tuple(bd_sqlite3_cursor.execute(f'''
SELECT art_str_req FROM {self.group_name}
WHERE art_type_name == '{self.art_type}'
'''))[0][0]
        # Данная строка проверяет бросок на неудачу и если она больше или равно 90, то у артефакта повышенные требования
        luck_mod = random.randint(0, 100)
        if luck_mod >= 90:
            art_reqs += 1
        self.str_requeriments = art_reqs
