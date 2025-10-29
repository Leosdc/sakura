"""
Serviço de integração com a API ElevenLabs
"""

import re
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY, ELEVENLABS_MODEL

# Cliente ElevenLabs (Voz Realista)
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def limpar_texto_para_voz(texto):
    """
    Remove emojis e caracteres especiais do texto para síntese de voz

    Args:
        texto: Texto a ser limpo

    Returns:
        Texto sem emojis
    """
    # Remove emojis comuns
    texto_limpo = re.sub(r"[⚔️⚙️💫✨🎯🗡️🌸💖😊💕🎤]", "", texto)
    return texto_limpo


def gerar_audio(texto, voice_id, voice_settings_dict, output_path="sakura_voice.mp3"):
    """
    Gera áudio usando ElevenLabs

    Args:
        texto: Texto a ser convertido em áudio
        voice_id: ID da voz a ser usada
        voice_settings_dict: Dicionário com configurações da voz
        output_path: Caminho do arquivo de saída

    Returns:
        Caminho do arquivo de áudio gerado
    """
    # Limpa o texto
    texto_limpo = limpar_texto_para_voz(texto)

    # Cria as configurações de voz
    voice_settings = VoiceSettings(**voice_settings_dict)

    # Gera áudio
    audio = elevenlabs_client.text_to_speech.convert(
        text=texto_limpo,
        voice_id=voice_id,
        model_id=ELEVENLABS_MODEL,
        voice_settings=voice_settings,
    )

    # Salva o áudio
    with open(output_path, "wb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)

    return output_path


def get_client():
    """Retorna o cliente ElevenLabs"""
    return elevenlabs_client
