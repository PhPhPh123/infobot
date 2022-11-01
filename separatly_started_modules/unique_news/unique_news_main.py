"""
    Данный отдельно стоящий модуль отвечает за создание интейфейса для записи новостей и записи данных в базу данных
    формирующуюся sqlalchemy. Данные новостей, затем, будут использоваться в основном новостном цикле. База данных
    не добавляется в индекс и формируется при первом запуске, отсутствие базы обрабатывается через блоки try\except
    в новостном модуле, отсутствие новостей тоже допустимо
"""

import tkinter
from tkinter.ttk import Combobox
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DataBase = declarative_base()  # Объявление декларативной базы данных


class UrgentlyUniqueNews(DataBase):
    """
    Столбцы для таблицы срочных новостей
    """
    __tablename__ = 'urgently_unique_news'
    db_id = Column(Integer, primary_key=True, autoincrement=True)
    news_id = Column(Integer, nullable=False)
    news_text = Column(Text, nullable=False)


class CommonUniqueNews(DataBase):
    """
    Столбцы для таблицы обычных новостей
    """
    __tablename__ = 'common_unique_news'
    db_id = Column(Integer, primary_key=True, autoincrement=True)
    news_id = Column(Integer, nullable=False)
    news_text = Column(Text, nullable=False)


def control_interface() -> None:
    """
    Данная функция будет осуществлять основной контроль за другими функциями. Она реализует шаблон проектирования Фасад
    @return: None
    """

    win = tkinter.Tk()  # Создание объекта окна
    table_obj = NewsInterface(win)  # Создание объект интерфейса
    table_obj.call_text_field_interface()  # Вызов основного метода формирования интерфейса
    win.mainloop()  # Основной цикл интерфейса
    table_obj.write_to_db()  # Запись данных в БД


class NewsInterface(tkinter.Frame):
    """
    Данный класс отвечает за создание интерфейса ktinker и обладает методами вызова текстового поля, для записи туда
    новости, методами вызова выбора типа новости, срочной или обычной и методом записи новости в соответствующий csv
    файл
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.win = parent
        self.geometry = self.win.geometry('700x250')
        self.news_next = None
        self.type_of_news = None
        self.text_field = None
        self.start_button = None
        self.text = None

        self.type_name = None
        self.type_combo = None
        self.type_result = None

    def call_text_field_interface(self):
        """
        Данный метод вызывает интерфейс текстового ввода tkinter, в который будет вписываться текст новости сохраняя
        результат в self.news_next
        @return:
        """
        # Элемент основного текстового поля
        self.text_field = tkinter.Text(width=80, height=10)
        self.text_field.pack()

        # Кнопка START для начала записи данных из текстового поля
        self.start_button = tkinter.Button(self.win, text='Сохранить', command=self.get_text)
        self.start_button.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.7)

        # Элемент с названием комбобокса
        self.type_name = tkinter.Label(self.win, text='Срочность новости')
        self.type_name.place(relx=0.7, rely=0.65)

        # Элемент-Комбобокс с двумя типами новостей
        self.type_combo = Combobox(self.win, values=('срочная новость', 'несрочная новость'))
        self.type_combo.bind('<<ComboboxSelected>>',
                             lambda event: self.choise_type_news(event))
        self.type_combo.place(relwidth=0.2, relheight=0.1, relx=0.7, rely=0.75)

    def choise_type_news(self, event) -> None:
        """
        Данная функция выбирает текущий элемент комбобокса
        @param event: аттрибут комбобокса
        @return: None
        """
        self.type_result = self.type_combo.get()

    def get_text(self) -> None:
        """
        Данная функция собирает весь такст, написанный на текстовом поле и вызывает метод закрытия интерфейса
        @return: None
        """
        self.text = self.text_field.get("1.0", "end")
        self.interface_close()

    def write_to_db(self) -> None:
        """
        Данная функция записывает новости во временные в базу данных, в один из двух столбцов после чего коммитит данные
        @return: None
        """
        news = None

        # На основании типа выбранной новости осуществляется запись в соответствующую таблицу, id новости это
        # выполнение функции id на экземпляр класса
        if self.type_result == 'срочная новость':
            news = UrgentlyUniqueNews(news_id=id(self), news_text=self.text)
        elif self.type_result == 'несрочная новость':
            news = CommonUniqueNews(news_id=id(self), news_text=self.text)

        # Добавление и запись результато в БД
        session.add(news)
        session.commit()

    def interface_close(self) -> None:
        """
        Данная функция закрытвает интерфейс
        @return: None
        """
        self.quit()


if __name__ == "__main__":
    engine = create_engine('sqlite:///unique_news.db')  # Создание движка БД
    DataBase.metadata.create_all(engine)  # Создание метаданных
    DataBase.metadata.bind = engine  # Запись метаданных
    DBSession = sessionmaker(bind=engine)  # Объявление сессии БД
    session = DBSession()  # Создание сессии БД

    control_interface()  # Вызов основной фасадной функции
else:
    raise Exception('Неимпортируемый модуль')

