"""
Script para encontrar e corrigir prefixos ! para >
Execute na raiz do projeto
"""

import os
import re

def corrigir_prefixo_arquivo(filepath):
    """Corrige prefixos ! para > em um arquivo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Padrões a serem substituídos
    correcoes = [
        (r'Use >entrar', 'Use >entrar'),
        (r'use >entrar', 'use >entrar'),
        (r'comando >', 'comando >'),
        (r'">', '">'),
        (r"'>", "'>"),
        (r'>voz', '>voz'),
        (r'>entrar', '>entrar'),
        (r'>sair', '>sair'),
        (r'>ai', '>ai'),
        (r'>kawaii', '>kawaii'),
        (r'>androide', '>androide'),
        (r'>vozauto', '>vozauto'),
        (r'>limpar', '>limpar'),
        (r'>apagar', '>apagar'),
        (r'>castigo', '>castigo'),
        (r'>perdoar', '>perdoar'),
        (r'>ajuda', '>ajuda'),
    ]
    
    conteudo_original = conteudo
    
    for padrao, substituicao in correcoes:
        conteudo = re.sub(padrao, substituicao, conteudo)
    
    # Só escreve se houve mudança
    if conteudo != conteudo_original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        return True
    return False

def main():
    """Procura e corrige todos os arquivos Python"""
    print("🔍 Procurando arquivos com prefixo ! ...\n")
    
    arquivos_corrigidos = []
    
    # Percorre todos os arquivos .py do projeto
    for root, dirs, files in os.walk('.'):
        # Ignora venv e __pycache__
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if corrigir_prefixo_arquivo(filepath):
                    arquivos_corrigidos.append(filepath)
                    print(f"✅ Corrigido: {filepath}")
    
    if arquivos_corrigidos:
        print(f"\n🎉 Total de arquivos corrigidos: {len(arquivos_corrigidos)}")
    else:
        print("\n✅ Nenhum arquivo precisou de correção!")

if __name__ == "__main__":
    main()