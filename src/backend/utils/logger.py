################################################################################
#  
#	FILE: 	<logger.py>
#	BY	: 	<kbelx_>
#	FOR	:	<HARRP_>
#	ON	:	<18 Novembro 2025>
#	WHAT:	<Sistema de logging para a aplicação>
#
################################################################################

import logging
import os
from datetime import datetime
from pathlib import Path


class Logger:
    """
    Sistema de logging centralizado para a aplicação.
    """
    
    _loggers = {}
    
    @staticmethod
    def obter_logger(nome: str = "pebbl") -> logging.Logger:
        """
        Obtém ou cria um logger com o nome especificado.
        
        Args:
            nome (str): Nome do logger
            
        Returns:
            logging.Logger: Instância do logger
        """
        if nome in Logger._loggers:
            return Logger._loggers[nome]
        
        logger = logging.getLogger(nome)
        logger.setLevel(logging.DEBUG)
        
        # Remover handlers existentes para evitar duplicação
        logger.handlers.clear()
        
        # Criar diretório de logs se não existir
        log_dir = Path(__file__).parent.parent.parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Handler para arquivo
        arquivo_log = log_dir / f"pebbl_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(arquivo_log, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Handler para console (apenas WARNING e acima)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        Logger._loggers[nome] = logger
        return logger
