"""
Módulo core do bot Sakura
"""

from .bot import bot, get_bot, get_voz_automatica, toggle_voz_automatica

from .conversation import (
    inicializar_historico,
    atualizar_personalidade_historico,
    adicionar_mensagem_usuario,
    adicionar_mensagem_assistente,
    obter_historico,
    limpar_historico,
    get_personalidade_atual,
    set_personalidade,
    get_mensagem,
)

__all__ = [
    "bot",
    "get_bot",
    "get_voz_automatica",
    "toggle_voz_automatica",
    "inicializar_historico",
    "atualizar_personalidade_historico",
    "adicionar_mensagem_usuario",
    "adicionar_mensagem_assistente",
    "obter_historico",
    "limpar_historico",
    "get_personalidade_atual",
    "set_personalidade",
    "get_mensagem",
]
