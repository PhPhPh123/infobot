"""
    Данный модуль обрабатывает команды !infoexport *название мира* и !infoimport *название мира*
    и отправляет в основной модуль bot_main строковую информацию для вывода боту. Работа модуля основываетсмя
    на приеме строки с выбранным миром, доступа в базу данных, формированию строки запросов по нескольким пунктам
    через шаблонизатор, получения из БД кортежей и формированию на их основе готового строкового ответа. Текст
    SQL-запроса берется из модуля sql_queries
"""
from settings_imports_globalVariables import *
from user_info import sql_queries
import exceptions

def choice_deal_and_returns_bot_answer(world_name: str, deal_name: str) -> str:
    """
    Функция осуществляет контроль основых операций для получения итоговой строки которую отдает в модуль bot_main
    для исполнения функцией и выдачей ответа ботом. Объект курсора bd_sqlite3_cursor это МЕЖМОДУЛЬНАЯ ГЛОБАЛЬНАЯ
    переменная:
    1 этап: получает строку для sql-запроса в БД через функцию form_query
    2 этап: с помощью экзекьюта в БД через курсор получает результат их работы в виде кортежа
    3 этап: получает итоговую строку с помощью функции form_string
    :param world_name: название мира
    :param deal_name: название текущей сделки, import или export
    :return: итоговый ответ для бота
    """
    select_systems = None

    # 1 этап
    if deal_name == 'import':
        select_systems = form_query(world_name, deal_name, 1.25)
    elif deal_name == 'export':
        select_systems = form_query(world_name, deal_name)

    # 2 этап
    world_tuple = tuple(global_bd_sqlite3_cursor.execute(select_systems))

    # 3 этап
    trade_answer = form_string(world_tuple, deal_name)
    if world_tuple[0][2] != 3:
        trade_answer = 'Недостаточный уровень доступа'

    return trade_answer


def form_query(world_name: str, deal_name: str, margin: float = 1.0) -> str:
    """
    Данная функция формирует текстовый запрос для запроса в базу данных
    :param world_name: название мира
    :param deal_name: название текущей сделки, import или export
    :param margin: параметр, увеличивающий стоимость покупки товаров чтобы симулировать спрос на него в факторе цены
    :return: строка sql-запроса
    """
    for_format = '{{ world_name }}'  # вставка для метода format
    template_for_select = ''  # Инициализация пустой строкой

    # В запросах используется метод format, чтобы создать темплейт на основе строк, хранимых в словарях
    # в модуле sql_queries. Методом добавляется значение наценки(margin) и строчка for_format нужная для шаблонизатора.
    # Операторами if/elif выбираются разные тексты запросов, поэтому между ними идет выбор на основе
    # переменной deal_name, указывающей тип команды.
    if deal_name == "import":
        template_for_select = Template(sql_queries.import_and_export_query_dict['import'].format(for_format))
    elif deal_name == 'export':
        template_for_select = Template(sql_queries.import_and_export_query_dict['export'].format(for_format))

    query_string = template_for_select.render(world_name=world_name, margin=margin)
    return query_string


def form_string(world_tuple: tuple, deal_name: str):
    """
    Данная фукнция формирует строку на основе кортежа с помощью шаблонизатора
    :param world_tuple: кортеж, где первый элемент это название товара, второй это его стоимость после рассчетов, а
    третий это уровень доступа на мире
    :param deal_name: название текущей сделки, import или export
    :return: итоговая строка для отправки боту
    """
    message = 'Примерная цена покупки импортных товаров' if deal_name == 'import' else 'Примерная цена продажи товаров'

    # сначала выводится сообщение message, а затем в цикле выводятся 0 и 1 элементы кортежа(название товара и стоимость)
    answer_systems_temp = Template('''
    {{ message }}:
    {% for world in sys_tuple %}
        {{ '{} : {}'.format(world[0], world[1]) }}
    {% endfor %}
    ''')

    answer_render_systems = answer_systems_temp.render(sys_tuple=world_tuple, message=message)
    return answer_render_systems


if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
