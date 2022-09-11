"""
    Данный модуль управляет остальными news-модулями, выбирая какой тип новости будет выдан и отдавая управление
    на модули и функции, формирующие сообщения
"""

from settings_imports_globalVariables import *
from news import bot_news_access, bot_news_static_info, bot_news_enemies, production_buffs_and_debuffs


def choise_random_news() -> str:
    """
    Данная функция выбирает случайную новость путем случайного выбора функции, которая ее обработает и вернет
    Ролл от 1 до 100 ведется, чтобы определить удачливость событий новостей. Ролл 1-5 считается удачливым,
    поэтому и новости будут полезными и влияющими на геймплей игроков непосредственно
    :return: строка с новостью-ответом ботом
    """
    random_roll = random.randint(1, 100)

    list_of_type_news = ['Новости о наличии врагов в системе',
                         'Статичные новости о делах в субсекторе',
                         'Статичные новости о лоре вархаммера 40к',
                         'Новости об изменениях в дефицитах и перепроизводствах']

    if random_roll > 5:  # Обычный исход ролла
        news = random.choice([list_of_type_news])
        if news == 'Новости о наличии врагов в системе':
            bot_news_enemies.form_enemy_news()
        elif news == 'Статичные новости о делах в субсекторе':
            bot_news_static_info.form_subsector_news()
        elif news == 'Статичные новости о лоре вархаммера 40к':
            bot_news_static_info.form_lore_info()
        elif news == 'Новости об изменениях в дефицитах и перепроизводствах':
            production_buffs_and_debuffs.form_production_changes_news()
    else:  # Удачливый исход ролла
        news = bot_news_access.control_other_func()

    return news
