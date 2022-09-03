"""
    В этом модуле собраны внешние импорты и настройки для бота. Остальные модули импортируют его
"""
import sqlite3
import sqlalchemy
import discord
import tkinter
import random
import os
import discord.ext.commands.context

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


'''
Загрузка токена из переменной окружения и параметры бота
'''
load_dotenv(find_dotenv())
token = os.environ['TOKEN']
settings = {
    'token': token,
    'bot': 'Infobot_wh40k',
    'id': 992438215254487143,
    'prefix': '!'
}
