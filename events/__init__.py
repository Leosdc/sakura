"""
Módulo de eventos do bot Sakura

Este módulo importa todos os event handlers para registrá-los no bot.
Basta importar este módulo para que todos os eventos sejam carregados.
"""

# Importa o módulo de message_handler para registrar os decoradores @bot.event
from . import message_handler

__all__ = ["message_handler"]
