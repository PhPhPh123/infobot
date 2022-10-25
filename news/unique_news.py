
from settings_imports_globalVariables import *
import exceptions


def control_form_news(type_of_news: str) -> str:
    """
    Данная функция создает экземпляр класса FormUniqueNews, контролирует вызовы методов изъятия новостей
    из базы данных, формирования строк ответа и удаления записей с новостями из базы БД
    @return: строковый ответ для бота
    """
    unique_news = FormUniqueNews(type_of_news)

    unique_news.get_news_from_db()

    if type_of_news == 'срочная новость':
        unique_news.form_urgently_unique_news()
    elif type_of_news == 'несрочная новость':
        unique_news.form_common_unique_news()

    unique_news.del_from_db()

    return unique_news.final_str


class FormUniqueNews:
    def __init__(self, type_of_news):
        self.type_of_news = type_of_news
        self.news_text = None
        self.final_str = None
        self.news_id = None

    def get_news_from_db(self):
        """
        Данный метод достает запись о новости для использования ее в дальнейшем другими методами
        @return:
        """
        news = ''
        table = 'common_unique_news' if self.type_of_news == 'несрочная новость' else 'urgently_unique_news'

        if table == 'common_unique_news':
            news = tuple(global_unique_news_cursor.execute(f'SELECT news_text, news_id FROM {table} ORDER BY RANDOM() LIMIT 1'))
        elif table == 'urgently_unique_news':
            news = tuple(global_unique_news_cursor.execute(f'SELECT news_text, news_id FROM {table} LIMIT 1'))

        self.news_id = news[0][1]
        self.news_text = news[0][0]

    def form_common_unique_news(self):
        """
        Данная функция будет формировать итоговую строку ответа для обычных новостей
        @return: готовая строка ответа
        """
        self.final_str = f'[ВАЖНАЯ УНИКАЛЬНАЯ НОВОСТЬ] {self.news_text}'

    def form_urgently_unique_news(self):
        """
        Данная функция изымает из csv файла текст срочной первой в списке новости и преобразует ее в строку ее вызов будет
        идти во время работы модуля bot_news_main. После формирования срочки вызывается метод, удаляющий новость из csv файла
        @return: готовая строка ответа
        """
        self.final_str = f'[СРОЧНАЯ УНИКАЛЬНАЯ НОВОСТЬ] {self.news_text}'

    def del_from_db(self):
        """
        Данный метод удаляет новости из csv файла чтобы новости не повторялись
        @return:
        """
        table = 'common_unique_news' if self.type_of_news == 'несрочная новость' else 'urgently_unique_news'

        global_unique_news_cursor.execute(f'DELETE FROM {table} WHERE news_id == {self.news_id}')
        global_unique_news_connect.commit()


if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
