###############################################################################
#  
#	FILE: 	formatter.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	24 02 2026
#	WHAT:	Contem funções de utilidades e formatação
#
################################################################################
# Importações built-in
import os
import platform

def limpar_tela():
    """Limpa a tela do terminal de forma confiavel."""
    os.system("cls" if platform.system() == "Windows" else "clear")
