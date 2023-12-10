"""
Данный модуль отвечает за сбор статистики у спец. лута и записи его в соответствующие базы данных
--переделать базу данных в декларативную через sqlalchemy потом
"""

import exceptions

if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


def write_to_consumable_statistics(loot_data: dict) -> None:
    """
    Основная функция, записывающая статистику по расходникам
    """
    stat_string = form_consumable_string(loot_data)  # формирую строку запроса в БД

    global_consumables_statistics_cursor.execute(stat_string)  # записываю в базу
    global_consumables_statistics_connect.commit()


def form_consumable_string(loot_data: dict) -> str:
    """
    Функция, формирующая строку для sql-транзакции в базу данных
    """
    stat_string = f"""
INSERT INTO main_log ('event_result', 'consumable_name', 'roll_result', 
                      'group_name', 'type_name', 'sub_list_name',
                      'sub_list_element', 'date')
VALUES('{"failure" if loot_data["roll_result"] >= 17 else "success"}',
       '{loot_data['consumable_name']}', '{loot_data["roll_result"]}',
       '{loot_data['group_name']}', '{loot_data['type_name']}',
       '{loot_data['sub_list_name']}', '{loot_data['sub_list_element']}',
       '{loot_data['date']}')
"""
    return stat_string
