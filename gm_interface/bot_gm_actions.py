def bot_gm_interface_controller(*args):
    """
    Создает экземпляр класса графического интерфейса и по итогу его работы отправляет UPDATE запрос в БД
    :param args:
    :return:
    """
    pass


def update_form(*args):
    """
    Формирует текст UPDATE запроса с помощью шаблонизатора jinja на основе данных переданных из графического интерфейса
    :param args:
    :return:
    """
    pass


def db_update(*args):
    """
    Отправляет запрос на UPDATE в БД
    :param args:
    :return:
    """
    pass


class AdminInterface:
    """
    Графический интерфейс tkinter вызываемый командой $admin_update. Должен вносить изменения в параметры опасности
    зоны и уровня угрозы отдельных врагов в системах в целом и на отдельных планетах
    """
    pass