"""
Данный модуль является основным управляющим модулем пакета и отвечает на прием, обработку и выдачу информации о
получении особого игрового лута
"""

from imports_globalVariables import *
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from special_loot.loot_categories.consumables import *


def to_control_loot_forming(loot_params: dict, loot_type: str = 'consumables') -> str:
    if loot_type not in ['consumables']:
        return 'неверный тип лута'

    loot_string, loot_data = to_control_consumable_forming(loot_params)
    write_to_statistics(loot_data)

    return loot_string


def write_to_statistics(loot_data: list) -> None:
    pass
