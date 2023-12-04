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
    """
    if_error_message = game_sessions.control_writing(game_hours)

    if if_error_message:
        await ctx.send(if_error_message)
    else:
        pass


@infobot.command()
async def display_sessions_stat(ctx: discord.ext.commands.context.Context, week_or_month):
    """
    """
    plot_object = game_sessions_plots.AvgSessionDuration(week_or_month)
    plot_object.control_plot_forming()

    await ctx.send(file=discord.File('logs_and_temp_files/game_sessions_plot.png'))


@infobot.command()
@commands.has_permissions(administrator=True)
async def start_new_game(ctx: discord.ext.commands.context.Context):
    """
    """
    pass

