#!/usr/bin/env python3
"""
Script para carregar variáveis de ambiente do arquivo .env
Execute este arquivo antes de rodar a aplicação
"""

import os
from pathlib import Path

def load_env():
    """Carrega variáveis de ambiente do arquivo .env"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("⚠️  Arquivo .env não encontrado")
        return False
    
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Pula comentários e linhas vazias
                if not line or line.startswith('#'):
                    continue
                
                # Parse do formato KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove aspas se presentes
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    os.environ[key] = value
                    print(f"✅ {key}={value[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao carregar .env: {e}")
        return False

if __name__ == "__main__":
    if load_env():
        print("\n✅ Variáveis de ambiente carregadas com sucesso!")
        print(f"FIREBASE_DATABASE_URL={os.getenv('FIREBASE_DATABASE_URL')}")
    else:
        print("\n❌ Erro ao carregar variáveis de ambiente")
