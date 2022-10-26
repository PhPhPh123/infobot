"""
    Данный модуль управляет остальными news-модулями, выбирая какой тип новости будет выдан и отдавая управление
    на модули и функции, формирующие сообщения
"""

from settings_imports_globalVariables import *
from news import bot_news_access, bot_news_static_info, bot_news_enemies, production_buffs_and_debuffs, mini_quests, unique_news
import exceptions


def choise_random_news() -> str:
    """
    Данная функция выбирает случайную новость путем случайного выбора функции, которая ее обработает и вернет
    Ролл от 1 до 100 ведется, чтобы определить удачливость событий новостей. Ролл 1-5 считается удачливым,
    поэтому и новости будут полезными и влияющими на геймплей игроков непосредственно
    :return: строка с новостью-ответом ботом
    """
    random_roll = random.randint(1, 100)

    list_of_type_news = [
        'Новости о наличии врагов в системе',
        'Статичные новости о делах в субсекторе',
        'Статичные новости о лоре вархаммера 40к',
        'Новости об изменениях в дефицитах и перепроизводствах']

    if check_common_news_not_empty():
        list_of_type_news.append('Уникальные несрочные новости')

    bot_answer = ''

    if check_urgently_news_not_empty():  # проверка, что в базе срочных новостей есть срочные новости
        bot_answer = unique_news.control_form_news('срочная новость')
    else:
        if random_roll >= 15:  # Обычный исход ролла
            news = random.choice(list_of_type_news)
            if news == 'Новости о наличии врагов в системе':
                bot_answer = bot_news_enemies.form_enemy_news()
            elif news == 'Статичные новости о делах в субсекторе':
                bot_answer = bot_news_static_info.form_subsector_news()
            elif news == 'Статичные новости о лоре вархаммера 40к':
                bot_answer = bot_news_static_info.form_lore_info()
            elif news == 'Новости об изменениях в дефицитах и перепроизводствах':
                bot_answer = production_buffs_and_debuffs.form_production_changes_news()
            elif news == 'Уникальные несрочные новости':
                bot_answer = unique_news.control_form_news('несрочная новость')

        elif 6 <= random_roll <= 14:  # Удачливый исход ролла для квеста
            bot_answer = mini_quests.control_quests()

        else:  # Максимально удачливый исход ролла
            bot_answer = bot_news_access.control_other_func()

    register_statistics(bot_answer)

    return bot_answer


def register_statistics(bot_answer: str) -> None:
    quest_name = re.split("[\[\]]", bot_answer)[1]

    global_news_statistics(quest_name, bot_answer)


def check_urgently_news_not_empty() -> bool:
    """
    Данная функция проверяет наличие записей(новостей) во второстепенной базе данных unique_news.db,
    таблицу urgently_news
    @return: булево значение
    """
    try:
        all_urgently_news = tuple(global_unique_news_cursor.execute('SELECT * FROM urgently_unique_news'))
        if all_urgently_news:  # Если база выдает значения, значит список новостей не пустой
            return True
        else:
            return False
    except AttributeError:  # Если базы не существует, будет данное исключение
        return False


def check_common_news_not_empty():
    """
    Данная функция проверяет наличие записей(новостей) во второстепенной базе данных unique_news.db,
    таблицу common_news
    @return: булево значение
    """
    try:
        all_common_news = tuple(global_unique_news_cursor.execute('SELECT * FROM common_unique_news'))
        if all_common_news:  # Если база выдает значения, значит список новостей не пустой
            return True
        else:
            return False
    except AttributeError:  # Если базы не существует, будет данное исключение
        return False


if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
