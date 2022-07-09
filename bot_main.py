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


@infobot.command()
async def helpme(ctx):
    bot_answer = '''
    Команды:
        !infoworld - вызывает инфу по конкретному миру согласно имеющемуся уровню доступа
        !infosystem - показывает количество имеющихся миров внутри системы
        !access - показывает информацию по уровням доступа для миров
        '''
    await ctx.send(bot_answer)


@infobot.command()
async def access(ctx):
    bot_answer = '''
    Нулевой уровень: недоступно ничего, мир скрыт для запросов полностью
    Первый уровень доступно: название системы, имперский класс, общий уровень опасности
    Второй уровень доступно: уровень имперской власти, население, угроза отдельных врагов, основные типы местности
    Третий уровень доступно: экспорт, импорт и дополнительные особенности мира'''
    await ctx.send(bot_answer)


if __name__ == '__main__':
    infobot.run(settings['token'])
