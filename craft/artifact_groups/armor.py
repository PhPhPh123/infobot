"""
    Данный модуль содержит в себе класс нательной брони. В __init__ реализован шаблон проектирования
    Строитель путем самосбора
"""
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *
from craft.base_artifact import Artifact


class Armor(Artifact):
    """
    Данный артефактный класс создает объект и является конечным в цепочке наследования. Он формирует бижутерию и
    наследуюется от класса Artifact
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """
    def __init__(self, grade_modifier, armor_type):
        super().__init__(grade_modifier)
        self.group_name = 'artifact_armor'

        # Данные аттрибуты формируют в родительском классе Artifact
        self.art_type = armor_type if armor_type != 'random' else self.get_random_type_of_artifact(self.group_name)
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.get_weight()
        self.get_requiriments()

        # Данные аттрибуты формируют методы в данном классе
        self.armor = self.get_armor(grade_modifier)
        self.speed_modifier = self.get_speed_bonus()
        self.evasion_modifier = self.get_evasion()

    def get_armor(self, grade_modifier: float) -> int:
        """
        Данный метод формирует параметр ВУ(вычета урона), он же броня для артефакта
        :param grade_modifier: модификатор грейда, на который будет умножаться базовая броня
        :return: int число с количеством брони(ВУ)
        """
        base_armor = tuple(global_bd_sqlite3_cursor.execute(f'''
SELECT art_armor FROM artifact_armor
WHERE art_type_name == '{self.art_type}'
        '''))[0][0]  # [0][0] отвечает за извлечение числа из кортежа с кортежами

        final_armor = int(base_armor * grade_modifier) # перемножаю базовую броню, из БД с модификатором грейда

        return final_armor

    def get_speed_bonus(self) -> int:
        """
        Данный метод формирует бонус или штраф к броне на основе значения, полученного из БД и применения
        модификатора удачи, если результат броска будет меньше 5
        :return: int число с параметром бонуса/штрафа
        """
        base_speed_mod = tuple(global_bd_sqlite3_cursor.execute(f'''
        SELECT art_speed FROM artifact_armor
        WHERE art_type_name == '{self.art_type}'
                '''))[0][0]  # [0][0] отвечает за извлечение числа из кортежа с кортежами
        random_mod = 1 if random.randint(0, 100) <= 5 else 0

        final_speed_mod = base_speed_mod + random_mod

        return final_speed_mod

    def get_evasion(self):
        """
        Данный метод формирует бонус или штраф к уклонению на основе значения, полученного из БД и применения
        модификатора удачи, если результат броска будет меньше 5
        :return: int число с параметром бонуса/штрафа
        """
        base_evasion = tuple(global_bd_sqlite3_cursor.execute(f'''
        SELECT art_evasion FROM artifact_armor
        WHERE art_type_name == '{self.art_type}'
                '''))[0][0]  # [0][0] отвечает за извлечение числа из кортежа с кортежами
        random_mod = 1 if random.randint(0, 100) <= 5 else 0

        final_speed_mod = base_evasion + random_mod

        return final_speed_mod
