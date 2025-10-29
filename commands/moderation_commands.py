"""
Comandos relacionados a moderação
"""

import discord
from core import bot, get_mensagem
from utils import (
    validar_quantidade_apagar,
    validar_tempo_castigo,
    validar_permissao_moderacao,
    validar_permissao_mensagens,
    verificar_protecao_leonardo,
)


@bot.command(name="apagar")
async def apagar_mensagens(ctx, quantidade: int = 10):
    """Apaga mensagens do canal"""
    if not validar_permissao_mensagens(ctx.author):
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
        return

    # Valida quantidade
    valido, erro = validar_quantidade_apagar(quantidade)
    if not valido:
        await ctx.send(f"{ctx.author.mention} {erro}")
        return

    try:
        deleted = await ctx.channel.purge(limit=quantidade + 1)
        await ctx.send(
            f"{ctx.author.mention} {get_mensagem('apagar_sucesso', count=len(deleted) - 1)}",
            delete_after=5,
        )
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
    except discord.HTTPException as e:
        await ctx.send(
            f"{ctx.author.mention} {get_mensagem('erro_generico', error=str(e))}"
        )


@bot.command(name="castigo")
async def castigo(
    ctx,
    membro: discord.Member = None,
    tempo: str = "5m",
    *,
    motivo: str = "Comportamento inadequado",
):
    """Coloca um membro de castigo (timeout)"""
    if not validar_permissao_moderacao(ctx.author):
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
        return

    if membro is None:
        await ctx.send(f"{ctx.author.mention} Especifique um membro.")
        return

    # PROTEÇÃO: Nunca castigar o Leonardo da Cruz
    if verificar_protecao_leonardo(membro):
        await ctx.send(f"{ctx.author.mention} {get_mensagem('castigo_leonardo')}")
        return

    if membro.id == ctx.author.id or membro.id == bot.user.id:
        await ctx.send(f"{ctx.author.mention} Operação inválida.")
        return

    # Valida tempo
    valido, resultado = validar_tempo_castigo(tempo)
    if not valido:
        await ctx.send(f"{ctx.author.mention} {resultado}")
        return

    duracao = resultado

    try:
        await membro.timeout(duracao, reason=f"Sakura: {motivo}")
        await ctx.send(
            f"{ctx.author.mention} {get_mensagem('castigo_sucesso', member=membro.mention, time=tempo, reason=motivo)}"
        )
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
    except Exception as e:
        await ctx.send(
            f"{ctx.author.mention} {get_mensagem('erro_generico', error=str(e))}"
        )


@bot.command(name="perdoar")
async def perdoar(ctx, membro: discord.Member = None):
    """Remove o castigo de um membro"""
    if not validar_permissao_moderacao(ctx.author):
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
        return

    if membro is None:
        await ctx.send(f"{ctx.author.mention} Especifique um membro.")
        return

    try:
        await membro.timeout(None, reason="Perdoado pela Sakura")
        await ctx.send(
            f"{ctx.author.mention} {get_mensagem('perdoar_sucesso', member=membro.mention)}"
        )
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
    except Exception as e:
        await ctx.send(
            f"{ctx.author.mention} {get_mensagem('erro_generico', error=str(e))}"
        )
