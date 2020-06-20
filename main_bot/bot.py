import discord
import os
import sys
from discord.ext import commands

# Adiciona em 'sys.path' o diretório da pasta 'discord-bot-py' para não dar erro de
# exportação de módulo em cogs/events --> 'from main_bot.cogs.tasks import Tasks'
import re
path = re.match(r"(?P<path>.+)\\", sys.path[0])
sys.path.append(f"{path['path']}")
# ---------------------------------------------------

import logging
logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



# Importa as configurações
import settings

bot_token = settings.bot_token()
prefix = settings.prefix()

client = commands.Bot(command_prefix=prefix)

cogs_PATH = f'{sys.path[0]}\cogs'

def permsVerify(context):
    if context.message.author.id == context.guild.owner.id:
        return True
    else:
        context.send("Você não tem permissão para usar essa comando.")
        return False


@client.command()
async def load(ctx, extension):
    if permsVerify(ctx):
        await ctx.send(f'Ativando o arquivo "{extension}.py".')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Ativado o arquivo "{extension}.py".')


@client.command()
async def unload(ctx, extension):
    if permsVerify(ctx):
        await ctx.send(f'Desativando o arquivo "{extension}.py".')
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Desativado o arquivo "{extension}.py".')


@client.command()
async def reload(ctx, extension):
    if permsVerify(ctx):
        await ctx.send(f'Recarregando o arquivo "{extension}.py".')
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Recarregado o arquivo "{extension}.py".')


@client.command()
async def reload_all(ctx):
    if permsVerify(ctx):
        await ctx.send(f'Recarregando todos os arquivos.')

        for filename_unload in os.listdir(cogs_PATH):
            if filename_unload.endswith('.py'):
                client.unload_extension(f'cogs.{filename_unload[:-3]}')

        for filename_load in os.listdir(cogs_PATH):
            if filename_load.endswith('.py'):
                client.load_extension(f'cogs.{filename_load[:-3]}')

        await ctx.send(f'Todos os módulos foram recarregados.')

for filename in os.listdir(cogs_PATH):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# The token is necessary to connect the client with the API
# on discord and use the bot.

client.run(bot_token)
