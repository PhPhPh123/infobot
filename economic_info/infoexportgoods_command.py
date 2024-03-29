"""
    Данный модуль обрабатывает команды !infoexportgoods и !infoimportgoods и отправляет в основной модуль bot_main
    строковую информацию для вывода боту. Модуль запрашивает у БД информацию и формирует из нее matplotlib изображение.
    Вывод выглядит в формате перечисления названий миров, покупающих или продающих данный товар
"""
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *
import economic_info.sql_queries


def choise_deal_and_execute_in_db(goods_name: str, name_deal: str) -> None:
    """
    Данная функция выбирает тип сделки, экспорт или импорт, осуществляет экзекьют в базу данных и запрашивает строку у
    нижестоящей функции. Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНУЮ ГЛОБАЛЬНУЮ переменную
    :param goods_name: название товара
    :param name_deal: название сделки, export или import
    :return: строка ответа боту
    """
    select_systems = None

    # Выбираю тип сделки на основе имени сделки(name_deal) и отправляю в функции формирования запроса название товара
    # запроса название товара goods_name
    if name_deal == 'import':
        select_systems = form_import_query(goods_name)
    elif name_deal == 'export':
        select_systems = form_export_query(goods_name)

    tuple_with_worlds = tuple(global_main_db_cursor.execute(select_systems))

    form_answer(tuple_with_worlds, name_deal)


def form_export_query(goods_name: str) -> str:
    """
    Данная функция формирует текст запроса в БД для сделки экспорта
    :param goods_name: название товара
    :return: строка для экзекьюта в БД
    """
    # Текст sql-запроса берется из модуля sql_queries
    select_temp_systems = Template(economic_info.sql_queries.info_goods_query_dict['export'])
    select_render_systems = select_temp_systems.render(goods_name=goods_name)
    return select_render_systems


def form_import_query(goods_name: str) -> str:
    """
    Данная функция формирует текст запроса в БД для сделки импорта
    :param goods_name: название товара
    :return: строка для экзекьюта в БД
    """
    # Текст sql-запроса берется из модуля sql_queries
    select_temp_systems = Template(economic_info.sql_queries.info_goods_query_dict['import'])
    select_render_systems = select_temp_systems.render(goods_name=goods_name)
    return select_render_systems


def form_answer(tuple_with_worlds: tuple, deal_name: str):
    """
    Данная функция формирует итоговую строку с помощью шаблонизатора для ответа ботом
    :param tuple_with_worlds: кортеж из кортежей. Во внутренних кортежах только 1 значение - название мира
    :param deal_name: название сделки, export или import
    :return: итоговая строка ответа бота
    """
    index = [x[0] for x in tuple_with_worlds]
    values = [int(x[1]) for x in tuple_with_worlds]

    plt.figure(figsize=(15, 5))
    bars = plt.barh(index, values)
    plotname = 'Экспорт' if deal_name == 'export' else 'Импорт'
    plt.title(plotname, fontdict={'fontsize': 36})

    for bar in bars:
        width = bar.get_width()
        label_y = bar.get_y() + bar.get_height() / 2
        plt.text(width, label_y, s=f'{width}')
    plt.savefig('logs_and_temp_files/info_export_import_goods.png')
    plt.close()  # закрываю объект фигуры

    return None

