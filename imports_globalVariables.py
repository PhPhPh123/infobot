"""
    В этом модуле собраны внешние импорты, подключение к базам данных, подключение логирования и глобальные
    межмодульные переменные. Остальные модули импортируют его
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

# внешние импорты
import sqlite3
import sqlalchemy
import discord
import pandas as pd
import numpy
import random
import os
import discord.ext.commands.context
import openpyxl
import re
import matplotlib.pyplot as plt
import seaborn as sns
import string
from typing import Optional, Union
from pprint import pprint
from abc import abstractmethod, ABC
from jinja2 import Template
from discord.ext import commands, tasks
from sqlalchemy.orm import mapper, sessionmaker
from dotenv import load_dotenv, find_dotenv
from datetime import date
from time import time, strftime, localtime
from loguru import logger


from statistics_output.news_session_stats import count_news_statistics  # импорт модуля статистики сессий
from db_connects import *  # импорт функций подключений к базам данных


"""
Глобальное подключение логирования
"""
# логгер для новостей
logger.add('logs_and_temp_files/news.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[economic_news]' in x['message'])
# логгер для принтов
logger.add('logs_and_temp_files/print.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[print]' in x['message'])
# логгер для статистики запусков сессии бота
logger.add('logs_and_temp_files/sessions.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[bot_run]' in x['message'])
# логгер для вызываемых артефактов
logger.add('logs_and_temp_files/artifacts.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[artifact]' in x['message'])
# логгер для артефактов, генерируемых квестами
logger.add('logs_and_temp_files/quest_artifacts.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[artifact_for_quest]' in x['message'])
# логгер для описания квестов
logger.add('logs_and_temp_files/quests_description.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[quest]' in x['message'])


"""
Глобальные межмодульные переменные
"""
# Объекты курсора и коннекта для доступа в основную базу данных
global_main_db_cursor, global_main_db_connect = connect_sqlite(db_path='infobot_db.db')

# Объекты курсора и коннекта для доступа во второстепенную базу уникальных новостей
# База динамически формируется при первом запуске модуля unique_news_main поэтому может не существовать. В данном
# случае создание объектов курсора и соединения пропускаются, структуры, работающие с данными глобальными переменными
# работают через try\except
if os.path.exists(get_bot_dir() + os.path.sep + 'separatly_started_modules\\unique_news\\unique_news.db'):
    global_unique_news_cursor, global_unique_news_connect = connect_sqlite('separatly_started_modules\\unique_news\\unique_news.db')
else:
    pass

# Объекты курсора и коннекта для доступа в базу данных лута
global_artifacts_cursor, global_artifacts_connect = connect_sqlite('artifacts\\artifacts.db')

# Объекты курсора и коннекта для доступа в базу данных лута
global_consumables_loot_cursor, global_consumables_loot_connect = connect_sqlite('special_loot\\consumables_loot_db',
                                                                                 row_factory=True)

# Объекты курсора и коннекта для доступа в базу данных статистики по луту
global_consumables_statistics_cursor, global_consumables_statistics_connect = connect_sqlite('special_loot\\consumables_statistics_db',
                                                                                             row_factory=True)

# Объекты курсора и коннекта для доступа в базу данных статистики по броскам кубика
global_dice_roll_statistics_cursor, global_dice_roll_statistics_connect = connect_sqlite('roll_mechanics\\roll_stat_db',
                                                                                         row_factory=True)

# Объекты курсора и коннекта для доступа в базу данных статистики по проведенным игровым сессиям
global_game_sessions_cursor, global_game_sessions_connect = connect_sqlite('other_mechanics\\game_sessions\\game_sessions_db',
                                                                           row_factory=True)

# Объект замыкания для хранения статистики по новостям и выводу ее при завершении сессии новостей
# хранит значения в течении всей сессии бота вплоть до его отключения
global_news_statistics = count_news_statistics()
