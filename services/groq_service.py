"""
Serviço de integração com a API Groq
"""

from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE, GROQ_MAX_TOKENS

# Cliente da API Groq (GRATUITA)
client = Groq(api_key=GROQ_API_KEY)


def gerar_resposta(messages, temperature=None, max_tokens=None):
    """
    Gera uma resposta usando a API do Groq

    Args:
        messages: Lista de mensagens no formato do histórico de conversas
        temperature: Temperatura para geração (opcional, usa padrão se não informado)
        max_tokens: Número máximo de tokens (opcional, usa padrão se não informado)

    Returns:
        String com a resposta gerada pela IA
    """
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=temperature if temperature is not None else GROQ_TEMPERATURE,
        max_tokens=max_tokens if max_tokens is not None else GROQ_MAX_TOKENS,
    )

    return response.choices[0].message.content


def get_client():
    """Retorna o cliente Groq"""
    return client
