from user_info.bot_user_info_main import *
from user_info.bot_user_info_systems import *
from user_info.bot_import_and_export import *
from user_info.bot_user_access import *
from user_info.bot_user_info_goods import *
from news.bot_news_main import *

"""
Данный модуль содержит все команды к боту и отправляет их обработку в нижестоящие модули. Запуск бота осуществляется
именно через этот модуль. Боты организованы через асинхронные функции API discord с добавлением декораторов для команд и
прав доступа. Все необходимые модули импортируются включая модуль с настройками
"""

infobot = commands.Bot(command_prefix=settings['prefix'])  # Экземпляр класса бота


@infobot.command()
async def infoworld(ctx, world_name: str):
    """
    Функция, выдающая ответ по характеристикам запрашиваемого мира на основании запроса в базу данных
    :param ctx: стандартный аргумент библиотеки
    :param world_name: название запрашиваемого мира
    :return: строка, полученная путем выполнения нижестоящих функций и даюткоманду боту на вывод текста в чате дискорда
    """
    bot_answer = returns_string_for_infoworld_command(world_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infosystem(ctx, system_name: str):
    """
    Функция, выдающая список миров внутри системы на основании запроса в базу данных
    :param ctx: стандартный аргумент библиотеки
    :param system_name: название запрашиваемой системы
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = bot_user_info_controller_systems(system_name)
    await ctx.send(bot_answer)


@infobot.command()
async def helpme(ctx):
    """
    Функция, отправляющая ботом в дискорде информацию по доступным игрокам командам
    :param ctx: стандартный аргумент библиотеки
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = '''
Команды:
!infoworld *название системы* - вызывает инфу по конкретному миру согласно имеющемуся уровню доступа
!infosystem *название системы* - показывает количество имеющихся миров внутри системы
!infoexport *название системы* - показывает какие экспортные товары производятся в системе и их приблизительная цена
!infoimport *название системы* - показывается какие импортные товары покупают в системе и по какой примерно цене
!infoaccess - показывает уровень доступа на всех известных мирах, где уровень выше 0
!access - показывает информацию по уровням доступа для миров
!infoallgoods - показывает весь список товаров
!infoexportgoods *название товара* - показывает системы с необходимым уровнем доступа, которые экспортируют данный товар
!infoimportgoods *название товара* - показывает системы с необходимым уровнем доступа, которые импортируют данный товар
        
Название систем можно посмотреть на сайте - на карте'''
    await ctx.send(bot_answer)


@infobot.command()
async def access(ctx):
    """
    Функция, отправляющая ботом в дискорде информацию по тому, за что отвечают уровни доступа на мирах
    :param ctx: стандартный аргумент библиотеки
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = '''
Нулевой уровень: недоступно ничего, мир скрыт для запросов полностью
Первый уровень доступно: название системы, имперский класс, общий уровень опасности
Второй уровень доступно: уровень имперской власти, население, угроза отдельных врагов, основные типы местности
Третий уровень доступно: экспорт, импорт и дополнительные особенности мира'''
    await ctx.send(bot_answer)


@infobot.command()
async def infoexport(ctx, world_name: str):
    """
    Функция, отправляющая ботом в чат список товаров, которые экспортирует запрашиваемый мир и их цену после пересчета
    всех модификаторов влияющих на среднюю стоимость
    :param ctx: стандартный аргумент библиотеки
    :param world_name: название запрашиваемого мира
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    deal_name = 'export'
    bot_answer = bot_user_info_controller_trade(world_name, deal_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infoimport(ctx, world_name: str):
    """
    Функция, отправляющая ботом в чат список товаров, которые импортирует запрашиваемый мир и их цену после пересчета
    всех модификаторов влияющих на среднюю стоимость
    :param ctx: стандартный аргумент библиотеки
    :param world_name: название запрашиваемого мира
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    deal_name = 'import'
    bot_answer = bot_user_info_controller_trade(world_name, deal_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infoaccess(ctx):
    """
    Функция, отправляющая ботов в чат общий список миров, в которых уровень доступа отличен от 0(т.е. фактически есть)
    :param ctx: стандартный аргумент библиотеки
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = bot_user_info_controller_access()
    await ctx.send(bot_answer)


@infobot.command()
async def infoallgoods(ctx):
    """
    Функция выводит список имеющихся торговых товаров в игре
    :param ctx: стандартный аргумент библиотеки
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = '''
Нормальное-продовольствие
Питательная-паста
Деликатесы
Стрелковое-оружие-и-экипировка
Боеприпасы
Одежда-и-украшения
Гражданская-техника
Медицина-и-парфюмерия
Опасные-вещества
Электронные-компоненты
Тяжелые-машинные-детали
Прометий-и-субпродукты
Строй-материалы
Металлы
Редкие-минералы'''
    await ctx.send(bot_answer)


@infobot.command()
async def infoimportgoods(ctx, goods_name: str):
    """
    Функция выводит список миров, которые импортируют данный товар
    :param ctx: стандартный аргумент библиотеки
    :param goods_name: название товара
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    deal_name = 'import'
    bot_answer = bot_user_info_controller_goods(goods_name, deal_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infoexportgoods(ctx, goods_name):
    """
    Функция выводит список миров, которые экспортируют данный товар
    :param ctx: стандартный аргумент библиотеки
    :param goods_name: название товара
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    deal_name = 'export'
    bot_answer = bot_user_info_controller_goods(goods_name, deal_name)
    await ctx.send(bot_answer)


@tasks.loop(seconds=5)
async def news_send(channel):
    """
    Функция отправляющая с определенной переодичностью(доп.параметр декоратора tasks.loop) сообщения рандомно
    выбранные из списка в нижестоящей функции bot_news_controller. За запуск данного цикла отвечает функция startnews
    :param channel: стандартный аргумент библиотеки
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    news = bot_news_controller()

    await channel.send(news)


@infobot.command()
@commands.has_permissions(administrator=True)
async def startnews(ctx):
    """
    Функция, запускающая цикл отправки ботом в чат сообщений с новостями, декоратор commands.has_premissions отвечает
    за роль, которая может его запустить, а именно только администратор группы
    :param ctx: стандартный аргумент библиотеки
    :return: отправка строки боту для вывода в текущем чате дискорда сначала сообщения 'Поиск слухов...', а затем вызов
    функции news_send
    """
    await ctx.send("Поиск слухов...")
    news_send.start(ctx.channel)


if __name__ == '__main__':
    infobot.run(settings['token'])
