"""

"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


class ConsumablesPlotsFormer:
    def __init__(self, group_or_type):
        self.query_str = None  # строка запрос в базу данных
        self.raw_dataset = None  # список словарей в котором ключ это название столбца, а значения это его значения
        self.dataset = None  # датасэт pandas
        self.group_or_type = group_or_type  # группа или тип предметов, в разрезе которых будет группироваться датасэт
        self.is_error = False  # флаг ошибки
        self.error_message = None  # строка ошибки

    def verify_data(self):
        """
        Данный метод проверяет данные и вешает флаг ошибки и дает строку ошибки которая будет выведена в чат
        """
        if self.group_or_type not in ('type', 'group'):
            self.is_error = True
            self.error_message = 'Нужно указать что будет отображаться, тип или группа(type или group)'

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
        grouped_dataset = self.raw_dataset.groupby(self.group_or_type + '_name').agg({'event_id': 'count'}).reset_index()
        grouped_dataset = grouped_dataset.rename(columns={self.group_or_type + '_name': 'Группы' if self.group_or_type == 'group' else 'Типы',
                                                          'event_id': 'Количество предметов'})
        grouped_dataset = grouped_dataset.sort_values(by='Количество предметов')

        self.dataset = grouped_dataset

    def draw_plot(self):
        sns.set_style("darkgrid")  # выставляю стиль с сеткой

        sns.barplot(data=self.dataset,
                    x='Количество предметов',
                    y='Группы' if self.group_or_type == 'group' else 'Типы',
                    palette='deep')
        plt.gcf().set_size_inches(17, 14)  # выставляю размер для png картинки
        plt.title('Статистика выпадения предметов по группам' if self.group_or_type == 'group' else 'Статистика выпадения предметов по типам')

        plt.savefig('logs_and_temp_files/consumables_plot.png')  # сохраняю в файл
        plt.close()  # закрываю фигуру

    def control_plot_forming(self):
        self.verify_data()
        if self.is_error:
            return None
        self.execute_db()
        self.form_dataset()
        self.draw_plot()



