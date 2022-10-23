
from settings_imports_globalVariables import *


def control_form_news():
    """
    Данная функция создает экземпляр класса FormUniqueNews, контролирует вызовы методов изъятия новостей
    из csv файла, методы формирования новостей и методы удаления данных из cvs файла. Данная функция не связана
    напрямую с функцией control_interface и классом NewsInterface, она лишь работает с результатами их работы
    записанными в csv-файлы при вызове чат-команды !startnews
    @return:
    """
    unique_news = FormUniqueNews()
    return


class FormUniqueNews:
    def __init__(self):
        self.news_text = None

    def get_news_from_csv(self):
        """
        Данный метод достает запись о новости для использования ее в дальнейшем другими методами
        @return:
        """
        pass

    def form_common_unique_news(self):
        """
        Данная функция будет формировать итоговую строку ответа для обычных новостей
        @return: готовая строка ответа
        """

    def form_urgently_unique_news(self):
        """
        Данная функция изымает из csv файла текст срочной первой в списке новости и преобразует ее в строку ее вызов будет
        идти во время работы модуля bot_news_main. После формирования срочки вызывается метод, удаляющий новость из csv файла
        @return: готовая строка ответа
        """
    def del_from_csv(self):
        """
        Данный метод удаляет новости из csv файла чтобы новости не повторялись
        @return:
        """