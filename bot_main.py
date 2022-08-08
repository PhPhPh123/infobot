"""
Данный модуль содержит все команды к боту и отправляет их обработку в нижестоящие модули. Запуск бота осуществляется
именно через этот модуль. Боты организованы через асинхронные функции API discord с добавлением декораторов для команд и
прав доступа. Первая функция подключается к базе данных, а остальные представляют собой команды боту.
Все необходимые модули импортируются включая модуль с настройками
"""

from settings_and_imports import *

import static_messages
import user_info.bot_user_info_world
import user_info.bot_user_info_systems
import user_info.bot_user_access
import user_info.bot_import_and_export
import user_info.bot_user_info_goods
import news.bot_news_main
from minor_commands import roll_module

infobot = commands.Bot(command_prefix=settings['prefix'])  # Экземпляр класса бота


def connect_to_db_sqlite3() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """
    Функция, которая подключается к базе данных и создает объекты курсора и коннекта, абсолютный путь берет из файла
    настроек
    :return: объекты курсора и коннекта
    """
    db_name = 'infobot_db.db'
    abspath = get_script_dir() + os.path.sep + db_name  # Формирование абсолютного пути для файла базы данных
    connect = sqlite3.connect(abspath)  # Подключение к базе данных
    cursor = connect.cursor()  # Создание курсора
    return cursor, connect


def connect_to_db_sqlalchemy():
    """
    Данный модуль подключается к orm sqlalchemy
    :return: объекты коннектора и таблички worlds
    """
    db_engine = sqlalchemy.create_engine('sqlite:///infobot_db.db')
    db_connector = db_engine.connect()

    metadata = sqlalchemy.MetaData(db_engine)
    worlds = sqlalchemy.Table('worlds', metadata, autoload=True)

    return db_connector, worlds


@infobot.command()
async def infoworld(ctx: discord.ext.commands.context.Context, world_name: str):
    """
    Функция, выдающая ответ по характеристикам запрашиваемого мира на основании запроса в базу данных
    :param ctx: объект класса контекст библиотеки discord
    :param world_name: название запрашиваемого мира
    :return: строка, полученная путем выполнения нижестоящих функций и даюткоманду боту на вывод текста в чате дискорда
    """
    global db_cursor
    bot_answer = user_info.bot_user_info_world.to_control_other_functions_and_returns_bot_answer(db_cursor, world_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infosystem(ctx: discord.ext.commands.context.Context, system_name: str):
    """
    Функция, выдающая список миров внутри системы на основании запроса в базу данных
    :param ctx: объект класса контекст библиотеки discord
    :param system_name: название запрашиваемой системы
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    global db_cursor
    bot_answer = user_info.bot_user_info_systems.db_select_systems(db_cursor, system_name)
    await ctx.send(bot_answer)


@infobot.command()
async def helpme(ctx: discord.ext.commands.context.Context):
    """
    Функция, отправляющая ботом в дискорде информацию по доступным игрокам командам,
    строку для вывода берет из модуля static_messages
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = static_messages.help_commands
    await ctx.send(bot_answer)


@infobot.command()
async def access(ctx: discord.ext.commands.context.Context):
    """
    Функция, отправляющая ботом в дискорде информацию по тому, за что отвечают уровни доступа на мирах,
    строку для вывода берет из модуля static_messages
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = static_messages.access_level
    await ctx.send(bot_answer)


@infobot.command()
async def infoexport(ctx: discord.ext.commands.context.Context, world_name: str):
    """
    Функция, отправляющая ботом в чат список товаров, которые экспортирует запрашиваемый мир и их цену после пересчета
    всех модификаторов влияющих на среднюю стоимость
    :param ctx: объект класса контекст библиотеки discord
    :param world_name: название запрашиваемого мира
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    global db_cursor
    deal_name = 'export'
    bot_answer = user_info.bot_import_and_export.choice_deal_and_returns_bot_answer(db_cursor, world_name, deal_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infoimport(ctx: discord.ext.commands.context.Context, world_name: str):
    """
    Функция, отправляющая ботом в чат список товаров, которые импортирует запрашиваемый мир и их цену после пересчета
    всех модификаторов влияющих на среднюю стоимость
    :param ctx: объект класса контекст библиотеки discord
    :param world_name: название запрашиваемого мира
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    global db_cursor
    deal_name = 'import'
    bot_answer = user_info.bot_import_and_export.choice_deal_and_returns_bot_answer(db_cursor, world_name, deal_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infoaccess(ctx: discord.ext.commands.context.Context):
    """
    Функция, отправляющая ботов в чат общий список миров, в которых уровень доступа отличен от 0(т.е. фактически есть)
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    global db_cursor, alch_connect, alch_world
    bot_answer = user_info.bot_user_access.form_tuple_in_db(alch_connect, alch_world)
    await ctx.send(bot_answer)


@infobot.command()
async def infoallgoods(ctx: discord.ext.commands.context.Context):
    """
    Функция выводит список имеющихся торговых товаров в игре, строку для вывода берет из модуля static_messages
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = static_messages.goods
    await ctx.send(bot_answer)


@infobot.command()
async def infoimportgoods(ctx: discord.ext.commands.context.Context, goods_name: str):
    """
    Функция выводит список миров, которые импортируют данный товар
    :param ctx: объект класса контекст библиотеки discord
    :param goods_name: название товара
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    global db_cursor
    deal_name = 'import'
    bot_answer = user_info.bot_user_info_goods.choise_deal_and_execute_in_db(db_cursor, goods_name, deal_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infoexportgoods(ctx: discord.ext.commands.context.Context, goods_name: str):
    """
    Функция выводит список миров, которые экспортируют данный товар
    :param ctx: объект класса контекст библиотеки discord
    :param goods_name: название товара
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    global db_cursor
    deal_name = 'export'
    bot_answer = user_info.bot_user_info_goods.choise_deal_and_execute_in_db(db_cursor, goods_name, deal_name)
    await ctx.send(bot_answer)


@tasks.loop(minutes=30)
async def news_send(channel: discord.channel.TextChannel):
    """
    Функция отправляющая с определенной переодичностью(доп.параметр декоратора tasks.loop) сообщения рандомно
    выбранные из списка в нижестоящей функции bot_news_controller. За запуск данного цикла отвечает функция startnews
    :param channel: стандартный аргумент библиотеки
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    global db_cursor, db_connect
    chosen_news = news.bot_news_main.choise_random_news(db_cursor, db_connect)

    await channel.send(chosen_news)


@infobot.command()
async def roll(ctx: discord.ext.commands.context.Context, user_roll: str):
    """
    :param ctx: ctx: discord.ext.commands.context.Context
    :param user_roll: строка ролла, например '3d6'
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = roll_module.roll_func(user_roll)
    await ctx.send(bot_answer)


@infobot.command()
@commands.has_permissions(administrator=True)
async def startnews(ctx: discord.ext.commands.context.Context):
    """
    Функция, запускающая цикл отправки ботом в чат сообщений с новостями, декоратор commands.has_premissions отвечает
    за роль, которая может его запустить, а именно только администратор группы
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда сначала сообщения 'Поиск слухов...', а затем вызов
    функции news_send
    """
    await ctx.send("Поиск слухов...")
    news_send.start(ctx.channel)


@infobot.command()
@commands.has_permissions(administrator=True)
async def artifact(ctx: discord.ext.commands.context.Context,
                   grade: str,
                   group_art: str = 'random',
                   type_art: str = 'random',
                   unique_bonus: str = 'random',
                   ):
    await ctx.send(f'{grade}, {group_art}, {type_art}, {unique_bonus}')


if __name__ == '__main__':
    session = connect_to_db_sqlalchemy()

    db_cursor, db_connect = connect_to_db_sqlite3()
    alch_connect, alch_world = connect_to_db_sqlalchemy()

    infobot.run(settings['token'])
