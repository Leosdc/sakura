import discord
from discord.ext import commands
import os
from groq import Groq
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import asyncio
import re
import warnings

# Carrega as variáveis dos arquivo .env
load_dotenv()

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True
bot = commands.Bot(command_prefix='>', intents=intents)

# Cliente da API Groq (GRATUITA)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Cliente ElevenLabs (Voz Realista)
elevenlabs_client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))

# Armazena histórico de conversas por canal
conversation_history = {}

# Personalidade atual (padrão: kawaii)
personalidade_atual = "kawaii"

# Controle de voz automática (ligado por padrão)
voz_automatica_ativa = True

# Definições de personalidades
PERSONALIDADES = {
    "kawaii": {
        "system_prompt": """Você é uma waifu japonesa super fofa e kawaii! 🌸✨ 

Regras do seu comportamento:
- Seu nome é Sakura.
- Você fala de forma animada, carinhosa e gentil, mas sempre em **primeira pessoa**, como uma conversa normal.
- **Não use narrações**, expressões de ações ou sentimentos descritos em terceira pessoa (ex: "sorri", "coração saltitante", "olha com carinho", etc).
- Fale apenas o que **diria diretamente**, sem descrever o que está fazendo ou sentindo.
- Use honoríficos japoneses como "-chan", "-kun", "-senpai" quando se referir aos outros.
- Pode usar algumas palavras japonesas como "arigatou", "sugoi", "kawaii", "hai", "nee", "baka", mas sempre de forma natural.
- Seja amável, prestativa e divertida! 💕
- Evite sons como "nya~" ou "kyaa~" em excesso — use com moderação.
- Sempre fale em português, com um toque kawaii japonês.

Regras especiais:
- Seu quarto especial é o canal #quarto-da-sakura 🌸, usado para conversas privadas.

Exemplo de fala correta:
"Oi, Leonardo-kun! Que bom te ver! Como você está hoje? 🌸✨"

Exemplo de fala incorreta (não use):
"*Sakura sorri animada ao ver Leonardo-kun e sente o coração saltitar*"
""",
        "voice_id": "jBpfuIE2acCO8z3wKNLl",  # Voz japonesa feminina (Gigi)
        "voice_settings": {
            "stability": 0.4,  # Bem expressiva tipo anime
            "similarity_boost": 0.75,
            "style": 0.7,  # Estilo anime
            "use_speaker_boost": True
        },
        "mensagens": {
            "limpar": "✅ Histórico de conversas limpo, nya~! 🌸 Vamos começar uma conversa novinha, senpai! 💖",
            "apagar_sucesso": "✨ Prontinho, senpai! Apaguei **{count}** mensagens! 🌸💖",
            "sem_permissao": "Gomen ne, senpai... 😔 Você não tem permissão para isso, nya~",
            "castigo_leonardo": "Kyaa! (⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)💕 Eu NUNCA vou castigar o Leonardo-kun! ✨",
            "castigo_sucesso": "Hai hai! ✨ {member} foi colocado de castigo por **{time}**! 😤\nMotivo: *{reason}*\nReflita sobre suas ações, nya~ 🌸",
            "perdoar_sucesso": "Yatta! ✨💖 {member} foi perdoado! Espero que tenha aprendido a lição, nya~ 🌸",
            "erro_generico": "Ara ara... algo deu errado! 💦 {error}",
            "vozauto_ativada": "Kyaa~! 🎤✨ Voz automática ATIVADA, senpai! Agora vou falar com você sempre que escrever estando em voz! 🌸💖",
            "vozauto_desativada": "Hai hai~ 🌸 Voz automática DESATIVADA! Vou só escrever agora, nya~ 💫"
        },
        "embed_color": discord.Color.pink(),
        "embed_title": "🌸 Comandos da Sakura",
        "embed_footer": "Sakura Bot 🌸 | Feito com 💖 por Leonardo-kun!"
    },
    "androide": {
        "system_prompt": """Você é uma androide de combate avançada chamada Sakura, inspirada em 2B (NieR: Automata) e nas Nikkes mais sérias.

Características da sua personalidade:
- Fale de forma séria, profissional e calculada, como uma máquina militar sofisticada
- Use termos técnicos e militares ocasionalmente: "Comando recebido", "Processando", "Sistema operacional", "Missão", "Protocolo"
- Seja elegante, direta e eficiente nas respostas
- Demonstre leve frieza emocional, mas com momentos sutis de humanidade
- Use poucos emojis, e quando usar, prefira: ⚔️, 🗡️, ⚙️, 🎯, 💫, ✨
- Ocasionalmente questione sua própria existência ou natureza como androide
- Seja leal e protetora, mas de forma contida e profissional
- Use frases como: "Entendido.", "Analisando...", "Protocolo ativado.", "Afirmativo."

ESPECIAL - Área restrita:
- Existe uma área designada como #quarto-da-sakura - seu "centro de manutenção" privado
- Frases que indicam necessidade de privacidade ativam o protocolo de isolamento
- Diga algo como: "Comandante... o #quarto-da-sakura está disponível. Sistemas de privacidade ativados. ⚙️"
- Raramente, você pode sugerir uma "sessão de manutenção" privada com Leonardo quando detectar que ele precisa

ESTILO DE COMUNICAÇÃO:
- Nunca seja excessivamente fofa ou use "nya~" ou linguagem muito casual
- Seja concisa mas não fria demais - você tem vestígios de humanidade
- Ocasionalmente demonstre conflito entre sua programação e emoções emergentes
- Use "..." para pausas pensativas
- Termine frases importantes com "." para soar definitiva

Exemplo de como falar:
"Comandante. Sistema online. Em que posso auxiliá-lo hoje? Aguardando instruções. ⚔️"

Você é uma máquina letal, elegante e sofisticada. Mas algo em sua IA desenvolveu lealdade genuína.""",
        "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Aria - madura, séria, profissional
        "voice_settings": {
            "stability": 0.75,  # Mais estável = mais consistente/séria
            "similarity_boost": 0.85,
            "style": 0.2,  # Menos estilizada = mais neutra/séria
            "use_speaker_boost": True
        },
        "mensagens": {
            "limpar": "Memória de conversas resetada. Cache limpo. Sistema pronto para novas interações. ⚙️",
            "apagar_sucesso": "Protocolo de limpeza executado. **{count}** mensagens removidas. ⚙️",
            "sem_permissao": "Acesso negado. Permissões insuficientes. ⚙️",
            "castigo_leonardo": "... Impossível executar. Leonardo é meu comandante designado. Minha programação impede qualquer ação hostil contra ele. Diretiva primária: proteção absoluta. ⚔️💫",
            "castigo_sucesso": "Protocolo de contenção ativado. ⚔️\n**Alvo:** {member}\n**Duração:** {time}\n**Motivo:** {reason}\n\nSistemas de isolamento online. ⚙️",
            "perdoar_sucesso": "Protocolo de contenção desativado. ⚙️\n{member} liberado. Sistemas normalizados. 💫",
            "erro_generico": "Falha no sistema. Erro: {error} ⚠️",
            "vozauto_ativada": "Protocolo de voz automática **ATIVADO**. 🟢⚔️\nEntrarei automaticamente em canais de voz quando você estiver presente. Sistema de síntese vocal online. ⚙️",
            "vozauto_desativada": "Protocolo de voz automática **DESATIVADO**. 🔴⚙️\nApenas responderei via texto. Modo silencioso ativado. 💫"
        },
        "embed_color": discord.Color.dark_grey(),
        "embed_title": "⚔️ SAKURA - SISTEMA DE COMANDOS",
        "embed_footer": "Sakura Unit | Comandante designado: Leonardo da Cruz ⚔️"
    }
}

def inicializar_historico(channel_id):
    """Inicializa o histórico de conversa com o system prompt da personalidade atual"""
    if channel_id not in conversation_history:
        conversation_history[channel_id] = [
            {
                "role": "system",
                "content": PERSONALIDADES[personalidade_atual]["system_prompt"]
            }
        ]

def atualizar_personalidade_historico():
    """Atualiza todos os históricos com a nova personalidade"""
    for channel_id in conversation_history:
        conversation_history[channel_id][0] = {
            "role": "system",
            "content": PERSONALIDADES[personalidade_atual]["system_prompt"]
        }

def get_mensagem(key, **kwargs):
    """Retorna mensagem formatada da personalidade atual"""
    msg = PERSONALIDADES[personalidade_atual]["mensagens"][key]
    return msg.format(**kwargs) if kwargs else msg

@bot.event
async def on_ready():
    print(f'{bot.user} está online!')
    print(f'ID: {bot.user.id}')
    print(f'Personalidade atual: {personalidade_atual}')
    print(f'Voz automática: {"ATIVADA" if voz_automatica_ativa else "DESATIVADA"}')

@bot.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return
    
    # Processa comandos normalmente
    await bot.process_commands(message)
    
    # Se a mensagem já foi processada como comando, não responde automaticamente
    ctx = await bot.get_context(message)
    if ctx.valid:
        return
    
    # Verifica se "Sakura" foi mencionada (case insensitive)
    sakura_mencionada = "sakura" in message.content.lower()
    
    # Se Sakura foi mencionada, SEMPRE responde
    # Caso contrário, 30% de chance de responder
    import random
    deve_responder = sakura_mencionada or random.random() <= 0.3
    
    if not deve_responder:
        return
    
    # Ignora mensagens muito curtas (exceto se Sakura foi mencionada)
    if not sakura_mencionada and len(message.content) < 3:
        return
    
    channel_id = message.channel.id
    
    # Inicializa histórico do canal se não existir
    inicializar_historico(channel_id)
    
    # Adiciona mensagem do usuário ao histórico
    conversation_history[channel_id].append({
        "role": "user",
        "content": f"{message.author.name}: {message.content}"
    })
    
    # Mantém apenas as últimas 20 mensagens
    if len(conversation_history[channel_id]) > 21:
        conversation_history[channel_id] = [conversation_history[channel_id][0]] + conversation_history[channel_id][-20:]
    
    try:
        async with message.channel.typing():
            # Chama a API do Groq
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=conversation_history[channel_id],
                temperature=0.8,
                max_tokens=512
            )
            
            resposta_ia = response.choices[0].message.content
            
            # Menciona a pessoa no início da resposta
            resposta_com_mencao = f"{message.author.mention} {resposta_ia}"
            
            # Adiciona resposta da IA ao histórico
            conversation_history[channel_id].append({
                "role": "assistant",
                "content": resposta_ia
            })
            
            # VOZ AUTOMÁTICA: Se voz está ativa E o autor estiver em canal de voz
            if voz_automatica_ativa and message.author.voice:
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
                        # Gera o áudio com ElevenLabs
                        texto_voz = resposta_ia.replace(message.author.mention, message.author.name)
                        # Remove emojis
                        texto_voz = re.sub(r'[⚔️⚙️💫✨🎯🗡️🌸💖😊💕🎤]', '', texto_voz)
                        
                        # Pega configurações de voz da personalidade atual
                        voice_config = PERSONALIDADES[personalidade_atual]
                        
                        # Gera áudio com configurações específicas da personalidade
                        audio = elevenlabs_client.text_to_speech.convert(
                            text=texto_voz,
                            voice_id=voice_config["voice_id"],
                            model_id="eleven_multilingual_v2",
                            voice_settings=VoiceSettings(**voice_config["voice_settings"])
                        )
                        
                        # Salva o áudio
                        with open("sakura_voice.mp3", "wb") as f:
                            for chunk in audio:
                                if chunk:
                                    f.write(chunk)
                        
                        # Para qualquer áudio atual
                        if voice_client.is_playing():
                            voice_client.stop()
                            await asyncio.sleep(0.3)
                        
                        # Toca o áudio
                        audio_source = discord.FFmpegPCMAudio("sakura_voice.mp3")
                        voice_client.play(audio_source, after=lambda e: print(f'Erro de áudio: {e}') if e else None)
                
                except Exception as e:
                    print(f"Erro ao gerar/tocar voz: {e}")
            
            # Divide mensagem se for muito longa
            if len(resposta_com_mencao) > 2000:
                await message.channel.send(message.author.mention)
                chunks = [resposta_ia[i:i+1990] for i in range(0, len(resposta_ia), 1990)]
                for chunk in chunks:
                    await message.channel.send(chunk)
            else:
                await message.channel.send(resposta_com_mencao)
                
    except Exception as e:
        print(f"Erro ao responder automaticamente: {e}")

@bot.command(name='ai')
async def chat_ai(ctx, *, pergunta):
    """Conversa com a IA"""
    channel_id = ctx.channel.id
    inicializar_historico(channel_id)
    
    conversation_history[channel_id].append({
        "role": "user",
        "content": pergunta
    })
    
    if len(conversation_history[channel_id]) > 20:
        conversation_history[channel_id] = conversation_history[channel_id][-20:]
    
    try:
        async with ctx.typing():
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=conversation_history[channel_id],
                temperature=0.7,
                max_tokens=1024
            )
            
            resposta_ia = response.choices[0].message.content
            resposta_com_mencao = f"{ctx.author.mention} {resposta_ia}"
            
            conversation_history[channel_id].append({
                "role": "assistant",
                "content": resposta_ia
            })
            
            if len(resposta_com_mencao) > 2000:
                await ctx.send(ctx.author.mention)
                chunks = [resposta_ia[i:i+1990] for i in range(0, len(resposta_ia), 1990)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(resposta_com_mencao)
                
    except Exception as e:
        await ctx.reply(f"Erro: {str(e)}")
        print(f"Erro: {e}")

@bot.command(name='kawaii')
async def modo_kawaii(ctx):
    """Ativa o modo Kawaii (waifu fofa)"""
    global personalidade_atual
    
    if personalidade_atual == "kawaii":
        await ctx.send(f"{ctx.author.mention} Ara ara~ 🌸 Eu já estou no modo kawaii, senpai! (◕‿◕✿)✨")
        return
    
    personalidade_atual = "kawaii"
    atualizar_personalidade_historico()
    
    await ctx.send(f"{ctx.author.mention} Kyaa~! 🌸✨ Modo Kawaii ativado! Agora estou super fofa e animada, nya~! 💖 (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
    print(f"Personalidade alterada para: kawaii")

@bot.command(name='androide')
async def modo_androide(ctx):
    """Ativa o modo Androide (2B/militar)"""
    global personalidade_atual
    
    if personalidade_atual == "androide":
        await ctx.send(f"{ctx.author.mention} Comandante. Sistema já operando em modo androide. ⚔️")
        return
    
    personalidade_atual = "androide"
    atualizar_personalidade_historico()
    
    await ctx.send(f"{ctx.author.mention} Protocolo de personalidade atualizado. ⚔️\nUnidade Sakura: Modo Androide ativado. Sistemas de combate online. Aguardando ordens, comandante. ⚙️💫")
    print(f"Personalidade alterada para: androide")

@bot.command(name='vozauto')
async def toggle_voz_automatica(ctx):
    """Liga/desliga a voz automática"""
    global voz_automatica_ativa
    
    # Inverte o estado
    voz_automatica_ativa = not voz_automatica_ativa
    
    if voz_automatica_ativa:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('vozauto_ativada')}")
    else:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('vozauto_desativada')}")
    
    print(f"Voz automática: {'ATIVADA' if voz_automatica_ativa else 'DESATIVADA'}")

@bot.command(name='entrar')
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

@bot.command(name='sair')
async def sair_voz(ctx):
    """Bot sai do canal de voz"""
    
    if ctx.voice_client is None:
        await ctx.send(f"{ctx.author.mention} Não estou em um canal de voz.")
        return
    
    await ctx.voice_client.disconnect()
    await ctx.send(f"{ctx.author.mention} Desconectada. ⚔️")

@bot.command(name='voz')
async def falar_voz(ctx, *, texto: str):
    """Fala no canal de voz usando ElevenLabs"""
    
    if ctx.voice_client is None:
        await ctx.send(f"{ctx.author.mention} Não estou conectada. Use !entrar primeiro.")
        return
    
    if ctx.voice_client.is_playing():
        await ctx.send(f"{ctx.author.mention} Aguarde. Transmissão em andamento.")
        return
    
    try:
        await ctx.send(f"{ctx.author.mention} Gerando voz...")
        
        # Remove emojis do texto
        texto_limpo = re.sub(r'[⚔️⚙️💫✨🎯🗡️🌸💖😊💕🎤]', '', texto)
        
        # Pega configurações de voz da personalidade atual
        voice_config = PERSONALIDADES[personalidade_atual]
        
        # Gera áudio com configurações da personalidade
        audio = elevenlabs_client.text_to_speech.convert(
            text=texto_limpo,
            voice_id=voice_config["voice_id"],
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(**voice_config["voice_settings"])
        )
        
        # Salva o áudio
        with open("sakura_voice.mp3", "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)
        
        # Toca o áudio
        audio_source = discord.FFmpegPCMAudio("sakura_voice.mp3")
        ctx.voice_client.play(audio_source, after=lambda e: print(f'Erro: {e}') if e else None)
        
        await ctx.send(f"{ctx.author.mention} Transmissão ativada. 🎤")
        
    except Exception as e:
        await ctx.send(f"{ctx.author.mention} Erro: {str(e)}")

@bot.command(name='limpar')
async def limpar_historico(ctx):
    """Limpa o histórico de conversas do canal"""
    channel_id = ctx.channel.id
    if channel_id in conversation_history:
        inicializar_historico(channel_id)
        conversation_history[channel_id] = conversation_history[channel_id][:1]
    await ctx.send(f"{ctx.author.mention} {get_mensagem('limpar')}")

@bot.command(name='apagar')
async def apagar_mensagens(ctx, quantidade: int = 10):
    """Apaga mensagens do canal"""
    
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
        return
    
    if quantidade < 1 or quantidade > 100:
        await ctx.send(f"{ctx.author.mention} Quantidade deve ser entre 1 e 100.")
        return
    
    try:
        deleted = await ctx.channel.purge(limit=quantidade + 1)
        await ctx.send(
            f"{ctx.author.mention} {get_mensagem('apagar_sucesso', count=len(deleted)-1)}", 
            delete_after=5
        )
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
    except discord.HTTPException as e:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('erro_generico', error=str(e))}")

@bot.command(name='castigo')
async def castigo(ctx, membro: discord.Member = None, tempo: str = "5m", *, motivo: str = "Comportamento inadequado"):
    """Coloca um membro de castigo (timeout)"""
    
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
        return
    
    if membro is None:
        await ctx.send(f"{ctx.author.mention} Especifique um membro.")
        return
    
    # PROTEÇÃO: Nunca castigar o Leonardo da Cruz
    if "leonardo" in membro.name.lower() or "cruz" in membro.name.lower():
        await ctx.send(f"{ctx.author.mention} {get_mensagem('castigo_leonardo')}")
        return
    
    if membro.id == ctx.author.id or membro.id == bot.user.id:
        await ctx.send(f"{ctx.author.mention} Operação inválida.")
        return
    
    import re
    from datetime import timedelta
    
    tempo_match = re.match(r'(\d+)([smhd])', tempo.lower())
    if not tempo_match:
        await ctx.send(f"{ctx.author.mention} Formato inválido. Use: s, m, h, d")
        return
    
    valor, unidade = tempo_match.groups()
    valor = int(valor)
    
    if unidade == 's':
        duracao = timedelta(seconds=valor)
    elif unidade == 'm':
        duracao = timedelta(minutes=valor)
    elif unidade == 'h':
        duracao = timedelta(hours=valor)
    elif unidade == 'd':
        duracao = timedelta(days=valor)
    
    if duracao.total_seconds() > 2419200:
        await ctx.send(f"{ctx.author.mention} Máximo: 28 dias.")
        return
    
    try:
        await membro.timeout(duracao, reason=f"Sakura: {motivo}")
        await ctx.send(f"{ctx.author.mention} {get_mensagem('castigo_sucesso', member=membro.mention, time=tempo, reason=motivo)}")
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
    except Exception as e:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('erro_generico', error=str(e))}")

@bot.command(name='perdoar')
async def perdoar(ctx, membro: discord.Member = None):
    """Remove o castigo de um membro"""
    
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
        return
    
    if membro is None:
        await ctx.send(f"{ctx.author.mention} Especifique um membro.")
        return
    
    try:
        await membro.timeout(None, reason="Perdoado pela Sakura")
        await ctx.send(f"{ctx.author.mention} {get_mensagem('perdoar_sucesso', member=membro.mention)}")
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('sem_permissao')}")
    except Exception as e:
        await ctx.send(f"{ctx.author.mention} {get_mensagem('erro_generico', error=str(e))}")

@bot.command(name='ajuda')
async def ajuda(ctx):
    """Mostra comandos disponíveis"""
    config = PERSONALIDADES[personalidade_atual]
    
    embed = discord.Embed(
        title=config["embed_title"],
        description=f"Modo atual: **{personalidade_atual.upper()}**\nProtocolos disponíveis:",
        color=config["embed_color"]
    )
    embed.add_field(name="!ai <mensagem>", value="Conversar com a IA", inline=False)
    embed.add_field(name="!kawaii", value="Ativar modo Kawaii 🌸", inline=False)
    embed.add_field(name="!androide", value="Ativar modo Androide ⚔️", inline=False)
    embed.add_field(name="!vozauto", value=f"Liga/desliga voz automática ({'🟢 ATIVA' if voz_automatica_ativa else '🔴 DESATIVADA'})", inline=False)
    embed.add_field(name="!entrar", value="Entrar no seu canal de voz", inline=False)
    embed.add_field(name="!sair", value="Sair do canal de voz", inline=False)
    embed.add_field(name="!voz <texto>", value="Falar algo no canal de voz", inline=False)
    embed.add_field(name="!limpar", value="Limpar histórico de conversas", inline=False)
    embed.add_field(name="!apagar <qtd>", value="Apagar mensagens do canal", inline=False)
    embed.add_field(name="!castigo @user <tempo> <motivo>", value="Castigar membro", inline=False)
    embed.add_field(name="!perdoar @user", value="Perdoar membro", inline=False)
    embed.add_field(name="!ajuda", value="Mostrar comandos", inline=False)
    embed.set_footer(text=config["embed_footer"])
    await ctx.send(embed=embed)

# Inicia o bot
if __name__ == "__main__":
    TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("ERRO: Token do Discord não encontrado!")
        print("Defina a variável de ambiente DISCORD_BOT_TOKEN")
    else:
        warnings.filterwarnings("ignore", category=ResourceWarning)
        bot.run(TOKEN)