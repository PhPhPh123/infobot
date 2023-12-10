"""
    Данный модуль отвечает за обработку команды !goodspie и выводит общий список товаров в субсекторе и их базовые цены
    в виде пироговой диаграмы matplotlib
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


def to_control_other_functions() -> None:
    """
    Основная управляющая функция, вызывающая остальные и формирующая пироговые диаграммы
    """

    # получаю строки для sql-запроса для экспорта и импорта
    export_goods_str_for_query, export_base_prices_str_for_query = form_sql_query('export')
    import_goods_str_for_query, import_base_prices_str_for_query = form_sql_query('import')

    # получение кортежей для импорта и экспорта из базы данных
    export_tuple_goods, export_tuple_prices = execute_db(export_goods_str_for_query,
                                                         export_base_prices_str_for_query)
    import_tuple_goods, import_tuple_prices = execute_db(import_goods_str_for_query,
                                                         import_base_prices_str_for_query)

    # готовые списки с товарами и мирами где ими торгуют для экспорта и импорта
    goods_list_export, counts_worlds_with_this_good_export = form_lists_for_labels(export_tuple_goods,
                                                                                   export_tuple_prices)

    goods_list_import, counts_worlds_with_this_good_import = form_lists_for_labels(import_tuple_goods,
                                                                                   import_tuple_prices)

    # отрисовка пироговых диаграмм на основе собранных данных
    form_pie_plot(goods_list_export, counts_worlds_with_this_good_export,
                  goods_list_import, counts_worlds_with_this_good_import)


def form_sql_query(export_or_import: str) -> tuple:
    """
    Данная функция формирует строки для запроса в базу данных
    :param export_or_import: для каждого из пирогов, экспорта или импорта запрашиваются свои данные в базе поэтому в данном
    параметре стоит флаг названия типа операции
    """

    goods_name_str = f'''
    SELECT trade_{export_or_import}.{export_or_import}_name, COUNT(worlds_trade_{export_or_import}_relations.{export_or_import}_name)
    FROM trade_{export_or_import}
    INNER JOIN worlds_trade_{export_or_import}_relations ON trade_{export_or_import}.{export_or_import}_name == worlds_trade_{export_or_import}_relations.{export_or_import}_name
    WHERE trade_{export_or_import}.base_price IS NOT NULL
    GROUP BY trade_{export_or_import}.{export_or_import}_name
    ORDER BY trade_{export_or_import}.{export_or_import}_name'''

    goods_price_str = f'''
    SELECT base_price FROM trade_{export_or_import}
    WHERE base_price IS NOT NULL
    ORDER BY {export_or_import}_name'''

    return goods_name_str, goods_price_str


def execute_db(goods_str, prices_str):
    """
    Данная функция использует ГЛОБАЛЬНУЮ МЕЖМОДУЛЬНУЮ переменную bd_sqlite3_cursor для доступа в базу данных и
    осуществляет в нее экзекьют получая необходимые кортежи
    """
    goods_tuple = tuple(global_main_db_cursor.execute(goods_str))
    prices_tuple = tuple(global_main_db_cursor.execute(prices_str))
    return goods_tuple, prices_tuple


def form_lists_for_labels(goods_tuple: tuple, prices_tuple: tuple) -> tuple:
    """
    Данная функция форматирует данные чтобы их можно было использовать для построения пироговых диаграмм
    :param goods_tuple: кортеж с кортежами в котором во внутреннем кортеже название товара и количество миров торгующих
    этим товаром
    :param prices_tuple: кортеж с кортежами, где находятся цены на товары
    """

    goods_prices = []  # список с ценами на товары, которые будут использоваться для данных
    goods_names = []  # список с названиями товаров
    goods_counts = []  # список с количеством миров, торгующих этим товаров. Они определяют размеры кусков пирога

    for tuple_elem in goods_tuple:  # заполняю списки элементами
        goods_names.append(tuple_elem[0])
        goods_counts.append(tuple_elem[1])

    for tuple_elem in prices_tuple:  # заполняю список элементами
        goods_prices.append(str(tuple_elem[0]))

    # соединяю названия товаров и их цены в одну двустрочную строку, эти значения будут использовать для меток
    # кусков пирога
    goods_with_prices = ['\n'.join(x) for x in zip(goods_names, goods_prices)]
    return goods_with_prices, goods_counts


def form_pie_plot(goods_list_export: list, counts_world_list_export: list,
                  goods_list_import: list, counts_world_list_import: list) -> None:
    """
    Данная функция отрисовывает фигуру с двумя пироговыми диаграммами
    """
    plt.style.use('fivethirtyeight')  # выставляю стиль
    fig = plt.figure(figsize=(22, 9))  # создаю фигуру

    ax1 = fig.add_subplot(1, 2, 1)  # создаю первый подграфик
    plt.title('Экспорт', fontdict={'fontsize': 36})  # даю ему название

    ax2 = fig.add_subplot(1, 2, 2)  # создаю второй подграфик
    plt.title('Импорт', fontdict={'fontsize': 36})  # даю ему название

    ax1.pie(counts_world_list_export, labels=goods_list_export)  # первый пирог
    ax2.pie(counts_world_list_import, labels=goods_list_import)  # второй пирог
    plt.savefig('logs_and_temp_files/answer_pie.png')
    plt.close()  # закрываю объект фигуры


