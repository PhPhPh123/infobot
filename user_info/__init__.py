"""
    Данный пакет отвечает за пользовательский вывод информации по игровому субсектору. Общего управляющего модуля у него
    нет и каждый модуль независим от другого и отвечает за одну или несколько команд

    Пакет работает с основной базойданных infobot_db.db
    В связи с большим количеством сырых sql запросов, они были выведены в отдельный модуль
    sql_queries

    Все модули пакеты реализоны через шаблон проектирования Фасад в котором фасадная функция получает нужные данные и
    возвращает итоговую строку ответа
"""