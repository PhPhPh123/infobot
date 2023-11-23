"""
Данный модуль содержит все команды к боту и отправляет их обработку в нижестоящие модули. Запуск бота осуществляется
именно через этот модуль. Бот организован через асинхронные функции API discord с добавлением декораторов для команд и
прав доступа. Под конструкцией name-main идут базовые стартовые настройки, а все остальные
функции представляют собой команды боту. Одна функция - одна команда. Все необходимые модули импортируются,
включая модуль с глобальными переменными и соединениями с БД.
Последняя строчка в модуле запускает асинхронный цикл бота. Данный модуль, за исключением модулей в каталоге
separatly_started_modules, является единственным запускаемым напрямую. Все остальные импортируются и отдельного вызова
не допускают
"""

from imports_globalVariables import *

import static_answer_messages
import in_game_info.infoworld_command
import in_game_info.infosystem_command
import in_game_info.info_access_command
import in_game_info.import_and_export_commands
import in_game_info.infoexportgoods_command
import in_game_info.goodspie_command
import in_game_info.info_all_goods
import in_game_info.ingame_goods
import in_game_news.bot_news_main
import artifacts.main_artifact_factory
import in_game_news.unique_news
import special_loot.main_loot_factory
import roll_mechanics.common_roll_module
import roll_mechanics.statistics_roll_module

if __name__ == '__main__':
    '''
    Настройки бота и загрузка токена для него при старте модуля
    '''
    load_dotenv(find_dotenv())  # загрузка переменных окружения из файла .env с токеном, именем и id бота
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
    raise exceptions.NotImportedModuleException  # модуль не подразумевает импорт, он вызывается только непосредственно

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
    bot_answer, world_url = in_game_info.infoworld_command.to_control_other_functions_and_returns_bot_answer(world_name)
    await ctx.send(content=bot_answer, file=discord.File(f'static_files/image/world_image/{world_url}'))


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
    bot_answer, world_url = in_game_info.infoworld_command.to_control_other_functions_and_returns_bot_answer(world_name,
                                                                                                             gmflag)
    await ctx.send(content=bot_answer, file=discord.File(f'static_files/image/world_image/{world_url}'))


@infobot.command()
async def infosystem(ctx: discord.ext.commands.context.Context, system_name: str):
    """
    Функция, выдающая список миров внутри системы на основании запроса в базу данных
    :param ctx: объект класса контекст библиотеки discord
    :param system_name: название запрашиваемой системы
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = in_game_info.infosystem_command.to_control_other_functions_and_returns_bot_answer(system_name)
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
    bot_answer = in_game_info.import_and_export_commands.choice_deal_and_returns_bot_answer(world_name, deal_name)
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
    bot_answer = in_game_info.import_and_export_commands.choice_deal_and_returns_bot_answer(world_name, deal_name)
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
        bot_answer_list = in_game_info.info_access_command.form_tuple_in_db()
        # строка ответа может быть больше 2000 знаков, поэтому ответ размещается в списке и выводится по частям
        for message in bot_answer_list:
            await ctx.send(message)

    elif type_of_output == 'excel':
        # если запрос является экселем, то вызывается фасад с аргументом экселя
        in_game_info.info_access_command.form_tuple_in_db(excel_answer=True)
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
    bot_answer = in_game_info.info_all_goods.to_control_other_functions()
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
    in_game_info.infoexportgoods_command.choise_deal_and_execute_in_db(goods_name, deal_name)
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
    in_game_info.infoexportgoods_command.choise_deal_and_execute_in_db(goods_name, deal_name)
    await ctx.send(file=discord.File('logs_and_temp_files/info_export_import_goods.png'))


@infobot.command()
async def common_roll(ctx: discord.ext.commands.context.Context, user_roll: str = None):
    """
    :param ctx: ctx: discord.ext.commands.context.Context
    :param user_roll: строка ролла, например '3d6'
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    bot_answer = roll_mechanics.common_roll_module.roll_func_without_statistics(user_roll)
    await ctx.send(bot_answer)


@infobot.command()
async def roll(ctx: discord.ext.commands.context.Context, dice_roll_required: str, crit_modifier: str = 0):
    """
    Данная команда осуществляет обычный статистический ролл кубиков с дальнейшей записью в базу данных
    :param ctx: ctx: discord.ext.commands.context.Context
    :param dice_roll_required: указывает, какое минимальное число нужно для броска, так называемая сложность броска
    :param crit_modifier: указывает изменение диапазона критической удачи или неудачи(отрицательное значение - неудача,
                                                                                      положительное значение - удача)
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    user_id = ctx.message.author.id  # достаю id игрока в дискорде

    # создаю объект класса броска кубика
    roll_object = roll_mechanics.statistics_roll_module.DiceRollerWithStatistics(user_id,
                                                                                 dice_roll_required,
                                                                                 crit_modifier,
                                                                                 mega_roll=False,
                                                                                 is_luck_roll=False)
    # вызываю основной управляющий метод
    roll_object.control_roll_forming()

    # из сформированного объекта изымаю строку с ответом в чат
    bot_answer = roll_object.chat_answer
    await ctx.send(bot_answer)


@infobot.command()
async def mega_roll(ctx: discord.ext.commands.context.Context, dice_roll_required: str, crit_modifier: str = 0):
    """
    Данная команда осуществляет статистический ролл кубиков с дополнительным шансом на улучшение результата, с
    дальнейшей записью результатов в базу данных
    :param ctx: ctx: discord.ext.commands.context.Context
    :param dice_roll_required: указывает, какое минимальное число нужно для броска, так называемая сложность броска
    :param crit_modifier: указывает изменение диапазона критической удачи или неудачи(отрицательное значение - неудача,
                                                                                      положительное значение - удача)
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    user_id = ctx.message.author.id  # достаю id игрока в дискорде

    # создаю объект класса броска кубика. Отличие от базовой команды в параметре mega_roll который отправляется с True
    roll_object = roll_mechanics.statistics_roll_module.DiceRollerWithStatistics(user_id,
                                                                                 dice_roll_required,
                                                                                 crit_modifier,
                                                                                 mega_roll=True,
                                                                                 is_luck_roll=False)
    # вызываю основной управляющий метод
    roll_object.control_roll_forming()

    # из сформированного объекта изымаю строку с ответом в чат
    bot_answer = roll_object.chat_answer
    await ctx.send(bot_answer)


@infobot.command()
async def luck_roll(ctx: discord.ext.commands.context.Context, dice_roll_required: str, crit_modifier: str = 0):
    """
    Данная команда осуществляет статистический ролл кубиков с двойным броском кубиков и выбором лучшего результата,
    с дальнейшей записью лучшего результата в базу данных
    :param ctx: ctx: discord.ext.commands.context.Context
    :param dice_roll_required: указывает, какое минимальное число нужно для броска, так называемая сложность броска
    :param crit_modifier: указывает изменение диапазона критической удачи или неудачи(отрицательное значение - неудача,
                                                                                      положительное значение - удача)
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    user_id = ctx.message.author.id  # достаю id игрока в дискорде

    # создаю объект класса броска кубика. Отличие от базовой команды в параметре is_luck_roll который с флагом True
    roll_object = roll_mechanics.statistics_roll_module.DiceRollerWithStatistics(user_id,
                                                                                 dice_roll_required,
                                                                                 crit_modifier,
                                                                                 mega_roll=False,
                                                                                 is_luck_roll=True)
    # вызываю основной управляющий метод
    roll_object.control_roll_forming()

    # из сформированного объекта изымаю строку с ответом в чат
    bot_answer = roll_object.chat_answer
    await ctx.send(bot_answer)


@infobot.command()
async def display_avg_roll(ctx: discord.ext.commands.context.Context):
    plot_object = roll_mechanics.statistics_roll_module.MeanResultsByGamers()
    plot_object.control_plot_forming()
    await ctx.send(file=discord.File('logs_and_temp_files/mean_results_by_gamers.png'))


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
                   prefix: str = 'random',
                   suffix: str = 'random'
                   ):
    """
    Данная команда отвечает за формирование артефактов, она доступка только админу
    Полный список доступен либо при просмотре базы данных либо в __init__.py артефактного пакета artifacts
    @param ctx: объект класса контекст библиотеки discord
    @param grade: грейд артефакта(возможны зеленый, синий, фиолетовый, красный)
    @param group_art: группа артефактов
    @param type_art: тип артефактов
    @param prefix: префиксный модификатор
    @param suffix: суффиксный модификатор
    @return: отправка ботом в чат информации с параметрами и названием артефакта
    """
    # Словарь со значениями запрошенных параметров, обязательным является только грейд, остальное, по умолчанию, будет
    # выбираться случайно
    param_dict = {'грейд': grade.lower(),
                  'группа': group_art.lower(),
                  'тип': type_art.lower(),
                  'префикс': prefix.lower(),
                  'суффикс': suffix.lower()}

    bot_answer = artifacts.main_artifact_factory.choise_class_objects(param_dict)
    await ctx.send(bot_answer)


@infobot.command()
@commands.has_permissions(administrator=True)
async def consumable_loot(ctx: discord.ext.commands.context.Context,
                          loot_group: str = 'random',
                          loot_type: str = 'random'
                          ):
    """
    Данная команда отвечает за генерацию случайного расходуемого предмета с записью в статистику. Данная команда
    вызывается в случае, если запрос осуществляется полностью случайно. Можно вызывать и неслучайно, но тогда
    это может попортить статистику
    """
    # Словарь со значениями запрошенных параметров
    param_dict = {'группа расходника': loot_group.lower(), 'тип расходника': loot_type.lower()}

    bot_answer = special_loot.main_loot_factory.to_control_loot_forming(param_dict, 'consumables')

    await ctx.send(bot_answer)


@infobot.command()
@commands.has_permissions(administrator=True)
async def consumable_loot_no_stat(ctx: discord.ext.commands.context.Context,
                                  loot_group: str = 'random',
                                  loot_type: str = 'random',
                                  stat: bool = False
                                  ):
    """
    Данная команда отвечает за генерацию случайного расходуемого предмета без записи в статистику. Это функция
    используется в 2х случаях - когда нужно выдать неслучайную группу или тип предмета либо когда выполняются
    тестировочные запросы
    """
    # Словарь со значениями запрошенных параметров
    param_dict = {'группа расходника': loot_group.lower(), 'тип расходника': loot_type.lower(), 'no_stat': stat}

    bot_answer = special_loot.main_loot_factory.to_control_loot_forming(param_dict, 'consumables')

    await ctx.send(bot_answer)


@infobot.command()
async def consumable_all_groups(ctx: discord.ext.commands.context.Context):
    """
    Данная команда выводит весь список имеющихся групп расходников в чат дискорда
    """
    bot_answer = special_loot.main_loot_factory.display_items_groups_and_type('consumables', 'groups')

    await ctx.send(bot_answer)


@infobot.command()
async def consumable_all_types(ctx: discord.ext.commands.context.Context):
    """
    Данная команда выводит весь список всех имеющихся типов расходников в чат дискорда
    """
    bot_answer = special_loot.main_loot_factory.display_items_groups_and_type('consumables', 'types')

    await ctx.send(bot_answer)


@infobot.command()
async def goodspie(ctx: discord.ext.commands.context.Context):
    """
    Данная команда выводит полный список товаров, экспорта и импорта, в субсекторе согласно их количества на планетах,
    а также их базовые цены. Это более развернутая и подробный аналог команды !infoallgoods
    @param ctx: объект класса контекст библиотеки discord
    @return: отправка в чат картинки с двумя пироговыми диаграммами созданными библиотекой matplotlib
    """
    in_game_info.goodspie_command.to_control_other_functions()
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
    bot_answer = in_game_info.ingame_goods.to_control_other_functions_and_returns_bot_answer(good_name)
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
    chosen_news = in_game_news.bot_news_main.choise_random_news()
    # Новости записываются в лог
    logger.info('[in_game_news]' + chosen_news)
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
