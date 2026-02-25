###############################################################################
#  
#	FILE: 	remover.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	24 02 2026
#	WHAT:	Remove algum dado
#
################################################################################

from rich.prompt import Confirm


def remover(controller, console, id: int):
    """
    Remove um contato pelo ID.
    """
    contato = controller.obter_contato_por_id(id)

    if not contato:
        console.print(f"[bold red]Erro:[/bold red] Contato com ID {id} nao encontrado.")
        return

    if Confirm.ask(f"Tem certeza que deseja remover [bold red]{contato.nome_completo}[/bold red]?"):
        sucesso, msg = controller.remover_contato(id)
        if sucesso:
            console.print(f"[bold green]OK:[/bold green] {msg}")
        else:
            console.print(f"[bold red]Erro:[/bold red] {msg}")
