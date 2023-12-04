"""
    Данный модуль отвечает за вывод в чат статистических графиков касательно исторических данных о выпавших игрокам
    расходуемых предметов согласно специальной игровой механики. Данные о полученных предметах записывается в модуле
    special_loot/special_loot_statistics_collect, а сами данные хранятся в базе consumables_loot_db в директории
    того же пакета
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


class ConsumablesPlotsFormer:
    """
    Данный класс занимается выводом статистических графиков по количеству выпавших предметов в разрезе групп или типов
    данных предметов
    :param group_or_type: параметр отвечает за разрез, в котором будет происходить подсчёт предметов, типу или группе.
    Может содержать только 2 варианта, строку 'type' или 'group'
    """
    def __init__(self, group_or_type: str, top_value: (str, None)):
        self.query_str = None  # строка запрос в базу данных
        self.raw_dataset = None  # список словарей в котором ключ это название столбца, а значения это его значения
        self.dataset = None  # датасэт pandas
        self.group_or_type = group_or_type  # группа или тип предметов, в разрезе которых будет группироваться датасэт
        self.top_value = top_value  # параметр содержащий число, ограничивающее количество выведенных предметов
        self.is_error = False  # флаг ошибки
        self.error_message = None  # строка ошибки

    def verify_data(self):
        """
        Данный метод проверяет данные и вешает флаг ошибки и дает строку ошибки которая будет выведена в чат
        """
        if self.group_or_type not in ('type', 'group'):  # аргументом для команды должны быть только 2 варианта
            self.is_error = True
            self.error_message = 'Нужно указать что будет отображаться, тип или группа(type или group)'

        try:
            if self.top_value:  # Если параметр равен None, то проверка не нужна
                # посколько из чата приходят аргументы в виде строки то число нужно привести к int
                self.top_value = int(self.top_value)
                assert self.top_value >= 0
                assert type(self.top_value) != float

        except (ValueError, TypeError, AssertionError):  # если приведение к типу int вызвало ошибку значит аргумент некорректный
            self.is_error = True
            self.error_message = 'Топ вывода должны быть целым числом больше нуля'

    def execute_db(self):
        """
        Данный метод осуществляет запрос в базу данных и преобразует сырые данные так, чтобы они представляли собой
        словарь
        """
        self.query_str = """SELECT * FROM main_log"""

        result = global_consumables_statistics_sqlite3_cursor.execute(self.query_str)  # собственно экзекьют в базу
        result = [dict(row) for row in result]  # преобразование в список словарей
        self.raw_dataset = pd.DataFrame(result)  # преобразую сырые данные в сырой датасэт pandas

    def form_dataset(self):
        """
        Данный метод формирует pandas датасэт на основе которого будет отрисован график
        """
        # поля для группировки формируется из аргумента команды и _name, по итогу будет group_name или type_name
        # и подсчитывая количество событий в разрезе группировки
        grouped_dataset = self.raw_dataset.groupby(self.group_or_type + '_name').agg({'event_id': 'count'}).reset_index()

        # меняю названия столбцов на основе полученного аргумента команды
        grouped_dataset = grouped_dataset.rename(columns={self.group_or_type + '_name': 'Группы' if self.group_or_type == 'group' else 'Типы',
                                                          'event_id': 'Количество предметов'})
        # сортирую по количеству предметов
        grouped_dataset = grouped_dataset.sort_values(by='Количество предметов')
        if self.top_value:
            grouped_dataset = grouped_dataset.tail(self.top_value)

        self.dataset = grouped_dataset

    def draw_plot(self):
        """
        Данный метод отрисовывает столбчатый график который впоследствии будет выведен в чат
        """
        sns.set_style("darkgrid")  # выставляю стиль с сеткой

        sns.barplot(data=self.dataset, # строю график
                    x='Количество предметов',
                    y='Группы' if self.group_or_type == 'group' else 'Типы',
                    palette='deep')
        plt.gcf().set_size_inches(17, 14)  # выставляю размер для png картинки
        plt.title('Статистика выпадения предметов по группам' if self.group_or_type == 'group' else 'Статистика выпадения предметов по типам')

        plt.savefig('logs_and_temp_files/consumables_plot.png')  # сохраняю в файл
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



