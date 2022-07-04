import jinja2
import sqlite3
import discord
import tkinter
import random
from discord.ext import commands

'''
Settings
'''
settings = {
    'token': 'OTkyNDM4MjE1MjU0NDg3MTQz.Gzbd3D.bwujHkk9thKD_CooZ3304pZhNFSNh7HNsRjn5Q',
    'bot': 'Infobot_wh40k',
    'id': 992438215254487143,
    'prefix': '!'
}

infobot = commands.Bot(command_prefix=settings['prefix'])


@infobot.command()
async def info(ctx, world_name):
    await ctx.send('123')


if __name__ == '__main__':
    infobot.run(settings['token'])
