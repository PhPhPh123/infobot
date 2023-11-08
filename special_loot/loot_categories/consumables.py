"""
Данный модуль управляет выбором, выдачей предметов расходников таких как аптечки, уникальные патроны, гранаты, меды итд
"""
from imports_globalVariables import *
import exceptions

if __name__ == '__main__':
    raise exceptions.NotCallableModuleException


class Consumbales:
    def __init__(self, loot_params):
        self.loot_params = loot_params
        self.answer_string = None
        self.all_groups = self.select_all_groups()
        self.all_types = self.select_all_types()
        self.chosen_group = None
        self.chosen_type = None
        self.consumable_data = {}
        self.roll = None
        self.roll_dice()
        self.is_error = False

    def to_control_consumable_forming(self):
        # если неверное название группы расходника, то метод вываливается с None и ответом, что неверная группа
        if self.loot_params['группа расходника'] not in self.all_groups and self.loot_params['группа расходника'] != 'random':
            self.answer_string = 'Неверная группа расходников'
            self.is_error = True
            return None

        # если неверное название типа расходника, то метод вываливается с None и ответом, что неверный тип
        if self.loot_params['тип расходника'] not in self.all_types and self.loot_params['тип расходника'] != 'random':
            self.answer_string = 'Неверный тип расходников'
            self.is_error = True
            return None

        roll_dict = {'roll_result': self.roll}
        if self.roll < 17:  # если ролл меньше 17, то формирование нормальное и ничего делать не нужно
            pass
        else:  # если ролл больше 17, то формирование вываливается со строкой неудачи и словарём для статистики
            self.answer_string = 'Выпала критнеудача. Упс.'
            self.process_data_for_statistics(roll_dict)
            return None

        if self.loot_params['группа расходника'] == 'random':  # если группа случайная
            self.select_consumable_group()  # то выбираем случайную группу
        else:
            self.chosen_group = self.loot_params['группа расходника']  # иначе выбранная группа указанная в запросе

        # тут выдается кусок строки для select-а если в запросе выдается тип расходника, иначе не выставляется ничего
        # и подразумевается случайный выбор
        self.chosen_type = '' if self.loot_params[
                             'тип расходника'] == 'random' else f"AND t.type_name = '{self.loot_params['тип расходника']}'"

        # выполняю экзекьют в базу
        self.select_consumable_item()

        # формирую строку ответа для пользователя
        self.form_consumable_string()

        # формирую данные для статистики
        self.process_data_for_statistics(roll_dict)

    @staticmethod
    def select_all_groups():
        groups_query = 'SELECT group_name FROM groups'
        groups = global_consumables_loot_sqlite3_cursor.execute(groups_query)
        groups = [elem[0] for elem in groups]
        return groups

    @staticmethod
    def select_all_types():
        types_query = 'SELECT type_name FROM types'
        types = global_consumables_loot_sqlite3_cursor.execute(types_query)
        types = [elem[0] for elem in types]
        return types

    def roll_dice(self):
        result = 0
        for dice in range(3):
            roll = random.randint(1, 6)
            result += roll
        self.roll = result

    def select_consumable_group(self):
        consumable_group = random.choice(self.all_groups)

        self.chosen_group = consumable_group

    def process_data_for_statistics(self, roll: dict):
        current_time = time()
        formatted_time = strftime("%Y-%m-%d", localtime(current_time))

        self.consumable_data.update(roll)
        self.consumable_data.update({'date': formatted_time})

    def select_consumable_item(self):
        item_select_string = f"""
        SELECT *
        FROM consumables c
        LEFT JOIN consumables_sub_lists cst ON c.sub_list_id=cst.sub_list_id
        LEFT JOIN sub_lists_elements sle ON cst.sub_list_id=sle.sub_list_id
        INNER JOIN consumables_types_relations ctr ON c.consumable_id=ctr.consumable_id
        INNER JOIN types t ON ctr.type_id=t.type_id
        INNER JOIN groups g ON t.group_id=g.group_id
        WHERE g.group_name = '{self.chosen_group}' AND
              c.min_dice_roll <= {self.roll} AND
              c.max_dice_roll >= {self.roll}
              {self.chosen_type}
        ORDER BY random()
        LIMIT 1
        """

        rows = global_consumables_loot_sqlite3_cursor.execute(item_select_string)
        item = [dict(row) for row in rows]
        self.consumable_data = item[0]

    def form_consumable_string(self):
        consumable_string = f'''
Название: {self.consumable_data['consumable_name']}
Эффект: {self.consumable_data['consumable_description']}
Тип расходника: {self.consumable_data['type_name']}
Связанная характеристика: {"отсутствует" if self.consumable_data['sub_list_element'] is None else self.consumable_data['sub_list_element']}
    '''
        self.answer_string = consumable_string

