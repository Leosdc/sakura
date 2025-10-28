"""
Gerenciamento de histórico de conversas
"""

from config import MAX_HISTORY_MESSAGES, PERSONALIDADES

# Armazena histórico de conversas por canal
conversation_history = {}

# Personalidade atual (padrão: kawaii)
personalidade_atual = "kawaii"


def inicializar_historico(channel_id):
    """Inicializa o histórico de conversa com o system prompt da personalidade atual"""
    if channel_id not in conversation_history:
        conversation_history[channel_id] = [
            {
                "role": "system",
                "content": PERSONALIDADES[personalidade_atual]["system_prompt"],
            }
        ]


def atualizar_personalidade_historico():
    """Atualiza todos os históricos com a nova personalidade"""
    for channel_id in conversation_history:
        conversation_history[channel_id][0] = {
            "role": "system",
            "content": PERSONALIDADES[personalidade_atual]["system_prompt"],
        }


def adicionar_mensagem_usuario(channel_id, author_name, content):
    """Adiciona uma mensagem do usuário ao histórico"""
    inicializar_historico(channel_id)

    conversation_history[channel_id].append(
        {"role": "user", "content": f"{author_name}: {content}"}
    )

    # Mantém apenas as últimas MAX_HISTORY_MESSAGES mensagens
    if len(conversation_history[channel_id]) > MAX_HISTORY_MESSAGES + 1:
        conversation_history[channel_id] = [
            conversation_history[channel_id][0]
        ] + conversation_history[channel_id][-MAX_HISTORY_MESSAGES:]


def adicionar_mensagem_assistente(channel_id, content):
    """Adiciona uma mensagem da IA ao histórico"""
    conversation_history[channel_id].append({"role": "assistant", "content": content})


def obter_historico(channel_id):
    """Retorna o histórico de conversas de um canal"""
    inicializar_historico(channel_id)
    return conversation_history[channel_id]


def limpar_historico(channel_id):
    """Limpa o histórico de conversas de um canal"""
    inicializar_historico(channel_id)
    conversation_history[channel_id] = conversation_history[channel_id][:1]


def get_personalidade_atual():
    """Retorna a personalidade atual"""
    return personalidade_atual


def set_personalidade(nova_personalidade):
    """Define uma nova personalidade"""
    global personalidade_atual
    personalidade_atual = nova_personalidade
    atualizar_personalidade_historico()


def get_mensagem(key, **kwargs):
    """Retorna mensagem formatada da personalidade atual"""
    msg = PERSONALIDADES[personalidade_atual]["mensagens"][key]
    return msg.format(**kwargs) if kwargs else msg
