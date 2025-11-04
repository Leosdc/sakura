# 📜 Changelog

## [1.0.3] - 2025-11-03
### 🔒 Segurança e Controle
- **Adicionado** restrição de canais permitidos para respostas
- **Limitado** respostas de texto apenas para #mesas-da-taverna e #quarto-da-sakura
- **Adicionado** validação de canal em comandos de IA e respostas automáticas
- **Melhorada** organização e controle de onde o bot pode interagir

## [1.0.2] - 2025-11-01
### 🏗️ Reestruturado - Organização Modular Completa
- **Divisão total do código** em módulos (`commands`, `config`, `core`, `events`, `services`, `utils`)
- **Removido** o arquivo único `bot_kawaii_androide.py`
- **Criado** `main.py` como ponto de entrada principal
- **Adicionado** arquivos de configuração (`settings.py`, `personalities.py`)
- **Adicionado** integração de serviços (`groq_service.py`, `elevenlabs_service.py`)
- **Adicionado** módulos de comandos separados (IA, voz, moderação, personalidade e utilidades)
- **Adicionado** camada de núcleo (`bot.py`, `conversation.py`) e eventos (`message_handler.py`)
- **Centralizado** funções auxiliares em `utils/` (`helpers.py`, `validators.py`)
- **Melhorada** a escalabilidade e legibilidade do projeto

## [1.0.1] - 2025-10-28
### 💫 Melhorado - 
- **LLM treinado com nova engenharia de prompt**

### 💫 Versionamento aplicado
- **Sakura agora possui versionamento**