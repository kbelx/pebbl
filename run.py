#!/usr/bin/env python3
"""Ponto de entrada da aplicação Pebbl"""

import os
from pathlib import Path

# Carregar variáveis de ambiente do .env
env_file = Path('.env')
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from app.main import app

if __name__ == '__main__':
    app()