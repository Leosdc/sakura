"""
Configurações e variáveis de ambiente do bot
"""

import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Tokens e API Keys
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Configurações do Bot
BOT_PREFIX = ">"
MAX_HISTORY_MESSAGES = 20  # Máximo de mensagens no histórico
AUTO_RESPONSE_CHANCE = 0.3  # 30% de chance de responder automaticamente
MIN_MESSAGE_LENGTH = 3  # Tamanho mínimo de mensagem para resposta automática
ALLOWED_CHANNELS = ["quarto-da-sakura", "mesas-da-taverna"]

# Configurações da API Groq
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = 0.8
GROQ_MAX_TOKENS = 512

# Configurações do ElevenLabs
ELEVENLABS_MODEL = "eleven_multilingual_v2"

# Limites de comandos
MAX_PURGE_MESSAGES = 100
MAX_TIMEOUT_DAYS = 28
MESSAGE_SPLIT_LENGTH = 1990  # Tamanho máximo antes de dividir mensagem


# Validação de configuração
def validate_config():
    """Valida se todas as variáveis de ambiente necessárias estão configuradas"""
    if not DISCORD_BOT_TOKEN:
        raise ValueError(
            "ERRO: Token do Discord não encontrado! Defina DISCORD_BOT_TOKEN"
        )
    if not GROQ_API_KEY:
        raise ValueError("ERRO: API Key do Groq não encontrada! Defina GROQ_API_KEY")
    if not ELEVENLABS_API_KEY:
        raise ValueError(
            "ERRO: API Key do ElevenLabs não encontrada! Defina ELEVENLABS_API_KEY"
        )
    return True
