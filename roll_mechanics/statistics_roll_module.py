"""
    Данный модуль отвечает броски статистических кубиков, расчета результатов броска и вывод его в чате, а также
    записью результатов броска в базу данных
"""

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
                 is_common_roll: bool = False,
                 is_mega_roll: bool = False,
                 is_luck_roll: bool = False):

        self.user_id = user_id
        self.dice_roll_required = dice_roll_required
        self.is_common_roll = is_common_roll
        self.is_mega_roll = is_mega_roll
        self.is_luck_roll = is_luck_roll
        self.crit_modifier = crit_modifier
        self.user_name = None
        self.dice_result = None
        self.roll_description = None
        self.chat_answer = None
        self.mega_roll_success = False
        self.db_query_string = None
        self.is_error = False

    @staticmethod
    def check_gamers() -> tuple[list, list]:
        """
        Данный статический метод собирает id(discord-а) и имя игровой из базы данных метод
        """
        gamers_str = 'SELECT * FROM gamers'
        all_gamers = global_dice_roll_statistics_sqlite3_cursor.execute(gamers_str)  # запрос в бд
        all_gamers_ids = [elem[0] for elem in all_gamers]  # создаю список с discord id игроков
        return all_gamers_ids, list(all_gamers)

    def set_user_name(self):
        """
        Данный метод выбирает из таблицы с игроками имя игрока на основании его id
        """
        gamers_str = f"SELECT user_name FROM gamers WHERE discord_user_id = {self.user_id}"

        # изымаю имя из кортежа с кортежами
        user_name = list(global_dice_roll_statistics_sqlite3_cursor.execute(gamers_str))[0][0]
        self.user_name = user_name

    def verify_user_input(self):
        """
        Данный метод верифицирует введенные данные для команды ролла
        """
        try:  # проверяю, может ли модификатор крита быть приведен к int-типу
            int(self.crit_modifier)
        except (TypeError, ValueError):  # если нет, то вывожу чат что введено нет
            self.chat_answer = 'Параметр диапазона критической удачи должен быть числом от -5 до 5'
            self.is_error = True

        if self.user_id not in self.check_gamers()[0]:
            self.chat_answer = 'Вы не зарегистрированы как игрок'
            self.is_error = True

        if int(self.crit_modifier) < -2 or int(self.crit_modifier) > 2:
            self.chat_answer = 'Критический модификатор должен быть в диапазоне от -2 до 2'
            self.is_error = True

        try:
            int(self.dice_roll_required)
            assert 3 <= int(self.dice_roll_required) < 18
            assert int(self.dice_roll_required) == float(self.dice_roll_required)
        except (TypeError, ValueError, AssertionError):
            self.chat_answer = 'Неверный формат сложности броска, введите число от 3 до 18'
            self.is_error = True

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
        if self.is_mega_roll:
            megaroll = random.randint(1, 5)

            if megaroll == 1 and self.dice_result != 3:
                self.dice_result -= 1
                self.mega_roll_success = True
        else:
            pass

    def check_result(self):
        required_and_rolled_diff = self.dice_roll_required - self.dice_result
        crit_success_values = [3, 4]
        crit_failure_values = [17, 18]

        if self.crit_modifier > 0:
            for digit in range(self.crit_modifier):
                crit_success_values.append(max(crit_success_values) + 1)
        if self.crit_modifier < 0:
            for digit in range(abs(self.crit_modifier)):
                crit_failure_values.append(min(crit_failure_values) - 1)

        if self.dice_result in crit_success_values:
            self.roll_description = 'критический успех'
        elif self.dice_result in crit_failure_values:
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
        elif -2 >= required_and_rolled_diff >= -3:
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
    INSERT INTO roll_results (discord_user_id, dice_roll_required, dice_result, roll_description, roll_timestamp,
                              is_luck_roll, is_mega_roll, is_common_roll, mega_roll_success, crit_modifier)
    VALUES({self.user_id}, {self.dice_roll_required}, {self.dice_result}, 
           '{self.roll_description}', datetime('now'), {self.is_luck_roll}, 
           {self.is_mega_roll}, {self.is_common_roll}, {self.mega_roll_success},
           {self.crit_modifier})
        """
        global_dice_roll_statistics_sqlite3_cursor.execute(insert_query_string)
        global_dice_roll_statistics_sqlite3_connect.commit()

    def control_roll_forming(self):
        self.verify_user_input()
        if self.is_error:
            return None
        self.process_user_input()
        self.set_user_name()
        self.roll_dice()
        self.check_result()
        self.check_mega_roll_()
        self.form_answer()
        self.write_to_stat_database()
