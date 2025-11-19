################################################################################
#  
#	FILE: 	<main.py>
#	BY	: 	<kbelx_>
#	FOR	:	<HARRP_>
#	ON	:	<18 Novembro 2025>
#	WHAT:	<Entrada principal da aplicação (CLI Moderna)>
#
################################################################################

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import print as rprint
from typing import Optional
import sys
import os

# Adicionar diretório atual ao path para importar módulos do projeto
sys.path.append('app')

from backend.controller.contato_controller import ContatoController

# Inicializar Typer e Rich
app = typer.Typer(
    help="Pebbl_ - Sistema de Gerenciamento de Contatos",
    add_completion=False,
    no_args_is_help=False
)
console = Console()
controller = ContatoController()

# ═══════════════════════════════════════════════════════════════════════════════
# COMANDOS
# ═══════════════════════════════════════════════════════════════════════════════

@app.command()
def adicionar():
    """
    Adiciona um novo contato através de um formulário interativo.
    """
    console.print(Panel.fit("[bold cyan]Adicionar Novo Contato[/bold cyan]", border_style="cyan"))
    
    nome = Prompt.ask("[bold]Nome completo[/bold]")
    if not nome:
        console.print("[bold red]Erro:[/bold red] Nome é obrigatório!")
        return

    data_nasc = Prompt.ask("Data de nascimento (DD/MM/AAAA)", default="")
    email = Prompt.ask("Email", default="")
    telefone = Prompt.ask("Telefone", default="")
    endereco = Prompt.ask("Endereço", default="")
    nome_pai = Prompt.ask("Nome do Pai", default="")
    nome_mae = Prompt.ask("Nome da Mãe", default="")
    cpf = Prompt.ask("CPF", default="")
    rg = Prompt.ask("RG", default="")
    notas = Prompt.ask("Notas", default="")

    if Confirm.ask("Salvar este contato?"):
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
            notas=notas
        )
        
        if sucesso:
            console.print(f"[bold green]✓ {msg}[/bold green]")
        else:
            console.print(f"[bold red]✗ {msg}[/bold red]")
    else:
        console.print("[yellow]Operação cancelada.[/yellow]")

@app.command()
def listar():
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
            contato.telefone or "-"
        )

    console.print(table)

@app.command()
def buscar(termo: str):
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
            f"[bold]Endereço:[/bold] {contato.endereco}\n"
            f"[bold]Pai:[/bold] {contato.nome_pai}\n"
            f"[bold]Mãe:[/bold] {contato.nome_mae}\n"
            f"[bold]CPF:[/bold] {contato.cpf}\n"
            f"[bold]RG:[/bold] {contato.rg}\n"
            f"[italic]{contato.notas}[/italic]",
            title=f"[bold cyan]{contato.nome_completo}[/bold cyan]",
            expand=False
        ))

@app.command()
def modificar(id: int):
    """
    Modifica um contato existente.
    """
    contato = controller.obter_contato_por_id(id)
    
    if not contato:
        console.print(f"[bold red]Erro:[/bold red] Contato com ID {id} não encontrado.")
        return

    console.print(Panel(f"Editando: [bold cyan]{contato.nome_completo}[/bold cyan]", border_style="yellow"))
    console.print("[italic]Pressione Enter para manter o valor atual[/italic]\n")

    # Coletar novos dados (ou manter atuais)
    novo_nome = Prompt.ask("Nome completo", default=contato.nome_completo)
    nova_data = Prompt.ask("Data de nascimento", default=contato.data_nascimento)
    novo_email = Prompt.ask("Email", default=contato.email)
    novo_telefone = Prompt.ask("Telefone", default=contato.telefone)
    novo_endereco = Prompt.ask("Endereço", default=contato.endereco)
    novo_nome_pai = Prompt.ask("Nome do Pai", default=contato.nome_pai)
    novo_nome_mae = Prompt.ask("Nome da Mãe", default=contato.nome_mae)
    novo_cpf = Prompt.ask("CPF", default=contato.cpf)
    novo_rg = Prompt.ask("RG", default=contato.rg)
    novas_notas = Prompt.ask("Notas", default=contato.notas)

    if Confirm.ask("Salvar alterações?"):
        sucesso, msg = controller.modificar_contato(
            id,
            nome_completo=novo_nome,
            data_nascimento=nova_data,
            email=novo_email,
            telefone=novo_telefone,
            endereco=novo_endereco,
            nome_pai=novo_nome_pai,
            nome_mae=novo_nome_mae,
            cpf=novo_cpf,
            rg=novo_rg,
            notas=novas_notas
        )
        
        if sucesso:
            console.print(f"[bold green]✓ {msg}[/bold green]")
        else:
            console.print(f"[bold red]✗ {msg}[/bold red]")
    else:
        console.print("[yellow]Alterações descartadas.[/yellow]")

@app.command()
def remover(id: int):
    """
    Remove um contato pelo ID.
    """
    contato = controller.obter_contato_por_id(id)
    
    if not contato:
        console.print(f"[bold red]Erro:[/bold red] Contato com ID {id} não encontrado.")
        return

    if Confirm.ask(f"Tem certeza que deseja remover [bold red]{contato.nome_completo}[/bold red]?"):
        sucesso, msg = controller.remover_contato(id)
        if sucesso:
            console.print(f"[bold green]✓ {msg}[/bold green]")
        else:
            console.print(f"[bold red]✗ {msg}[/bold red]")

@app.command()
def exportar(formato: str = typer.Option("csv", help="Formato de exportação: csv ou txt")):
    """
    Exporta todos os contatos para um arquivo.
    """
    formato = formato.lower()
    
    if formato not in ['csv', 'txt']:
        console.print(f"[bold red]Erro:[/bold red] Formato '{formato}' inválido. Use 'csv' ou 'txt'.")
        return

    if formato == 'csv':
        sucesso, msg = controller.exportar_para_csv()
    else:
        sucesso, msg = controller.exportar_para_txt()
        
    if sucesso:
        console.print(f"[bold green]✓ {msg}[/bold green]")
    else:
        console.print(f"[bold red]✗ {msg}[/bold red]")

# ═══════════════════════════════════════════════════════════════════════════════
# MENU INTERATIVO
# ═══════════════════════════════════════════════════════════════════════════════

def menu_interativo():
    """Exibe o menu principal interativo."""
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]PEBBL_ - Menu Principal[/bold cyan]", border_style="cyan"))
        
        console.print("[1] [bold]Adicionar[/bold] novo contato")
        console.print("[2] [bold]Listar[/bold] todos os contatos")
        console.print("[3] [bold]Buscar[/bold] contato")
        console.print("[4] [bold]Modificar[/bold] contato")
        console.print("[5] [bold]Remover[/bold] contato")
        console.print("[6] [bold]Exportar[/bold] dados")
        console.print("[0] [bold red]Sair[/bold red]")
        console.print()
        
        opcao = Prompt.ask("Escolha uma opção", choices=["1", "2", "3", "4", "5", "6", "0"], default="0")
        
        if opcao == "0":
            console.print("[yellow]Saindo... Até logo![/yellow]")
            break
            
        elif opcao == "1":
            adicionar()
            Prompt.ask("\nPressione Enter para voltar ao menu")
            
        elif opcao == "2":
            listar()
            Prompt.ask("\nPressione Enter para voltar ao menu")
            
        elif opcao == "3":
            termo = Prompt.ask("Digite o nome para buscar")
            buscar(termo)
            Prompt.ask("\nPressione Enter para voltar ao menu")
            
        elif opcao == "4":
            id_str = Prompt.ask("ID do contato a modificar")
            if id_str.isdigit():
                modificar(int(id_str))
            else:
                console.print("[red]ID inválido![/red]")
            Prompt.ask("\nPressione Enter para voltar ao menu")
            
        elif opcao == "5":
            id_str = Prompt.ask("ID do contato a remover")
            if id_str.isdigit():
                remover(int(id_str))
            else:
                console.print("[red]ID inválido![/red]")
            Prompt.ask("\nPressione Enter para voltar ao menu")
            
        elif opcao == "6":
            formato = Prompt.ask("Formato", choices=["csv", "txt"], default="csv")
            exportar(formato)
            Prompt.ask("\nPressione Enter para voltar ao menu")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Sistema de Gerenciamento de Contatos Pebbl_.
    
    Se nenhum comando for passado, abre o menu interativo.
    """
    if ctx.invoked_subcommand is None:
        menu_interativo()

# ═══════════════════════════════════════════════════════════════════════════════
