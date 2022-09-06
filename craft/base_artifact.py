"""
    Данный модуль содержит в себе базовый класс артефакта, который наследуют остальные классы
"""
from settings_imports_globalVariables import *


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
