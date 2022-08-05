"""
    Данный модуль выбирает статичные новости относящиеся к субсектору либо лору, и каким то игровым особенностям
    Данные новости вносятся вручную ГМом в таблицы subsector_news и lore_info и могут добавляться/удаляться по
    ходу игры при необходимости. Функции этого модуля в связи с малой работой, выполняет экзекьют в БД формируя кортеж
    и сразу изымая из него строковое значение новости news_text после чего отдавая строку в управляющую
    функцию в модуле bot_news_main
"""
from settings_and_imports import *


def form_subsector_news(curs: sqlite3.Cursor) -> str:
    """
    Данная функция обрабатывает новости касательно крупных субсекторных событий или сюжетных поворотов
    :param curs: объект курсора
    :return: итоговая строка ответа ботом
    """
    select_gm_news_string = '''
    SELECT news_text FROM subsector_news
    ORDER BY RANDOM()
    LIMIT 1
    '''
    # Из кортежа с кортежами изымается строка с новостью
    subsector_string = tuple(curs.execute(select_gm_news_string))[0][0]
    return subsector_string


def form_lore_info(curs: sqlite3.Cursor) -> str:
    """
    Данная функция обрабатывает подсказки или лорные особенности мира warhammer40k, про которые игрокам не стоит
    забывать или стоит обратить внимание
    :param curs: объект курсора
    :return: итоговая строка ответа ботом
    """
    select_gm_news_string = '''
    SELECT lore_text FROM lore_info
    ORDER BY RANDOM()
    LIMIT 1
    '''
    # Из кортежа с кортежами изымается строка с новостью
    lore_string = tuple(curs.execute(select_gm_news_string))[0][0]
    return lore_string
