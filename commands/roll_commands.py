import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from bot_settings import *

import roll_mechanics.common_roll_module
import roll_mechanics.statistics_roll_module
import statistics_output.dice_statistics.general_plots


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
                                                                                 is_common_roll=True,
                                                                                 is_mega_roll=False,
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
                                                                                 is_common_roll=False,
                                                                                 is_mega_roll=True,
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
                                                                                 is_common_roll=False,
                                                                                 is_mega_roll=False,
                                                                                 is_luck_roll=True)
    # вызываю основной управляющий метод
    roll_object.control_roll_forming()

    # из сформированного объекта изымаю строку с ответом в чат
    bot_answer = roll_object.chat_answer
    await ctx.send(bot_answer)


@infobot.command()
async def display_avg_rolls(ctx: discord.ext.commands.context.Context):
    """
    Данная команда выводит в чат график со средними значениями брошенных кубиков по всем игрокам
    """
    plot_object = statistics_output.dice_statistics.general_plots.AvgRollsPlotFormer()  # создаю экземпляр класса
    plot_object.control_plot_forming()  # выполняю основной формирующий метод после который создаст картинку графика
    await ctx.send(file=discord.File('logs_and_temp_files/mean_results_by_gamers.png'))  # загружаю ее в чат


@infobot.command()
async def display_all_rolls(ctx: discord.ext.commands.context.Context, user_name=''):
    """
    Данная команда выводит в чат график по всем броскам либо сразу всех игроков, либо конкретного, если после ее
    вызова указан его зарегистрированный ник. Если ник неправильный, то будет выведена текстовая шибка
    """
    # создаю экземпляр класса
    plot_object = statistics_output.dice_statistics.general_plots.AllRollsPlotFormer(user_name=user_name)
    plot_object.control_plot_forming()  # выполняю основной формирующий метод после который создаст картинку графика

    if not plot_object.is_error:  # если ошибки нет, то в чат загружается картинка
        await ctx.send(file=discord.File('logs_and_temp_files/all_results_by_gamers.png'))
    else:  # иначе в чат выводится сообщение с ошибкой
        await ctx.send(plot_object.error_message)