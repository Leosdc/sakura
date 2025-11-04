"""
Funções de validação
"""

import re
from datetime import timedelta
from config import MAX_PURGE_MESSAGES, MAX_TIMEOUT_DAYS, CANAIS_PERMITIDOS


def validar_quantidade_apagar(quantidade):
    """
    Valida a quantidade de mensagens a apagar

    Args:
        quantidade: Número de mensagens

    Returns:
        Tuple (valido: bool, mensagem_erro: str ou None)
    """
    if quantidade < 1 or quantidade > MAX_PURGE_MESSAGES:
        return False, f"Quantidade deve ser entre 1 e {MAX_PURGE_MESSAGES}."
    return True, None


def validar_tempo_castigo(tempo_str):
    """
    Valida e converte string de tempo para timedelta

    Args:
        tempo_str: String no formato "5m", "2h", "1d", etc

    Returns:
        Tuple (valido: bool, resultado: timedelta ou str com erro)
    """
    tempo_match = re.match(r"(\d+)([smhd])", tempo_str.lower())

    if not tempo_match:
        return False, "Formato inválido. Use: s, m, h, d"

    valor, unidade = tempo_match.groups()
    valor = int(valor)

    # Converte para timedelta
    if unidade == "s":
        duracao = timedelta(seconds=valor)
    elif unidade == "m":
        duracao = timedelta(minutes=valor)
    elif unidade == "h":
        duracao = timedelta(hours=valor)
    elif unidade == "d":
        duracao = timedelta(days=valor)

    # Valida máximo (28 dias)
    max_seconds = MAX_TIMEOUT_DAYS * 24 * 60 * 60
    if duracao.total_seconds() > max_seconds:
        return False, f"Máximo: {MAX_TIMEOUT_DAYS} dias."

    return True, duracao


def validar_permissao_moderacao(member):
    """
    Valida se o membro tem permissão de moderação

    Args:
        member: Objeto discord.Member

    Returns:
        bool: True se tem permissão, False caso contrário
    """
    return member.guild_permissions.moderate_members


def validar_permissao_mensagens(member):
    """
    Valida se o membro tem permissão de gerenciar mensagens

    Args:
        member: Objeto discord.Member

    Returns:
        bool: True se tem permissão, False caso contrário
    """
    return member.guild_permissions.manage_messages


def validar_canal_permitido(channel):
    """
    Valida se o canal está na lista de canais permitidos

    Args:
        channel: Objeto discord.Channel

    Returns:
        bool: True se o canal é permitido, False caso contrário
    """
    return channel.name in CANAIS_PERMITIDOS
