"""

"""
import random

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


class DiceRollerWithStatistics:
    """
    Данная класс осуществляет ролл кубика исключительно 3d6 согласно правилам GURPS, а также осуществляет запись
    результатов бросков в специальную базу данных
    user_id: int, dice_roll_required: str, important_dice: str) -> str:
    :return: результат сложения бросков кубика
    """

    def __init__(self,
                 user_id: int,
                 dice_roll_required: str,
                 crit_modifier: str,
                 mega_roll: bool = False,
                 is_luck_roll: bool = False):

        self.user_id = user_id
        self.dice_roll_required = dice_roll_required
        self.mega_roll = mega_roll
        self.is_luck_roll = is_luck_roll
        self.crit_modifier = crit_modifier
        self.user_name = None
        self.dice_result = None
        self.roll_description = None
        self.chat_answer = None
        self.mega_roll_success = False
        self.db_query_string = None

    @staticmethod
    def check_gamers():
        gamers_str = 'SELECT discord_user_id FROM gamers'
        all_gamers = global_dice_roll_statistics_sqlite3_cursor.execute(gamers_str)
        all_gamers = [elem[0] for elem in all_gamers]
        return all_gamers

    def select_user_name(self):
        gamers_str = f"SELECT ser_name FROM gamers WHERE discord_user_id = '{self.user_id}'"
        user_name = global_dice_roll_statistics_sqlite3_cursor.execute(gamers_str)[0]
        self.user_name = user_name

    def verify_user_input(self):
        try:
            int(self.crit_modifier)
        except Exception:
            self.chat_answer = 'Параметр диапазона критической удачи должен быть числом от -5 до 5'

        if self.user_id not in self.check_gamers():
            self.chat_answer = 'Вы не зарегистрированы как игрок'

        try:
            int(self.dice_roll_required)
            assert 3 <= int(self.dice_roll_required) < 18
            assert int(self.dice_roll_required) == float(self.dice_roll_required)
        except Exception:
            self.chat_answer = 'Неверный формат сложности броска, введите число от 3 до 18'

    def process_user_input(self):
        self.dice_roll_required = int(self.dice_roll_required)
        self.crit_modifier = int(self.crit_modifier)

    def roll_dice(self):
        def roll():
            roll_result = 0
            for dice in range(3):
                # бросаю каждый кубик отдельно (первый элемент) и добавляю его результат к сумме
                dice_result = random.randint(1, 6)
                roll_result += dice_result
            return roll_result

        if not self.is_luck_roll:
            self.dice_result = roll()
        else:
            self.dice_result = min(roll(), roll())

    def check_mega_roll_(self):
        if self.mega_roll:
            megaroll = random.randint(1, 10)

            if megaroll == 1 and self.dice_result != 3:
                self.dice_result -= 1
                self.mega_roll_success = True
        else:
            pass

    def check_result(self):
        required_and_rolled_diff = self.dice_roll_required - self.dice_result
        print(required_and_rolled_diff)

        if self.dice_result in (3, 4):
            self.roll_description = 'критический успех'
        elif self.dice_result == (17, 18):
            self.roll_description = 'критическая неудача'

        elif required_and_rolled_diff > 10:
            self.roll_description = 'очень значительный успех'
        elif 5 <= required_and_rolled_diff <= 9:
            self.roll_description = 'значительный успех'
        elif 2 <= required_and_rolled_diff <= 4:
            self.roll_description = 'обычный успех'
        elif 0 <= required_and_rolled_diff <= 1:
            self.roll_description = 'минимальный успех'

        elif required_and_rolled_diff == -1:
            self.roll_description = 'минимальный провал'
        elif -2 <= required_and_rolled_diff <= -3:
            self.roll_description = 'обычный провал'
        elif required_and_rolled_diff <= -4:
            self.roll_description = 'серьезный провал'

    def form_answer(self):
        answer_temp = f'''
Игрок: {self.user_name}
Результат броска: {self.roll_description}, Значение кубика: {self.dice_result}
Бросок с удачей: {'нет' if not self.is_luck_roll else 'да'}
Сработал ли мегабросок: {'нет' if not self.mega_roll_success else 'да'}
        '''
        self.chat_answer = answer_temp

    def write_to_stat_database(self):
        insert_query_string = f"""
    INSERT INTO roll_results (discord_user_id, dice_roll_required, dice_result, roll_description, 
                              mega_roll, mega_roll_success, roll_timestamp, crit_modifier)
    VALUES({self.user_id}, {self.dice_roll_required}, {self.dice_result}, 
           '{self.roll_description}', {self.mega_roll}, {self.mega_roll_success},
           datetime('now'), {self.crit_modifier})
        """
        print(insert_query_string)
        global_dice_roll_statistics_sqlite3_cursor.execute(insert_query_string)
        global_dice_roll_statistics_sqlite3_connect.commit()

    def control_roll_forming(self):
        self.verify_user_input()
        self.process_user_input()
        self.roll_dice()
        self.check_result()
        self.form_answer()
        self.write_to_stat_database()
        print('after stat')
