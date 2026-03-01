################################################################################
#  
#	FILE: 	<main.py>
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	18 11 2025
#	WHAT:	<Entrada principal da aplicação (CLI Moderna)>
#
################################################################################

import sys
import os
from pathlib import Path


def _carregar_env_de_arquivo(env_path: Path) -> bool:
    """Carrega variáveis de ambiente de um arquivo .env."""
    if not env_path.exists():
        return False

    with env_path.open("r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    for linha in linhas:
        linha = linha.rstrip("\n")
        conteudo = linha.strip()

        if not conteudo:
            continue
        if conteudo.startswith("#"):
            continue
        if "=" not in conteudo:
            continue

        chave, valor = conteudo.split("=", 1)
        os.environ[chave.strip()] = valor.strip()
    return True


def carregar_env():
    """
    Carrega variáveis de ambiente procurando em caminhos conhecidos.

    Prioridade:
    1. src/tokens/.env (estrutura atual do projeto)
    2. tokens/.env (compatibilidade)
    3. .env na raiz do projeto
    """
    base_dir = Path(__file__).resolve().parent
    candidatos = [
        base_dir / "tokens" / ".env",
        base_dir.parent / "tokens" / ".env",
        base_dir.parent / ".env",
    ]

    for env_path in candidatos:
        if _carregar_env_de_arquivo(env_path):
            return


carregar_env()

# Adicionar diretório raiz ao path para importar módulos do projeto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controller.contato_controller import ContatoController
from rich.console import Console

from src.views.cli.cli import build_app

################################################################################

def main():
    console = Console()
    controller = ContatoController()
    app = build_app(controller, console)
    app()

if __name__ == "__main__":
    main()
