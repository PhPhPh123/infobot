"""
    Данный модуль содержит в себе класс оружия ближнего боя. В __init__ реализован шаблон проектирования
    Строитель путем самосбора
"""
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *
from artifacts.artifact_groups.weapons.base_weapons import Weapon


class CloseCombatWeapon(Weapon):
    """
    Класс, отвечающий за оружие ближнего боя
    Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ переменная
    """
    def __init__(self, grade_modifier, weapon_type, prefix, suffix):
        super().__init__(grade_modifier, prefix)
        # Данные аттрибуты/методы идут из базовых классов
        self.group_name = 'artifact_close_combat'
        self.art_type = weapon_type if weapon_type != 'random' else self.get_random_type_of_artifact(self.group_name)
        self.unique_suffix = self.get_suffix(self.group_name, self.art_type, suffix)
        self.get_name(self.unique_prefix, self.art_type, self.unique_suffix)
        self.damage = self.get_damage(self.group_name, self.art_type, grade_modifier)
        self.penetration = self.get_penetration(self.group_name, self.art_type)
        self.prescision_modifier = self.get_prescision(self.group_name, self.art_type)
        self.get_weight()
        self.get_requiriments()

        # Собственные аттрибуты и методы
        self.parry_modifier = self.get_parry_bonus()

    def get_parry_bonus(self):
        """
        Данный метод формирует параметр парирования у оружия ближнего боя
        :return: численный модификатор бонуса или штрафа к парированию
        """

        # Бросок на удачу, чем ниже результат тем лучше
        luck_modifier = random.randint(1, 100)
        parry_modifier = 0  # иницилизация параметра дополнительного изменения парирования

        art_parry = tuple(global_bd_sqlite3_cursor.execute(f'''
                    SELECT art_parry_bonus FROM artifact_close_combat
                    WHERE art_type_name == '{self.art_type}'
'''))[0][0]  # достаю из БД базовый показатель парирования, [0][0] чтобы вытащить значение из кортежа с кортежами

        # Чем меньше ролл удачи тем выше бонус к парированию, высокие значения дают штраф
        if luck_modifier <= 5:
            parry_modifier = 2
        elif 6 <= luck_modifier <= 10:
            parry_modifier = 1
        elif luck_modifier >= 90:
            parry_modifier = -1

        return parry_modifier + art_parry
