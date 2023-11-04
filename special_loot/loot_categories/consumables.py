"""
Данный модуль управляет выбором, выдачей предметов расходников таких как аптечки, уникальные патроны, гранаты, меды итд
"""
import random

from imports_globalVariables import *
import exceptions

if __name__ == '__main__':
    raise exceptions.NotCallableModuleException


def to_control_consumable_forming(loot_params: dict) -> (str, list):
    def select_all_groups():
        groups_query = 'SELECT group_name FROM groups'
        groups = global_consumables_loot_sqlite3_cursor.execute(groups_query)
        groups = [elem[0] for elem in groups]
        return groups

    all_groups = select_all_groups()

    if loot_params['группа расходника'] not in all_groups and loot_params['группа расходника'] != 'random':
        return 'неверная группа расходников'

    roll_result = roll_dice()
    if roll_result < 17:
        pass
    else:
        return 'выпала критнеудача'

    if loot_params['группа расходника'] == 'random':
        consumable_group = select_consumable_group(all_groups)
    else:
        consumable_group = loot_params['группа расходника']

    consumable_data = select_consumable_item(consumable_group, roll_result)

    consumable_string = form_consumable_string(consumable_data)

    return consumable_string, consumable_data


def roll_dice():
    result = 0
    for dice in range(3):
        roll = random.randint(1, 6)
        result += roll

    return result


def select_consumable_group(all_groups) -> str:
    consumable_group = random.choice(all_groups)

    return consumable_group


def select_consumable_item(group: str, roll_result: int) -> dict:
    item_select_string = f"""
    SELECT *
    FROM consumables c
    LEFT JOIN consumables_sub_lists cst ON c.sub_list_id=cst.sub_list_id
    LEFT JOIN sub_lists_elements sle ON cst.sub_list_id=sle.sub_list_id
    INNER JOIN consumables_types_relations ctr ON c.consumable_id=ctr.consumable_id
    INNER JOIN types t ON ctr.type_id=t.type_id
    INNER JOIN groups g ON t.group_id=g.group_id
    WHERE g.group_name = '{group}' AND
          c.min_dice_roll <= {roll_result} AND
          c.max_dice_roll >= {roll_result}
    ORDER BY random()
    LIMIT 1
    """

    rows = global_consumables_loot_sqlite3_cursor.execute(item_select_string)
    item = [dict(row) for row in rows]
    return item[0]


def form_consumable_string(item: dict):
    consumable_string = f'''
Название: {item['consumable_name']}
Эффект: {item['consumable_description']}
Тип расходника: {item['type_name']}
Связанная характеристика(если есть): {"отсутствует" if item['sub_list_element'] is None else item['sub_list_element']}
'''
    return consumable_string
