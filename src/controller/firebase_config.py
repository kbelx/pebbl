################################################################################
#  
#	FILE: 	firebase_config.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	09 12 2025
#	WHAT:	Configuração e setup do Firebase
#
################################################################################

import os
from pathlib import Path


def verificar_configuracao_firebase() -> bool:
    """
    Verifica se o Firebase está corretamente configurado.
    
    Returns:
        bool: True se configurado, False caso contrário
    """
    # Verifica variável de ambiente
    if not os.getenv('FIREBASE_DATABASE_URL'):
        print("⚠️  FIREBASE_DATABASE_URL não configurada")
        return False
    
    # Verifica arquivo de credenciais
    base_dir = Path(__file__).parent.parent.parent.parent
    credentials_path = base_dir / 'serviceAccountKey.json'
    
    if not credentials_path.exists():
        print(f"⚠️  Arquivo de credenciais não encontrado em {credentials_path}")
        return False
    
    print("✅ Firebase configurado corretamente")
    return True


def configurar_firebase(database_url: str, credentials_path: str = None):
    """
    Configura variáveis de ambiente do Firebase.
    
    Args:
        database_url (str): URL do banco de dados Firebase
        credentials_path (str): Caminho para o arquivo serviceAccountKey.json
    """
    # Define variável de ambiente
    os.environ['FIREBASE_DATABASE_URL'] = database_url
    
    # Se credenciais não informadas, assume padrão
    if credentials_path is None:
        base_dir = Path(__file__).parent.parent.parent.parent
        credentials_path = str(base_dir / 'serviceAccountKey.json')
    
    print(f"✅ Firebase configurado")
    print(f"   Database URL: {database_url}")
    print(f"   Credenciais: {credentials_path}")
