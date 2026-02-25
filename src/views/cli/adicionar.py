###############################################################################
#  
#	FILE: 	adicionar.py
#	BY	: 	Bruno Costa
#	FOR	:	Pebbl_
#	ON	:	24 02 2026
#	WHAT:	adicionar novos dados
#
################################################################################

# importações Rich
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.align import Align

# importação do projeto
from src.views.utils.formatter import limpar_tela

def adicionar(controller, console):
    """
    Adiciona um novo contato atraves de um formulario interativo.
    """
    limpar_tela()
    console.print(Panel.fit("[bold cyan]Adicionar Novo Contato[/bold cyan]", border_style="cyan", padding=(0, 2)))

    nome = Prompt.ask("[bold cyan]Nome completo[/bold cyan]")
    if not nome:
        console.print("[bold red]Erro:[/bold red] Nome e obrigatorio!")
        return

    data_nasc = Prompt.ask("[dim]Data de nascimento (DD/MM/AAAA)[/dim]", default="")
    email = Prompt.ask("[dim]Email[/dim]", default="")
    telefone = Prompt.ask("[dim]Telefone[/dim]", default="")
    endereco = Prompt.ask("[dim]Endereco[/dim]", default="")
    nome_pai = Prompt.ask("[dim]Nome do Pai[/dim]", default="")
    nome_mae = Prompt.ask("[dim]Nome da Mae[/dim]", default="")
    cpf = Prompt.ask("[dim]CPF[/dim]", default="")
    rg = Prompt.ask("[dim]RG[/dim]", default="")
    notas = Prompt.ask("[dim]Notas[/dim]", default="")

    console.print()
    if Confirm.ask("[bold]Salvar este contato?[/bold]"):
        sucesso, msg = controller.criar_contato(
            nome_completo=nome,
            data_nascimento=data_nasc,
            email=email,
            telefone=telefone,
            endereco=endereco,
            nome_pai=nome_pai,
            nome_mae=nome_mae,
            cpf=cpf,
            rg=rg,
            notas=notas,
        )

        if sucesso:
            console.print(f"[bold green]OK:[/bold green] {msg}")
        else:
            console.print(f"[bold red]Erro:[/bold red] {msg}")
    else:
        console.print("[yellow]Operacao cancelada.[/yellow]")
