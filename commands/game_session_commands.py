import exceptions

if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from bot_settings import *

from other_mechanics.game_sessions import game_sessions
from statistics_output import game_sessions_plots


@infobot.command()
@commands.has_permissions(administrator=True)
async def start_game_session(ctx: discord.ext.commands.context.Context, game_hours):
    """
    Данный метод записывает в базу данных игровых сессий текущую дату и количество игровых часов
    :param ctx: стандартный параметр контекста библиотеки discord
    :param game_hours: параметр, содержащий целое число количества игровых часов, в которые будет проводится текущая
    игровая сессия
    """

    # Если команда запрошена неверно, то в переменной будет строка с ошибкой, иначе там будет None
    if_error_message = game_sessions.control_writing(game_hours)

    if if_error_message:  # печатаю в чат сообщение об ошибке
        await ctx.send(if_error_message)
    else:  # иначе пишу в чат, что все прошло успешно и сессия записалась в базу данных
        await ctx.send('Сессия записана')


@infobot.command()
async def display_sessions_stat(ctx: discord.ext.commands.context.Context, week_or_month: str = 'month'):
    """
    Данная команда отвечает за вывод в чат линейного графика по сумме часов проведенных игровых сессий в разрезе
    месяцев или недель
    :param ctx: стандартный параметр контекста библиотеки discord
    :param week_or_month: параметр, который должен обязательно содержать строку month или week. Отвечает за временной
    диапазон, в разрезе которого будут агреггироваться игровые часы
    """
    plot_object = game_sessions_plots.SessionHoursPlotFormer(week_or_month)
    plot_object.control_plot_forming()

    if not plot_object.is_error:  # если ошибок в команде нет, то загружается картинка графика
        await ctx.send(file=discord.File('logs_and_temp_files/game_sessions_plot.png'))
    else:  # иначе выводится в чат сообщение об ошибки
        await ctx.send(plot_object.error_message)


@infobot.command()
@commands.has_permissions(administrator=True)
async def start_new_game(ctx: discord.ext.commands.context.Context):
    """
    """
    pass
