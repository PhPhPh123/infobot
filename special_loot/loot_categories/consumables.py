"""
Данный модуль управляет выбором, выдачей предметов расходников таких как аптечки, уникальные патроны, гранаты, меды итд
"""
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

    def select_all_types():
        types_query = 'SELECT type_name FROM types'
        types = global_consumables_loot_sqlite3_cursor.execute(types_query)
        types = [elem[0] for elem in types]
        return types

    all_groups = select_all_groups()
    all_types = select_all_types()

    if loot_params['группа расходника'] not in all_groups and loot_params['группа расходника'] != 'random':
        return 'Неверная группа расходников', None

    if loot_params['тип расходника'] not in all_types and loot_params['тип расходника'] != 'random':
        return 'Неверный тип расходников', None

    roll_result = roll_dice()
    roll_dict = {'roll_result': roll_result}
    if roll_result < 17:
        pass
    else:
        return 'Выпала критнеудача. Упс.', process_data_for_statistics({}, roll_dict)

    if loot_params['группа расходника'] == 'random':
        consumable_group = select_consumable_group(all_groups)
    else:
        consumable_group = loot_params['группа расходника']

    type_str = '' if loot_params['тип расходника'] == 'random' else f"AND t.type_name = '{loot_params['тип расходника']}'"

    raw_consumable_data = select_consumable_item(consumable_group, type_str, roll_result)

    consumable_string = form_consumable_string(raw_consumable_data)

    processed_consumable_data = process_data_for_statistics(raw_consumable_data, roll_dict)

    return consumable_string, processed_consumable_data


def roll_dice():
    result = 0
    for dice in range(3):
        roll = random.randint(1, 6)
        result += roll

    return result


def select_consumable_group(all_groups) -> str:
    consumable_group = random.choice(all_groups)

    return consumable_group


def process_data_for_statistics(data: dict, roll: dict):
    current_time = time()
    formatted_time = strftime("%Y-%m-%d", localtime(current_time))

    data.update(roll)
    data.update({'date': formatted_time})

    return data


def select_consumable_item(group_name: str, type_str: str, roll_result: int) -> dict:
    item_select_string = f"""
    SELECT *
    FROM consumables c
    LEFT JOIN consumables_sub_lists cst ON c.sub_list_id=cst.sub_list_id
    LEFT JOIN sub_lists_elements sle ON cst.sub_list_id=sle.sub_list_id
    INNER JOIN consumables_types_relations ctr ON c.consumable_id=ctr.consumable_id
    INNER JOIN types t ON ctr.type_id=t.type_id
    INNER JOIN groups g ON t.group_id=g.group_id
    WHERE g.group_name = '{group_name}' AND
          c.min_dice_roll <= {roll_result} AND
          c.max_dice_roll >= {roll_result}
          {type_str}
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
Связанная характеристика: {"отсутствует" if item['sub_list_element'] is None else item['sub_list_element']}
'''
    return consumable_string
