from settings_and_imports import *
from . import bot_news_access, bot_news_static_info, bot_news_enemies


def rand_news(curs, db):
    """
    Будет формирования основные сообщения по уже имеющимся данным по системам
    :return:
    """
    random_roll = random.randint(1, 100)
    if random_roll > 5:
        news = random.choice([bot_news_enemies.select_enemy_news(curs),
                              bot_news_static_info.select_subsector_news(curs),
                              bot_news_static_info.select_lore_info(curs)])
    else:
        news = bot_news_access.access_main_news(curs, db)

    return news
