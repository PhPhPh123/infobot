"""
Данный модуль содержит все команды к боту и отправляет их обработку в нижестоящие модули. Запуск бота осуществляется
именно через этот модуль. Боты организованы через асинхронные функции API discord с добавлением декораторов для команд и
прав доступа. Первая функция подключается к базе данных, а остальные представляют собой команды боту.
Все необходимые модули импортируются включая модуль с настройками
"""

from settings_imports_globalVariables import *

import static_answer_messages
import user_info.infoworld_command
import user_info.infosystem_command
import user_info.info_access_command
import user_info.import_and_export_commands
import user_info.infoexportgoods_command
import user_info.goodspie_command
import news.bot_news_main
import craft.main_artifact_builder
from minor_commands import roll_module


intents = discord.Intents.all()
intents.members = True
infobot = commands.Bot(command_prefix=settings['prefix'], intents=intents)  # Экземпляр класса бота


def connect_to_db_sqlalchemy():
    """
    Данный модуль подключается к orm sqlalchemy
    :return: объекты коннектора и таблички worlds
    """
    db_engine = sqlalchemy.create_engine('sqlite:///infobot_db.db')
    db_connector = db_engine.connect()

    metadata = sqlalchemy.MetaData(db_engine)
    worlds = sqlalchemy.Table('worlds', metadata, autoload=True)
    systems = sqlalchemy.Table('systems', metadata, autoload=True)

    return db_connector, worlds, systems


@infobot.command()
async def infoworld(ctx: discord.ext.commands.context.Context, world_name: str):
    """
    Функция, выдающая ответ по характеристикам запрашиваемого мира на основании запроса в базу данных
    :param ctx: объект класса контекст библиотеки discord
    :param world_name: название запрашиваемого мира
    :return: строка, полученная путем выполнения нижестоящих функций и даюткоманду боту на вывод текста в чате дискорда
    """
    bot_answer = user_info.infoworld_command.to_control_other_functions_and_returns_bot_answer(world_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infosystem(ctx: discord.ext.commands.context.Context, system_name: str):
    """
    Функция, выдающая список миров внутри системы на основании запроса в базу данных
    :param ctx: объект класса контекст библиотеки discord
    :param system_name: название запрашиваемой системы
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = user_info.infosystem_command.to_control_other_functions_and_returns_bot_answer(system_name)
    await ctx.send(bot_answer)


@infobot.command()
async def helpme(ctx: discord.ext.commands.context.Context):
    """
    Функция, отправляющая ботом в дискорде информацию по доступным игрокам командам,
    строку для вывода берет из модуля static_messages
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = static_answer_messages.help_commands
    await ctx.send(bot_answer)


@infobot.command()
async def access(ctx: discord.ext.commands.context.Context):
    """
    Функция, отправляющая ботом в дискорде информацию по тому, за что отвечают уровни доступа на мирах,
    строку для вывода берет из модуля static_messages
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = static_answer_messages.access_level
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
    bot_answer = user_info.import_and_export_commands.choice_deal_and_returns_bot_answer(world_name, deal_name)
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
    deal_name = 'import'
    bot_answer = user_info.import_and_export_commands.choice_deal_and_returns_bot_answer(world_name, deal_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infoaccess(ctx: discord.ext.commands.context.Context):
    """
    Функция, отправляющая ботов в чат общий список миров, в которых уровень доступа отличен от 0(т.е. фактически есть)
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    global alch_connect, alch_world
    bot_answer = user_info.info_access_command.form_tuple_in_db(alch_connect, alch_world)
    await ctx.send(bot_answer)


@infobot.command()
async def infoallgoods(ctx: discord.ext.commands.context.Context):
    """
    Функция выводит список имеющихся торговых товаров в игре, строку для вывода берет из модуля static_messages
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = static_answer_messages.goods
    await ctx.send(bot_answer)


@infobot.command()
async def infoimportgoods(ctx: discord.ext.commands.context.Context, goods_name: str):
    """
    Функция выводит список миров, которые импортируют данный товар
    :param ctx: объект класса контекст библиотеки discord
    :param goods_name: название товара
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    deal_name = 'import'
    user_info.infoexportgoods_command.choise_deal_and_execute_in_db(goods_name, deal_name)
    await ctx.send(file=discord.File('logs_and_temp_files/info_export_import_goods.png'))


@infobot.command()
async def infoexportgoods(ctx: discord.ext.commands.context.Context, goods_name: str):
    """
    Функция выводит список миров, которые экспортируют данный товар
    :param ctx: объект класса контекст библиотеки discord
    :param goods_name: название товара
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    deal_name = 'export'
    user_info.infoexportgoods_command.choise_deal_and_execute_in_db(goods_name, deal_name)
    await ctx.send(file=discord.File('logs_and_temp_files/info_export_import_goods.png'))


@tasks.loop(minutes=30)
async def news_send(channel: discord.channel.TextChannel):
    """
    Функция отправляющая с определенной переодичностью(доп.параметр декоратора tasks.loop) сообщения рандомно
    выбранные из списка в нижестоящей функции bot_news_controller. За запуск данного цикла отвечает функция startnews
    :param channel: стандартный аргумент библиотеки
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    chosen_news = news.bot_news_main.choise_random_news()
    # Новости записываются в лог
    logger.info('[news]' + chosen_news)
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
                   unique_bonus: str = 'random'
                   ):

    param_dict = {'грейд': grade.lower(),
                  'группа': group_art.lower(),
                  'тип': type_art.lower(),
                  'особенность': unique_bonus.lower()}

    bot_answer = craft.main_artifact_builder.choise_class_objects(param_dict)
    await ctx.send(bot_answer)


@infobot.command()
async def goodspie(ctx: discord.ext.commands.context.Context):

    user_info.goodspie_command.to_control_other_functions()
    await ctx.send(file=discord.File('answer_pie.png'))


@infobot.event
async def on_voice_state_update(member, before, after):
    # присоединение к каналу
    if before.channel is None and after.channel is not None:
        print('1', member.id)

    # покинул канал
    elif before.channel is not None and after.channel is None:
        print('2', member.id)

    # перешел в другой канал
    elif before.channel is not None and after.channel is not None:
        print('3', member.id)


if __name__ == '__main__':
    logger.info('[bot_run]')

    session = connect_to_db_sqlalchemy()

    alch_connect, alch_world, alch_systems = connect_to_db_sqlalchemy()

    infobot.run(settings['token'])
