#!/usr/bin/env python3
"""
Script para migrar dados do JSON local para Firebase
"""

import os
import json
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

from app.backend.database.firebase_manager import FirebaseManager
from app.backend.models.contato import Contato


def migrar_json_para_firebase():
    """Migra contatos do JSON local para Firebase"""
    
    # Caminho do arquivo JSON
    json_file = Path('app/backend/database/data/contatos.json')
    
    if not json_file.exists():
        print(f"❌ Arquivo {json_file} não encontrado")
        return False
    
    print("=" * 60)
    print("🔄 MIGRAÇÃO JSON → FIREBASE")
    print("=" * 60)
    print()
    
    try:
        # Carregar dados do JSON
        print("1️⃣  Lendo dados do JSON...")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        contatos_data = data.get('contatos', [])
        print(f"✅ Encontrados {len(contatos_data)} contatos no JSON")
        print()
        
        # Inicializar Firebase
        print("2️⃣  Conectando ao Firebase...")
        db = FirebaseManager()
        print("✅ Conectado ao Firebase")
        print()
        
        # Migrar contatos
        print("3️⃣  Migrando contatos...")
        sucesso_count = 0
        erro_count = 0
        
        for contato_dict in contatos_data:
            try:
                # Criar objeto Contato do dicionário
                contato = Contato.from_dict(contato_dict)
                
                # Adicionar ao Firebase
                sucesso, msg = db.adicionar_contato(contato)
                
                if sucesso:
                    print(f"   ✅ {contato.nome_completo}")
                    sucesso_count += 1
                else:
                    print(f"   ❌ {contato.nome_completo}: {msg}")
                    erro_count += 1
            except Exception as e:
                print(f"   ❌ Erro ao migrar contato: {e}")
                erro_count += 1
        
        print()
        print("=" * 60)
        print("📊 RESULTADO DA MIGRAÇÃO")
        print("=" * 60)
        print(f"✅ Migrados com sucesso: {sucesso_count}")
        print(f"❌ Erros: {erro_count}")
        print(f"📊 Total: {sucesso_count + erro_count}")
        print()
        
        if sucesso_count > 0:
            print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print()
            print("💡 Seus contatos agora estão no Firebase!")
            print("   Acesse: https://console.firebase.google.com")
            return True
        else:
            print("❌ Nenhum contato foi migrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante migração: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = migrar_json_para_firebase()
    exit(0 if sucesso else 1)
