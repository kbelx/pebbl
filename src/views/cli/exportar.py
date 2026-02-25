###############################################################################
#  
#	FILE: 	exportar.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	24 02 2026
#	WHAT:	exporta a base de dados no tipo de arquivo escolhido
#
################################################################################

import typer


def exportar(controller, console, formato: str = typer.Option("csv", help="Formato de exportacao: csv ou txt")):
    """
    Exporta todos os contatos para um arquivo.
    """
    formato = formato.lower()

    if formato not in ["csv", "txt"]:
        console.print(f"[bold red]Erro:[/bold red] Formato '{formato}' invalido. Use 'csv' ou 'txt'.")
        return

    if formato == "csv":
        sucesso, msg = controller.exportar_para_csv()
    else:
        sucesso, msg = controller.exportar_para_txt()

    if sucesso:
        console.print(f"[bold green]OK:[/bold green] {msg}")
    else:
        console.print(f"[bold red]Erro:[/bold red] {msg}")
