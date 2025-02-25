"""
    Данный модуль хранит в себе основные настройки для бота, необходимые для его запуска и работы
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException
from imports_globalVariables import *


'''
Настройки бота и загрузка токена для него при старте модуля. Всё должно быть в глобальных переменных
'''
load_dotenv(find_dotenv())  # загрузка переменных окружения из файла ..env с токеном, именем и id бота
token = os.environ['TOKEN']  # токен для доступа к боту
bot_name = os.environ['NAME']  # имя бота в discord
bot_id = os.environ['ID']  # id бота в discord
settings = {
    'token': token,
    'bot': bot_name,
    'id': bot_id,
    'prefix': '!'  # команды бота стартуют с данного префикса
}

# установка полномочий бота
intents = discord.Intents.all()
intents.members = True

infobot = commands.Bot(command_prefix=settings['prefix'], intents=intents)  # Экземпляр класса бота

logger.info('[bot_run]')  # запись в лог старт сессии

