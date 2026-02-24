################################################################################
#  
#	FILE: 	database_manager.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	18 11 2025
#	WHAT:	Gerenciador de banco de dados usando JSON
#
################################################################################

import json
import os
from pathlib import Path
from typing import List, Optional
from models.contato import Contato
from controller.logger import Logger

logger = Logger.obter_logger("pebbl.database")


class DatabaseManager:
    """
    Gerenciador de banco de dados para contatos usando JSON.
    
    Fornece operações CRUD completas e funcionalidades de busca e exportação.
    """
    
    def __init__(self, data_file: str = None):
        """
        Inicializa o gerenciador de banco de dados.
        
        Args:
            data_file (str): Caminho para o arquivo JSON. Se None, usa o padrão.
        """
        if data_file is None:
            # Caminho padrão: backend/database/data/contatos.json
            base_dir = Path(__file__).parent
            data_dir = base_dir / 'data'
            data_dir.mkdir(exist_ok=True)
            self.data_file = str(data_dir / 'contatos.json')
        else:
            self.data_file = data_file
        
        self.contatos: List[Contato] = []
        self.ultimo_id: int = 0
        self._carregar_dados()
    
    def _carregar_dados(self):
        """Carrega dados do arquivo JSON."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.ultimo_id = data.get('ultimo_id', 0)
                    
                    # Converter dicionários em objetos Contato
                    contatos_data = data.get('contatos', [])
                    self.contatos = [Contato.from_dict(c) for c in contatos_data]
                
                logger.debug(f"Carregados {len(self.contatos)} contatos do arquivo")
            else:
                # Criar arquivo com estrutura inicial
                logger.info(f"Arquivo de dados não encontrado. Criando novo em {self.data_file}")
                self._salvar_dados()
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise Exception(f"Erro ao carregar dados: {e}")
    
    def _salvar_dados(self):
        """Salva dados no arquivo JSON."""
        try:
            data = {
                'versao': '1.0',
                'ultimo_id': self.ultimo_id,
                'contatos': [c.to_dict() for c in self.contatos]
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise Exception(f"Erro ao salvar dados: {e}")
    
    def _gerar_id(self) -> int:
        """Gera um novo ID único."""
        self.ultimo_id += 1
        return self.ultimo_id
    
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
            # Validar contato
            valido, mensagem = contato.validar()
            if not valido:
                logger.warning(f"Tentativa de adicionar contato inválido: {mensagem}")
                return False, mensagem
            
            # Verificar se email já existe (se fornecido)
            if contato.email:
                for c in self.contatos:
                    if c.email and c.email.lower() == contato.email.lower():
                        logger.warning(f"Email duplicado ao tentar adicionar contato: {contato.email}")
                        return False, f"Já existe um contato com o email '{contato.email}'."
            
            # Atribuir ID
            contato.id = self._gerar_id()
            
            # Adicionar à lista
            self.contatos.append(contato)
            
            # Salvar no arquivo
            self._salvar_dados()
            
            logger.info(f"Contato adicionado com sucesso: {contato.nome_completo} (ID: {contato.id})")
            return True, f"Contato '{contato.nome_completo}' adicionado com sucesso! (ID: {contato.id})"
            
        except Exception as e:
            logger.error(f"Erro ao adicionar contato: {e}")
            return False, f"Erro ao adicionar contato: {e}"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES READ
    # ═══════════════════════════════════════════════════════════════════════════
    
    def listar_todos(self) -> List[Contato]:
        """
        Retorna todos os contatos.
        
        Returns:
            List[Contato]: Lista de todos os contatos
        """
        return self.contatos.copy()
    
    def buscar_por_id(self, contato_id: int) -> Optional[Contato]:
        """
        Busca um contato por ID.
        
        Args:
            contato_id (int): ID do contato
            
        Returns:
            Optional[Contato]: Contato encontrado ou None
        """
        for contato in self.contatos:
            if contato.id == contato_id:
                return contato
        return None
    
    def buscar_por_nome(self, nome: str) -> List[Contato]:
        """
        Busca contatos por nome (parcial, case-insensitive).
        
        Args:
            nome (str): Nome ou parte do nome a buscar
            
        Returns:
            List[Contato]: Lista de contatos encontrados
        """
        nome_lower = nome.lower()
        resultados = []
        
        for contato in self.contatos:
            if nome_lower in contato.nome_completo.lower():
                resultados.append(contato)
        
        return resultados
    
    def buscar_por_email(self, email: str) -> Optional[Contato]:
        """
        Busca um contato por email (exato, case-insensitive).
        
        Args:
            email (str): Email a buscar
            
        Returns:
            Optional[Contato]: Contato encontrado ou None
        """
        email_lower = email.lower()
        
        for contato in self.contatos:
            if contato.email and contato.email.lower() == email_lower:
                return contato
        
        return None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES UPDATE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def atualizar_contato(self, contato_id: int, dados: dict) -> tuple[bool, str]:
        """
        Atualiza dados de um contato existente.
        
        Args:
            contato_id (int): ID do contato a atualizar
            dados (dict): Dicionário com campos a atualizar
                         Campos válidos: nome_completo, data_nascimento, email,
                                       telefone, endereco, notas
            
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            contato = self.buscar_por_id(contato_id)
            
            if not contato:
                return False, f"Contato com ID {contato_id} não encontrado."
            
            # Atualizar campos fornecidos
            campos_validos = ['nome_completo', 'data_nascimento', 'email', 
                            'telefone', 'endereco', 'nome_pai', 'nome_mae', 
                            'cpf', 'rg', 'notas']
            
            for campo, valor in dados.items():
                if campo in campos_validos:
                    setattr(contato, campo, str(valor).strip())
            
            # Validar após atualização
            valido, mensagem = contato.validar()
            if not valido:
                # Recarregar dados originais
                self._carregar_dados()
                return False, mensagem
            
            # Verificar duplicação de email (se alterado)
            if 'email' in dados and dados['email']:
                for c in self.contatos:
                    if c.id != contato_id and c.email and c.email.lower() == dados['email'].lower():
                        self._carregar_dados()
                        return False, f"Já existe outro contato com o email '{dados['email']}'."
            
            # Atualizar timestamp de modificação
            contato.atualizar_modificacao()
            
            # Salvar alterações
            self._salvar_dados()
            
            return True, f"Contato '{contato.nome_completo}' atualizado com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao atualizar contato: {e}"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES DELETE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def remover_contato(self, contato_id: int) -> tuple[bool, str]:
        """
        Remove um contato do banco de dados.
        
        Args:
            contato_id (int): ID do contato a remover
            
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            contato = self.buscar_por_id(contato_id)
            
            if not contato:
                logger.warning(f"Tentativa de remover contato inexistente com ID: {contato_id}")
                return False, f"Contato com ID {contato_id} não encontrado."
            
            nome = contato.nome_completo
            self.contatos.remove(contato)
            self._salvar_dados()
            
            logger.info(f"Contato removido com sucesso: {nome} (ID: {contato_id})")
            return True, f"Contato '{nome}' removido com sucesso!"
            
        except Exception as e:
            logger.error(f"Erro ao remover contato com ID {contato_id}: {e}")
            return False, f"Erro ao remover contato: {e}"
    
    def remover_todos(self) -> tuple[bool, str]:
        """
        Remove todos os contatos (usar com cuidado!).
        
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            quantidade = len(self.contatos)
            self.contatos.clear()
            self.ultimo_id = 0
            self._salvar_dados()
            
            return True, f"{quantidade} contato(s) removido(s) com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao remover contatos: {e}"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES DE EXPORTAÇÃO
    # ═══════════════════════════════════════════════════════════════════════════
    
    def exportar_csv(self, caminho: str = None) -> tuple[bool, str]:
        """
        Exporta contatos para arquivo CSV.
        
        Args:
            caminho (str): Caminho do arquivo. Se None, usa 'contatos.csv'
            
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            if caminho is None:
                caminho = 'contatos.csv'
            
            if not self.contatos:
                return False, "Não há contatos para exportar."
            
            with open(caminho, 'w', encoding='utf-8') as f:
                # Cabeçalho
                f.write("ID,Nome Completo,Data Nascimento,Email,Telefone,Endereço,Nome Pai,Nome Mãe,CPF,RG,Notas\n")
                
                # Dados
                for c in self.contatos:
                    linha = f'{c.id},"{c.nome_completo}","{c.data_nascimento}","{c.email}","{c.telefone}","{c.endereco}","{c.nome_pai}","{c.nome_mae}","{c.cpf}","{c.rg}","{c.notas}"\n'
                    f.write(linha)
            
            return True, f"Dados exportados para '{caminho}' com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao exportar CSV: {e}"
    
    def exportar_txt(self, caminho: str = None) -> tuple[bool, str]:
        """
        Exporta contatos para arquivo TXT formatado.
        
        Args:
            caminho (str): Caminho do arquivo. Se None, usa 'contatos.txt'
            
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            if caminho is None:
                caminho = 'contatos.txt'
            
            if not self.contatos:
                return False, "Não há contatos para exportar."
            
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
            return False, f"Erro ao exportar TXT: {e}"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTODOS AUXILIARES
    # ═══════════════════════════════════════════════════════════════════════════
    
    def total_contatos(self) -> int:
        """Retorna o número total de contatos."""
        return len(self.contatos)
    
    def estatisticas(self) -> dict:
        """
        Retorna estatísticas sobre os contatos.
        
        Returns:
            dict: Dicionário com estatísticas
        """
        total = len(self.contatos)
        com_email = sum(1 for c in self.contatos if c.email)
        com_telefone = sum(1 for c in self.contatos if c.telefone)
        com_endereco = sum(1 for c in self.contatos if c.endereco)
        
        return {
            'total': total,
            'com_email': com_email,
            'com_telefone': com_telefone,
            'com_endereco': com_endereco
        }
