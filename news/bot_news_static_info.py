"""
    Данный модуль выбирает статичные новости относящиеся к субсектору либо лору, и каким то игровым особенностям
    Данные новости вносятся вручную ГМом в таблицы subsector_news и lore_info и могут добавляться/удаляться по
    ходу игры при необходимости. Функции этого модуля в связи с малой работой, выполняет экзекьют в БД формируя кортеж
    и сразу изымая из него строковое значение новости news_text после чего отдавая строку в управляющую
    функцию в модуле bot_news_main
"""
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from imports_globalVariables import *


def form_subsector_news() -> str:
    """
    Данная функция обрабатывает новости касательно крупных субсекторных событий или сюжетных поворотов
    Объект курсора bd_sqlite3_cursor и объект коннекта bd_sqlite3_connect это МЕЖМОДУЛЬНЫЕ ГЛОБАЛЬНЫЕ переменные
    :return: итоговая строка ответа ботом
    """
    select_gm_news_string = '''
    SELECT news_text FROM subsector_news
    ORDER BY RANDOM()
    LIMIT 1
    '''
    # Из кортежа с кортежами изымается строка с новостью
    subsector_string = tuple(global_bd_sqlite3_cursor.execute(select_gm_news_string))[0][0]
    return '[НОВОСТЬ СУБСЕКТОРА] ' + subsector_string


def form_lore_info() -> str:
    """
    Данная функция обрабатывает подсказки или лорные особенности мира warhammer40k, про которые игрокам не стоит
    забывать или стоит обратить внимание
    :return: итоговая строка ответа ботом
    """
    select_gm_news_string = '''
    SELECT lore_text FROM lore_info
    ORDER BY RANDOM()
    LIMIT 1
    '''
    # Из кортежа с кортежами изымается строка с новостью
    lore_string = tuple(global_bd_sqlite3_cursor.execute(select_gm_news_string))[0][0]
    return '[ЛОРНАЯ НОВОСТЬ] ' + lore_string
