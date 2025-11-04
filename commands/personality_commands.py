"""
Gerenciamento de eventos de mensagens
"""

import discord
import asyncio
from core import (
    bot,
    get_voz_automatica,
    adicionar_mensagem_usuario,
    adicionar_mensagem_assistente,
    obter_historico,
    get_personalidade_atual,
)
from services import gerar_resposta, gerar_audio
from utils import deve_responder_automaticamente, dividir_mensagem_longa, validar_canal_permitido
from config import PERSONALIDADES, GROQ_TEMPERATURE, GROQ_MAX_TOKENS


@bot.event
async def on_ready():
    """Evento disparado quando o bot fica online"""
    print(f"{bot.user} está online!")
    print(f"ID: {bot.user.id}")
    print(f"Personalidade atual: {get_personalidade_atual()}")
    print(f"Voz automática: {'ATIVADA' if get_voz_automatica() else 'DESATIVADA'}")
    
    # Define a atividade do bot
    try:
        personalidade = get_personalidade_atual()
        if personalidade == "kawaii":
            activity = discord.Activity(
                type=discord.ActivityType.listening,
                name="conversas na taverna 🌸"
            )
        else:  # androide
            activity = discord.Activity(
                type=discord.ActivityType.listening,
                name="ordens do comandante ⚔️"
            )
        
        await bot.change_presence(activity=activity, status=discord.Status.online)
        print(f"✅ Status definido: Ouvindo '{activity.name}'")
    except Exception as e:
        print(f"❌ Erro ao definir status: {e}")


@bot.event
async def on_message(message):
    """Evento disparado quando uma mensagem é enviada"""
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return

    # Processa comandos normalmente
    await bot.process_commands(message)

    # Se a mensagem já foi processada como comando, não responde automaticamente
    ctx = await bot.get_context(message)
    if ctx.valid:
        return

    # Verifica se o canal é permitido para respostas automáticas
    if not validar_canal_permitido(message.channel):
        return

    # Verifica se deve responder automaticamente
    deve_responder, sakura_mencionada = deve_responder_automaticamente(message.content)

    if not deve_responder:
        return

    channel_id = message.channel.id

    # Adiciona mensagem do usuário ao histórico
    adicionar_mensagem_usuario(channel_id, message.author.name, message.content)

    try:
        async with message.channel.typing():
            # Obtém histórico e gera resposta
            historico = obter_historico(channel_id)
            resposta_ia = gerar_resposta(
                messages=historico,
                temperature=GROQ_TEMPERATURE,
                max_tokens=GROQ_MAX_TOKENS,
            )

            # Menciona a pessoa no início da resposta
            resposta_com_mencao = f"{message.author.mention} {resposta_ia}"

            # Adiciona resposta da IA ao histórico
            adicionar_mensagem_assistente(channel_id, resposta_ia)

            # VOZ AUTOMÁTICA: Se voz está ativa E o autor estiver em canal de voz
            if get_voz_automatica() and message.author.voice:
                await processar_voz_automatica(message, resposta_ia)

            # Divide mensagem se for muito longa
            if len(resposta_com_mencao) > 2000:
                await message.channel.send(message.author.mention)
                chunks = dividir_mensagem_longa(resposta_ia)
                for chunk in chunks:
                    await message.channel.send(chunk)
            else:
                await message.channel.send(resposta_com_mencao)

    except Exception as e:
        print(f"Erro ao responder automaticamente: {e}")


async def processar_voz_automatica(message, resposta_ia):
    """Processa a voz automática quando o usuário está em canal de voz"""
    voice_channel = message.author.voice.channel

    try:
        voice_client = message.guild.voice_client

        # Se não está conectada ou conexão está quebrada, conecta
        if voice_client is None or not voice_client.is_connected():
            if voice_client:
                await voice_client.disconnect(force=True)
            voice_client = await voice_channel.connect()
            await asyncio.sleep(2)
        # Se está em outro canal, move
        elif voice_client.channel.id != voice_channel.id:
            await voice_client.move_to(voice_channel)
            await asyncio.sleep(1)

        # Verifica se realmente está conectada
        if voice_client.is_connected():
            # Prepara texto para voz (remove menções)
            texto_voz = resposta_ia.replace(message.author.mention, message.author.name)

            # Pega configurações de voz da personalidade atual
            personalidade = get_personalidade_atual()
            voice_config = PERSONALIDADES[personalidade]

            # Gera o áudio com ElevenLabs
            audio_path = gerar_audio(
                texto=texto_voz,
                voice_id=voice_config["voice_id"],
                voice_settings_dict=voice_config["voice_settings"],
            )

            # Para qualquer áudio atual
            if voice_client.is_playing():
                voice_client.stop()
                await asyncio.sleep(0.3)

            # Toca o áudio
            audio_source = discord.FFmpegPCMAudio(audio_path)
            voice_client.play(
                audio_source,
                after=lambda e: print(f"Erro de áudio: {e}") if e else None,
            )

    except Exception as e:
        print(f"Erro ao gerar/tocar voz: {e}")