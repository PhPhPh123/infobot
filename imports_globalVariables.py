"""
    В этом модуле собраны внешние импорты, настройки для бота и глобальные переменные. Остальные модули импортируют его
"""
import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

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
from typing import Optional, Union
from pprint import pprint
from abc import abstractmethod, ABC
from jinja2 import Template
from discord.ext import commands, tasks
from sqlalchemy.orm import mapper, sessionmaker
from dotenv import load_dotenv, find_dotenv
from loguru import logger
from datetime import date

from bot_statistics import count_news_statistics


def get_bot_dir() -> str:
    """
    Функция собирающая абсолютный путь к текущей директории
    :return: возвращает этот путь
    """
    abs_path = os.path.abspath(__file__)  # полный путь к файлу скрипта
    return os.path.dirname(abs_path)


def connect_to_main_db() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """
    Функция, которая подключается к базе данных и создает объекты курсора и коннекта, абсолютный путь берет из файла
    настроек
    :return: объекты курсора и коннекта
    """
    db_name = 'infobot_db.db'
    abspath = get_bot_dir() + os.path.sep + db_name  # Формирование вабсолютного пути для файла базы данных
    connect = sqlite3.connect(abspath)  # Подключение к базе данных
    cursor = connect.cursor()  # Создание курсора
    return cursor, connect


def connect_to_unique_news_db() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """
    Функция, которая подключается к второстепенной базе данных unique_news.db, хранящей уникальные новости
    :return: объекты курсора и коннекта
    """
    db_name = 'separatly_started_modules\\unique_news\\unique_news.db'
    abspath = get_bot_dir() + os.path.sep + db_name   # Формирование вабсолютного пути для файла базы данных
    connect = sqlite3.connect(abspath)  # Подключение к базе данных
    cursor = connect.cursor()  # Создание курсора
    return cursor, connect


"""
Глобальное подключение логирования
"""
# логгер для новостей
logger.add('logs_and_temp_files/news.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[news]' in x['message'])
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
global_bd_sqlite3_cursor, global_bd_sqlite3_connect = connect_to_main_db()

# Объекты курсора и коннекта для доступа во второстепенную базу уникальных новостей
# База динамически формируется при первом запуске модуля unique_news_main поэтому может не существовать. В данном
# случае создание объектов курсора и соединения пропускаются, структуры, работающие с данными глобальными переменными
# работают через try\except
if os.path.exists(get_bot_dir() + os.path.sep + 'separatly_started_modules\\unique_news\\unique_news.db'):
    global_unique_news_cursor, global_unique_news_connect = connect_to_unique_news_db()
else:
    pass

# Объект замыкания для хранения статистики по новостям и выводу ее при завершении сессии новостей
# хранит значения в течении всей сессии бота вплоть до его отключения
global_news_statistics = count_news_statistics()


