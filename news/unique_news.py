def control_interface():
    """
    Данная функция будет осуществлять основной контроль за другими функциями
    @return: None
    """

    """Создание экземпляра класса интерфейса
       Вызов метода call_text_field_interface
       Вызов метода call_type_of_news_interface
       Вызов метода write_to_csv
       """


class NewsInterface:
    """
    Данный класс отвечает за создание интерфейса ktinker и обладает методами вызова текстового поля, для записи туда
    новости, методами вызова выбора типа новости, срочной или обычной и методом записи новости в соответствующий csv
    файл
    """

    def __init__(self):
        self.news_next = None
        self.type_of_news = None

    def call_text_field_interface(self):
        pass

    def call_type_of_news_interface(self):
        pass

    def write_to_csv(self):
        pass


def control_form_news():
    """
    Данная функция создает экземпляр класса FormUniqueNews, контролирует вызовы методов изъятия новостей
    из csv файла, методы формирования новостей и методы удаления данных из cvs файла. Данная функция не связана
    напрямую с функцией control_interface и классом NewsInterface, она лишь работает с результатами их работы
    записанными в csv-файлы при вызове чат-команды !startnews
    @return:
    """


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