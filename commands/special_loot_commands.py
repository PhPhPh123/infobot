import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from bot_settings import *

import special_loot.main_loot_factory
import statistics_output.consumables_statistics.consumables_plots


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
async def display_consumables(ctx: discord.ext.commands.context.Context, group_or_type):
    """
    """

    plot_object = statistics_output.consumables_statistics.consumables_plots.ConsumablesPlotsFormer(group_or_type)
    plot_object.control_plot_forming()  # выполняю основной формирующий метод после который создаст картинку графика

    if not plot_object.is_error:  # если ошибки нет, то в чат загружается картинка
        await ctx.send(file=discord.File('logs_and_temp_files/consumables_plot.png'))
    else:  # иначе в чат выводится сообщение с ошибкой
        await ctx.send(plot_object.error_message)
