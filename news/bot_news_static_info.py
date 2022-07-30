def select_subsector_news(curs):
    select_gm_news_string = '''
    SELECT news_text FROM subsector_news
    ORDER BY RANDOM()
    LIMIT 1
    '''
    subsector_string = tuple(curs.execute(select_gm_news_string))[0][0]
    return subsector_string


def select_lore_info(curs):
    select_gm_news_string = '''
    SELECT lore_text FROM lore_info
    ORDER BY RANDOM()
    LIMIT 1
    '''
    lore_string = tuple(curs.execute(select_gm_news_string))[0][0]
    return lore_string
