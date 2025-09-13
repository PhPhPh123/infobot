import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from bot_settings import *

import artifacts.main_artifact_factory


@infobot.command()
@commands.has_permissions(administrator=True)
async def artifact(ctx: discord.ext.commands.context.Context,
                   grade: str,
                   group_art: str = 'random',
                   type_art: str = 'random',
                   prefix: str = 'random',
                   suffix: str = 'random',
                   wh_flag: bool = False
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
                  'суффикс': suffix.lower(),
                  "game_mode": 'whfb'
                  }

    bot_answer = artifacts.main_artifact_factory.choise_class_objects(param_dict)
    await ctx.send(bot_answer)


def is_admin_or_allowed_user():
    async def predicate(ctx: commands.Context) -> bool:
        # Проверяем, есть ли у автора право администратора
        is_admin = ctx.author.guild_permissions.administrator
        # Проверяем, есть ли ID автора в нашем списке разрешенных
        is_allowed = ctx.author.id in [187268400647634945]

        # Команда будет выполнена, если хотя бы одно из условий истинно
        return is_admin or is_allowed

    return commands.check(predicate)

@infobot.command()
@is_admin_or_allowed_user()
async def artifactfb(ctx: discord.ext.commands.context.Context,
                   grade: str,
                   group_art: str = 'random',
                   type_art: str = 'random',
                   prefix: str = 'random',
                   suffix: str = 'random'):
    """
    Данная команда отвечает за формирование артефактов для WH ролок, она доступка только админу и PotatoSpy
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
                  'суффикс': suffix.lower(),
                  "game_mode": 'whfb'}

    bot_answer = artifacts.main_artifact_factory.choise_class_objects(param_dict)
    await ctx.send(bot_answer)