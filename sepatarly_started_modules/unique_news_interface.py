import tkinter
from tkinter.ttk import Combobox


def control_interface():
    """
    Данная функция будет осуществлять основной контроль за другими функциями
    @return: None
    """

    win = tkinter.Tk()
    table_obj = NewsInterface(win)
    table_obj.call_text_field_interface()
    win.mainloop()

    """Создание экземпляра класса интерфейса
       Вызов метода call_text_field_interface
       Вызов метода call_type_of_news_interface
       Вызов метода write_to_csv
       """


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
        self.type_name.place(relx=0.2, rely=0.6)
        self.type_combo = Combobox(self.win, values=('срочная новость', 'несрочная новость'))
        self.type_combo.current(0)
        self.type_combo.bind('<<ComboboxSelected>>',
                             lambda event: add_button_result_to_dict(event,
                                                                     'тип события',
                                                                     'type_combo'))
        self.type_combo.place(relwidth=0.2, relheight=0.1, relx=0.799, rely=0.7)

    def call_type_of_news_interface(self):
        """
        Данный метод вызывает интерфейс выбора кнопок, результат которых будет записываться в виде
        cтроки в self.type_of_news
        @return:
        """
        pass

    def write_to_csv(self):
        """
        Данная функция записывает новости во временные cvs-файлы в директорию временных файлов
        @return:
        """

    def get_text(self):
        self.text = self.text_field.get("1.0", "end")
        print(self.text)


if __name__ == "__main__":
    control_interface()
