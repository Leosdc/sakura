"""
Comandos relacionados à IA e conversação
"""

from discord.ext import commands
from core import (
    bot,
    inicializar_historico,
    adicionar_mensagem_usuario,
    adicionar_mensagem_assistente,
    obter_historico,
    limpar_historico,
    get_mensagem,
)
from services import gerar_resposta
from utils import dividir_mensagem_longa, validar_canal_permitido
from config import GROQ_TEMPERATURE


@bot.command(name="ai")
async def chat_ai(ctx, *, pergunta):
    """Conversa com a IA"""
    # Verifica se o canal é permitido
    if not validar_canal_permitido(ctx.channel):
        await ctx.reply(
            f"Este comando só funciona nos canais: #mesas-da-taverna e #quarto-da-sakura 🌸"
        )
        return

    channel_id = ctx.channel.id

    # Adiciona mensagem ao histórico
    adicionar_mensagem_usuario(channel_id, ctx.author.name, pergunta)

    try:
        async with ctx.typing():
            # Gera resposta usando o serviço Groq
            historico = obter_historico(channel_id)
            resposta_ia = gerar_resposta(
                messages=historico, temperature=GROQ_TEMPERATURE, max_tokens=1024
            )

            resposta_com_mencao = f"{ctx.author.mention} {resposta_ia}"

            # Adiciona resposta ao histórico
            adicionar_mensagem_assistente(channel_id, resposta_ia)

            # Divide mensagem se for muito longa
            if len(resposta_com_mencao) > 2000:
                await ctx.send(ctx.author.mention)
                chunks = dividir_mensagem_longa(resposta_ia)
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(resposta_com_mencao)

    except Exception as e:
        await ctx.reply(f"Erro: {str(e)}")
        print(f"Erro: {e}")


@bot.command(name="limpar")
async def limpar_historico_cmd(ctx):
    """Limpa o histórico de conversas do canal"""
    channel_id = ctx.channel.id
    limpar_historico(channel_id)
    await ctx.send(f"{ctx.author.mention} {get_mensagem('limpar')}")
