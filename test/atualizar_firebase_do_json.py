#!/usr/bin/env python3
"""
Script para atualizar o Firebase com dados de um arquivo JSON
"""

import os
import sys
import json
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Carregar variáveis de ambiente do .env
env_file = Path('.env')
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from app.backend.database.firebase_manager import FirebaseManager
from app.backend.models.contato import Contato


def atualizar_firebase_do_json(caminho_json: str) -> bool:
    """
    Atualiza o Firebase com dados de um arquivo JSON.
    
    Args:
        caminho_json: Caminho do arquivo JSON com os contatos
        
    Returns:
        bool: True se sucesso, False caso contrário
    """
    
    print("=" * 70)
    print("🔄 ATUALIZAR FIREBASE COM DADOS DO JSON")
    print("=" * 70)
    print()
    
    try:
        # Ler arquivo JSON
        print(f"1️⃣  Lendo arquivo JSON: {caminho_json}")
        with open(caminho_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        quantidade = len(data.get('contatos', []))
        print(f"   ✅ Arquivo carregado com {quantidade} contatos")
        print()
        
        # Conectar ao Firebase
        print("2️⃣  Conectando ao Firebase...")
        db = FirebaseManager()
        print("   ✅ Conectado")
        print()
        
        # Limpar contatos existentes
        print("3️⃣  Limpando contatos existentes...")
        db.contatos.clear()
        db.ultimo_id = 0
        db._salvar_dados()
        print("   ✅ Limpo")
        print()
        
        # Carregar contatos do JSON
        print("4️⃣  Carregando contatos do JSON...")
        contatos_adicionados = 0
        erros = 0
        
        for contato_data in data.get('contatos', []):
            try:
                # Criar objeto Contato a partir do dicionário
                contato = Contato.from_dict(contato_data)
                db.contatos.append(contato)
                contatos_adicionados += 1
                
            except Exception as e:
                erros += 1
                print(f"   ⚠️  Erro ao carregar contato: {e}")
        
        print(f"   ✅ {contatos_adicionados} contatos carregados")
        if erros > 0:
            print(f"   ⚠️  {erros} erros encontrados")
        print()
        
        # Realoccar IDs em ordem alfabética
        print("5️⃣  Realocando IDs em ordem alfabética...")
        db._realocarealocar_ids()
        print("   ✅ IDs realocados")
        print()
        
        # Salvar no Firebase
        print("6️⃣  Salvando no Firebase...")
        db._salvar_dados()
        print("   ✅ Salvo com sucesso")
        print()
        
        # Verificar resultado
        print("7️⃣  Verificando resultado...")
        contatos_firebase = db.listar_contatos()
        print(f"   ✅ Total de contatos no Firebase: {len(contatos_firebase)}")
        print()
        
        print("=" * 70)
        print(f"✅ SUCESSO! Banco atualizado com {len(contatos_firebase)} contatos")
        print("=" * 70)
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho_json}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Usar o JSON da pasta data
    json_path = Path('app/backend/database/data/contatos.json')
    sucesso = atualizar_firebase_do_json(str(json_path))
    exit(0 if sucesso else 1)
