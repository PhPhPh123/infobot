"""
Данный модуль содержит все команды к боту и отправляет их обработку в нижестоящие модули. Запуск бота осуществляется
именно через этот модуль. Боты организованы через асинхронные функции API discord с добавлением декораторов для команд и
прав доступа. Первая функция подключается к базе данных, а остальные представляют собой команды боту.
Все необходимые модули импортируются включая модуль с настройками
"""

from imports_globalVariables import *

from minor_commands import roll_module
import static_answer_messages
import user_info.infoworld_command
import user_info.infosystem_command
import user_info.info_access_command
import user_info.import_and_export_commands
import user_info.infoexportgoods_command
import user_info.goodspie_command
import user_info.info_all_goods
import user_info.ingame_goods
import news.bot_news_main
import craft.main_artifact_factory
import news.unique_news

if __name__ == '__main__':
    '''
    Настройки бота и загрузка токена для него при старте модуля
    '''
    load_dotenv(find_dotenv())  # загрузка переменных окружения из файла ..env с токеном, именем и id бота
    token = os.environ['TOKEN']
    bot_name = os.environ['NAME']
    bot_id = os.environ['ID']
    settings = {
        'token': token,
        'bot': bot_name,
        'id': bot_id,
        'prefix': '!'  # команды бота стартуют с данного префикса
    }

    # установка полномочий бота
    intents = discord.Intents.all()
    intents.members = True

    infobot = commands.Bot(command_prefix=settings['prefix'], intents=intents)  # Экземпляр класса бота

    logger.info('[bot_run]')  # запись в лог старт сессии
else:
    raise exceptions.NotImportedModuleException  # модуль не подразумевает импорт, он вызывает только непосредственно

"""
#######################################################################################################################
Ниже идут команды для бота в виде отдельных функций. Название команды совпадает с названием функции
#######################################################################################################################
"""


@infobot.command()
async def infoworld(ctx: discord.ext.commands.context.Context, world_name: str):
    """
    Функция, выдающая ответ по характеристикам запрашиваемого мира на основании запроса в базу данных
    :param ctx: объект класса контекст библиотеки discord
    :param world_name: название запрашиваемого мира
    :return: строка, полученная путем выполнения нижестоящих функций и даюткоманду боту на вывод текста в чате дискорда
    """
    bot_answer, world_url = user_info.infoworld_command.to_control_other_functions_and_returns_bot_answer(world_name)
    await ctx.send(content=bot_answer, file=discord.File(f'static/image/world_image/{world_url}'))


@infobot.command()
@commands.has_permissions(administrator=True)
async def infoworldgm(ctx: discord.ext.commands.context.Context, world_name: str):
    """
    Функция, выдающая ответ по характеристикам запрашиваемого мира на основании запроса в базу данных, отличие от
    обычной функции в том, что она игнорирует уровень доступа и выдает полную информацию по миру. Команда доступна
    только для ГМа
    :param ctx: объект класса контекст библиотеки discord
    :param world_name: название запрашиваемого мира
    :return: строка, полученная путем выполнения нижестоящих функций и даюткоманду боту на вывод текста в чате дискорда
    """
    gmflag = True
    bot_answer, world_url = user_info.infoworld_command.to_control_other_functions_and_returns_bot_answer(world_name,
                                                                                                          gmflag)
    await ctx.send(content=bot_answer, file=discord.File(f'static/image/world_image/{world_url}'))


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
async def infoaccess(ctx: discord.ext.commands.context.Context, type_of_output='string'):
    """
    Функция, отправляющая ботов в чат общий список миров, в которых уровень доступа отличен от 0(т.е. фактически есть)
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    @param ctx: объект класса контекст библиотеки discord
    @param type_of_output: параметр отвечает за тип вывода информации: строка или отправка excel-файла
    """
    if type_of_output == 'string':
        # если тип ответа строка(либо ничего т.к. аргумент по умолчанию), то вызывается фасад без аргументов
        bot_answer_list = user_info.info_access_command.form_tuple_in_db()
        # строка ответа может быть больше 2000 знаков, поэтому ответ размещается в списке и выводится по частям
        for message in bot_answer_list:
            await ctx.send(message)

    elif type_of_output == 'excel':
        # если запрос является экселем, то вызывается фасад с аргументом экселя
        user_info.info_access_command.form_tuple_in_db(excel_answer=True)
        await ctx.send(file=discord.File('logs_and_temp_files/access.xlsx'))
    else:  # некорректный запрос
        await ctx.send('Некорректный тип вывода для запроса, укажите либо string либо ничего либо excel')


@infobot.command()
async def infoallgoods(ctx: discord.ext.commands.context.Context):
    """
    Функция выводит полный список имеющихся торговых товаров в игре путем вызова фасадного метода
    из модуля info_all_goods
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = user_info.info_all_goods.to_control_other_functions()
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
async def stopnews(ctx: discord.ext.commands.context.Context):
    """
    Данная функция прерывает основной цикл новостей news_send и распечатывает в чат статистику по новостному циклу
    @param ctx: объект класса контекст библиотеки discord
    @return: отправка ботом в чат информации об остановке цикла новостей
    """
    news_send.cancel()
    bot_answer = global_news_statistics()
    await ctx.send(bot_answer)


@infobot.command()
@commands.has_permissions(administrator=True)
async def artifact(ctx: discord.ext.commands.context.Context,
                   grade: str,
                   group_art: str = 'random',
                   type_art: str = 'random',
                   unique_bonus: str = 'random'
                   ):
    """
    Данная команда отвечает за формирование артефактов, она доступка только админу
    Полный список доступен либо при просмотре базы данных либо в __init__.py артефактного пакета craft
    @param ctx: объект класса контекст библиотеки discord
    @param grade: грейд артефакта(возможны зеленый, синий, фиолетовый, красный)
    @param group_art: группа артефактов
    @param type_art: тип артефактов
    @param unique_bonus: уникальный бонус
    @return: отправка ботом в чат информации с параметрами и названием артефакта
    """
    # Словарь со значениями запрошенных параметров, обязательным является только грейд, остальное, по умолчанию, будет
    # выбираться случайно
    param_dict = {'грейд': grade.lower(),
                  'группа': group_art.lower(),
                  'тип': type_art.lower(),
                  'особенность': unique_bonus.lower()}

    bot_answer = craft.main_artifact_factory.choise_class_objects(param_dict)
    await ctx.send(bot_answer)


@infobot.command()
@commands.has_permissions(administrator=True)
async def special_loot(ctx: discord.ext.commands.context.Context,
                       loot_amount: str
                       ):
    # Словарь со значениями запрошенных параметров, обязательным является только 'размер лута'
    param_dict = {'размер лута': loot_amount.lower()}

    bot_answer = ''
    await ctx.send(bot_answer)


@infobot.command()
async def goodspie(ctx: discord.ext.commands.context.Context):
    """
    Данная команда выводит полный список товаров, экспорта и импорта, в субсекторе согласно их количества на планетах,
    а также их базовые цены. Это более развернутая и подробный аналог команды !infoallgoods
    @param ctx: объект класса контекст библиотеки discord
    @return: отправка в чат картинки с двумя пироговыми диаграммами созданными библиотекой matplotlib
    """
    user_info.goodspie_command.to_control_other_functions()
    await ctx.send(file=discord.File('logs_and_temp_files/answer_pie.png'))


@infobot.command()
async def price(ctx: discord.ext.commands.context.Context, good_name='all'):
    """
    Данная команда выводит список внутриигровых товаров с их базовой стоимостью для упрощения подсказок ГМу, на какие
    примерные цены стоит ориентироваться
    @param ctx: объект класса контекст библиотеки discord
    @param good_name: название товара, по умолчанию вывод полного списка
    @return: отправка в чат картинки с двумя пироговыми диаграммами созданными библиотекой matplotlib
    """
    bot_answer = user_info.ingame_goods.to_control_other_functions_and_returns_bot_answer(good_name)
    await ctx.send(bot_answer)


"""
#######################################################################################################################
Ниже идут функции событий(events) и циклов(loop) бота
#######################################################################################################################
"""


@tasks.loop(minutes=30)
async def news_send(channel: discord.channel.TextChannel):
    """
    Функция отправляющая с определенной переодичностью(доп.параметр декоратора tasks.loop) сообщения рандомно
    выбранные из списка в нижестоящей функции bot_news_controller. За запуск данного цикла отвечает функция startnews
    :param channel: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    chosen_news = news.bot_news_main.choise_random_news()
    # Новости записываются в лог
    logger.info('[news]' + chosen_news)
    await channel.send(chosen_news)


@infobot.event
async def on_command_error(ctx: discord.ext.commands.context.Context, error):
    """
    Данное событие выводит в чат сообщение, если команды не существует либо она введена неправильно
    @param ctx: объект класса контекст библиотеки discord
    @param error: объект исключения библиотеки discord
    @return: отправка в чат сообщения о неверной команде
    """
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("Неверная команда")


infobot.run(settings['token'])  # запуск основного асинхронного цикла бота, любые команды ниже выполнены не будут
