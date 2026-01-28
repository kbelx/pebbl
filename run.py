#!/usr/bin/env python3
"""Ponto de entrada da aplicação Pebbl"""

import os
import sys
from pathlib import Path

def validar_args():
    """Bloqueia comandos da interface gráfica removida."""
    if len(sys.argv) < 2:
        return

    comando = sys.argv[1].strip().lower()
    if comando in ("gui", "tk", "tkinter", "PySide"):
        print(
            "A interface grafica foi removida. "
            "Use `python run.py` ou `python -m app.main <comando>`."
        )
        sys.exit(0)


def carregar_env():
    """Carrega variáveis de ambiente do arquivo .env, se existir."""
    env_path = Path(".env")
    if not env_path.exists():
        return

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

validar_args()
carregar_env()

from app.main import app

if __name__ == '__main__':
    app()
