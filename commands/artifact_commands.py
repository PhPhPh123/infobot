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
                   suffix: str = 'random'
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
                  'суффикс': suffix.lower()}

    bot_answer = artifacts.main_artifact_factory.choise_class_objects(param_dict)
    await ctx.send(bot_answer)
