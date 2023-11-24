"""
    Данный модуль отвечает за вывод в чат статистических графиков касательно исторических данных о выброшенных игроками
    игральных кубиков, сложности броска и их результата, а также дополнительных модификаторов. Данные о брошенных
    кубиков записываются в модуле roll_mechanics/statistics_roll_module.py, а сами данные хранятся в базе roll_stat_db
    в директории того же пакета
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


class BasePlotFormer:
    """
    Базовый класс для запросов из базы данных информации по броскам, формированию из нее датасэта и визуализации
    в виде графиков. Данный класс является абстрактным и наследуется остальными классами конкретных графиков формируя
    для них структуру через наследуемые аттрибуты и методы, а также требуя реализации абстрактных методов
    """
    def __init__(self):
        self.query_str = None
        self.query_result = None
        self.dataset = None
        self.allow_common_rolls = True
        self.allow_luck_rolls = False
        self.allow_mega_rolls = False
        self.allow_crit_modifier = False

    @abstractmethod
    def form_dataset(self):
        pass

    @abstractmethod
    def draw_plot(self):
        pass

    @abstractmethod
    def control_plot_forming(self):
        pass

    def form_query_str(self):
        self.query_str = f"""
    SELECT dice_result, user_name FROM roll_results r
    INNER JOIN gamers g ON r.discord_user_id=g.discord_user_id
    WHERE {'' if self.allow_common_rolls else 'NOT'} is_common_roll
          {'' if self.allow_luck_rolls else 'AND NOT is_luck_roll'}
          {'' if self.allow_mega_rolls else 'AND NOT is_mega_roll'}
          {'' if self.allow_crit_modifier else 'AND crit_modifier == 0'}
        """

    def execute_db(self):
        result = global_dice_roll_statistics_sqlite3_cursor.execute(self.query_str)
        result = [dict(row) for row in result]
        self.query_result = result


class MeanResultsByGamers(BasePlotFormer):
    """
    Данный класс занимается отрисовкой и выдачей в чат столбчатую диаграмму по среднему кубу игроков. Учитываются
    только обычные кубы команды !roll без дополнительных модификаторов. Наследует базовый класс
    """
    def __init__(self):
        super().__init__()

    def form_dataset(self):
        raw_dataset = pd.DataFrame(self.query_result)
        grouped_dataset = raw_dataset.groupby('user_name', as_index=False).agg({'dice_result': 'mean'})
        grouped_dataset = grouped_dataset.sort_values(by='dice_result')
        grouped_dataset['dice_result'] = round(grouped_dataset['dice_result'], 2)

        self.dataset = grouped_dataset

    def draw_plot(self):
        plt.Figure(figsize=(10, 15))
        sns.set_style("darkgrid")
        ax = sns.barplot(x='user_name', y='dice_result', data=self.dataset, palette='deep')
        ax.set(title='Среднее значение обычных кубиков по игрокам', xlabel='Игроки', ylabel='Среднее значение кубика')

        plt.savefig('logs_and_temp_files/mean_results_by_gamers.png')

    def control_plot_forming(self):
        self.form_query_str()
        self.execute_db()
        self.form_dataset()
        self.draw_plot()


class HistResultsByGamers(BasePlotFormer):
    """
    Данный класс занимается отрисовкой и выдачей в чат гистограммы по брошенным кубам в разрезе по игрокам.
    Учитываются только обычные кубы команды !roll без дополнительных модификаторов
    """
    def __init__(self):
        super().__init__()

    def form_dataset(self):
        pass

    def draw_plot(self):
        pass

    def control_plot_forming(self):
        self.form_query_str()
        self.execute_db()
        self.form_dataset()
        self.draw_plot()
