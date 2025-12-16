"""
Comandos relacionados a mudança de personalidade
"""

from core import bot, get_personalidade_atual, set_personalidade


@bot.command(name="kawaii")
async def modo_kawaii(ctx):
    """Ativa o modo Kawaii (waifu fofa)"""
    if get_personalidade_atual() == "kawaii":
        await ctx.send(
            f"{ctx.author.mention} Ara ara~ 🌸 Eu já estou no modo kawaii, senpai! (◕‿◕✿)✨"
        )
        return

    set_personalidade("kawaii")

    await ctx.send(
        f"{ctx.author.mention} Kyaa~! 🌸✨ Modo Kawaii ativado! Agora estou super fofa e animada, nya~! 💖 (ノ◕ヮ◕)ノ*:･ﾟ✧"
    )
    print(f"Personalidade alterada para: kawaii")


@bot.command(name="androide")
async def modo_androide(ctx):
    """Ativa o modo Androide (2B/militar)"""
    if get_personalidade_atual() == "androide":
        await ctx.send(
            f"{ctx.author.mention} Comandante. Sistema já operando em modo androide. ⚔️"
        )
        return

    set_personalidade("androide")

    await ctx.send(
        f"{ctx.author.mention} Protocolo de personalidade atualizado. ⚔️\nUnidade Sakura: Modo Androide ativado. Sistemas de combate online. Aguardando ordens, comandante. ⚙️💫"
    )
    print(f"Personalidade alterada para: androide")