"""
Comandos relacionados a voz
"""

import discord
from core import (
    bot,
    get_voz_automatica,
    toggle_voz_automatica,
    get_mensagem,
    get_personalidade_atual,
)
from services import gerar_audio
from config import PERSONALIDADES


@bot.command(name="vozauto")
async def toggle_voz_automatica_cmd(ctx):
    """Liga/desliga a voz automática"""
    voz_ativa = toggle_voz_automatica()

    if voz_ativa:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('vozauto_ativada')}")
    else:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('vozauto_desativada')}")

    print(f"Voz automática: {'ATIVADA' if voz_ativa else 'DESATIVADA'}")


@bot.command(name="entrar")
async def entrar_voz(ctx):
    """Bot entra no canal de voz do usuário"""
    if not ctx.author.voice:
        await ctx.send(f"{ctx.author.mention} Você não está em um canal de voz!")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
        await ctx.send(f"{ctx.author.mention} Movendo para {channel.mention}. ⚔️")
    else:
        await channel.connect()
        await ctx.send(f"{ctx.author.mention} Conectada em {channel.mention}. ⚙️")


@bot.command(name="sair")
async def sair_voz(ctx):
    """Bot sai do canal de voz"""
    if ctx.voice_client is None:
        await ctx.send(f"{ctx.author.mention} Não estou em um canal de voz.")
        return

    await ctx.voice_client.disconnect()
    await ctx.send(f"{ctx.author.mention} Desconectada. ⚔️")


@bot.command(name="voz")
async def falar_voz(ctx, *, texto: str):
    """Fala no canal de voz usando ElevenLabs"""
    if ctx.voice_client is None:
        await ctx.send(
            f"{ctx.author.mention} Não estou conectada. Use >entrar primeiro."
        )
        return

    if ctx.voice_client.is_playing():
        await ctx.send(f"{ctx.author.mention} Aguarde. Transmissão em andamento.")
        return

    try:
        await ctx.send(f"{ctx.author.mention} Gerando voz...")

        # Pega configurações de voz da personalidade atual
        personalidade = get_personalidade_atual()
        voice_config = PERSONALIDADES[personalidade]

        # Gera áudio usando o serviço ElevenLabs
        audio_path = gerar_audio(
            texto=texto,
            voice_id=voice_config["voice_id"],
            voice_settings_dict=voice_config["voice_settings"],
        )

        # Toca o áudio
        audio_source = discord.FFmpegPCMAudio(audio_path)
        ctx.voice_client.play(
            audio_source, after=lambda e: print(f"Erro: {e}") if e else None
        )

        await ctx.send(f"{ctx.author.mention} Transmissão ativada. 🎤")

    except Exception as e:
        await ctx.send(f"{ctx.author.mention} Erro: {str(e)}")
