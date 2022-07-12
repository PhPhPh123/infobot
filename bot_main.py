from user_info.bot_user_info_main import *
from user_info.bot_user_info_systems import *
from user_info.bot_import_and_export import *
from user_info.bot_user_access import *

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
!infoworld *название системы* - вызывает инфу по конкретному миру согласно имеющемуся уровню доступа

!infosystem *название системы* - показывает количество имеющихся миров внутри системы

!infoexport *название системы* - показывает какие экспортные товары производятся в системе и их приблизительная цена

!infoimport *название системы* - показывается какие импортные товары покупают в системе и по какой примерно цене

!infoaccess - показывает уровень доступа на всех известных мирах, где уровень выше 0

!access - показывает информацию по уровням доступа для миров
        
Название систем можно посмотреть на сайте - на карте
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


@infobot.command()
async def infoexport(ctx, world_name):
    deal_name = 'export'
    bot_answer = bot_user_info_controller_trade(world_name, deal_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infoimport(ctx, world_name):
    deal_name = 'import'
    bot_answer = bot_user_info_controller_trade(world_name, deal_name)
    await ctx.send(bot_answer)


@infobot.command()
async def infoaccess(ctx):
    bot_answer = bot_user_info_controller_access()
    await ctx.send(bot_answer)


if __name__ == '__main__':
    infobot.run(settings['token'])
