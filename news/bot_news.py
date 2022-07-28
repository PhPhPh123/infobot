from settings_and_imports import *


def bot_news_controller():
    """
    Случайный выбор типа события из 4х видов и вызов его
    :return:
    """
    db_name = 'infobot_db.db'
    abspath = get_script_dir() + path.sep + db_name  # Формирование абсолютного пути для файла базы данных
    db = sqlite3.connect(abspath)  # connect to sql base
    cursor = db.cursor()  # Creation sqlite cursor
    result = rand_news(cursor)

    return result


def rand_news(curs):
    """
    Будет формирования основные сообщения по уже имеющимся данным по системам
    :return:
    """
    rand_list = [select_enemy_news(curs), select_gm_news(curs)]
    news = random.choice(rand_list)
    return news


def select_enemy_news(curs):
    select_enemy = '''
    SELECT worlds.world_name, enemies.group_name
    FROM worlds
    INNER JOIN worlds_enemies_relations ON worlds.world_name == worlds_enemies_relations.world_name
    INNER JOIN enemies ON worlds_enemies_relations.enemy_name == enemies.enemy_name
    ORDER BY RANDOM()
    LIMIT 1
    '''

    enemy_news_tuple = tuple(curs.execute(select_enemy))
    str_enemy_news = str_form_enemy_news(enemy_news_tuple)
    return str_enemy_news


def str_form_enemy_news(enemy_tuple):
    """
    Будет повышать уровень доступа путем формирования запроса на update в БД и формировать сообщение о повышении доступа
    :return:
    """
    warning_messages = ['Будьте внимательнее, путешествуя на этот мир',
                        'Для уточнения информации обратитесь в ближайший к системе имперский информационный центр',
                        'Посещать данный мир не будучи вооруженными - не рекомендуется',
                        'Путешествуя в данный мир будьте готовы к столкновению с врагами человечества',
                        'Да прибудет с вами Бог-Император!',
                        'Сохраняйте веру в своем сердце и праведная сила никогда вас не покинет',
                        'Уничтожайте врагов Империума при первой возможности',
                        'Каждый убитый еретик, ксенос и мутант приближают вас к Богу-Императору',
                        'Взаимодействие с врагами человечество, отличное от боестолкновения - запрещено',
                        'Любые враги Человечества должны быть уничтожены',
                        'Если у вас в голове появились еретические мысли - немедленно доложите в ближайшее отделение инквизиции']

    peace_messages = ['Блажен тот кто верует',
                      'Спасибо Богу-Императору за мирное небо над головой',
                      'Не забудьте внести пожертвование в ближайший Храм Бога-Императора',
                      'Лишь благодаря Имперским Воинствам на этом мире нет угроз',
                      'Вступайте в Имперскую гвардию и СПО! Лишь общими усилиями этот мир будет сохранять безопасность',
                      'Не впадайте в порок безделия, посещая данный мир',
                      'Враги могут скрываться даже на внешне благополучном мире. Нашли еретика или предателя? Доложите немедленно']

    if enemy_tuple[0][1]:
        str_answer = f'''
Ходят слухи, что на мире {enemy_tuple[0][0]} есть представляющие угрозу {enemy_tuple[0][1]}. 
{random.choice(warning_messages)}
    '''
    else:
        str_answer = f'''
Ходят слухи, что на мире {enemy_tuple[0][0]} нет опасных врагов. {random.choice(peace_messages)}
'''

    return str_answer


def select_gm_news(curs):
    select_string = '''
    SELECT news_text FROM gm_news
    ORDER BY RANDOM()
    LIMIT 1
    '''
    gm_string = tuple(curs.execute(select_string))[0][0]
    return gm_string
