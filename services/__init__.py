"""
Módulo de serviços externos do bot Sakura
"""

from .groq_service import gerar_resposta, get_client as get_groq_client

from .elevenlabs_service import (
    gerar_audio,
    limpar_texto_para_voz,
    get_client as get_elevenlabs_client,
)

__all__ = [
    "gerar_resposta",
    "get_groq_client",
    "gerar_audio",
    "limpar_texto_para_voz",
    "get_elevenlabs_client",
]
