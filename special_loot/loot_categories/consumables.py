"""
Данный модуль управляет выбором, выдачей предметов расходников таких как аптечки, уникальные патроны, гранаты, меды итд
"""
from imports_globalVariables import *
import exceptions

if __name__ == '__main__':
    raise exceptions.NotCallableModuleException


class Consumables:
    """
    Данный класс отвечает за формирование расходников, формирование данных для записи в статистику, но саму статистику
    в базу не записывает
    """
    def __init__(self, loot_params):
        self.loot_params = loot_params
        self.answer_string = None
        self.all_groups = self.select_all_groups()
        self.all_types = self.select_all_types()
        self.chosen_group = None
        self.chosen_type = None
        self.consumable_data = {}
        self.roll = None
        self.is_error = False

    def to_control_consumable_forming(self):
        """
        Основная управляющая функция класса, которая вызывается для формирования ответа
        """
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

        self.roll_dice()
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
        """
        Данный метод выбирает список всех групп расходников
        """
        groups_query = 'SELECT group_name FROM groups'
        groups = global_consumables_loot_cursor.execute(groups_query) # запрос в базу данных
        groups = [elem[0] for elem in groups]  # изымаю из кортежей значения названий групп и формирую список
        return groups

    @staticmethod
    def select_all_types():
        """
        Данный метод выбирает список всех типов расходников
        """
        types_query = 'SELECT type_name FROM types'
        types = global_consumables_loot_cursor.execute(types_query)  # запрос в базу данных
        types = [elem[0] for elem in types]  # изымаю из кортежей значения названий типов и формирую список
        return types

    def roll_dice(self):
        """
        Данная функция роллит кубики и формирует общий результат трёх бросков
        """
        result = 0
        for dice in range(3):  # бросок 3х кубиков
            roll = random.randint(1, 6)  # выбирается случайное значение от 1 до 6
            result += roll  # результат броска добавляется к общему значению
        self.roll = result

    def select_consumable_group(self):
        """
        Данна метод выбирает случайное значение из списка всех групп, если в запросе подразумевается рандом
        """
        consumable_group = random.choice(self.all_groups)  # выбираю случайный элемент из списка групп расходников
        self.chosen_group = consumable_group

    def select_consumable_item(self):
        """
        Данный метод вставляет в строку запроса в бд нужные значения и осуществляет запрос в базу данных
        """
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

        rows = global_consumables_loot_cursor.execute(item_select_string)  # осуществляется запрос в БД
        item = [dict(row) for row in rows]  # формирую из ответа в базу данных словарь из ключ-значений, где ключ это
        # название столбца, а значение это значение аттрибута
        self.consumable_data = item[0]  # изымаю словарь из списка

    def form_consumable_string(self):
        """
        Данный метод формирует строку ответа для пользователя. Именно она отображается в итоге в дискорде
        """
        consumable_string = f'''
Название: {self.consumable_data['consumable_name']}
Эффект: {self.consumable_data['consumable_description']}
Тип расходника: {self.consumable_data['type_name']}
Связанная характеристика: {"отсутствует" if self.consumable_data['sub_list_element'] is None else self.consumable_data['sub_list_element']}
{'Damage 8d(0-6 клетки)4d(7-12клеток)' if self.consumable_data['type_name'] == 'фраг-гранаты' else ''}
{'Damage 6d(0-4клеток)4d(5-8клеток.Игнор половины ВУ' if self.consumable_data['type_name'] == 'крак-гранаты' else ''}

    '''
        self.answer_string = consumable_string

    def process_data_for_statistics(self, roll: dict):
        """
        Данный метод обрабатывает статистику по результатам запроса в базу данных
        """
        current_time = time()  # берется текущий таймстэмп
        formatted_time = strftime("%Y-%m-%d", localtime(current_time))  # таймстэмп форматируется в дату

        self.consumable_data.update(roll)  # добавляю в словарь данных по расходнику ключ-значение с броском кубика
        self.consumable_data.update({'date': formatted_time})  # добавляю в словарь данные по дате запроса


def all_groups() -> str:
    """
    Данный метод выбирает список всех групп расходников
    """
    groups_query = 'SELECT group_name FROM groups'
    groups = global_consumables_loot_cursor.execute(groups_query)  # запрос в базу данных
    groups = [elem[0] for elem in groups]  # изымаю из кортежей значения названий групп и формирую список

    answer_template = Template('''
    Группы расходников:
    
{% for group in groups -%}
    {{ group }}
{% endfor %}
    ''')
    answer_string = answer_template.render(groups=groups)
    return answer_string


def all_types() -> str:
    """
    Данный метод выбирает список всех типов расходников
    """
    types_query = 'SELECT type_name FROM types'
    types = global_consumables_loot_cursor.execute(types_query)  # запрос в базу данных
    types = [elem[0] for elem in types]  # изымаю из кортежей значения названий типов и формирую список

    answer_template = Template('''
    Типы расходников:
    
{% for type in types -%}
    {{ type }}
{% endfor %}
    ''')
    answer_string = answer_template.render(types=types)
    return answer_string
