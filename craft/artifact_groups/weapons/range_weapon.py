"""
    Данный модуль содержит в себе класс оружия дальнего боя
"""

from settings_imports_globalVariables import *
from craft.artifact_groups.weapons.base_weapons import Weapon
import exceptions


class RangeWeapon(Weapon):
    """
    Класс, отвечающий за оружие ближнего боя
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """

    def __init__(self, grade_modifier, weapon_type):
        super().__init__(grade_modifier)

        # Данные аттрибуты/методы идут из базовых классов
        self.group_name = 'artifact_range_weapon'
        self.art_type = weapon_type if weapon_type != 'random' else self.get_random_type_of_artifact(self.group_name)
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.damage = self.get_damage(self.group_name, self.art_type, grade_modifier)
        self.penetration = self.get_penetration(self.art_type)
        self.prescision_modifier = self.get_prescision(self.group_name, self.art_type)
        self.get_weight()
        self.get_requiriments()

        # Собственные аттрибуты и методы
        self.attack_speed = self.get_attack_speed()
        self.range = self.get_range()

    def get_range(self):
        """
        Данный метод формирует параметр дистанции стрельбы
        :return: численный модификатор дистанции стрельбы
        """
        # достаю из БД базовый показатель парирования, [0][0] чтобы вытащить значение из кортежа с кортежами
        base_range = tuple(global_bd_sqlite3_cursor.execute(f'''
                SELECT art_range FROM artifact_range_weapon
                WHERE art_type_name == '{self.art_type}'
                        '''))[0][0]

        final_range = 0  # инициализация итогового параметра дальности стрельбы

        # чем больше базовая дистанция, тем выше коридор рандома в функции randint, с перекосом в сторону увеличения
        if base_range <= 7:
            final_range = random.randint((base_range - 1), (base_range + 1))
        elif 8 <= base_range <= 14:
            final_range = random.randint((base_range - 1), (base_range + 3))
        elif base_range >= 15:
            final_range = random.randint((base_range - 2), (base_range + 4))

        return final_range

    def get_attack_speed(self):
        """
        Данный метод формирует параметр скорости стрельбы
        :return: численный модификатор скорости стрельбы
        """

        # достаю из БД базовый показатель скорости стрельбы, [0][0] чтобы вытащить значение из кортежа с кортежами
        base_attack_speed = tuple(global_bd_sqlite3_cursor.execute(f'''
                SELECT art_attack_speed FROM artifact_range_weapon
                WHERE art_type_name == '{self.art_type}'
                '''))[0][0]

        final_attack_speed = 1  # инициализация итоговой скорости стрельбы

        # чем больше базовой скорости стрельбы, тем выше коридор рандома в функции randint, с перекосом
        # в сторону увеличения
        if base_attack_speed == 1:  # Если скорость стрельбы равна 1, то менять ее не нужно т.к. это для баланса
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


if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
