from settings_and_imports import *
from bot_user_info_main import *
from bot_user_info_systems import *

infobot = commands.Bot(command_prefix=settings['prefix'])


@infobot.command()
async def infoworld(ctx, world_name):
    bot_answer = bot_user_info_controller_worlds(world_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infosystem(ctx, system_name):
    bot_answer = bot_user_info_controller_systems(system_name)
    await ctx.send(bot_answer)


if __name__ == '__main__':
    infobot.run(settings['token'])
