"""

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

    def __init__(self, user_id: str, dice_roll_required: str, mega_roll: bool = False):
        self.user_id = user_id
        self.dice_roll_required = dice_roll_required
        self.mega_roll = mega_roll
        self.dice_result = None
        self.roll_success = None
        self.chat_answer = None
        self.db_query_string = None

    def process_user_input(self):
        try:
            int(self.user_id)
            assert len(self.user_id) == 18 # работаю без интернета, проверить потом сколько цифр в id
            assert int(self.user_id) == float(self.user_id)
            self.user_id = int(self.user_id)
        except Exception:
            self.chat_answer = 'Некорректный id пользователя'

    def control_dice_roll(self):
        self.verify_data()
