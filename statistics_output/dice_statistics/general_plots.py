"""
    Данный модуль отвечает за вывод в чат статистических графиков касательно исторических данных о выброшенных игроками
    игральных кубиков, сложности броска и их результата, а также дополнительных модификаторов. Данные о брошенных
    кубиков записываются в модуле roll_mechanics/statistics_roll_module.py, а сами данные хранятся в базе roll_stat_db
    в директории того же пакета
"""
from abc import ABC

import pandas as pd

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
        self.query_str = None  # строка запрос в базу данных
        self.query_result = None  # список словарей в котором ключ это название столбца, а значения это его значения
        self.dataset = None  # датасэт pandas
        self.allow_common_rolls = True  # флаг определяющий учет или не учет обычных бросков командой !roll
        self.allow_luck_rolls = False  # флаг определяющий учет или не учет бросков с модификатором удачи(двойных)
        self.allow_mega_rolls = False  # флаг определяющий учет или не учет бросков с шансом на улучшение результата
        self.allow_crit_modifier = False  # флаг определяющий учитывать или нет броски с измененным модификатором крита
        self.is_error = False  # флаг, определяющий ошибку
        self.error_message = None  # строка для ответа в чат в случае если запрос ошибочен

    @abstractmethod
    def form_dataset(self):
        """
        Метод, который в дочерних классах содержит данные для формирования датасэта pandas
        """
        pass

    @abstractmethod
    def draw_plot(self):
        """
        Метод, который в дочерних классах содержит данные для отрисовки графика в matplotlib или seaborn и сохранения
        в виде png картинки
        """
        pass

    @abstractmethod
    def control_plot_forming(self):
        """
        Метод, который в дочерних классах содержит управляющие вызовы остальных методов и определяет порядок выполнения
        остальных методов
        """
        pass

    def form_query_str(self):
        """
        Данный метод содержит sql строку, которая отправляется в базу для получения необходимых данных. Конструкции
        f-строки нужны чтобы исключить флаги, определяющие учет или не учет конкретных групп бросков(бросок с удачей,
        бросок с улучшением mega_roll, модификаторами такими как диапазон критической удачи итд. Данные особые броски
        могут исключаться из собранной статистики чтобы не портить ее или наоборот, быть включены исключительно они)
        """
        self.query_str = f"""
    SELECT * FROM roll_results r
    INNER JOIN gamers g ON r.discord_user_id=g.discord_user_id
    WHERE {'' if self.allow_common_rolls else 'NOT'} is_common_roll
          {'' if self.allow_luck_rolls else 'AND NOT is_luck_roll'}
          {'' if self.allow_mega_rolls else 'AND NOT is_mega_roll'}
          {'' if self.allow_crit_modifier else 'AND crit_modifier == 0'}
        """

    def execute_db(self):
        """
        Данный метод осуществляет запрос в базу данных и преобразует сырые данные так, чтобы они представляли собой
        словарь
        """
        result = global_dice_roll_statistics_sqlite3_cursor.execute(self.query_str)  # собственно экзекьют в базу
        result = [dict(row) for row in result]  # преобразование в список словарей
        self.query_result = result


class AvgRollsPlotFormer(BasePlotFormer):
    """
    Данный класс занимается отрисовкой и выдачей в чат столбчатой диаграммы по среднему кубу игроков. Учитываются
    только обычные кубы команды !roll без дополнительных модификаторов. Наследует базовый класс
    """
    def __init__(self):
        super().__init__()

    def form_dataset(self):
        """
        Данный метод формирует pandas датасэт путем группировки по имени игрока и агрегации его, среднего значения
        брошенных кубов, он обязателен и наследуется от абстрактного метода базового класса
        """
        raw_dataset = pd.DataFrame(self.query_result)  # преобразую сырые данные в сырой датасэт pandas

        # группирую по имени игрока и аггрегирую средние результаты бросков кубика
        grouped_dataset = raw_dataset.groupby('user_name', as_index=False).agg({'dice_result': 'mean'})
        grouped_dataset = grouped_dataset.sort_values(by='dice_result')  # сортирую по значению среднего кубика
        grouped_dataset['dice_result'] = round(grouped_dataset['dice_result'], 2)  # округляю значения

        self.dataset = grouped_dataset

    def draw_plot(self):
        """
        Данный метод отрисовывает столбчатую диаграмму по средним значениям результатов брошенных игроком за всё время,
        он обязателен и наследуется от абстрактного метода базового класса
        """
        sns.set_style("darkgrid")  # выставляю стиль с сеткой
        ax = sns.barplot(x='user_name', y='dice_result', data=self.dataset, palette='deep')  # рисую график
        # выставляю названия осей и графика
        ax.set(title='Среднее значение обычных кубиков по игрокам', xlabel='Игроки', ylabel='Среднее значение кубика')

        # сохраняю в виде картинки в каталоге с времеменными файлами откуда она будет загружена в чат
        plt.savefig('logs_and_temp_files/mean_results_by_gamers.png')
        plt.close()  # закрываю объект фигуры

    def control_plot_forming(self):
        """
        Метод осуществляет последовательный вызов необходимых методов
        """
        self.form_query_str()
        self.execute_db()
        self.form_dataset()
        self.draw_plot()


class AllRollsPlotFormer(BasePlotFormer):
    """
    Данный класс занимается отрисовкой и выдачей в чат гистограммы по брошенным кубам в разрезе по игрокам.
    Учитываются только обычные кубы команды !roll без дополнительных модификаторов
    """
    def __init__(self, user_name: str):
        super().__init__()
        self.user_name = user_name

    def check_gamers(self):
        """
        Данный метод проверяет, что выбранный игрок(если он выбран), зарегистрирован в таблице gamers
        """
        gamers_str = 'SELECT * FROM gamers'
        all_gamers = global_dice_roll_statistics_sqlite3_cursor.execute(gamers_str)  # запрос в бд
        all_gamers = [elem[1] for elem in all_gamers]  # создаю список именами игроков

        if self.user_name not in all_gamers:
            self.is_error = True
            self.error_message = f'Неверное имя игрока. Введите один из этих вариантов: {all_gamers}'

    def form_dataset(self):
        """
        Данный метод формирует pandas датасэт, он обязателен и наследуется от абстрактного метода базового класса
        """
        raw_dataset = pd.DataFrame(self.query_result)  # преобразую сыры данные в сырой датасэт pandas

        self.dataset = raw_dataset[['user_name', 'dice_result']]  # отбираю только данные по игроку и его броску куба

        # если команда подразумевает вывод под конкретного игрока, то датасэт фильтруется под него
        if self.user_name != '':
            self.dataset = self.dataset[self.dataset['user_name'] == self.user_name]

        # меняю названия столбцов
        self.dataset = self.dataset.rename(columns={'user_name': 'Игроки', 'dice_result': 'результат броска'})

    def draw_plot(self):
        """
        Данный метод отрисовывает гистограмму по всем броскам игроков за всё время, в разрезе игрока,
        он обязателен и наследуется от абстрактного метода базового класса
        """
        sns.set_style("darkgrid")  # выставляю стиль с сеткой

        # кол-во корзин должно быть равно кол-ву уник.значений кубов чтобы несколько значений в одно не смешивались
        bins = self.dataset['результат броска'].nunique()

        # строю гистограмму с типом stack и нужным количеством корзин
        ax = sns.histplot(x='результат броска', data=self.dataset, hue='Игроки', multiple="stack", bins=bins)
        # выставляю нужные параметры
        ax.set(title='Количество выпавших значений на кубах в разрезе игроков',
               xlabel='Значения кубов',
               ylabel='Количество бросков')
        plt.xticks(numpy.arange(3, 19, 1))  # количество тиков соответствует количество потенциальных результатов

        # сохраняю в виде картинки в каталоге с времеменными файлами откуда она будет загружена в чат
        plt.savefig('logs_and_temp_files/all_results_by_gamers.png')
        plt.close()  # закрываю объект фигуры

    def control_plot_forming(self):
        """
        Метод осуществляет последовательный вызов необходимых методов
        """
        # если команда не подразумевает вывод одного игрока, то метод не отрабатывает
        if self.user_name == '':
            pass
        else:
            self.check_gamers()
            if self.is_error:  # если в результате работы метода дался этот флаг, значит игрока нет в списке
                return None  # и формирование экземпляра класса нужно прекратить

        self.form_query_str()
        self.execute_db()
        self.form_dataset()
        self.draw_plot()


class MeanRollsByTimePlotFormer(BasePlotFormer):
    def __init__(self, datetime_type):
        super().__init__()
        self.datetime_type = datetime_type

    def form_dataset(self):
        """
        Данный метод формирует pandas датасэт, он обязателен и наследуется от абстрактного метода базового класса
        """
        raw_dataset = pd.DataFrame(self.query_result)  # преобразую сыры данные в сырой датасэт pandas

        dataset = raw_dataset.groupby([pd.to_datetime(raw_dataset['roll_timestamp']).dt.date,
                                       raw_dataset['user_name']]) \
                             .agg({'dice_result': 'mean'}).reset_index()

        dataset = dataset.rename(columns={
                                          'user_name': 'Игрок',
                                          'dice_result': 'Среднее значение кубика'})
        self.dataset = dataset

    def draw_plot(self):
        sns.set_style("darkgrid")  # выставляю стиль с сеткой

        ax = sns.lineplot(data=self.dataset, x='roll_timestamp', y='Среднее значение кубика', hue='Игрок')

        # выставляю нужные параметры
        ax.set(title='Среднее значение кубика в разрезе сессии',
               xlabel='Дата',
               ylabel='Среднее значение кубика')
        plt.xticks(rotation=27)

        plt.gcf().set_size_inches(12, 8)
        # сохраняю в виде картинки в каталоге с времеменными файлами откуда она будет загружена в чат
        plt.savefig('logs_and_temp_files/mean_results_by_datetime.png')
        plt.close()  # закрываю объект фигуры

    def control_plot_forming(self):
        self.form_query_str()
        self.execute_db()
        self.form_dataset()
        self.draw_plot()


