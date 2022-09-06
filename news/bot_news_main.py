"""
    Данный модуль управляет остальными news-модулями, выбирая какой тип новости будет выдан и отдавая управление
    на модули и функции, формирующие сообщения
"""

from settings_imports_globalVariables import *
from news import bot_news_access, bot_news_static_info, bot_news_enemies


def choise_random_news(curs: sqlite3.Cursor, db: sqlite3.Connection) -> str:
    """
    Данная функция выбирает случайную новость путем случайного выбора функции, которая ее обработает и вернет
    Ролл от 1 до 100 ведется, чтобы определить удачливость событий новостей. Ролл 1-5 считается удачливым,
    поэтому и новости будут полезными и влияющими на геймплей игроков непосредственно
    :return: строка с новостью-ответом ботом
    """
    random_roll = random.randint(1, 100)
    if random_roll > 5:  # Обычный исход ролла
        news = random.choice([bot_news_enemies.form_tuple_from_db(curs),
                              bot_news_static_info.form_subsector_news(curs),
                              bot_news_static_info.form_lore_info(curs)])
    else:  # Удачливый исход ролла
        news = bot_news_access.control_other_func(curs, db)

    return news
