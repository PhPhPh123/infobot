"""
    Данный модуль отвечает за вывод статистической информации по проведенным игровым сессиям. Он лишь выводит графики,
    а запись данных в базу осуществляется в модуле other_mechanics.game_sessions.game_sessions.py. Сами данные хранятся
    в базе game_sessions_db того же каталога
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from imports_globalVariables import *


class SessionHoursPlotFormer:
    """
    Данный класс занимается получением данных по проведенным игровым сессиям, а также формирование линейных графиков
    по этим данным в разрезе месяцов или недель
    """
    def __init__(self, week_or_month: str):
        self.week_or_month = week_or_month  # параметр должен должать строку 'week' или 'month', отвечает на группировку
        self.query_str = None  # строка sql запроса
        self.raw_dataset = None  # необработанный датасэт pandas на основе всех данных из бд
        self.dataset = None  # обработанный и сгруппированный датасэт
        self.is_error = False  # флаг, говорящий об ошибке
        self.error_message = None  # сообщение ошибки, которое будет выведено в чат

    def verify_data(self):
        """
        Данный метод верифицирует данные полученные командой
        """
        if self.week_or_month not in ('week', 'month'):  # проверяю корректность параметра
            self.is_error = True  # если нет, то даю флаг ошибки и ее текст
            self.error_message = 'Нужно указать параметр week или month, например !display_sessions_stat week'

    def execute_db(self):
        """
        Данный метод осуществляет запрос в базу данных и по итогу создает на его основе сырой pandas датасэт
        """
        self.query_str = 'SELECT * FROM sessions'

        result = global_game_sessions_cursor.execute(self.query_str)  # собственно экзекьют в базу
        result = [dict(row) for row in result]  # преобразование в список словарей
        self.raw_dataset = pd.DataFrame(result)  # преобразую сырые данные в сырой датасэт pandas

    def form_dataset(self):
        """
        Метод формирует сгруппированный датасэт на основе которого будет строиться график
        """
        if self.week_or_month == 'week':  # датасэт для группировки по неделям
            dataset = self.raw_dataset.groupby(pd.to_datetime(self.raw_dataset['session_timestamp']).dt.isocalendar().week)\
                                      .agg({'session_hours': 'sum'})\
                                      .reset_index()
            dataset = dataset.rename(columns={'week': 'недели', 'session_hours': 'игровые часы'})

        else:  # датасэт для группировки по месяцам
            dataset = self.raw_dataset.groupby(pd.to_datetime(self.raw_dataset['session_timestamp']).dt.strftime('%Y-%m'))\
                                      .agg({'session_hours': 'sum'})\
                                      .reset_index()
            dataset = dataset.rename(columns={'session_timestamp': 'месяцы', 'session_hours': 'игровые часы'})

        self.dataset = dataset

    def draw_plot(self):
        """
        Метод рисует график на основе готового pandas-датасэта
        """
        sns.set_style("darkgrid")  # выставляю стиль с сеткой

        sns.lineplot(x='месяцы' if self.week_or_month == "month" else 'недели',  # столбцы могут иметь разные названия
                     y='игровые часы',
                     data=self.dataset,
                     marker='o',
                     linewidth=3)

        # выставляю параметры
        plt.title(f'Количество игровых часов по {"месяцам" if self.week_or_month == "month" else "неделям"}')
        plt.xticks(rotation=60)  # наклоняю тики обозначений x-оси
        plt.gcf().set_size_inches(12, 9)  # выставляю размер для png картинки
        plt.savefig('logs_and_temp_files/game_sessions_plot')   # сохраняю в файл
        plt.close()  # закрываю фигуру

    def control_plot_forming(self):
        """
        Метод осуществляет последовательный вызов необходимых методов
        """
        self.verify_data()
        if self.is_error:  # если флаг получен True в методе verify_data, то формирование объекта прекращается
            return None
        self.execute_db()
        self.form_dataset()
        self.draw_plot()
