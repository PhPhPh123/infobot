from settings_and_imports import *


def to_control_other_functions(cursor) -> None:
    export_goods_str_for_query, export_base_prices_str_for_query = form_sql_query('export')
    import_goods_str_for_query, import_base_prices_str_for_query = form_sql_query('import')

    export_tuple_goods, export_tuple_prices = sql_query(export_goods_str_for_query,
                                                        export_base_prices_str_for_query, cursor)
    import_tuple_goods, import_tuple_prices = sql_query(import_goods_str_for_query,
                                                        import_base_prices_str_for_query, cursor)

    goods_list_export, counts_worlds_with_this_good_export = form_lists_for_labels(export_tuple_goods,
                                                                                   export_tuple_prices)

    goods_list_import, counts_worlds_with_this_good_import = form_lists_for_labels(import_tuple_goods,
                                                                                   import_tuple_prices)

    form_pie_plot(goods_list_export, counts_worlds_with_this_good_export,
                  goods_list_import, counts_worlds_with_this_good_import)


def form_sql_query(deal_name: str) -> tuple:
    goods_name_str = f'''
    SELECT trade_{deal_name}.{deal_name}_name, COUNT(worlds_trade_{deal_name}_relations.{deal_name}_name)
    FROM trade_{deal_name}
    INNER JOIN worlds_trade_{deal_name}_relations ON trade_{deal_name}.{deal_name}_name == worlds_trade_{deal_name}_relations.{deal_name}_name
    WHERE trade_{deal_name}.base_price IS NOT NULL
    GROUP BY trade_{deal_name}.{deal_name}_name
    ORDER BY trade_{deal_name}.{deal_name}_name'''

    goods_price_str = f'''
    SELECT base_price FROM trade_{deal_name}
    WHERE base_price IS NOT NULL
    ORDER BY {deal_name}_name'''

    return goods_name_str, goods_price_str


def sql_query(goods_str, prices_str, cursor):
    goods_tuple = tuple(cursor.execute(goods_str))
    prices_tuple = tuple(cursor.execute(prices_str))
    return goods_tuple, prices_tuple


def form_lists_for_labels(goods_tuple: tuple, prices_tuple: tuple) -> tuple:
    goods_prices = []
    goods_names = []
    goods_counts = []

    for tuple_elem in goods_tuple:
        goods_names.append(tuple_elem[0])
        goods_counts.append(tuple_elem[1])

    for tuple_elem in prices_tuple:
        goods_prices.append(str(tuple_elem[0]))

    goods_with_prices = ['\n'.join(x) for x in zip(goods_names, goods_prices)]

    return goods_with_prices, goods_counts


def form_pie_plot(goods_list_export, counts_world_list_export,
                  goods_list_import, counts_world_list_import):
    fig = plt.figure(figsize=(20, 7))

    ax1 = fig.add_subplot(1, 2, 1)
    plt.title('Экспорт', fontdict={'fontsize': 36})

    ax2 = fig.add_subplot(1, 2, 2)
    plt.title('Импорт', fontdict={'fontsize': 36})

    ax1.pie(counts_world_list_export, labels=goods_list_export)
    ax2.pie(counts_world_list_import, labels=goods_list_import)
    plt.savefig('answer_pie.png')
