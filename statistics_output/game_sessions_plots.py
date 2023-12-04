"""
    Данный модуль отвечает за вывод статистической информации по проведенным игровым сессиям. Он лишь выводит графики,
    а запись данных в базу осуществляется в модуле other_mechanics.game_sessions.game_sessions.py. Сами данные хранятся
    в базе game_sessions_db того же каталога
"""
from scipy.interpolate import make_interp_spline

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from imports_globalVariables import *


class AvgSessionDuration:
    def __init__(self, week_or_month: str):
        self.week_or_month = week_or_month
        self.query_str = None
        self.raw_dataset = None
        self.dataset = None
        self.is_error = None
        self.error_message = None

    def verify_data(self):
        pass

    def execute_db(self):
        self.query_str = 'SELECT * FROM sessions'

        result = global_game_sessions_sqlite3_cursor.execute(self.query_str)  # собственно экзекьют в базу
        result = [dict(row) for row in result]  # преобразование в список словарей
        self.raw_dataset = pd.DataFrame(result)  # преобразую сырые данные в сырой датасэт pandas

    def form_dataset(self):
        if self.week_or_month == 'week':
            dataset = self.raw_dataset.groupby(pd.to_datetime(self.raw_dataset['session_timestamp']).dt.isocalendar().week)\
                                      .agg({'session_hours': 'sum'})\
                                      .reset_index()
            dataset = dataset.rename(columns={'week': 'недели', 'session_hours': 'игровые часы'})
        else:
            dataset = self.raw_dataset.groupby(pd.to_datetime(self.raw_dataset['session_timestamp']).dt.strftime('%Y-%m'))\
                                      .agg({'session_hours': 'sum'})\
                                      .reset_index()
            dataset = dataset.rename(columns={'session_timestamp': 'месяцы', 'session_hours': 'игровые часы'})

        self.dataset = dataset

    def draw_plot(self):
        sns.set_style("darkgrid")  # выставляю стиль с сеткой

        sns.lineplot(x='месяцы' if self.week_or_month == "month" else 'недели',
                     y='игровые часы',
                     data=self.dataset,
                     estimator='mean',
                     marker='o',
                     linewidth=3)

        plt.title(f'Количество игровых часов по {"месяцам" if self.week_or_month == "month" else "неделям"}')
        plt.xticks(rotation=60)
        plt.gcf().set_size_inches(12, 9)  # выставляю размер для png картинки
        plt.savefig('logs_and_temp_files/game_sessions_plot')   # сохраняю в файл
        plt.close()  # закрываю фигуру

    def control_plot_forming(self):
        """
        Метод осуществляет последовательный вызов необходимых методов
        """
        self.verify_data()
        if self.is_error:
            return None
        self.execute_db()
        self.form_dataset()
        self.draw_plot()
