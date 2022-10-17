from jinja2 import Template

def count_news_statistics():
    stat_dict = {"НОВОСТЬ О ВРАГАХ": [],
                 "НОВОСТЬ О БЕЗОПАСНОМ МЕСТЕ": [],
                 "КВЕСТ": [],
                 "ИЗМЕНЕНИЕ ПРОИЗВОДСТВА": [],
                 "ПОВЫШЕНИЕ УРОВНЯ ДОСТУПА": [],
                 "Уникальные новости": [],
                 "НОВОСТЬ СУБСЕКТОРА": [],
                 "ЛОРНАЯ НОВОСТЬ": []
                 }

    def append_stat(type_news=None, value=None):
        if type_news:
            if value:
                stat_dict[type_news].append(value)
                return stat_dict

        return form_news_statitics(stat_dict)

    return append_stat


def form_news_statitics(isdict):
    stat_template = Template("""
    Статистика: 
    {% for item in isdict.items() -%}
        {{ item[0].capitalize() }}: {% if not item[1] %} 0 {% else %} {{ item[1]|length }} {% endif %}
    {% endfor %}""")
    stat_render = stat_template.render(isdict=isdict)
    return stat_render
