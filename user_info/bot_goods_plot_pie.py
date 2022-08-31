import matplotlib.pyplot as plt

from settings_and_imports import *


def choise_export_or_import(cursor):
    all_goods_tuple = tuple(cursor.execute('''
SELECT trade_export.export_name, COUNT(worlds_trade_export_relations.export_name)
FROM trade_export
INNER JOIN worlds_trade_export_relations ON trade_export.export_name == worlds_trade_export_relations.export_name
WHERE trade_export.export_name not in ('Экспорт-отсутствует', 'Ваааааах!')
GROUP BY trade_export.export_name'''))
    goods_names = []
    goods_counts = []

    for tuple_elem in all_goods_tuple:
        goods_names.append(tuple_elem[0])
        goods_counts.append(tuple_elem[1])

    fig1, ax1 = plt.subplots()
    ax1.pie(goods_counts, labels=goods_names)
    plt.savefig('anwer_pie.png')
