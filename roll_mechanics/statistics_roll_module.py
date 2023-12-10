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

    Механики бросков:

    Обычный бросок(common_roll): обычный бросок 3d6 кубика согласно механике GURPS, чем меньше результат тем лучше
    Значения 3, 4 считаются критической удачей, значения 17, 18 - критической неудачей

    Мега-бросок(mega_roll): бросок 3d6 с некоторым шансом улучшения итогового результата

    Удачливый-бросок(luck_roll): двойной бросок 3d6 и выбор лучшего результата как основного. Несовместим с мега-броском

    Критический модификатор(crit_modifier): диапазон увеличения или уменьшения критической удачи, например при значении
    2, к критической удаче будут добавлены значения 5 и 6, а при -2 к критической неудаче будет добавлено 15 и 16
    """

    def __init__(self,
                 user_id: int,
                 dice_roll_required: str,
                 crit_modifier: str,
                 is_common_roll: bool = False,
                 is_mega_roll: bool = False,
                 is_luck_roll: bool = False):

        self.user_id = user_id  # id пользователя из месседжера discord
        self.dice_roll_required = dice_roll_required  # требуемое значение для успешного броска(чем меньше тем сложнее)
        self.is_common_roll = is_common_roll  # флаг, говорящий, что бросок является обычным.
        self.is_mega_roll = is_mega_roll  # флаг, говорящий, что бросок проходит с механикой мегаброска
        self.is_luck_roll = is_luck_roll  # флаг, говорящий, что бросок проходит с механикой удачи
        self.crit_modifier = crit_modifier  # модификатор увеличения или уменьшения диапазона критической удачи
        self.crit_success_values = [3, 4]
        self.crit_failure_values = [17, 18]
        self.db_query_string = None  # строка запроса в базу данных
        self.user_name = None  # параметр с именем игрока, который берется из базы данных
        self.dice_result = None  # итоговый результат броска кубиков, суммированных из 3х бросков
        self.roll_description = None  # строковое описание итога броска на основе разныци между кубиком и сложность броска
        self.chat_answer = None  # итоговая строка ответа в чат игроку
        self.mega_roll_success = False  # флаг, определяющий удачна ли была механика мегаброска и сработал ли ее шанс
        self.is_error = False  # флаг, определяющий наличие ошибки при формировании класса

    @staticmethod
    def check_gamers() -> tuple[list, list]:
        """
        Данный статический метод собирает id(discord-а) и имя игровой из базы данных метод
        """
        gamers_str = 'SELECT * FROM gamers'
        all_gamers = global_dice_roll_statistics_cursor.execute(gamers_str)  # запрос в бд
        all_gamers_ids = [elem[0] for elem in all_gamers]  # создаю список с discord id игроков
        return all_gamers_ids, list(all_gamers)

    def set_user_name(self):
        """
        Данный метод выбирает из таблицы с игроками имя игрока на основании его id
        """
        gamers_str = f"SELECT user_name FROM gamers WHERE discord_user_id = {self.user_id}"

        # изымаю имя из кортежа с кортежами
        user_name = list(global_dice_roll_statistics_cursor.execute(gamers_str))[0][0]
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

        if self.user_id not in self.check_gamers()[0]:  # если id пользователя нет в списке пользователей
            self.chat_answer = 'Вы не зарегистрированы как игрок'
            self.is_error = True

        if int(self.crit_modifier) < -2 or int(self.crit_modifier) > 2:  # если крит. модификатор выходит за диапазон
            self.chat_answer = 'Критический модификатор должен быть в диапазоне от -2 до 2'
            self.is_error = True

        try:
            # если параметр на цифра то тут будет исключение
            int(self.dice_roll_required)

            # сложность броска должна быть в пределах в диапазона кубов, не больше не меньше
            assert 3 <= int(self.dice_roll_required) < 18

            # сложность броска должна быть integer числом или равна ему
            assert int(self.dice_roll_required) == float(self.dice_roll_required)

        except (TypeError, ValueError, AssertionError):
            self.chat_answer = 'Неверный формат сложности броска, введите число от 3 до 18'
            self.is_error = True

    def process_user_input(self):
        """
        Данный метод преобразует введенные в чате аргументы в нужный формат т.к. из чата всё приходит в виде строки
        """
        self.dice_roll_required = int(self.dice_roll_required)
        self.crit_modifier = int(self.crit_modifier)

    def roll_dice(self):
        """
        Данный метод осуществляет бросок кубов и записывает результат
        """
        def roll():
            """
            Внутренняя функция бросающая кубы
            """
            roll_result = 0
            for dice in range(3):
                # бросаю каждый кубик отдельно (первый элемент) и добавляю его результат к сумме
                dice_result = random.randint(1, 6)
                roll_result += dice_result
            return roll_result

        if not self.is_luck_roll:  # если бросок не является удачливым, то просто бросается 1 раз
            self.dice_result = roll()
        else: # иначе бросок удачливый и бросок осуществляется дважды с выбором лучшего результата(чем меньше тем лучше)
            self.dice_result = min(roll(), roll())

    def check_mega_roll(self):
        """
        Данный метод осуществляет проверку механики мега-ролла, если запрашивается команда с ним
        """
        if self.is_mega_roll:  # если флаг на мегаролл есть, то производятся проверки
            megaroll = random.randint(1, 5)  # бросок на удачу, мегаролл сработает при 1, т.е. шанс 20%

            # если результат удачливый и его есть куда улучшать(при броске 3 его некуда улучшать)
            if megaroll == 1 and self.dice_result != 3:
                self.dice_result -= 1  # итоговый результат улучшается на 1
                self.mega_roll_success = True  # и вешается флаг, что повезло
            else:  # если удача не сработала, то механика не отрабатывает
                pass
        else:  # если флага нет, то метод не отрабатывает
            pass

    def set_crit_modifier(self):
        """
        Данный метод на основе модификатора крита добавляет новые значения в список критический значений. Допустимые
        значения это -2, -1, 1, 2. Иные значения не пройдут валидацию
        """
        if self.crit_modifier > 0:  # если модификатор больше 0, то в список добавляется 5 или 5 и 6
            for digit in range(self.crit_modifier):
                self.crit_success_values.append(max(self.crit_success_values) + 1)
        elif self.crit_modifier < 0:  # если модификатор меньше 0 нуля то в список добавляются 16 или 16 и 15
            for digit in range(abs(self.crit_modifier)):
                self.crit_failure_values.append(min(self.crit_failure_values) - 1)
        else:  # если модификатор равен нулю, то механика не отрабатывает
            pass

    def check_result(self):
        """
        Данный метод проверяет результаты броска и определяет итоговую текстовую характеристику его удачности
        """
        # основной параметр, определяющий качество броска кубика на основе разницы между требуемым результатом и
        # выброшенным на кубиках
        required_and_rolled_diff = self.dice_roll_required - self.dice_result

        # если результат входит в критические диапазоны, то текстом это поясняется
        if self.dice_result in self.crit_success_values:
            self.roll_description = 'критический успех'
        elif self.dice_result in self.crit_failure_values:
            self.roll_description = 'критическая неудача'

        # Если бросок в целом успешный, но не критический, то на основе разницы между требуемым и полученным
        # результатом определяется настолько успешным был бросок кубика и на основе которого ГМ может опрелять
        # настолько вышло успешным действие
        elif required_and_rolled_diff > 10:
            self.roll_description = 'очень значительный успех'
        elif 5 <= required_and_rolled_diff <= 9:
            self.roll_description = 'значительный успех'
        elif 2 <= required_and_rolled_diff <= 4:
            self.roll_description = 'обычный успех'
        elif 0 <= required_and_rolled_diff <= 1:
            self.roll_description = 'минимальный успех'

        # Если бросок в целом не успешный, то тут определяется текстовое описание для ГМа насколько он не успешный
        # поскольку система GURPS, в целом, имеет некоторый перекос в сторону более успешных действий игрока в своей
        # базе, поэтому -5 уже считается серьезным провалом
        elif required_and_rolled_diff == -1:
            self.roll_description = 'минимальный провал'
        elif -2 >= required_and_rolled_diff >= -4:
            self.roll_description = 'обычный провал'
        elif required_and_rolled_diff <= -5:
            self.roll_description = 'серьезный провал'

    def form_answer(self):
        """
        Данный метод формирует строку ответа для пользователя в чате
        """
        answer_temp = f'''
Игрок: {self.user_name}
Результат броска: {self.roll_description}, Значение кубика: {self.dice_result}
Бросок с удачей: {'нет' if not self.is_luck_roll else 'да'}
Сработал ли мегабросок: {'нет' if not self.mega_roll_success else 'да'}
        '''
        self.chat_answer = answer_temp

    def write_to_stat_database(self):
        """
        Данный метод записывает результаты броска кубика в базу данных
        """
        insert_query_string = f"""
    INSERT INTO roll_results (discord_user_id, dice_roll_required, dice_result, roll_description, roll_timestamp,
                              is_luck_roll, is_mega_roll, is_common_roll, mega_roll_success, crit_modifier)
    VALUES({self.user_id}, {self.dice_roll_required}, {self.dice_result}, 
           '{self.roll_description}', datetime('now'), {self.is_luck_roll}, 
           {self.is_mega_roll}, {self.is_common_roll}, {self.mega_roll_success},
           {self.crit_modifier})
        """
        # тут используются глобальные переменные курсора и коннекта из модуля imports_globalVariables.py
        global_dice_roll_statistics_cursor.execute(insert_query_string)
        global_dice_roll_statistics_connect.commit()

    def control_roll_forming(self):
        """
        Основной управляющий метод строитель, вызывающий поэтапно все остальные и конструирующий экземляр класса
        """
        self.verify_user_input()
        if self.is_error:
            return None
        self.process_user_input()
        self.set_user_name()
        self.roll_dice()
        self.set_crit_modifier()
        self.check_result()
        self.check_mega_roll()
        self.form_answer()
        self.write_to_stat_database()
