def select_gm_news(curs):
    select_gm_news_string = '''
    SELECT news_text FROM gm_news
    ORDER BY RANDOM()
    LIMIT 1
    '''
    gm_string = tuple(curs.execute(select_gm_news_string))[0][0]
    return gm_string
