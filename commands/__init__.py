"""
Módulo de comandos do bot Sakura

Este módulo importa todos os comandos para registrá-los no bot.
Basta importar este módulo para que todos os comandos sejam carregados.
"""

# Importa todos os módulos de comandos para registrar os decoradores @bot.command
from . import ai_commands
from . import personality_commands
from . import voice_commands
from . import moderation_commands
from . import utility_commands

__all__ = [
    "ai_commands",
    "personality_commands",
    "voice_commands",
    "moderation_commands",
    "utility_commands",
]
