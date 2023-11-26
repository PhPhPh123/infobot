import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from bot_settings import *


import economic_info.infoworld_command
import economic_info.infosystem_command
import economic_info.info_access_command
import economic_info.import_and_export_commands
import economic_info.infoexportgoods_command
import economic_info.goodspie_command
import economic_info.info_all_goods
import economic_info.ingame_goods
from commands import static_answer_messages
import economic_news.bot_news_main
import economic_news.unique_news


@infobot.command()
async def infoworld(ctx: discord.ext.commands.context.Context, world_name: str):
    """
    Функция, выдающая ответ по характеристикам запрашиваемого мира на основании запроса в базу данных
    :param ctx: объект класса контекст библиотеки discord
    :param world_name: название запрашиваемого мира
    :return: строка, полученная путем выполнения нижестоящих функций и даюткоманду боту на вывод текста в чате дискорда
    """
    bot_answer, world_url = economic_info.infoworld_command.to_control_other_functions_and_returns_bot_answer(world_name)
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
    bot_answer, world_url = economic_info.infoworld_command.to_control_other_functions_and_returns_bot_answer(world_name,
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
    bot_answer = economic_info.infosystem_command.to_control_other_functions_and_returns_bot_answer(system_name)
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
    bot_answer = economic_info.import_and_export_commands.choice_deal_and_returns_bot_answer(world_name, deal_name)
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
    bot_answer = economic_info.import_and_export_commands.choice_deal_and_returns_bot_answer(world_name, deal_name)
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
        bot_answer_list = economic_info.info_access_command.form_tuple_in_db()
        # строка ответа может быть больше 2000 знаков, поэтому ответ размещается в списке и выводится по частям
        for message in bot_answer_list:
            await ctx.send(message)

    elif type_of_output == 'excel':
        # если запрос является экселем, то вызывается фасад с аргументом экселя
        economic_info.info_access_command.form_tuple_in_db(excel_answer=True)
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
    bot_answer = economic_info.info_all_goods.to_control_other_functions()
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
    economic_info.infoexportgoods_command.choise_deal_and_execute_in_db(goods_name, deal_name)
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
    economic_info.infoexportgoods_command.choise_deal_and_execute_in_db(goods_name, deal_name)
    await ctx.send(file=discord.File('logs_and_temp_files/info_export_import_goods.png'))


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


@tasks.loop(minutes=30)
async def news_send(channel: discord.channel.TextChannel):
    """
    Функция отправляющая с определенной переодичностью(доп.параметр декоратора tasks.loop) сообщения рандомно
    выбранные из списка в нижестоящей функции bot_news_controller. За запуск данного цикла отвечает функция startnews
    :param channel: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    chosen_news = economic_news.bot_news_main.choise_random_news()
    # Новости записываются в лог
    logger.info('[economic_news]' + chosen_news)
    await channel.send(chosen_news)


@infobot.command()
async def goodspie(ctx: discord.ext.commands.context.Context):
    """
    Данная команда выводит полный список товаров, экспорта и импорта, в субсекторе согласно их количества на планетах,
    а также их базовые цены. Это более развернутая и подробный аналог команды !infoallgoods
    @param ctx: объект класса контекст библиотеки discord
    @return: отправка в чат картинки с двумя пироговыми диаграммами созданными библиотекой matplotlib
    """
    economic_info.goodspie_command.to_control_other_functions()
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
    bot_answer = economic_info.ingame_goods.to_control_other_functions_and_returns_bot_answer(good_name)
    await ctx.send(bot_answer)
