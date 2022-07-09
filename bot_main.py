from settings_and_imports import *
from bot_user_info import *

infobot = commands.Bot(command_prefix=settings['prefix'])


@infobot.command()
async def infoworld(ctx, world_name):
    bot_answer = bot_user_info_controller(world_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infosystem(ctx, world_name):
    bot_answer = bot_user_info_controller(world_name)
    await ctx.send(bot_answer)


if __name__ == '__main__':
    infobot.run(settings['token'])
