#!/usr/bin/env python3
"""
Script para testar a realocação de IDs
"""

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

from app.backend.database.firebase_manager import FirebaseManager


def testar_realocacao():
    """Testa a realocação de IDs"""
    
    print("=" * 60)
    print("🔄 TESTE DE REALOCAÇÃO DE IDs")
    print("=" * 60)
    print()
    
    try:
        # Inicializar Firebase
        print("1️⃣  Conectando ao Firebase...")
        db = FirebaseManager()
        print("✅ Conectado")
        print()
        
        # Listar antes
        print("2️⃣  Estado ANTES da realocação:")
        contatos = db.listar_contatos()
        print(f"   Total de contatos: {len(contatos)}")
        print(f"   Último ID: {db.ultimo_id}")
        print("   IDs: ", [c.id for c in contatos])
        print()
        
        # Realoccar IDs
        print("3️⃣  Realocando IDs...")
        sucesso, msg = db.realoccar_ids_manual()
        print(f"   {msg}")
        print()
        
        # Listar depois
        print("4️⃣  Estado DEPOIS da realocação:")
        contatos = db.listar_contatos()
        print(f"   Total de contatos: {len(contatos)}")
        print(f"   Último ID: {db.ultimo_id}")
        print("   IDs: ", [c.id for c in contatos])
        print()
        
        # Verificar se está sequencial
        ids = [c.id for c in contatos]
        esperado = list(range(1, len(contatos) + 1))
        
        if ids == esperado:
            print("=" * 60)
            print("✅ SUCESSO! IDs realocados corretamente!")
            print("=" * 60)
            return True
        else:
            print("=" * 60)
            print("❌ ERRO! IDs não estão sequenciais")
            print(f"   Esperado: {esperado}")
            print(f"   Obtido: {ids}")
            print("=" * 60)
            return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = testar_realocacao()
    exit(0 if sucesso else 1)
