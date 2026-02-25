###############################################################################
#  
#	FILE: 	buscar.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	24 02 2026
#	WHAT:	Buscar dados na base de dados
#
################################################################################

from rich.panel import Panel


def buscar(controller, console, termo: str):
    """
    Busca contatos por nome.
    """
    resultados = controller.buscar_contatos_por_nome(termo)

    if not resultados:
        console.print(f"[yellow]Nenhum contato encontrado com o termo '{termo}'.[/yellow]")
        return

    console.print(f"[bold]Encontrados {len(resultados)} resultados para '{termo}':[/bold]")

    for contato in resultados:
        console.print(Panel(
            f"[bold]ID:[/bold] {contato.id}\n"
            f"[bold]Email:[/bold] {contato.email}\n"
            f"[bold]Telefone:[/bold] {contato.telefone}\n"
            f"[bold]Endereco:[/bold] {contato.endereco}\n"
            f"[bold]Pai:[/bold] {contato.nome_pai}\n"
            f"[bold]Mae:[/bold] {contato.nome_mae}\n"
            f"[bold]CPF:[/bold] {contato.cpf}\n"
            f"[bold]RG:[/bold] {contato.rg}\n"
            f"[italic]{contato.notas}[/italic]",
            title=f"[bold cyan]{contato.nome_completo}[/bold cyan]",
            expand=False,
        ))
