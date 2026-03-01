################################################################################
#  
#	FILE: 	firebase_manager.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	09 12 2025
#	WHAT:	Gerenciador de banco de dados usando Firebase Realtime Database
#
################################################################################

import firebase_admin
from firebase_admin import credentials, db
from typing import List, Optional
from src.models.contato import Contato
from src.controller.logger import Logger
import os
from pathlib import Path

logger = Logger.obter_logger("pebbl.firebase")


class FirebaseManager:
    """
    Gerenciador de banco de dados para contatos usando Firebase Realtime Database.
    
    Fornece operações CRUD completas e funcionalidades de busca e exportação.
    Mantém a mesma interface do DatabaseManager JSON.
    """
    
    _instance = None  # Singleton pattern para uma única conexão
    
    def __new__(cls, credentials_path: str = None):
        """Implementa singleton para evitar múltiplas inicializações."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializado = False
        return cls._instance
    

    def __init__(self, credentials_path: str = None):
        """
        Inicializa o gerenciador de banco de dados Firebase.
        
        Args:
            credentials_path (str): Caminho para o arquivo serviceAccountKey.json
        """
        if self._inicializado:
            return
            
        try:
            if credentials_path is None:
                credentials_path = self._obter_caminho_credencial()
            
            # Verifica se o arquivo de credenciais existe
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"Arquivo de credenciais não encontrado em {credentials_path}. "
                    f"Faça download do arquivo serviceAccountKey.json do Firebase Console."
                )
            
            # Inicializa Firebase Admin SDK
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': self._obter_database_url()
            })
            
            self.db = db
            self.contatos: List[Contato] = []
            self.ultimo_id: int = 0
            
            self._carregar_dados()
            logger.info("Firebase Manager inicializado com sucesso")
            self._inicializado = True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar Firebase: {e}")
            raise Exception(f"Erro ao inicializar Firebase: {e}")
    
    @staticmethod
    def _obter_caminho_credencial() -> str:
        """Obtém o primeiro caminho válido para o arquivo de credenciais."""
        caminhos = [
            Path(__file__).resolve().parents[1] / 'tokens' / 'serviceAccountKey.json',  # src/tokens/
            Path(__file__).resolve().parents[2] / 'tokens' / 'serviceAccountKey.json',  # tokens/ (raiz)
            Path(__file__).resolve().parents[2] / 'serviceAccountKey.json',             # raiz
        ]

        for caminho in caminhos:
            if caminho.exists():
                return str(caminho)

        return str(caminhos[0])

    @staticmethod
    def _carregar_variavel_de_env(chave: str) -> Optional[str]:
        """
        Tenta encontrar uma variável em arquivos .env conhecidos e injeta no ambiente.
        """
        caminhos_env = [
            Path(__file__).resolve().parents[1] / 'tokens' / '.env',  # src/tokens/.env
            Path(__file__).resolve().parents[2] / 'tokens' / '.env',  # tokens/.env
            Path(__file__).resolve().parents[2] / '.env',             # .env na raiz
            Path.cwd() / 'tokens' / '.env',                           # cwd/tokens/.env
            Path.cwd() / '.env',                                      # cwd/.env
        ]

        for caminho in caminhos_env:
            if not caminho.exists():
                continue

            try:
                with caminho.open("r", encoding="utf-8") as arquivo:
                    for linha in arquivo:
                        conteudo = linha.strip()
                        if not conteudo or conteudo.startswith("#") or "=" not in conteudo:
                            continue

                        nome, valor = conteudo.split("=", 1)
                        if nome.strip() == chave and valor.strip():
                            os.environ[chave] = valor.strip()
                            logger.debug(f"Variável {chave} carregada de {caminho}")
                            return valor.strip()
            except OSError as erro:
                logger.warning(f"Falha ao ler arquivo de ambiente {caminho}: {erro}")

        return None


    @staticmethod
    def _obter_database_url() -> str:
        """
        Obtém a URL do banco de dados Firebase das variáveis de ambiente.
        
        ### Returns:
            ``str``: URL do banco de dados
        """

        url = os.getenv('FIREBASE_DATABASE_URL')
        if url:
            return url

        url = FirebaseManager._carregar_variavel_de_env('FIREBASE_DATABASE_URL')
        if url:
            return url

        raise ValueError(
            "Variável de ambiente FIREBASE_DATABASE_URL não definida. "
            "Defina a variável no ambiente ou adicione em src/tokens/.env."
        )
    

    def _carregar_dados(self):
        """Carrega dados do Firebase Realtime Database."""
        try:
            ref = self.db.reference('pebbl/contatos')
            data = ref.get()
            
            if data:
                self.ultimo_id = data.get('ultimo_id', 0)
                contatos_data = data.get('lista', [])
                self.contatos = [Contato.from_dict(c) for c in contatos_data]
                logger.debug(f"Carregados {len(self.contatos)} contatos do Firebase")
            else:
                self.ultimo_id = 0
                self.contatos = []
                self._salvar_dados()  # Cria estrutura inicial
                logger.info("Nenhum dado encontrado. Criada estrutura inicial.")
        except Exception as e:
            logger.error(f"Erro ao carregar dados do Firebase: {e}")
            raise Exception(f"Erro ao carregar dados do Firebase: {e}")
    

    def _salvar_dados(self):
        """Salva dados no Firebase Realtime Database."""
        try:
            data = {
                'versao': '1.0',
                'ultimo_id': self.ultimo_id,
                'lista': [c.to_dict() for c in self.contatos]
            }
            
            ref = self.db.reference('pebbl/contatos')
            ref.set(data)
            logger.debug(f"Dados salvos no Firebase ({len(self.contatos)} contatos)")
        except Exception as e:
            logger.error(f"Erro ao salvar dados no Firebase: {e}")
            raise Exception(f"Erro ao salvar dados no Firebase: {e}")
    

    def _gerar_id(self) -> int:
        """Gera um novo ID único."""
        self.ultimo_id += 1
        self._salvar_dados()  # Salva imediatamente para garantir consistência
        return self.ultimo_id
    

    def _realocarealocar_ids(self):
        """
        Realoca os IDs dos contatos de acordo com ordem alfabética do nome.
        Útil quando contatos são deletados e deixam lacunas nos IDs.
        """
        try:
            if not self.contatos:
                self.ultimo_id = 0
                self._salvar_dados()
                logger.info("Nenhum contato. IDs realocados.")
                return
            
            # Ordena contatos por nome (ordem alfabética)
            self.contatos.sort(key=lambda c: c.nome_completo.lower())
            
            # Realoca IDs sequencialmente baseado na ordem alfabética
            for idx, contato in enumerate(self.contatos, 1):
                contato.id = idx
            
            # Atualiza o último ID
            self.ultimo_id = len(self.contatos)
            self._salvar_dados()
            logger.info(f"IDs realocados com sucesso (ordem alfabética). Total: {len(self.contatos)}")
        except Exception as e:
            logger.error(f"Erro ao realoccar IDs: {e}")
            raise Exception(f"Erro ao realoccar IDs: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES CREATE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def adicionar_contato(self, contato: Contato) -> tuple[bool, str]:
        """
        Adiciona um novo contato ao banco de dados.
        
        Args:
            contato (Contato): Objeto Contato a ser adicionado
            
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            contato.id = self._gerar_id()
            self.contatos.append(contato)
            self._salvar_dados()
            logger.info(f"Contato adicionado: {contato.nome_completo} (ID: {contato.id})")
            return True, f"Contato '{contato.nome_completo}' adicionado com sucesso!"
        except Exception as e:
            logger.error(f"Erro ao adicionar contato: {e}")
            return False, f"Erro ao adicionar contato: {e}"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES READ
    # ═══════════════════════════════════════════════════════════════════════════
    
    def obter_contato_por_id(self, contato_id: int) -> Optional[Contato]:
        """
        Obtém um contato pelo ID.
        
        Args:
            contato_id (int): ID do contato
            
        Returns:
            Optional[Contato]: Objeto Contato ou None
        """
        for contato in self.contatos:
            if contato.id == contato_id:
                return contato
        return None
    
    def listar_contatos(self) -> List[Contato]:
        """
        Lista todos os contatos ordenados por nome (ordem alfabética).
        
        Returns:
            List[Contato]: Lista de todos os contatos ordenados alfabeticamente
        """
        contatos_ordenados = sorted(self.contatos, key=lambda c: c.nome_completo.lower())
        return contatos_ordenados
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES UPDATE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def atualizar_contato(self, contato_id: int, dados_atualizados: dict) -> tuple[bool, str]:
        """
        Atualiza os dados de um contato existente.
        
        Args:
            contato_id (int): ID do contato a ser atualizado
            dados_atualizados (dict): Dicionário com os dados a atualizar
            
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            contato = self.obter_contato_por_id(contato_id)
            if not contato:
                return False, f"Contato com ID {contato_id} não encontrado"
            
            # Atualiza atributos do contato
            for chave, valor in dados_atualizados.items():
                if hasattr(contato, chave):
                    setattr(contato, chave, valor)
            
            self._salvar_dados()
            logger.info(f"Contato atualizado: {contato.nome_completo} (ID: {contato_id})")
            return True, f"Contato atualizado com sucesso!"
        except Exception as e:
            logger.error(f"Erro ao atualizar contato: {e}")
            return False, f"Erro ao atualizar contato: {e}"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES DELETE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def deletar_contato(self, contato_id: int) -> tuple[bool, str]:
        """
        Deleta um contato pelo ID e realoca os IDs dos demais contatos.
        
        Args:
            contato_id (int): ID do contato a ser deletado
            
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            contato = self.obter_contato_por_id(contato_id)
            if not contato:
                return False, f"Contato com ID {contato_id} não encontrado"
            
            nome_contato = contato.nome_completo
            self.contatos.remove(contato)
            
            # Realoca IDs dos contatos restantes
            self._realocarealocar_ids()
            
            logger.info(f"Contato deletado: {nome_contato} (ID: {contato_id}). IDs realocados.")
            return True, f"Contato '{nome_contato}' deletado com sucesso!"
        except Exception as e:
            logger.error(f"Erro ao deletar contato: {e}")
            return False, f"Erro ao deletar contato: {e}"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES SEARCH
    # ═══════════════════════════════════════════════════════════════════════════
    
    def buscar_por_nome(self, nome: str) -> List[Contato]:
        """
        Busca contatos pelo nome (busca parcial case-insensitive).
        
        Args:
            nome (str): Nome ou parte do nome a buscar
            
        Returns:
            List[Contato]: Lista de contatos encontrados
        """
        nome_lower = nome.lower()
        return [c for c in self.contatos if nome_lower in c.nome_completo.lower()]
    

    def buscar_por_email(self, email: str) -> Optional[Contato]:
        """
        Busca um contato pelo email.
        
        Args:
            email (str): Email a buscar
            
        Returns:
            Optional[Contato]: Contato encontrado ou None
        """
        for contato in self.contatos:
            if contato.email.lower() == email.lower():
                return contato
        return None
    

    def buscar_por_telefone(self, telefone: str) -> Optional[Contato]:
        """
        Busca um contato pelo telefone.
        
        Args:
            telefone (str): Telefone a buscar
            
        Returns:
            Optional[Contato]: Contato encontrado ou None
        """
        for contato in self.contatos:
            if contato.telefone == telefone:
                return contato
        return None
    

    def buscar_por_cpf(self, cpf: str) -> Optional[Contato]:
        """
        Busca um contato pelo CPF.
        
        Args:
            cpf (str): CPF a buscar
            
        Returns:
            Optional[Contato]: Contato encontrado ou None
        """
        for contato in self.contatos:
            if contato.cpf == cpf:
                return contato
        return None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES EXPORT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def exportar_json(self, caminho_arquivo: str) -> tuple[bool, str]:
        """
        Exporta todos os contatos para um arquivo JSON.
        
        Args:
            caminho_arquivo (str): Caminho do arquivo de destino
            
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            import json
            data = {
                'versao': '1.0',
                'quantidade': len(self.contatos),
                'contatos': [c.to_dict() for c in self.contatos]
            }
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Contatos exportados para {caminho_arquivo}")
            return True, f"Contatos exportados com sucesso para {caminho_arquivo}"
        except Exception as e:
            logger.error(f"Erro ao exportar contatos: {e}")
            return False, f"Erro ao exportar contatos: {e}"


    def exportar_csv(self, caminho: str = None) -> tuple[bool, str]:
        """
        Exporta contatos para arquivo CSV (salvo localmente).

        Args:
            caminho (str): Caminho do arquivo. Se None, usa 'contatos.csv'

        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            if caminho is None:
                caminho = 'contatos.csv'

            if not self.contatos:
                return False, "NЖo h  contatos para exportar."

            with open(caminho, 'w', encoding='utf-8') as f:
                f.write("ID,Nome Completo,Data Nascimento,Email,Telefone,Endere‡o,Nome Pai,Nome MЖe,CPF,RG,Notas\n")
                for c in self.contatos:
                    linha = (
                        f'{c.id},"{c.nome_completo}","{c.data_nascimento}","{c.email}","{c.telefone}",'
                        f'"{c.endereco}","{c.nome_pai}","{c.nome_mae}","{c.cpf}","{c.rg}","{c.notas}"\n'
                    )
                    f.write(linha)

            return True, f"Dados exportados para '{caminho}' com sucesso!"
        except Exception as e:
            logger.error(f"Erro ao exportar CSV: {e}")
            return False, f"Erro ao exportar CSV: {e}"


    def exportar_txt(self, caminho: str = None) -> tuple[bool, str]:
        """
        Exporta contatos para arquivo TXT formatado (salvo localmente).

        Args:
            caminho (str): Caminho do arquivo. Se None, usa 'contatos.txt'

        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            if caminho is None:
                caminho = 'contatos.txt'

            if not self.contatos:
                return False, "NЖo h  contatos para exportar."

            with open(caminho, 'w', encoding='utf-8') as f:
                f.write("=" * 74 + "\n")
                f.write("LISTA DE CONTATOS - PEBBL_\n")
                f.write("=" * 74 + "\n\n")

                for i, c in enumerate(self.contatos, 1):
                    f.write(f"[{i}] {str(c)}\n")
                    f.write("-" * 74 + "\n\n")

                f.write(f"Total de contatos: {len(self.contatos)}\n")

            return True, f"Dados exportados para '{caminho}' com sucesso!"
        except Exception as e:
            logger.error(f"Erro ao exportar TXT: {e}")
            return False, f"Erro ao exportar TXT: {e}"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES STAT
    # ═══════════════════════════════════════════════════════════════════════════
    
    def obter_total_contatos(self) -> int:
        """
        Obtém o número total de contatos.
        
        Returns:
            int: Quantidade de contatos
        """
        return len(self.contatos)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES DE MANUTENÇÃO
    # ═══════════════════════════════════════════════════════════════════════════
    
    def realoccar_ids_manual(self) -> tuple[bool, str]:
        """
        Realoca manualmente os IDs dos contatos para que sejam sequenciais.
        Útil para reorganizar IDs após múltiplas deleções.
        
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            total_antes = self.ultimo_id
            self._realocarealocar_ids()
            total_depois = len(self.contatos)
            
            msg = f"IDs realocados! Antes: {total_antes} | Depois: {total_depois}"
            logger.info(msg)
            return True, msg
        except Exception as e:
            logger.error(f"Erro ao realoccar IDs manualmente: {e}")
            return False, f"Erro ao realoccar IDs: {e}"
