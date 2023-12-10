"""
    Данный класс содержит базовый класс оружия, методы и аттрибуты, характерные для всех видов оружия
    В __init__ реализован шаблон проектирования Строитель путем самосбора
"""
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *
from artifacts.base_artifact import Artifact


class Weapon(Artifact):
    """
    Базовый класс для дочерних классов CloseCombatWeapon и RangeWeapon
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """
    def __init__(self, grade_modifier: float, prefix: str):
        super().__init__(grade_modifier, prefix)
        self.damage = 18
        self.penetration = 'Отсутствует'
        self.prescision_modifier = 0

    @staticmethod
    def get_damage(weapon_group: str, weapon_type: str, grade_modifier: float) -> int:
        """
        Данный метод формирует параметр урона оружия
        :param weapon_group: группа оружия, дальний бой или ближний
        :param weapon_type: тип оружия, например лазган, болтер, силовой меч итд
        :param grade_modifier модификатор грейда, на который будет умножаться итоговый урон
        :return: int число с количеством брони(ВУ)
        """
        random_modifier = random.uniform(0.9, 1.1)  # Дополнительный рандом, на который будет умножен итоговый урон
        base_damage = tuple(global_artifacts_cursor.execute(f'''
SELECT art_damage FROM {weapon_group}
WHERE art_type_name == '{weapon_type}'
        '''))[0][0]  # Достаю из бд, из кортежа с кортежами [0][0], значение урона

        # Перемножаю базовый урон с рандомным модификатором и модификатором грейда
        final_damage = int(base_damage * random_modifier * grade_modifier)

        return final_damage

    def get_penetration(self, group_name, weapon_type: str) -> str:
        """
        Данный метод формирует параметр игнора ВУ(пробития)
        @param weapon_type: тип оружия, например лазган, болтер, силовой меч итд
        @param group_name: группа оружия описывающая название таблицы artifact_range_weapon или artifact_close_combat
        :return: строка, описывающая есть ли пробитие и если есть то какое
        """
        # Проверка на удачу, значения ближе к 1 считаются хорошими
        luck = random.randint(1, 100)

        penetration = tuple(global_artifacts_cursor.execute(f"""
SELECT art_penetration
FROM {group_name}
WHERE art_type_name == '{weapon_type}'"""))[0][0]

        if penetration == 1:  # Игнорирующие ВУ вооружения
            self.penetration = 'Игнор ВУ'
        elif penetration == 0.5:  # Пробивающие броню вооружения
            self.penetration = 'Игнор половины ВУ'
        else:  # Пробитие отсутствует
            self.penetration = 'Пробитие отсутствует'

        if penetration == 0 and luck <= 3:  # Если очень повезет, оружие без пробитие может получить игнор половины ВУ
            self.penetration = 'Игнор половины ВУ'

        return self.penetration

    @staticmethod
    def get_prescision(weapon_group: str, weapon_type: str) -> int:
        """
        Данный метод формирует параметр точности у оружия
        :param weapon_group: группа оружия, дальний бой или ближний
        :param weapon_type: тип оружия, например лазган, болтер, силовой меч итд
        :return: строка, описывающая есть ли количественный бонус/штраф к точности
        """
        # Проверка на удачу, значения ближе к 1 считаются хорошими
        luck = random.randint(1, 100)

        base_prescision = tuple(global_artifacts_cursor.execute(f'''
        SELECT art_prescision FROM {weapon_group}
        WHERE art_type_name == '{weapon_type}'
                '''))[0][0]  # Достаю из БД базовую точность из кортежа с кортежами [0][0]

        # Если выпал хорошая удача в luck то значение увеличивается на 1
        final_prescision = base_prescision + 1 if luck <= 10 else base_prescision

        return final_prescision
