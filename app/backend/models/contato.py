################################################################################
#  
#	FILE: 	<contato.py>
#	BY	: 	<kbelx_>
#	FOR	:	<HARRP_>
#	ON	:	<18 Novembro 2025>
#	WHAT:	<Modelo de dados para Contato>
#
################################################################################

from datetime import datetime
from app.backend.utils.validators import validar_cpf, validar_rg, validar_email, validar_data, sanitizar_texto

class Contato:
    """
    Modelo de dados para representar um contato pessoal.
    
    Attributes:
        id (int): Identificador único do contato
        nome_completo (str): Nome completo (obrigatório)
        data_nascimento (str): Data de nascimento no formato DD/MM/AAAA
        email (str): Endereço de email
        telefone (str): Número de telefone
        endereco (str): Endereço completo
        nome_pai (str): Nome do pai
        nome_mae (str): Nome da mãe
        cpf (str): CPF (com validação)
        rg (str): RG
        notas (str): Notas adicionais sobre o contato
        data_criacao (str): Timestamp de criação
        data_modificacao (str): Timestamp da última modificação
    """
    
    def __init__(self, 
        nome_completo: str,
        data_nascimento: str = "",
        email: str = "",
        telefone: str = "",
        endereco: str = "",
        nome_pai: str = "",
        nome_mae: str = "",
        cpf: str = "",
        rg: str = "",
        notas: str = "",
        contato_id: int = None):
        """
        Inicializa um novo contato.
        
        Args:
            nome_completo (str): Nome completo do contato (obrigatório)
            data_nascimento (str): Data de nascimento (opcional)
            email (str): Email do contato (opcional)
            telefone (str): Telefone do contato (opcional)
            endereco (str): Endereço do contato (opcional)
            nome_pai (str): Nome do pai (opcional)
            nome_mae (str): Nome da mãe (opcional)
            cpf (str): CPF (opcional)
            rg (str): RG (opcional)
            notas (str): Notas adicionais (opcional)
            contato_id (int): ID do contato (gerado automaticamente se None)
        """
        self.id = contato_id
        self.nome_completo = nome_completo.strip()
        self.data_nascimento = data_nascimento.strip()
        self.email = email.strip()
        self.telefone = telefone.strip()
        self.endereco = endereco.strip()
        self.nome_pai = nome_pai.strip()
        self.nome_mae = nome_mae.strip()
        self.cpf = cpf.strip()
        self.rg = rg.strip()
        self.notas = notas.strip()
        
        # Timestamps
        agora = datetime.now().isoformat()
        self.data_criacao = agora
        self.data_modificacao = agora
    
    def validar(self) -> tuple[bool, str]:
        """
        Valida os dados do contato.
        
        Returns:
            tuple[bool, str]: (é_valido, mensagem_erro)
        """
        # Nome é obrigatório
        if not self.nome_completo or len(self.nome_completo.strip()) == 0:
            return False, "Nome completo é obrigatório."
        
        if len(self.nome_completo) < 3:
            return False, "Nome deve ter pelo menos 3 caracteres."
        
        if len(self.nome_completo) > 150:
            return False, "Nome não pode exceder 150 caracteres."
        
        # Validação de email (se fornecido)
        if self.email:
            if not validar_email(self.email):
                return False, "Formato de email inválido."
        
        # Validação de data de nascimento (se fornecida)
        if self.data_nascimento:
            valido, msg = validar_data(self.data_nascimento)
            if not valido:
                return False, f"Data de nascimento: {msg}"
        
        # Validação de CPF (se fornecido)
        if self.cpf:
            if not validar_cpf(self.cpf):
                return False, "CPF inválido."
                
        # Validação de RG (se fornecido)
        if self.rg:
            if not validar_rg(self.rg):
                return False, "Formato de RG inválido."
        
        # Validação de telefone (se fornecido)
        if self.telefone:
            from backend.utils.validators import validar_telefone
            if not validar_telefone(self.telefone):
                return False, "Formato de telefone inválido."
        
        return True, ""
    
    def to_dict(self) -> dict:
        """
        Converte o contato para dicionário.
        
        Returns:
            dict: Representação em dicionário do contato
        """
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'data_nascimento': self.data_nascimento,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'nome_pai': self.nome_pai,
            'nome_mae': self.nome_mae,
            'cpf': self.cpf,
            'rg': self.rg,
            'notas': self.notas,
            'data_criacao': self.data_criacao,
            'data_modificacao': self.data_modificacao
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Contato':
        """
        Cria um contato a partir de um dicionário.
        
        Args:
            data (dict): Dicionário com dados do contato
            
        Returns:
            Contato: Nova instância de Contato
        """
        contato = Contato(
            nome_completo=data.get('nome_completo', ''),
            data_nascimento=data.get('data_nascimento', ''),
            email=data.get('email', ''),
            telefone=data.get('telefone', ''),
            endereco=data.get('endereco', ''),
            nome_pai=data.get('nome_pai', ''),
            nome_mae=data.get('nome_mae', ''),
            cpf=data.get('cpf', ''),
            rg=data.get('rg', ''),
            notas=data.get('notas', ''),
            contato_id=data.get('id')
        )
        
        # Restaurar timestamps originais se existirem
        if 'data_criacao' in data:
            contato.data_criacao = data['data_criacao']
        if 'data_modificacao' in data:
            contato.data_modificacao = data['data_modificacao']
            
        return contato
    
    def atualizar_modificacao(self):
        """Atualiza o timestamp de modificação para o momento atual."""
        self.data_modificacao = datetime.now().isoformat()
    
    def __str__(self) -> str:
        """
        Retorna representação em string do contato.
        
        Returns:
            str: Formatação legível do contato
        """
        info = [f"ID: {self.id}", f"Nome: {self.nome_completo}"]
        
        if self.data_nascimento:
            info.append(f"Data de Nascimento: {self.data_nascimento}")
        if self.email:
            info.append(f"Email: {self.email}")
        if self.telefone:
            info.append(f"Telefone: {self.telefone}")
        if self.endereco:
            info.append(f"Endereço: {self.endereco}")
        if self.cpf:
            info.append(f"CPF: {self.cpf}")
        if self.rg:
            info.append(f"RG: {self.rg}")
        if self.nome_pai:
            info.append(f"Pai: {self.nome_pai}")
        if self.nome_mae:
            info.append(f"Mãe: {self.nome_mae}")
        if self.notas:
            info.append(f"Notas: {self.notas}")
            
        return "\n".join(info)
    
    def __repr__(self) -> str:
        """Retorna representação técnica do contato."""
        return f"Contato(id={self.id}, nome='{self.nome_completo}')"
