import exceptions

if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from bot_settings import *

from commands import static_answer_messages


@infobot.command()
async def helpme(ctx: discord.ext.commands.context.Context, commands_group='all'):
    """
    Функция, отправляющая ботом в дискорде информацию по доступным игрокам командам,
    строку для вывода берет из модуля static_messages
    :param ctx: объект класса контекст библиотеки discord
    :param commands_group: конкретная группа команда для вывода
    :return: отправка строки боту для вывода в текущем чате дискорда
    """
    message_dict = {'eco': static_answer_messages.economic_commands,
                    'roll': static_answer_messages.roll_commands,
                    'items': static_answer_messages.art_and_special_items_commands,
                    'session': static_answer_messages.game_session_commands}

    if commands_group == 'all':  # по умолчанию выводит список всех групп команд
        for message in message_dict.items():
            await ctx.send(message[1])
    elif commands_group in message_dict.keys():  # если группа команд корректная и есть в ключах, то выводится она
        await ctx.send(message_dict[commands_group])
    else:  # иначе выводится сообщение об ошибке
        await ctx.send('Неверная группа команд')


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


