from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align

# ======================================================================================================================
# Opções do Menu

MENU_ITEMS = [
    ("1", "[bold green]Adicionar[/bold green] novo contato"),
    ("2", "[bold blue]Listar[/bold blue] todos os contatos"),
    ("3", "[bold yellow]Buscar[/bold yellow] contato"),
    ("4", "[bold magenta]Modificar[/bold magenta] contato"),
    ("5", "[bold red]Remover[/bold red] contato"),
    ("6", "[bold cyan]Exportar[/bold cyan] dados"),
    ("0", "[bold red]Sair[/bold red]"),
]

# ======================================================================================================================

def tituloMenu():
    """Cria o título principal do menu"""

    # Define o título principal
    header_texto = "[bold cyan]PEBBL_ - Gerenciador de Contatos via CLI[/bold cyan]"

    # Cria um design no título
    header = Panel.fit(
        header_texto,
        border_style="cyan",
        padding=(1, 2),
    )

    return header

# ======================================================================================================================

def opcoesMenu():
    """Define o layout e cria das opções do menu"""

    menu_table = Table(show_header=False, 
                       show_footer=False, 
                       padding=(0, 3), 
                       border_style="dim cyan")
    
    menu_table.add_column(style="cyan", 
                          no_wrap=True, 
                          width=8)
    
    menu_table.add_column(style="white")

    for opcao, descricao in MENU_ITEMS:
        menu_table.add_row(f"[ {opcao} ]", descricao)

    return menu_table

# ======================================================================================================================

def inputMenu() -> str:
    """Lida com a entrada de usuário no menu principal"""

    opcoes_validas = [item[0] for item in MENU_ITEMS]
    prompt_texto = "[bold cyan]➤ Escolha uma opção[/bold cyan]"
    opcao = Prompt.ask(prompt_texto, choices=opcoes_validas, default="0")

    return opcao

# ======================================================================================================================

def menu_interativo(console, limpar_tela, handlers):
    """Exibe o menu principal interativo."""

    while True:
        limpar_tela()

        console.print(Align.center(tituloMenu()))
        console.print()
        console.print(Align.center(opcoesMenu()))
        console.print()

        if inputMenu() == "0":
            limpar_tela()
            mensagem_saida = Panel.fit(
                "[bold yellow]Saindo... Ate logo![/bold yellow]",
                border_style="yellow",
                padding=(1, 3),
            )
            console.print(Align.center(mensagem_saida))
            break

        acao = handlers.get(inputMenu())
        if acao is not None:
            acao()
        else:
            console.print("[red]Opcao invalida![/red]")

        Prompt.ask("\n[dim]Pressione Enter para voltar ao menu[/dim]")

