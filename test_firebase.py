#!/usr/bin/env python3
################################################################################
#  
#	FILE: 	<test_firebase.py>
#	BY	: 	<kbelx_>
#	FOR	:	<HARRP_>
#	ON	:	<09 Dezembro 2025>
#	WHAT:	<Script para testar integração Firebase>
#
################################################################################

import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent))

from app.backend.database.firebase_manager import FirebaseManager
from app.backend.database.firebase_config import verificar_configuracao_firebase
from app.backend.models.contato import Contato


def test_firebase():
    """Testa a conexão e operações básicas com Firebase."""
    
    print("=" * 60)
    print("🔥 TESTE DE INTEGRAÇÃO FIREBASE")
    print("=" * 60)
    print()
    
    # Verifica configuração
    print("1️⃣  Verificando configuração...")
    if not verificar_configuracao_firebase():
        print("\n❌ Falha na verificação de configuração")
        return False
    print()
    
    try:
        # Inicializa Firebase
        print("2️⃣  Conectando ao Firebase...")
        db = FirebaseManager()
        print("✅ Conexão estabelecida")
        print()
        
        # Testa adição de contato
        print("3️⃣  Testando adição de contato...")
        novo_contato = Contato(
            nome_completo="Teste Firebase",
            email="teste@firebase.com",
            telefone="11987654321"
        )
        sucesso, msg = db.adicionar_contato(novo_contato)
        if sucesso:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
            return False
        print()
        
        # Testa listagem
        print("4️⃣  Testando listagem de contatos...")
        contatos = db.listar_contatos()
        print(f"✅ Total de contatos: {len(contatos)}")
        for c in contatos:
            print(f"   - {c.nome_completo} ({c.email})")
        print()
        
        # Testa busca
        print("5️⃣  Testando busca por nome...")
        encontrados = db.buscar_por_nome("Teste")
        print(f"✅ Encontrados {len(encontrados)} contato(s)")
        print()
        
        # Testa obtenção de total
        print("6️⃣  Testando estatísticas...")
        total = db.obter_total_contatos()
        print(f"✅ Total de contatos no BD: {total}")
        print()
        
        print("=" * 60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Erro durante testes: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = test_firebase()
    sys.exit(0 if sucesso else 1)
