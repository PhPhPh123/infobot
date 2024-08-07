"""
Данный модуль является основным управляющим модулем пакета и отвечает на прием, обработку и выдачу информации о
получении особого игрового лута
"""


import exceptions

if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *
from special_loot.special_loot_statistics_collect import *
from special_loot.loot_categories.consumables import *


def to_control_loot_forming(loot_params: dict, loot_type: str = 'consumables') -> str:
    """
    Данная функция является фасадным методом, контролирующим работу фичи выдачи специальных предметов. На данный момент
    она ориентирована исключетельно на класс расходников, но в будущем появятся новые предметы и функция будет
    расширена
    """
    item_object = None  # инициализация объекта

    if loot_type == 'consumables':
        item_object = Consumables(loot_params)  # создаю объект класса расходников
        item_object.to_control_consumable_forming()  # вызываю основной управляющий метод
        try:  # пытаюсь узнать, если ли у параметров лута ключ, говорящий, что не нужен сбор статистики
            if loot_params['no_stat']:  # если его нет, то ничего не делаю. Статистику не записываю
                pass
        except KeyError:  # если ключа нет
            if not item_object.is_error:  # а также нет флага на ошибку
                write_to_consumable_statistics(item_object.consumable_data)  # то записываю статистику

    return item_object.answer_string  # возвращаю основную строку ответа которая уйдёт в чат


def display_items_groups_and_type(kind_loot, request) -> str:
    """
    Данная функция отвечает на выбор того, на что нужно выводить общий список из базы данных по специальным предметам
    """
    answer = None

    if kind_loot == 'consumables':
        if request == 'groups':
            answer = all_groups()
        else:
            answer = all_types()

    return answer
