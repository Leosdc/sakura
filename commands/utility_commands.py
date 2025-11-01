"""
Comandos utilitários
"""

import discord
from core import bot, get_personalidade_atual, get_voz_automatica
from config import PERSONALIDADES


@bot.command(name="ajuda")
async def ajuda(ctx):
    """Mostra comandos disponíveis"""
    personalidade = get_personalidade_atual()
    config = PERSONALIDADES[personalidade]
    voz_ativa = get_voz_automatica()

    embed = discord.Embed(
        title=config["embed_title"],
        description=f"Modo atual: **{personalidade.upper()}**\nProtocolos disponíveis:",
        color=config["embed_color"],
    )
    embed.add_field(name=">ai <mensagem>", value="Conversar com a IA", inline=False)
    embed.add_field(name=">kawaii", value="Ativar modo Kawaii 🌸", inline=False)
    embed.add_field(name=">androide", value="Ativar modo Androide ⚔️", inline=False)
    embed.add_field(
        name=">vozauto",
        value=f"Liga/desliga voz automática ({'🟢 ATIVA' if voz_ativa else '🔴 DESATIVADA'})",
        inline=False,
    )
    embed.add_field(name=">entrar", value="Entrar no seu canal de voz", inline=False)
    embed.add_field(name=">sair", value="Sair do canal de voz", inline=False)
    embed.add_field(
        name=">voz <texto>", value="Falar algo no canal de voz", inline=False
    )
    embed.add_field(name=">limpar", value="Limpar histórico de conversas", inline=False)
    embed.add_field(
        name=">apagar <qtd>", value="Apagar mensagens do canal", inline=False
    )
    embed.add_field(
        name=">castigo @user <tempo> <motivo>", value="Castigar membro", inline=False
    )
    embed.add_field(name=">perdoar @user", value="Perdoar membro", inline=False)
    embed.add_field(name=">ajuda", value="Mostrar comandos", inline=False)
    embed.set_footer(text=config["embed_footer"])
    await ctx.send(embed=embed)
