"""
    Данный класс содержит базовый класс оружия, методы и аттрибуты, характерные для всех видов оружия
"""
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from settings_imports_globalVariables import *
from craft.base_artifact import Artifact


class Weapon(Artifact):
    """
    Базовый класс для дочерних классов CloseCombatWeapon и RangeWeapon
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """
    def __init__(self, grade_modifier: float):
        super().__init__(grade_modifier)
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
        base_damage = tuple(global_bd_sqlite3_cursor.execute(f'''
SELECT art_damage FROM {weapon_group}
WHERE art_type_name == '{weapon_type}'
        '''))[0][0]  # Достаю из бд, из кортежа с кортежами [0][0], значение урона

        # Перемножаю базовый урон с рандомным модификатором и модификатором грейда
        final_damage = int(base_damage * random_modifier * grade_modifier)

        return final_damage

    def get_penetration(self, weapon_type: str) -> str:
        """
        Данный метод формирует параметр игнора ВУ(пробития)
        :param weapon_type: тип оружия, например лазган, болтер, силовой меч итд
        :return: строка, описывающая есть ли пробитие и если есть то какое
        """
        # Проверка на удачу, значения ближе к 1 считаются хорошими
        luck = random.randint(1, 100)

        # Данные типы вооружения по умолчанию считаются имеющими игнор ВУ
        if weapon_type in ('мельтаган', 'мельта-пистолет',
                           'одноручный-силовой-меч', 'двуручный-силовой-меч'):
            self.penetration = 'Игнор ВУ'
        # Данные типы вооружения считаются по умолчанию с игнором половины ВУ, но если очень повезет(luck <=3)
        # то и другие типы вооружения могут данный модификатор получить
        elif weapon_type in ('плазмаган', 'плазма-пистолет') or luck <= 3:
            if weapon_type not in ('лазган', 'лаз-пистолет'):
                self.penetration = 'Игнор половины ВУ'
        else:  # В иных случаях модификатор отсутствует
            self.penetration = 'Пробитие отсутствует'
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

        base_prescision = tuple(global_bd_sqlite3_cursor.execute(f'''
        SELECT art_prescision FROM {weapon_group}
        WHERE art_type_name == '{weapon_type}'
                '''))[0][0]  # Достаю из БД базовую точность из кортежа с кортежами [0][0]

        # Если выпал хорошая удача в luck то значение увеличивается на 1
        final_prescision = base_prescision + 1 if luck <= 10 else base_prescision

        return final_prescision
