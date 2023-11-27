"""
    В данном модуле хранятся строки для статичных ответов бота
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

economic_commands = """
Команды экономической модели

Общие:
!infoworld *название системы* - вызывает инфу по конкретному миру согласно имеющемуся уровню доступа
!infosystem *название системы* - показывает количество имеющихся миров внутри системы
!infoexport *название системы* - показывает какие экспортные товары производятся в системе и их приблизительная цена
!infoimport *название системы* - показывается какие импортные товары покупают в системе и по какой примерно цене
!infoaccess - показывает уровень доступа на всех известных мирах, где уровень выше 0
!access - показывает информацию по уровням доступа для миров
!infoallgoods - показывает весь список товаров
!infoexportgoods *название товара* - показывает системы с необходимым уровнем доступа, которые экспортируют данный товар
!infoimportgoods *название товара* - показывает системы с необходимым уровнем доступа, которые импортируют данный товар
!goodspie - наказывает 2 круговые диаграммы по соотношению экспортных и импортных товаров и их базовые цены
!price *название товара*, если названия нет то выводятся все внутриигровые товары с базовыми ценами

Админские:
!startnews - запускает цикл новостей бота с выводом сообщений
!stopnews - останавливает цикл новостей с выводом статистики по сессии
!infoworldgm *название системы* - вызывает инфу по конкретному миру без учета уровня доступа

Название систем можно посмотреть на сайте - на карте
"""
roll_commands = """
Команды системы бросков кубика

Общие:
!common_roll *количество кубиков*d*количество граней кубика* - роллит кубик с обозначенными гранями
!roll *сложность* *критический диапазон* - роллит кубик с записью в статистику
!mega_roll *сложность* *критический диапазон* - роллит кубик с записью в статистику с шансом на улучшение результата
!luck_roll *сложность* *критический диапазон* - роллит кубик с записью в статистику с двойным броском кубика и выбором лучшего результата
!consumable_all_groups - выводит весь список имеющихся групп расходников
!consumable_all_types - выводит весь список имеющихся типов расходников
"""

art_and_special_items_commands = """
Команды артефактов и специальных предметов

Админские:
!artifact *грейд артефакта* *группа артефакта* *тип артефакта*
!consumable_loot *название группы расходников* *название типа расходников* - выдает сгенерированный расходник со статистикой
!consumable_loot_no_stat *название группы расходников* *название типа расходников* - выдает сгенерированный расходник без статистики
        
Название систем можно посмотреть на сайте - на карте"""

access_level = """
Нулевой уровень: недоступно ничего, мир скрыт для запросов полностью
Первый уровень доступно: название системы, имперский класс, общий уровень опасности
Второй уровень доступно: уровень имперской власти, население, угроза отдельных врагов, основные типы местности
Третий уровень доступно: экспорт, импорт и дополнительные особенности мира"""