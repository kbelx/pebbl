################################################################################
#  
#	FILE: 	<validators.py>
#	BY	: 	<kbelx_>
#	FOR	:	<HARRP_>
#	ON	:	<18 Novembro 2025>
#	WHAT:	<Funções utilitárias de validação>
#
################################################################################

import re
import re
from typing import Tuple


def validar_cpf(cpf: str) -> bool:
    """
    Valida um número de CPF (Cadastro de Pessoas Físicas) brasileiro.
    
    ### Args:
        `cpf (str)`: O CPF a ser validado (_com ou sem pontuação_).
        
    ### Returns:
        bool: `True` se o CPF for válido, `False` caso contrário.
    """
    if not cpf or not isinstance(cpf, str):
        return False
    
    # Remover caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verificar tamanho
    if len(cpf) != 11:
        return False
        
    # Verificar se todos os dígitos são iguais (ex: 111.111.111-11)
    if cpf == cpf[0] * 11:
        return False
        
    # Cálculo do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
        
    if digito1 != int(cpf[9]):
        return False
        
    # Cálculo do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
        
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
        
    if digito2 != int(cpf[10]):
        return False
        
    return True

def validar_rg(rg: str) -> bool:
    """
    Valida o formato básico de um RG (Registro Geral).
    
    Nota: A validação de RG é complexa pois varia por estado.
    Esta função verifica apenas se o formato é razoável.
    
    Args:
        rg (str): O RG a ser validado.
        
    Returns:
        bool: True se o formato parecer válido.
    """
    if not rg or not isinstance(rg, str):
        return False
    
    # Remover caracteres não alfanuméricos
    rg_limpo = re.sub(r'[^a-zA-Z0-9]', '', rg)
    
    # Verificar tamanho mínimo razoável (alguns estados têm RGs menores, mas geralmente > 5)
    if len(rg_limpo) < 5 or len(rg_limpo) > 15:
        return False
        
    # Verificar se contém apenas números ou 'X' no final (comum em SP)
    # Permitir letras em geral pois alguns estados usam letras no meio
    return True


def validar_telefone(telefone: str) -> bool:
    """
    Valida um número de telefone brasileiro.
    
    Aceita formatos: (XX) XXXX-XXXX, (XX) XXXXX-XXXX, XX XXXX-XXXX, XX XXXXX-XXXX, etc.
    
    Args:
        telefone (str): O telefone a ser validado.
        
    Returns:
        bool: True se o formato parecer válido.
    """
    if not telefone or not isinstance(telefone, str):
        return False
    
    # Remover caracteres não numéricos
    telefone_limpo = re.sub(r'[^0-9]', '', telefone)
    
    # Telefone válido deve ter entre 10 e 11 dígitos (com possível código de país)
    if len(telefone_limpo) == 10:
        # (XX) XXXX-XXXX
        return True
    elif len(telefone_limpo) == 11:
        # (XX) XXXXX-XXXX
        return True
    elif len(telefone_limpo) == 12:
        # +55 XX XXXX-XXXX
        return True
    elif len(telefone_limpo) == 13:
        # +55 XX XXXXX-XXXX
        return True
    
    return False


def validar_email(email: str) -> bool:
    """
    Valida o formato de um endereço de email.
    
    Args:
        email (str): O email a ser validado.
        
    Returns:
        bool: True se o formato for válido.
    """
    if not email or not isinstance(email, str):
        return False
    
    padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao_email, email))


def validar_data(data: str) -> Tuple[bool, str]:
    """
    Valida uma data no formato DD/MM/AAAA.
    
    Args:
        data (str): A data a ser validada.
        
    Returns:
        Tuple[bool, str]: (é_válida, mensagem_erro)
    """
    if not data or not isinstance(data, str):
        return False, "Data não fornecida"
    
    # Validar formato
    padrao_data = r'^(\d{2})/(\d{2})/(\d{4})$'
    match = re.match(padrao_data, data)
    
    if not match:
        return False, "Formato inválido. Use DD/MM/AAAA"
    
    dia, mes, ano = match.groups()
    dia, mes, ano = int(dia), int(mes), int(ano)
    
    # Validar mês
    if mes < 1 or mes > 12:
        return False, "Mês inválido (1-12)"
    
    # Validar dia
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Verificar se é bissexto
    if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0):
        dias_por_mes[1] = 29
    
    if dia < 1 or dia > dias_por_mes[mes - 1]:
        return False, f"Dia inválido para o mês {mes}"
    
    # Validar ano (não permitir datas futuras muito distantes)
    from datetime import datetime
    ano_atual = datetime.now().year
    
    if ano > ano_atual + 10:
        return False, "Ano muito no futuro"
    
    if ano < 1900:
        return False, "Ano deve ser após 1900"
    
    return True, ""


def sanitizar_texto(texto: str) -> str:
    """
    Sanitiza um texto removendo caracteres perigosos.
    
    Args:
        texto (str): O texto a ser sanitizado.
        
    Returns:
        str: Texto sanitizado.
    """
    if not isinstance(texto, str):
        return ""
    
    # Remover caracteres de controle
    texto = re.sub(r'[\x00-\x1F\x7F]', '', texto)
    
    # Remover múltiplos espaços
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto.strip()
