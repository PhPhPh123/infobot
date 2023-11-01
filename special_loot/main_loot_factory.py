"""
Данный модуль является основным управляющим модулем пакета и отвечает на прием, обработку и выдачу информации о
получении особого игрового лута
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from loot_categories.consumables import *


def to_control_loot_forming(loot_params: dict, loot_type: str = 'consumables') -> str:
    loot_string = ''
    return loot_string


def write_to_statistics(loot_list: list):
    pass
