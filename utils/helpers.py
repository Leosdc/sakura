"""
Funções auxiliares gerais
"""

from config import MESSAGE_SPLIT_LENGTH


def dividir_mensagem_longa(texto, limite=MESSAGE_SPLIT_LENGTH):
    """
    Divide uma mensagem longa em chunks menores

    Args:
        texto: Texto a ser dividido
        limite: Tamanho máximo de cada chunk

    Returns:
        Lista de strings (chunks)
    """
    if len(texto) <= limite:
        return [texto]

    chunks = []
    for i in range(0, len(texto), limite):
        chunks.append(texto[i : i + limite])

    return chunks


def deve_responder_automaticamente(mensagem_content, chance=None):
    """
    Determina se o bot deve responder automaticamente a uma mensagem

    Args:
        mensagem_content: Conteúdo da mensagem
        chance: Probabilidade de responder (0.0 a 1.0), usa padrão se None

    Returns:
        Tuple (deve_responder: bool, sakura_mencionada: bool)
    """
    import random
    from config import AUTO_RESPONSE_CHANCE, MIN_MESSAGE_LENGTH

    # Verifica se "Sakura" foi mencionada (case insensitive)
    sakura_mencionada = "sakura" in mensagem_content.lower()

    # Se Sakura foi mencionada, SEMPRE responde
    if sakura_mencionada:
        return True, sakura_mencionada

    # Ignora mensagens muito curtas
    if len(mensagem_content) < MIN_MESSAGE_LENGTH:
        return False, sakura_mencionada

    # Chance aleatória de responder
    chance_usada = chance if chance is not None else AUTO_RESPONSE_CHANCE
    deve_responder = random.random() <= chance_usada

    return deve_responder, sakura_mencionada


def verificar_protecao_leonardo(member):
    """
    Verifica se o membro é o Leonardo (proteção especial)

    Args:
        member: Objeto discord.Member

    Returns:
        bool: True se for Leonardo, False caso contrário
    """
    nome_lower = member.name.lower()
    return "leonardo" in nome_lower or "cruz" in nome_lower
