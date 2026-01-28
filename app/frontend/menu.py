from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align


MENU_ITEMS = [
    ("1", "[bold green]Adicionar[/bold green] novo contato"),
    ("2", "[bold blue]Listar[/bold blue] todos os contatos"),
    ("3", "[bold yellow]Buscar[/bold yellow] contato"),
    ("4", "[bold magenta]Modificar[/bold magenta] contato"),
    ("5", "[bold red]Remover[/bold red] contato"),
    ("6", "[bold cyan]Exportar[/bold cyan] dados"),
    ("0", "[bold red]Sair[/bold red]"),
]


def menu_interativo(console, limpar_tela, handlers):
    """Exibe o menu principal interativo."""
    while True:
        limpar_tela()

        header_texto = "[bold cyan]PEBBL_ - Gerenciador de Contatos[/bold cyan]"
        header = Panel.fit(
            header_texto,
            border_style="cyan",
            padding=(1, 2),
        )

        menu_table = Table(show_header=False, show_footer=False, padding=(0, 2), border_style="dim cyan")
        menu_table.add_column(style="cyan", no_wrap=True, width=8)
        menu_table.add_column(style="white")

        for opcao, descricao in MENU_ITEMS:
            menu_table.add_row(f"[ {opcao} ]", descricao)

        console.print(Align.center(header))
        console.print()
        console.print(Align.center(menu_table))
        console.print()

        opcoes_validas = [item[0] for item in MENU_ITEMS]
        prompt_texto = "[bold cyan]➤ Escolha uma opção[/bold cyan]"
        opcao = Prompt.ask(prompt_texto, choices=opcoes_validas, default="0")

        if opcao == "0":
            limpar_tela()
            mensagem_saida = Panel.fit(
                "[bold yellow]Saindo... Ate logo![/bold yellow]",
                border_style="yellow",
                padding=(1, 3),
            )
            console.print(Align.center(mensagem_saida))
            break

        acao = handlers.get(opcao)
        if acao is not None:
            acao()
        else:
            console.print("[red]Opcao invalida![/red]")

        Prompt.ask("\n[dim]Pressione Enter para voltar ao menu[/dim]")
