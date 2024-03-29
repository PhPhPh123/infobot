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
        self.query_str = None  # строка запрос в базу данных
        self.raw_dataset = None  # список словарей в котором ключ это название столбца, а значения это его значения
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
        try:  # пытаюсь выполнить экзекьют в бд
            result = global_dice_roll_statistics_cursor.execute(self.query_str)  # собственно экзекьют в базу
        except sqlite3.Error as error:  # Если в базе данных вызникла ошибка
            self.is_error = True  # флаг, определяющий ошибку
            self.error_message = "Вылетела ошибка в базе данных"  # строка для ответа в чат в случае если запрос ошибочен
            print(f'Вылетела ошибка в базе данных {error}')
            return None  # прекращаю работу метода

        result = [dict(row) for row in result]  # преобразование в список словарей

        if not result:
            self.is_error = True  # флаг, определяющий ошибку
            self.error_message = "База данных выдала пустой ответ"

        self.raw_dataset = pd.DataFrame(result)  # преобразую сырые данные в сырой датасэт pandas


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
        # группирую по имени игрока и аггрегирую средние результаты бросков кубика
        grouped_dataset = self.raw_dataset.groupby('user_name', as_index=False).agg({'dice_result': 'mean'})
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

        try:
            all_gamers = global_dice_roll_statistics_cursor.execute(gamers_str)  # запрос в бд
        except sqlite3.Error as error:  # Если в базе данных вызникла ошибка
            self.is_error = True
            self.error_message = "Вылетела ошибка в базе данных" # строка для ответа в чат в случае если запрос ошибочен
            # в чат выводится сообщение об ошибке, а в принт более детализированная информация
            print(f'Вылетела ошибка в базе данных {error}')
            return None  # прекращаю работу метода

        all_gamers = [elem[1] for elem in all_gamers]  # создаю список именами игроков

        if not all_gamers:  # если список пустой значит игроков в базе нет
            self.is_error = True
            self.error_message = f'Не зарегистрировано ни одного игрока'

        if self.user_name not in all_gamers:  # если запрашиваемого игрока нет в базе данных
            self.is_error = True
            self.error_message = f'Неверное имя игрока. Введите один из этих вариантов: {all_gamers}'

    def form_dataset(self):
        """
        Данный метод формирует pandas датасэт, он обязателен и наследуется от абстрактного метода базового класса
        """
        self.dataset = self.raw_dataset[['user_name', 'dice_result']]  # отбираю только данные по игроку и его броску куба

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
    """
    Данный класс занимается отрисовкой линейного графика по игрокам в разрезе временных отрезков характерных для
    проведения игровых сессий(datetime)
    """
    def __init__(self, datetime_type):
        super().__init__()
        self.datetime_type = datetime_type  # по умолчанию datetime, но можно разрез и изменить

    def form_dataset(self):
        """
        Данный метод формирует pandas датасэт, он обязателен и наследуется от абстрактного метода базового класса
        """
        # привожу таймстэмп изъятый из базы данных к типу даты и изымаю ее для группировки
        dataset = self.raw_dataset.groupby([pd.to_datetime(self.raw_dataset['roll_timestamp']).dt.date,
                                            self.raw_dataset['user_name']]) \
                                  .agg({'dice_result': 'mean'}).reset_index()  # подсчитываю среднее результат бросков

        # меняю названия столбцов
        dataset = dataset.rename(columns={
                                          'user_name': 'Игрок',
                                          'dice_result': 'Среднее значение кубика'})
        self.dataset = dataset

    def draw_plot(self):
        """
        Данный метод отрисовывает линейный график в разрезе игроков по датам. он обязателен и наследуется
        от абстрактного метода базового класса
        """
        sns.set_style("darkgrid")  # выставляю стиль с сеткой

        # строю график в разрезе игроков
        ax = sns.lineplot(data=self.dataset, x='roll_timestamp', y='Среднее значение кубика', hue='Игрок')

        # выставляю нужные параметры
        ax.set(title='Среднее значение кубика в разрезе сессии',
               xlabel='Дата',
               ylabel='Среднее значение кубика')
        plt.xticks(rotation=60)

        plt.gcf().set_size_inches(12, 9)  # выставляю размер для png картинки
        # сохраняю в виде картинки в каталоге с времеменными файлами откуда она будет загружена в чат
        plt.savefig('logs_and_temp_files/mean_results_by_datetime.png')
        plt.close()  # закрываю объект фигуры

    def control_plot_forming(self):
        """
        Метод осуществляет последовательный вызов необходимых методов
        """
        self.form_query_str()
        self.execute_db()
        self.form_dataset()
        self.draw_plot()


class CritRatioPlotFormer(BasePlotFormer):
    """
    Данный класс отрисовывает столбчатую диаграмму отражающую процент критических удач или неудач игроков за
    всё время
    """
    def __init__(self, crit_type):
        super().__init__()
        self.crit_type = crit_type  # параметр отвечающий за тип крита - критическая неудача или критическая удача

    def form_dataset(self):
        """
        Данный метод формирует pandas датасэт, он обязателен и наследуется от абстрактного метода базового класса
        """

        # проверяется какой командой вызван данный метод после чего происходит фильтрация данных по этому критерию
        if self.crit_type == 'luck':
            crit_dataset = self.raw_dataset[self.raw_dataset['roll_description'] == 'критический успех']
        else:
            crit_dataset = self.raw_dataset[self.raw_dataset['roll_description'] == 'критическая неудача']

        # группирую по имени игрока и подсчитаю количество выброшенных кубиков с критической удачей или неудачей
        crit_dataset = crit_dataset.groupby('user_name').agg({'roll_id': 'count'}).reset_index()

        # группирую второй датасэт по имени игрока и подсчитываю общее количество бросков
        all_rolls_dataset = self.raw_dataset.groupby('user_name').agg({'roll_id': 'count'}).reset_index()

        # сливаю датасэты по имени игрока чтобы было известно общее количество бросков и количество бросков с критами
        merged_dataset = crit_dataset.merge(all_rolls_dataset, on='user_name')

        # меняю названия столбцов
        merged_dataset = merged_dataset.rename(columns={'user_name': 'Игрок',
                                                        'roll_id_x': 'Количество критов',
                                                        'roll_id_y': 'Общее количество бросков'})

        # создаваю столбец с соотношением между общим количеством бросков и бросков с критической удачей или неудачей
        merged_dataset['Соотношение'] = merged_dataset['Количество критов'] / merged_dataset['Общее количество бросков'] * 100

        # оставляю нужные столбцы и сортирую по параметру соотношения
        merged_dataset = merged_dataset[['Игрок', 'Соотношение']].sort_values(by='Соотношение')

        self.dataset = merged_dataset

    def draw_plot(self):
        """
        Данный метод отрисовывает столбчатый график в разрезе игроков. Он обязателен и наследуется от абстрактного
        метода базового класса
        """
        sns.set_style("darkgrid")  # выставляю стиль с сеткой

        sns.barplot(self.dataset, x='Игрок', y='Соотношение', palette='deep')  # строю столбчатую диаграмму

        # даю параметры
        plt.title(f"Соотношение {'критических удач' if self.crit_type == 'luck' else 'критических неудач'} к общему количеству бросков")
        plt.ylabel('Соотношение (проценты)')

        plt.savefig('logs_and_temp_files/crit_ratio.png')  # сохраняю в файл
        plt.close()  # закрываю фигуру

    def control_plot_forming(self):
        """
        Метод осуществляет последовательный вызов необходимых методов
        """
        self.form_query_str()
        self.execute_db()
        self.form_dataset()
        self.draw_plot()



