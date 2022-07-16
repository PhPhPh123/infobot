import sqlite3
import discord
import tkinter
import random
import os

from jinja2 import Template
from discord.ext import commands, tasks
from dotenv import load_dotenv, find_dotenv
from os import path


def get_script_dir() -> str:
    """
    Функция собирающая абсолютный путь к текущей директории
    :return: возвращает этот путь
    """
    abs_path = path.abspath(__file__)  # полный путь к файлу скрипта
    return path.dirname(abs_path)


'''
Settings
'''
load_dotenv(find_dotenv())
token = os.environ['TOKEN']
settings = {
    'token': token,
    'bot': 'Infobot_wh40k',
    'id': 992438215254487143,
    'prefix': '!'
}
