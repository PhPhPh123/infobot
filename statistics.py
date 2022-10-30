"""
    Данный модуль отвечает за запись, хранение и формирование строки выдачи статистики для сессии выдачи новостей
    через команду !startnews. Выдача статистики происходит после команды !stopnews
"""
import exceptions

if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from settings_imports_globalVariables import *


def count_news_statistics():
    """
    Функция замыкания хранящая статистику во внутренней функции append_stat
    Замыкание хранит ссылку на словарь stat_dict, где ключом стоит тэг новости, а значением - список итоговые строки
    с новостями
    @return: функция append_stat
    """
    stat_dict = {"НОВОСТЬ О ВРАГАХ": [],
                 "НОВОСТЬ О БЕЗОПАСНОМ МЕСТЕ": [],
                 "КВЕСТ": [],
                 "ИЗМЕНЕНИЕ ПРОИЗВОДСТВА": [],
                 "ПОВЫШЕНИЕ УРОВНЯ ДОСТУПА": [],
                 "НОВОСТЬ СУБСЕКТОРА": [],
                 "ЛОРНАЯ НОВОСТЬ": [],
                 'СРОЧНАЯ УНИКАЛЬНАЯ НОВОСТЬ': [],
                 'ВАЖНАЯ УНИКАЛЬНАЯ НОВОСТЬ': []
                 }

    def append_stat(type_news: str = None, value: str = None) -> Union[dict, form_news_statitics]:
        """
        Данная функция проверяет наличие тэга и значения и добавляет значение в словарь
        Значения по умолчанию None выставляются для того, чтобы в случае вызова без значений функция готовила отчет
        путем отправки словаря в функцию form_news_statitics и возврата итоговой строки отчета. Вызов функции без
        аргументов осуществляется в команде !stopnews основного модуля bot_main
        @param type_news: название тэга, должно совпадать с ключами stat_dict
        @param value: строка новости
        @return: либо словарь замыкания либо результат работы функции подготовки строкового ответа статистики
        """
        if type_news:
            if value:
                stat_dict[type_news].append(value)
                return stat_dict

        return form_news_statitics(stat_dict)

    return append_stat


def form_news_statitics(isdict: dict) -> str:
    """
    Данная функция готовит строку статистики с помощью шаблонизатора
    @param isdict: словарь со списком новостей в значениях, ключ это тэг новости
    @return: строка ответа для бота
    """
    stat_template = Template("""
    Статистика текущей сессии бота: 
    {% for item in isdict.items() -%}
        {{ item[0].capitalize() }}: {% if not item[1] %} 0 {% else %} {{ item[1]|length }} {% endif %}
    {% endfor %}""")
    stat_render = stat_template.render(isdict=isdict)
    return stat_render
