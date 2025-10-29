"""
Inicialização e configuração do bot Discord
"""

import discord
from discord.ext import commands
from config import BOT_PREFIX

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

# Controle de voz automática (ligado por padrão)
voz_automatica_ativa = True


def get_voz_automatica():
    """Retorna o estado da voz automática"""
    return voz_automatica_ativa


def toggle_voz_automatica():
    """Alterna o estado da voz automática"""
    global voz_automatica_ativa
    voz_automatica_ativa = not voz_automatica_ativa
    return voz_automatica_ativa


def get_bot():
    """Retorna a instância do bot"""
    return bot
