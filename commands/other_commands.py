import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from bot_settings import *

from commands import static_answer_messages


@infobot.command()
async def helpme(ctx: discord.ext.commands.context.Context):
    """
    Функция, отправляющая ботом в дискорде информацию по доступным игрокам командам,
    строку для вывода берет из модуля static_messages
    :param ctx: объект класса контекст библиотеки discord
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    message_list = [static_answer_messages.economic_commands,
                    static_answer_messages.roll_commands,
                    static_answer_messages.art_and_special_items_commands]

    for message in message_list:
        await ctx.send(message)


@infobot.event
async def on_command_error(ctx: discord.ext.commands.context.Context, error):
    """
    Данное событие выводит в чат сообщение, если команды не существует либо она введена неправильно
    @param ctx: объект класса контекст библиотеки discord
    @param error: объект исключения библиотеки discord
    @return: отправка в чат сообщения о неверной команде
    """
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("Неверная команда")
