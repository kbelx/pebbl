#!/usr/bin/env python3
################################################################################
#  
#	FILE: 	<exemplo_firebase.py>
#	BY	: 	<kbelx_>
#	FOR	:	<HARRP_>
#	ON	:	<09 Dezembro 2025>
#	WHAT:	<Exemplo prático de uso do Firebase Manager>
#
################################################################################

import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent))

from app.backend.database.firebase_manager import FirebaseManager
from app.backend.models.contato import Contato


def exemplo_completo():
    """
    Demonstra todas as operações principais do FirebaseManager.
    """
    
    print("\n" + "="*60)
    print("🔥 EXEMPLO PRÁTICO - FIREBASE MANAGER")
    print("="*60 + "\n")
    
    try:
        # 1. INICIALIZAR
        print("1️⃣  INICIALIZANDO CONEXÃO FIREBASE...")
        db = FirebaseManager()
        print("✅ Conectado!\n")
        
        # 2. ADICIONAR CONTATOS
        print("2️⃣  ADICIONANDO CONTATOS...")
        
        contato1 = Contato(
            nome_completo="João Silva",
            email="joao@example.com",
            telefone="11987654321",
            cpf="123.456.789-00"
        )
        sucesso, msg = db.adicionar_contato(contato1)
        print(f"   {msg}")
        
        contato2 = Contato(
            nome_completo="Maria Santos",
            email="maria@example.com",
            telefone="11999888777",
            cpf="987.654.321-00"
        )
        sucesso, msg = db.adicionar_contato(contato2)
        print(f"   {msg}\n")
        
        # 3. LISTAR CONTATOS
        print("3️⃣  LISTANDO TODOS OS CONTATOS...")
        contatos = db.listar_contatos()
        for c in contatos:
            print(f"   [{c.id}] {c.nome_completo} - {c.email}")
        print()
        
        # 4. BUSCAR CONTATOS
        print("4️⃣  BUSCANDO POR NOME...")
        resultado = db.buscar_por_nome("João")
        for c in resultado:
            print(f"   ✓ Encontrado: {c.nome_completo}")
        print()
        
        # 5. BUSCAR POR EMAIL
        print("5️⃣  BUSCANDO POR EMAIL...")
        encontrado = db.buscar_por_email("maria@example.com")
        if encontrado:
            print(f"   ✓ Encontrado: {encontrado.nome_completo}\n")
        
        # 6. ATUALIZAR CONTATO
        print("6️⃣  ATUALIZANDO CONTATO...")
        dados_atualizados = {
            'telefone': '11991234567',
            'email': 'joao.novo@example.com'
        }
        sucesso, msg = db.atualizar_contato(1, dados_atualizados)
        print(f"   {msg}\n")
        
        # 7. VERIFICAR ATUALIZAÇÃO
        print("7️⃣  VERIFICANDO ATUALIZAÇÃO...")
        atualizado = db.obter_contato_por_id(1)
        if atualizado:
            print(f"   Nome: {atualizado.nome_completo}")
            print(f"   Email: {atualizado.email}")
            print(f"   Telefone: {atualizado.telefone}\n")
        
        # 8. TOTAL DE CONTATOS
        print("8️⃣  TOTAL DE CONTATOS...")
        total = db.obter_total_contatos()
        print(f"   Total: {total} contato(s)\n")
        
        # 9. EXPORTAR PARA JSON
        print("9️⃣  EXPORTANDO PARA JSON...")
        caminho_export = Path(__file__).parent / "contatos_backup.json"
        sucesso, msg = db.exportar_json(str(caminho_export))
        print(f"   {msg}\n")
        
        # 10. DELETAR CONTATO
        print("🔟 DELETANDO CONTATO...")
        sucesso, msg = db.deletar_contato(1)
        print(f"   {msg}\n")
        
        # 11. VERIFICAR APÓS DELEÇÃO
        print("1️⃣1️⃣  VERIFICANDO APÓS DELEÇÃO...")
        total_final = db.obter_total_contatos()
        print(f"   Total agora: {total_final} contato(s)\n")
        
        print("="*60)
        print("✅ EXEMPLO FINALIZADO COM SUCESSO!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    sucesso = exemplo_completo()
    sys.exit(0 if sucesso else 1)
