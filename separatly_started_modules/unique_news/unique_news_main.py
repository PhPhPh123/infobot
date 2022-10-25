import tkinter
from tkinter.ttk import Combobox
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DataBase = declarative_base()


class UrgentlyUniqueNews(DataBase):
    __tablename__ = 'urgently_unique_news'
    db_id = Column(Integer, primary_key=True, autoincrement=True)
    news_id = Column(Integer, nullable=False)
    news_text = Column(Text, nullable=False)


class CommonUniqueNews(DataBase):
    __tablename__ = 'common_unique_news'
    db_id = Column(Integer, primary_key=True, autoincrement=True)
    news_id = Column(Integer, nullable=False)
    news_text = Column(Text, nullable=False)


def control_interface():
    """
    Данная функция будет осуществлять основной контроль за другими функциями
    @return: None
    """

    win = tkinter.Tk()
    table_obj = NewsInterface(win)
    table_obj.call_text_field_interface()
    win.mainloop()
    table_obj.write_to_csv()


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
        self.text_field = tkinter.Text(width=80, height=10)
        self.text_field.pack()

        self.start_button = tkinter.Button(self.win, text='Сохранить', command=self.get_text)
        self.start_button.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.7)

        self.type_name = tkinter.Label(self.win, text='Срочность новости')
        self.type_name.place(relx=0.7, rely=0.65)

        self.type_combo = Combobox(self.win, values=('срочная новость', 'несрочная новость'))
        self.type_combo.bind('<<ComboboxSelected>>',
                             lambda event: self.choise_type_news(event))
        self.type_combo.place(relwidth=0.2, relheight=0.1, relx=0.7, rely=0.75)

    def choise_type_news(self, event):
        self.type_result = self.type_combo.get()

    def get_text(self):
        self.text = self.text_field.get("1.0", "end")
        self.interface_close()

    def write_to_csv(self):
        """
        Данная функция записывает новости во временные cvs-файлы в директорию временных файлов
        @return:
        """
        news = None

        if self.type_result == 'срочная новость':
            news = UrgentlyUniqueNews(news_id=id(self), news_text=self.text)
        elif self.type_result == 'несрочная новость':
            news = CommonUniqueNews(news_id=id(self), news_text=self.text)
        session.add(news)
        session.commit()

    def interface_close(self):
        self.quit()


if __name__ == "__main__":
    engine = create_engine('sqlite:///unique_news.db')
    DataBase.metadata.create_all(engine)
    DataBase.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    control_interface()
