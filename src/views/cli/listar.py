###############################################################################
#  
#	FILE: 	listar.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	24 02 2026
#	WHAT:	Lista todos os dados contidos na base de dados
#
################################################################################

# importações Rich
from rich.table import Table

def listar(controller, console):
    """
    Lista todos os contatos cadastrados em uma tabela formatada.
    """
    contatos = controller.obter_todos_contatos()

    if not contatos:
        console.print("[yellow]Nenhum contato encontrado.[/yellow]")
        return

    table = Table(title=f"Contatos ({len(contatos)})")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Nome", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Telefone", style="yellow")

    for contato in contatos:
        table.add_row(
            str(contato.id),
            contato.nome_completo,
            contato.email or "-",
            contato.telefone or "-",
        )

    console.print(table)