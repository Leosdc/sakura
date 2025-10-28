# 🌸 Sakura Bot (Kawaii & Androide AI)

Um bot de Discord com **IA conversacional e voz realista**, capaz de alternar entre dois modos de personalidade:  
💖 **Kawaii** (waifu japonesa fofa) e ⚔️ **Androide** (inspirada em 2B / NIKKE).

> Desenvolvido com ❤️ e código por **Leonardo da Cruz**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-green.svg)
![Groq API](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange.svg)
![ElevenLabs](https://img.shields.io/badge/Voice-ElevenLabs-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/Version-v1.0.1-purple.svg)

---

## ✨ Recursos Principais

- 🤖 **IA Integrada (Groq / Llama 3.3-70B)**
  - Gera respostas inteligentes, contextuais e carismáticas
  - Mantém histórico por canal para conversas contínuas
  
- 🎤 **Voz Realista (ElevenLabs)**
  - Conversão de texto em voz com vozes distintas por personalidade
  - Pode falar automaticamente em canais de voz quando ativada
  
- 💕 **Personalidades Duplas**
  - **Kawaii** 🌸 – fala doce, alegre e carinhosa, com vocabulário japonês
  - **Androide** ⚔️ – fala fria, técnica e militar, protetora do comandante

- 🔧 **Comandos Moderativos e Utilitários**
  - Timeout, perdão, limpeza e purga de mensagens
  - Alternância de modos e personalidades em tempo real

---

## 🧠 Tecnologias Usadas

| Módulo | Função |
|--------|--------|
| **discord.py** | Controle dos eventos e comandos no Discord |
| **Groq API (Llama 3.3-70B)** | Geração de texto inteligente e contextual |
| **ElevenLabs API** | Geração de voz natural e expressiva |
| **dotenv** | Armazenamento seguro de chaves e tokens |
| **asyncio** | Execução assíncrona e reprodução de voz fluida |

---

## ⚙️ Instalação

### 1️⃣ Pré-requisitos
- Python 3.10 ou superior
- FFmpeg instalado no sistema
- Conta nas APIs [Groq](https://console.groq.com) e [ElevenLabs](https://elevenlabs.io)

### 2️⃣ Instale as dependências
```bash
pip install discord.py python-dotenv groq elevenlabs
```

### 3️⃣ Configure o `.env`
Crie um arquivo `.env` na raiz com:
```env
DISCORD_BOT_TOKEN=SEU_TOKEN_DO_DISCORD
GROQ_API_KEY=SUA_CHAVE_GROQ
ELEVENLABS_API_KEY=SUA_CHAVE_ELEVENLABS
```

### 4️⃣ Execute o bot
```bash
python bot_kawaii_androide.py
```

---

## 💬 Comandos Principais

| Comando | Descrição |
|----------|------------|
| `>ai <mensagem>` | Conversa com a IA da Sakura |
| `>kawaii` | Ativa o modo Kawaii (fofa 🌸) |
| `>androide` | Ativa o modo Androide (militar ⚔️) |
| `>vozauto` | Liga/desliga o modo de voz automática |
| `>entrar` | Faz o bot entrar no seu canal de voz |
| `>sair` | Faz o bot sair do canal de voz |
| `>voz <texto>` | Faz a Sakura falar algo no canal de voz |
| `>limpar` | Limpa o histórico de conversa |
| `>apagar <qtd>` | Apaga mensagens do canal |
| `>castigo @user <tempo> <motivo>` | Coloca usuário em timeout |
| `>perdoar @user` | Remove o timeout |
| `>ajuda` | Exibe os comandos disponíveis |

---

## 🌸 Modos de Personalidade

### 💖 **Kawaii**
- Fala animada, doce e meiga  
- Usa honoríficos e palavras japonesas (-chan, -kun, arigatou...)  
- Voz feminina e expressiva (Gigi / estilo anime)

### ⚔️ **Androide**
- Comunicação séria e profissional  
- Estilo militar, inspirada em 2B (NieR: Automata)  
- Voz madura e estável (Aria / ElevenLabs)

---

## 📁 Estrutura do Projeto

```
📦 Sakura-Bot
├── bot_kawaii_androide.py
├── .env
├── requirements.txt
├── README.md
└── changelog.md
```

---

## 🔒 Observações

- O bot **nunca** pune ou expulsa o usuário “Leonardo da Cruz”
- Cada modo possui **sua própria voz, cor e mensagens** embutidas
- Mensagens longas são divididas automaticamente para evitar limites do Discord
- Compatível com servidores com **múltiplos canais de voz e texto**

---

## 🧾 Licença

Distribuído sob a licença **MIT**.  
Feito com 💖 por [Leonardo da Cruz](https://github.com/Leosdc)

---

## 🎧 Exemplo de uso

> **Leonardo-kun:** Sakura, me conta algo fofo?  
> **Sakura:** Hai~! 🌸✨ Você sabia que fico feliz só de te ouvir, senpai? 💕  

> **Leonardo (modo androide):** Status do sistema.  
> **Sakura (androide):** Sistema operacional estável. Nenhum erro detectado. Aguardando ordens, comandante. ⚙️

## 🔮 **Roadmap Futuro**

### 🎯 **Modularização do código**
- [ ] Modularizar o código para que fique mais simples adicionar novas funções  

### 🎯 **Responder comandos por voz nos voice channels**
- [ ] Sakura responder falas de membros do canal