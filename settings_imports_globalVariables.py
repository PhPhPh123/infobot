"""
    В этом модуле собраны внешние импорты, настройки для бота и глобальные переменные. Остальные модули импортируют его
"""
import sqlite3
import sqlalchemy
import discord
import tkinter
import random
import os
import discord.ext.commands.context

from typing import Optional
from pprint import pprint
from abc import abstractmethod, ABC
from jinja2 import Template
from discord.ext import commands, tasks
from sqlalchemy.orm import mapper, sessionmaker
from dotenv import load_dotenv, find_dotenv
import matplotlib.pyplot as plt


def get_script_dir() -> str:
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
    abspath = get_script_dir() + os.path.sep + db_name  # Формирование вабсолютного пути для файла базы данных
    connect = sqlite3.connect(abspath)  # Подключение к базе данных
    cursor = connect.cursor()  # Создание курсора
    return cursor, connect


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
Глобальные межмодульные переменные
"""
bd_sqlite3_cursor, bd_sqlite3_connect = connect_to_db_sqlite3()  # Объекты курсора и коннекта для доступа в базу данных
