################################################################################
#  
#	FILE: 	<main.py>
#	BY	: 	<kbelx_>
#	FOR	:	<HARRP_>
#	ON	:	<18 Novembro 2025>
#	WHAT:	<Entrada principal da aplicação (CLI Moderna)>
#
################################################################################

import sys
import os

# Adicionar diretório raiz ao path para importar módulos do projeto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.backend.controller.contato_controller import ContatoController
from rich.console import Console

from app.frontend.cli import build_app


console = Console()
controller = ContatoController()
app = build_app(controller, console)
