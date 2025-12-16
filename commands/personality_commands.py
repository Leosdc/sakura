"""
Comandos relacionados à troca de personalidade
"""

import discord
from core import bot, set_personalidade, get_personalidade_atual, get_mensagem
from config import PERSONALIDADES


@bot.command(name="kawaii")
async def modo_kawaii(ctx):
    """Ativa o modo Kawaii da Sakura"""
    set_personalidade("kawaii")
    
    embed = discord.Embed(
        title="🌸 Modo Kawaii Ativado!",
        description="Kyaa~! Agora estou no modo kawaii, senpai! 💖✨",
        color=discord.Color.pink()
    )
    embed.add_field(
        name="Mudanças",
        value="• Personalidade fofa e animada 🌸\n• Voz Gigi (estilo anime)\n• Honoríficos japoneses ativados",
        inline=False
    )
    embed.set_footer(text="Arigatou, senpai~! 💕")
    
    await ctx.send(embed=embed)
    
    # Atualiza o status do bot
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="as mesas da taverna 🌸"
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)
    
    print(f"✅ Personalidade alterada para: KAWAII")


@bot.command(name="androide")
async def modo_androide(ctx):
    """Ativa o modo Androide da Sakura"""
    set_personalidade("androide")
    
    embed = discord.Embed(
        title="⚔️ MODO ANDROIDE ATIVADO",
        description="Sistema reiniciado. Protocolo militar online.",
        color=discord.Color.dark_grey()
    )
    embed.add_field(
        name="Status do Sistema",
        value="• Personalidade: Androide de combate ⚔️\n• Voz: Aria (perfil militar)\n• Protocolos táticos: Ativos",
        inline=False
    )
    embed.set_footer(text="Aguardando ordens, comandante. ⚙️")
    
    await ctx.send(embed=embed)
    
    # Atualiza o status do bot
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="o perímetro ⚔️"
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)
    
    print(f"✅ Personalidade alterada para: ANDROIDE")


@bot.command(name="status")
async def status_personalidade(ctx):
    """Mostra a personalidade atual"""
    personalidade = get_personalidade_atual()
    config = PERSONALIDADES[personalidade]
    
    embed = discord.Embed(
        title=config["embed_title"],
        description=f"**Modo atual:** {personalidade.upper()}",
        color=config["embed_color"]
    )
    
    if personalidade == "kawaii":
        embed.add_field(
            name="Características",
            value="🌸 Fofa e animada\n💖 Usa honoríficos japoneses\n✨ Voz: Gigi (anime)",
            inline=False
        )
    else:
        embed.add_field(
            name="Características",
            value="⚔️ Séria e profissional\n⚙️ Estilo militar\n💫 Voz: Aria (madura)",
            inline=False
        )
    
    embed.set_footer(text=config["embed_footer"])
    await ctx.send(embed=embed)