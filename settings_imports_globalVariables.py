"""
    В этом модуле собраны внешние импорты, настройки для бота и глобальные переменные. Остальные модули импортируют его
"""
import sqlite3
import sqlalchemy
import discord
import tkinter
import pandas as pd
import random
import os
import discord.ext.commands.context
import openpyxl
import re
import matplotlib.pyplot as plt
from typing import Optional
from pprint import pprint
from abc import abstractmethod, ABC
from jinja2 import Template
from discord.ext import commands, tasks
from sqlalchemy.orm import mapper, sessionmaker
from dotenv import load_dotenv, find_dotenv
from loguru import logger
from datetime import date

from statistics import count_news_statistics


def get_bot_dir() -> str:
    """
    Функция собирающая абсолютный путь к текущей директории
    :return: возвращает этот путь
    """
    abs_path = os.path.abspath(__file__)  # полный путь к файлу скрипта
    return os.path.dirname(abs_path)


def connect_to_db_sqlite3() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
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


def connect_to_db_sqlalchemy():
    """
    Данный модуль подключается к orm sqlalchemy
    :return: объекты коннектора и таблички worlds
    """
    db_engine = sqlalchemy.create_engine('sqlite:///infobot_db.db')
    db_connector = db_engine.connect()

    metadata = sqlalchemy.MetaData(db_engine)
    worlds = sqlalchemy.Table('worlds', metadata, autoload=True)
    systems = sqlalchemy.Table('systems', metadata, autoload=True)

    return db_connector, worlds, systems


'''
Настройки бота и загрузка токена для него
'''
load_dotenv(find_dotenv())
token = os.environ['TOKEN']
settings = {
    'token': token,
    'bot': 'Infobot_wh40k',
    'id': 992438215254487143,
    'prefix': '!'
}

"""
Подключение логирования
"""
logger.add('logs_and_temp_files/news.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[news]' in x['message'])

logger.add('logs_and_temp_files/print.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[print]' in x['message'])

logger.add('logs_and_temp_files/sessions.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[bot_run]' in x['message'])

logger.add('logs_and_temp_files/artifacts.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[artifact]' in x['message'])

logger.add('logs_and_temp_files/quest_artifacts.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[artifact_for_quest]' in x['message'])

logger.add('logs_and_temp_files/quests_description.log', format='{time}, {level}, {message}', level='DEBUG', backtrace=True,
           filter=lambda x: '[quest]' in x['message'])

"""
Глобальные межмодульные переменные
"""
alch_connect, alch_world, alch_systems = connect_to_db_sqlalchemy()  # Объекты sql-alchemy

bd_sqlite3_cursor, bd_sqlite3_connect = connect_to_db_sqlite3()  # Объекты курсора и коннекта для доступа в базу данных

news_statistics = count_news_statistics()
