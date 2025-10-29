"""
Bot Sakura - Discord Bot com IA e personalidades

Ponto de entrada principal do bot.
"""

import warnings
from config import validate_config, DISCORD_BOT_TOKEN
from core import bot

# Importa comandos e eventos para registrá-los
import commands
import events


def main():
    """Função principal que inicia o bot"""
    try:
        # Valida configurações
        validate_config()

        # Suprime warnings de ResourceWarning
        warnings.filterwarnings("ignore", category=ResourceWarning)

        # Inicia o bot
        print("Iniciando bot...")
        bot.run(DISCORD_BOT_TOKEN)

    except ValueError as e:
        print(f"Erro de configuração: {e}")
        return
    except Exception as e:
        print(f"Erro ao iniciar bot: {e}")
        return


if __name__ == "__main__":
    main()
