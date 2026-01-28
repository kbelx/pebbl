################################################################################
#  
#	FILE: 	<contato_controller.py>
#	BY	: 	<kbelx_>
#	FOR	:	<HARRP_>
#	ON	:	<18 Novembro 2025>
#	WHAT:	<Controlador para gerenciar operações de contatos>
#
################################################################################

from typing import List, Optional, Tuple
from app.backend.models.contato import Contato
from app.backend.database.firebase_manager import FirebaseManager

#db = FirebaseManager()

class ContatoController:
    """
    Controlador que gerencia a lógica de negócio entre a UI e o Database.
    
    Fornece uma camada de abstração para operações de contatos,
    incluindo validações e formatações específicas.
    """
    
    def __init__(self):
        """Inicializa o controlador com uma instância do DatabaseManager."""
        self.db = FirebaseManager()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES DE ADIÇÃO
    # ═══════════════════════════════════════════════════════════════════════════
    
    def criar_contato(self, 
        nome_completo: str,
        data_nascimento: str = "",
        email: str = "",
        telefone: str = "",
        endereco: str = "",
        nome_pai: str = "",
        nome_mae: str = "",
        cpf: str = "",
        rg: str = "",
        notas: str = "") -> Tuple[bool, str]:
        """
        Cria e adiciona um novo contato.
        
        Args:
            nome_completo (str): Nome completo do contato
            data_nascimento (str): Data de nascimento (DD/MM/AAAA)
            email (str): Email do contato
            telefone (str): Telefone do contato
            endereco (str): Endereço do contato
            nome_pai (str): Nome do pai
            nome_mae (str): Nome da mãe
            cpf (str): CPF
            rg (str): RG
            notas (str): Notas adicionais
            
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            # Criar objeto Contato
            contato = Contato(
                nome_completo=nome_completo,
                data_nascimento=data_nascimento,
                email=email,
                telefone=telefone,
                endereco=endereco,
                nome_pai=nome_pai,
                nome_mae=nome_mae,
                cpf=cpf,
                rg=rg,
                notas=notas
            )
            
            # Adicionar ao banco
            return self.db.adicionar_contato(contato)
            
        except Exception as e:
            return False, f"Erro ao criar contato: {e}"
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES DE CONSULTA
    # ═══════════════════════════════════════════════════════════════════════════
    
    def obter_todos_contatos(self) -> List[Contato]:
        """
        Obtém todos os contatos.
        
        Returns:
            List[Contato]: Lista de todos os contatos
        """
        return self.db.listar_contatos()
    
    def obter_contato_por_id(self, contato_id: int) -> Optional[Contato]:
        """
        Obtém um contato específico por ID.
        
        Args:
            contato_id (int): ID do contato
            
        Returns:
            Optional[Contato]: Contato encontrado ou None
        """
        return self.db.obter_contato_por_id(contato_id)
    
    def buscar_contatos_por_nome(self, nome: str) -> List[Contato]:
        """
        Busca contatos por nome.
        
        Args:
            nome (str): Nome ou parte do nome
            
        Returns:
            List[Contato]: Lista de contatos encontrados
        """
        if not nome or not nome.strip():
            return []
        
        return self.db.buscar_por_nome(nome)
    
    def buscar_contato_por_email(self, email: str) -> Optional[Contato]:
        """
        Busca um contato por email.
        
        Args:
            email (str): Email a buscar
            
        Returns:
            Optional[Contato]: Contato encontrado ou None
        """
        if not email or not email.strip():
            return None
        
        return self.db.buscar_por_email(email)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES DE MODIFICAÇÃO
    # ═══════════════════════════════════════════════════════════════════════════
    
    def modificar_contato(self, contato_id: int, **campos) -> Tuple[bool, str]:
        """
        Modifica um contato existente.
        
        Args:
            contato_id (int): ID do contato a modificar
            **campos: Campos a atualizar (nome_completo, email, telefone, nome_pai, etc.)
            
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        # Filtrar campos vazios
        dados = {k: v for k, v in campos.items() if v is not None}
        
        if not dados:
            return False, "Nenhum dado fornecido para atualização."
        
        return self.db.atualizar_contato(contato_id, dados)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES DE REMOÇÃO
    # ═══════════════════════════════════════════════════════════════════════════
    
    def remover_contato(self, contato_id: int) -> Tuple[bool, str]:
        """
        Remove um contato.
        
        Args:
            contato_id (int): ID do contato a remover
            
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        return self.db.deletar_contato(contato_id)
    
    def limpar_todos_contatos(self) -> Tuple[bool, str]:
        """
        Remove todos os contatos.
        
        ATENÇÃO: Esta operação é irreversível!
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        return self.db.remover_todos()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERAÇÕES DE EXPORTAÇÃO
    # ═══════════════════════════════════════════════════════════════════════════
    
    def exportar_para_csv(self, caminho: str = None) -> Tuple[bool, str]:
        """
        Exporta contatos para arquivo CSV.
        
        Args:
            caminho (str): Caminho do arquivo (opcional)
            
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        return self.db.exportar_csv(caminho)
    
    def exportar_para_txt(self, caminho: str = None) -> Tuple[bool, str]:
        """
        Exporta contatos para arquivo TXT.
        
        Args:
            caminho (str): Caminho do arquivo (opcional)
            
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        return self.db.exportar_txt(caminho)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTODOS AUXILIARES E ESTATÍSTICAS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def contar_contatos(self) -> int:
        """
        Retorna o número total de contatos.
        
        Returns:
            int: Total de contatos
        """
        return self.db.total_contatos()
    
    def obter_estatisticas(self) -> dict:
        """
        Obtém estatísticas sobre os contatos.
        
        Returns:
            dict: Dicionário com estatísticas
        """
        return self.db.estatisticas()
    
    def formatar_contato_para_exibicao(self, contato: Contato) -> str:
        """
        Formata um contato para exibição na UI.
        
        Args:
            contato (Contato): Contato a formatar
            
        Returns:
            str: String formatada para exibição
        """
        return str(contato)
    
    def formatar_lista_para_exibicao(self, contatos: List[Contato]) -> str:
        """
        Formata uma lista de contatos para exibição.
        
        Args:
            contatos (List[Contato]): Lista de contatos
            
        Returns:
            str: String formatada com todos os contatos
        """
        if not contatos:
            return "Nenhum contato encontrado."
        
        resultado = []
        for i, contato in enumerate(contatos, 1):
            resultado.append(f"\n[{i}] {contato.nome_completo}")
            resultado.append(f"    ID: {contato.id}")
            if contato.email:
                resultado.append(f"    Email: {contato.email}")
            if contato.telefone:
                resultado.append(f"    Telefone: {contato.telefone}")
            if contato.cpf:
                resultado.append(f"    CPF: {contato.cpf}")
        
        return "\n".join(resultado)
