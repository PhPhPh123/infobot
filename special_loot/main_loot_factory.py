"""
Данный модуль является основным управляющим модулем пакета и отвечает на прием, обработку и выдачу информации о
получении особого игрового лута
"""

from imports_globalVariables import *
import exceptions

if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from special_loot.special_loot_statistics import *
from special_loot.loot_categories.consumables import *


def to_control_loot_forming(loot_params: dict, loot_type: str = 'consumables') -> str:
    if loot_type not in ['consumables']:
        return 'неверный тип лута'

    item_object = Consumbales(loot_params)
    item_object.to_control_consumable_forming()

    if loot_type == 'consumables':
        try:
            if loot_params['no_stat']:
                pass
        except KeyError:
            if not item_object.is_error:
                write_to_consumable_statistics(item_object.consumable_data)

    return item_object.answer_string
