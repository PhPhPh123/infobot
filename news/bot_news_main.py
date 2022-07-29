from settings_and_imports import *
from . import bot_news_access, bot_news_gm, bot_news_enemies


def bot_news_controller():
    """
    Случайный выбор типа события из 4х видов и вызов его
    :return:
    """
    db_name = 'infobot_db.db'
    abspath = get_script_dir() + path.sep + db_name  # Формирование абсолютного пути для файла базы данных
    db = sqlite3.connect(abspath)  # connect to sql base
    cursor = db.cursor()  # Creation sqlite cursor
    result = rand_news(cursor, db)

    return result


def rand_news(curs, db):
    """
    Будет формирования основные сообщения по уже имеющимся данным по системам
    :return:
    """
    random_roll = random.randint(1, 100)
    print(random_roll)
    if random_roll > 5:
        rand_list = [bot_news_enemies.select_enemy_news(curs),
                     bot_news_gm.select_gm_news(curs)]
        news = random.choice(rand_list)
    else:
        news = bot_news_access.access_main_news(curs, db)

    return news



